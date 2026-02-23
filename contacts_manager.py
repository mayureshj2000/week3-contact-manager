import json
import re
import os
from datetime import datetime
import csv

CONTACTS_FILE = "contacts_data.json"
BACKUP_FILE = "contacts_backup.json"

def validate_phone(phone):
    "validating phone 10 digit number"
    digits = re.sub(r"\D", "", phone)
    if 10 <= len(digits) <= 11:
        return True, digits
    return False, None

def validate_email(email):
    "validating email address"
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def load_from_file():
    "load contacts from JSON file and return empty dict if file is missing"
    if not os.path.exists(CONTACTS_FILE):
        print("No contacts file found. Restarting")
        return {}
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, PermissionError) as e:
        print(f"Error loading contacts file: {e}. Restarting")
        return {}

def save_to_file(contacts):
    "save contacts to JSON file"
    try:
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r", encoding="utf-8") as src:
                with open(BACKUP_FILE, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
        print(f"Contacts saved to {CONTACTS_FILE}")
    except (PermissionError, OSError) as e:
        print(f"Error saving contacts: {e}")

# ---------- helper for case-insensitive name lookup ----------

def find_contact_key(contacts, name_input):
    "Return stored key matching name_input (case-insensitive), or None"
    target = name_input.strip().lower()
    for stored_name in contacts.keys():
        if stored_name.lower() == target:
            return stored_name
    return None

# --------------------------------------------------------------

def add_contact(contacts):
    "add a new contact with validation"
    print("\n--- ADD NEW CONTACT ---")
    while True:
        name = input("Enter name: ").strip()
        if not name:
            print("Name cannot be empty. Please try again.")
            continue

        # use case-insensitive duplicate check
        existing_key = find_contact_key(contacts, name)
        if existing_key is not None:
            print(f"Contact with name '{existing_key}' already exists.")
            choice = input("Do you want to update instead? (y/n): ").strip().lower()
            if choice == "y":
                update_contact(contacts, existing_key)
                return contacts
            continue
        break

    while True:
        phone = input("Enter phone number: ").strip()
        is_valid, cleaned_phone = validate_phone(phone)
        if is_valid:
            break
        print("Invalid phone number! Please enter 10-11 digits.")

    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip()
        if not email or validate_email(email):
            break
        print("Invalid email format!")

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"

    contacts[name] = {
        "phone": cleaned_phone,
        "email": email or None,
        "address": address or None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    print(f"Contact '{name}' added successfully!")
    return contacts

def search_contacts(contacts, search_term):
    "search contacts by name (partial, case-insensitive)."
    search_term = search_term.lower()
    return {
        name: info
        for name, info in contacts.items()
        if search_term in name.lower()
    }

def display_search_results(results):
    "display search results"
    if not results:
        print("No contacts found.")
        return
    print(f"\nFound {len(results)} contact(s):")
    print("-" * 50)
    for i, (name, info) in enumerate(results.items(), 1):
        print(f"{i}. {name}")
        print(f"   Phone: {info['phone']}")
        if info["email"]:
            print(f"   Email: {info['email']}")
        if info["address"]:
            print(f"   Address: {info['address']}")
        print(f"   Group: {info['group']}")
        print()

def update_contact(contacts, name=None):
    "update an existing contact (case-insensitive name)"
    if name is None:
        name = input("Enter name to update: ").strip()

    key = find_contact_key(contacts, name)
    if key is None:
        print("Contact not found.")
        return contacts
    
    info = contacts[key]
    print(f"\n--- UPDATE: {key} ---")
    print(f"Current phone: {info['phone']}")
    new_phone = input("Enter new phone (Enter to keep current): ").strip()
    if new_phone:
        is_valid, cleaned = validate_phone(new_phone)
        if is_valid:
            info["phone"] = cleaned
        else:
            print("Invalid phone number, keeping old value.")
    
    print(f"Current email: {info['email'] or 'None'}")
    new_email = input("Enter new email (Enter to keep current): ").strip()
    if new_email:
        if validate_email(new_email):
            info["email"] = new_email
        else:
            print("Invalid email format, keeping old value.")
    
    print(f"Current address: {info['address'] or 'None'}")
    new_address = input("Enter new address (Enter to keep current): ").strip()
    if new_address:
        info["address"] = new_address
    
    print(f"Current group: {info['group']}")
    new_group = input("Enter new group (Enter to keep current): ").strip()
    if new_group:
        info["group"] = new_group
    
    info["updated_at"] = datetime.now().isoformat()
    print(f"Contact '{key}' updated successfully!")
    return contacts

def delete_contact(contacts):
    "Delete a contact with confirmation (case-insensitive name)"
    name_input = input("Enter name to delete: ").strip()
    key = find_contact_key(contacts, name_input)
    if key is None:
        print("Contact not found.")
        return contacts

    confirm = input(f"Are you sure you want to delete '{key}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion canceled.")
        return contacts
    del contacts[key]
    print(f"Contact '{key}' deleted successfully!")
    return contacts

def display_all(contacts):
    "Display all contacts"
    if not contacts:
        print("No contacts found.")
        return
    print(f"\n--- ALL CONTACTS ({len(contacts)} total) ---")
    print("=" * 60)
    for name, info in contacts.items():
        print(f"Name: {name}")
        print(f"Phone: {info['phone']}")
        if info["email"]:
            print(f"Email: {info['email']}")
        if info["address"]:
            print(f"Address: {info['address']}")
        print(f"Group: {info['group']}")
        print(f"Created At: {info['created_at']}")
        print(f"Updated At: {info['updated_at']}")
        print("-" * 60)

def export_to_csv(contacts):
    "Export contacts to CSV"
    if not contacts:
        print("No contacts found to export.")
        return
    filename = "contacts_export.csv"
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone", "Email", "Address", "Group", "Created At", "Updated At"])
            for name, info in contacts.items():
                writer.writerow([
                    name, 
                    info["phone"], 
                    info["email"] or "", 
                    info["address"] or "", 
                    info["group"], 
                    info["created_at"], 
                    info["updated_at"],
                ])
        print(f"Contacts exported to '{filename}' successfully!")
    except (PermissionError, OSError) as e:
        print(f"Error exporting contacts: {e}")

def view_statistics(contacts):
    "View statistics"
    if not contacts:
        print("No contacts found.")
        return
    total = len(contacts)
    groups = {}
    for info in contacts.values():
        g = info["group"]
        groups[g] = groups.get(g, 0) + 1
    
    print("\n--- STATISTICS ---")
    print(f"Total contacts: {total}")
    print("Contacts by Group:")
    for g, count in sorted(groups.items()):
        print(f"  {g}: {count} contact(s)")
    
    # recently updated (last 7 days)
    now = datetime.now()
    recent = 0
    for info in contacts.values():
        updated = datetime.fromisoformat(info["updated_at"])
        if (now - updated).days <= 7:
            recent += 1
    print(f"Recently updated (last 7 days): {recent}")

def show_menu():
    "display the menu"
    print("\n" + "=" * 50)
    print("--- CONTACT MANAGEMENT SYSTEM ---")
    print("1. Add Contact")
    print("2. Search Contacts")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Display All Contacts")
    print("6. Export to CSV")
    print("7. View Statistics")
    print("8. Exit")
    print("=" * 50)

def main():
    contacts = load_from_file()
    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()
        if choice == "1":
            contacts = add_contact(contacts)
            save_to_file(contacts)
        elif choice == "2":
            term = input("Enter name search: ").strip()
            results = search_contacts(contacts, term)
            display_search_results(results)
        elif choice == "3":
            contacts = update_contact(contacts)
            save_to_file(contacts)
        elif choice == "4":
            contacts = delete_contact(contacts)
            save_to_file(contacts)
        elif choice == "5":
            display_all(contacts)
        elif choice == "6":
            export_to_csv(contacts)
        elif choice == "7":
            view_statistics(contacts)
        elif choice == "8":
            save_to_file(contacts)
            print("\n" + "=" * 50)
            print("Thank you for using Contact Management System!")
            print("=" * 50)
            break
        else:
            print("Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    main()
