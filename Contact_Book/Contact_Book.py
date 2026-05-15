import json 
import os

FILE = "contact.json"

def load_contact():
    if not os.path.exists(FILE):
        return{}
    with open(FILE , 'r') as f:
        contents = f.read().strip()
        return json.loads(contents) if contents else {}
    
def save_contact(contact):
    with open(FILE, 'w') as f:
        json.dump(contact, f , indent = 4 )
        
def add_contact(name , phone , email):
    contact = load_contact()
    key = name.lower().strip()
    if key in contact:
        print(f"Contact{name} already exists.")
        return
    contact[key] ={"name": name.strip() , "phone": phone.strip() , "email": email.strip()}
    save_contact(contact) 
    print(f"✔️Contact {name} added successfully.")
    
def view_contact():
    contact = load_contact()
    if not contact:
        print("No contact found")
        return
    print(f"\n {"Name":<20} , {"Phone":<15} , {"Email"}")
    print(" " + "-" *55)
    for c in sorted(contact.values() ,key = lambda x : x['name'].lower()):
        print(f"{c["name"]:<20} ,{c["phone"]:<15} , {c["email"]}")
    print()
    
def search_contact(query):
    contact = load_contact()
    query = query.lower().strip()
    
    results = [c for c in contact.values() if query in c['name'].lower() or query in c['phone'] or query in c['email'].lower]
    
    if not results:
        print(f'No contact found for {query}')
        return
    print(f"\n Found {len(results)} result(s):")
    for c in results:
        print(f"Name: {c['name']} | Phone: {c['phone']} | Email: {c['email']}")
    print()
    
def update_contact(name , phone = None , email = None ):
    contact = load_contact()
    key = name.lower().strip()
    
    if key not in contact:
        print(f"Contact {name} not found.")
        return
    if phone:
        contact[key]['phone'] = phone.strip()
    if email:
        contact[key]['email'] = email.strip()
    save_contact(contact)
    print(f"✔️Contact {name} updated successfully.")
    
def delete_contact(name):
    contact =load_contact()
    key = name.lower().strip()
    
    if key not in contact:
        print(f"Contact {name} not found.")
        return
        
    del contact[key]
    save_contact(contact)
    print(f"✔️Contact {name} deleted successfully.")
    
def menu():      
    print("\n  📒 CONTACT BOOK")
    print("  1. Add contact")
    print("  2. List all contacts")
    print("  3. Search contact")
    print("  4. Update contact")
    print("  5. Delete contact")
    print("  6. Exit")
    
def main():
    while True:
        menu()
        choice = input("Enter your choice from 1 to 6: ").strip()
        if choice =='1':
            name = input("Enter contact name: ")
            phone = input("Enter contact phone: ")
            email = input("Enter contact email: ")
            add_contact(name , phone , email)
        elif choice == "2":
            view_contact()
        elif choice =="3":
            name = input("Enter  name to search: ")
            search_contact(name)
        elif choice == "4":
            name = input(" Contact Name to update: ").strip()
            phone = input("Contact Phone to update(Leave blank to skip): ").strip()
            email = input("Contact Email to update(Leave blank to skip): ").strip()
            update_contact(name , phone or None , email or None)
        elif choice == "5":
            name = input("Contact name to delete: ").strip()
            delete_contact(name)
        elif choice =="6":
            print ("\n Goodbye! We will meet again.👋\n")
            break
        else:
            print("  Invalid choice. Enter a number from 1 to 6.")
            
if __name__ == '__main__':
    main()
            