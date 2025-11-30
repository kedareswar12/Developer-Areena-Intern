contacts = {}

def load_contacts():
    try:
        with open('contacts.txt', 'r') as file:
            for line in file:
                name, phone = line.strip().split(',')
                contacts[name] = phone
        print("Contacts loaded successfully.")
    except FileNotFoundError:
        print("No existing contacts file found. Starting fresh.")

def save_contacts():
    with open('contacts.txt', 'w') as file:
        for name, phone in contacts.items():
            file.write(f"{name},{phone}\n")
    print("Contacts saved successfully.")

def add_contact(name, phone):
    contacts[name] = phone
    save_contacts()
    print(f"Contact '{name}' added successfully.")

def search_contact(name):
    if name in contacts:
        print(f"Name: {name}, Phone: {contacts[name]}")
    else:
        print(f"Contact '{name}' not found.")

def display_contacts():
    if contacts:
        print("\nAll Contacts:")
        for name, phone in contacts.items():
            print(f"Name: {name}, Phone: {phone}")
    else:
        print("No contacts available.")

def main():
    load_contacts()
    
    while True:
        print("\n--- Contact Management System ---")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Display All Contacts")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            add_contact(name, phone)
        elif choice == '2':
            name = input("Enter name to search: ")
            search_contact(name)
        elif choice == '3':
            display_contacts()
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()