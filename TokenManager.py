import json
import os
import uuid
from datetime import datetime

FILE = "tokens.json"


def load_tokens():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    data = []
    save_tokens(data)
    return data


def save_tokens(tokens):
    with open(FILE, "w") as f:
        json.dump(tokens, f, indent=2)


def create_token(tokens):
    print("\n--- Add New Token ---")
    name = input("Service name: ").strip()
    if not name:
        print("Service name cannot be empty.")
        return

    token = input("Token value: ").strip()
    if not token:
        print("Token cannot be empty.")
        return

    billing = input("Billing amount (default 0.0): ").strip()
    try:
        billing = float(billing) if billing else 0.0
    except ValueError:
        billing = 0.0

    entry = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "token": token,
        "status": "active",
        "billing": billing,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tokens.append(entry)
    save_tokens(tokens)
    print(f"Token '{name}' added with ID: {entry['id']}")


def read_tokens(tokens):
    print("\n--- Token List ---")
    if not tokens:
        print("No tokens found.")
        return

    query = input("Search by service name (press Enter to show all): ").strip().lower()
    results = [t for t in tokens if query in t["name"].lower()] if query else tokens

    if not results:
        print("No matching tokens.")
        return

    total_billing = sum(t["billing"] for t in results)

    print(f"\n{'ID':<10} {'Service':<20} {'Status':<10} {'Billing':>10} {'Created':<18}")
    print("-" * 72)
    for t in results:
        token_preview = t["token"][:6] + "..." if len(t["token"]) > 6 else t["token"]
        print(f"{t['id']:<10} {t['name']:<20} {t['status']:<10} ${t['billing']:>9.2f} {t['created_at']:<18}")
    print("-" * 72)
    print(f"{'Total billing:':<42} ${total_billing:>9.2f}")
    print(f"Found: {len(results)} token(s)")


def update_token(tokens):
    print("\n--- Update Token ---")
    token_id = input("Enter token ID: ").strip()
    token = next((t for t in tokens if t["id"] == token_id), None)

    if not token:
        print("Token not found.")
        return

    print(f"Editing: {token['name']} | Status: {token['status']} | Billing: ${token['billing']:.2f}")
    print("Leave field empty to keep current value.")

    new_name = input(f"New service name [{token['name']}]: ").strip()
    if new_name:
        token["name"] = new_name

    new_token = input(f"New token value [hidden]: ").strip()
    if new_token:
        token["token"] = new_token

    new_status = input(f"New status (active/inactive) [{token['status']}]: ").strip().lower()
    if new_status in ("active", "inactive"):
        token["status"] = new_status
    elif new_status:
        print("Invalid status. Keeping current.")

    new_billing = input(f"New billing amount [{token['billing']}]: ").strip()
    if new_billing:
        try:
            token["billing"] = float(new_billing)
        except ValueError:
            print("Invalid amount. Keeping current.")

    save_tokens(tokens)
    print("Token updated.")


def delete_token(tokens):
    print("\n--- Delete Token ---")
    token_id = input("Enter token ID: ").strip()
    token = next((t for t in tokens if t["id"] == token_id), None)

    if not token:
        print("Token not found.")
        return

    confirm = input(f"Delete '{token['name']}' (ID: {token_id})? (yes/no): ").strip().lower()
    if confirm == "yes":
        tokens.remove(token)
        save_tokens(tokens)
        print("Token deleted.")
    else:
        print("Cancelled.")


def show_stats(tokens):
    print("\n--- Statistics ---")
    if not tokens:
        print("No tokens found.")
        return

    active = [t for t in tokens if t["status"] == "active"]
    inactive = [t for t in tokens if t["status"] == "inactive"]
    total_billing = sum(t["billing"] for t in tokens)
    active_billing = sum(t["billing"] for t in active)

    print(f"Total tokens:    {len(tokens)}")
    print(f"Active:          {len(active)}")
    print(f"Inactive:        {len(inactive)}")
    print(f"Total billing:   ${total_billing:.2f}")
    print(f"Active billing:  ${active_billing:.2f}")

    if tokens:
        top = max(tokens, key=lambda t: t["billing"])
        print(f"Highest billing: {top['name']} (${top['billing']:.2f})")


MENU = """
=== API Token Manager ===
1. Add token
2. List / Search tokens
3. Update token
4. Delete token
5. Statistics
0. Exit
"""


def main():
    tokens = load_tokens()
    while True:
        print(MENU)
        choice = input("Choice: ").strip()
        if choice == "1":
            create_token(tokens)
        elif choice == "2":
            read_tokens(tokens)
        elif choice == "3":
            update_token(tokens)
        elif choice == "4":
            delete_token(tokens)
        elif choice == "5":
            show_stats(tokens)
        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()