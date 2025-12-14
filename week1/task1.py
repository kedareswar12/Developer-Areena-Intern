import json
import os
from datetime import datetime

class PersonalInfoManager:
    def __init__(self, filename="people_data.json"):
        self.filename = filename
        self.people = []
        self.load_data()
    
    def load_data(self):
        """Load data from JSON file if it exists"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.people = json.load(file)
                print("Data loaded successfully!")
            except json.JSONDecodeError:
                print("Error reading data file. Starting fresh.")
                self.people = []
        else:
            print("No existing data found. Starting fresh.")
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.people, file, indent=4)
            print("✓ Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_person(self):
        print("\n" + "="*50)
        print("ADD NEW PERSON")
        print("="*50)
        
        name = input("Enter name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return
        
        try:
            age = int(input("Enter age: "))
            if age < 0 or age > 150:
                print("Please enter a valid age!")
                return
        except ValueError:
            print("Age must be a number!")
            return
        
        city = input("Enter city: ").strip()
        if not city:
            print("City cannot be empty!")
            return
        
        hobbies_input = input("Enter hobbies (comma-separated): ").strip()
        hobbies = [hobby.strip() for hobby in hobbies_input.split(',') if hobby.strip()]
        
        person = {
            'id': len(self.people) + 1,
            'name': name,
            'age': age,
            'city': city,
            'hobbies': hobbies,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.people.append(person)
        self.save_data()
        print(f"\n✓ {name} added successfully!")
    
    def display_all(self):

        if not self.people:
            print("\n📭 No records found. Add some people first!")
            return
        
        print("\n" + "="*50)
        print("ALL RECORDS")
        print("="*50)
        
        for person in self.people:
            self.display_person(person)
            print("-" * 50)
    
    def display_person(self, person):

        print(f"\n ID: {person['id']}")
        print(f"Name: {person['name']}")
        print(f" Age: {person['age']} years")
        print(f" City: {person['city']}")
        print(f"  Hobbies: {', '.join(person['hobbies']) if person['hobbies'] else 'No hobbies listed'}")
        print(f" Added on: {person.get('created_at', 'N/A')}")
    
    def search_person(self):

        if not self.people:
            print("\n No records to search!")
            return
        
        search_name = input("\nEnter name to search: ").strip().lower()
        found = False
        
        print("\n" + "="*50)
        print("SEARCH RESULTS")
        print("="*50)
        
        for person in self.people:
            if search_name in person['name'].lower():
                self.display_person(person)
                print("-" * 50)
                found = True
        
        if not found:
            print(f"\n No person found with name containing '{search_name}'")
    
    def update_person(self):
        
        if not self.people:
            print("\n No records to update!")
            return
        
        self.display_all()
        
        try:
            person_id = int(input("\nEnter ID of person to update: "))
            person = next((p for p in self.people if p['id'] == person_id), None)
            
            if not person:
                print(" Person not found!")
                return
            
            print("\nLeave blank to keep current value")
            
            name = input(f"Enter new name [{person['name']}]: ").strip()
            if name:
                person['name'] = name
            
            age_input = input(f"Enter new age [{person['age']}]: ").strip()
            if age_input:
                try:
                    person['age'] = int(age_input)
                except ValueError:
                    print("Invalid age, keeping old value")
            
            city = input(f"Enter new city [{person['city']}]: ").strip()
            if city:
                person['city'] = city
            
            hobbies_input = input(f"Enter new hobbies [{', '.join(person['hobbies'])}]: ").strip()
            if hobbies_input:
                person['hobbies'] = [h.strip() for h in hobbies_input.split(',') if h.strip()]
            
            self.save_data()
            print("\n✓ Person updated successfully!")
            
        except ValueError:
            print("Invalid ID!")
    
    def delete_person(self):

        if not self.people:
            print("\n📭 No records to delete!")
            return
        
        self.display_all()
        
        try:
            person_id = int(input("\nEnter ID of person to delete: "))
            person = next((p for p in self.people if p['id'] == person_id), None)
            
            if not person:
                print("Person not found!")
                return
            
            confirm = input(f"Are you sure you want to delete {person['name']}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                self.people.remove(person)
                self.save_data()
                print(f"\n✓ {person['name']} deleted successfully!")
            else:
                print("Deletion cancelled.")
                
        except ValueError:
            print("Invalid ID!")
    
    def display_statistics(self):
        
        if not self.people:
            print("\n📭 No records to show statistics!")
            return
        
        print("\n" + "="*50)
        print("STATISTICS")
        print("="*50)
        
        total = len(self.people)
        avg_age = sum(p['age'] for p in self.people) / total
        cities = set(p['city'] for p in self.people)
        all_hobbies = []
        for p in self.people:
            all_hobbies.extend(p['hobbies'])
        
        print(f" Total Records: {total}")
        print(f" Average Age: {avg_age:.1f} years")
        print(f" Cities Represented: {len(cities)}")
        print(f" Total Hobbies Listed: {len(all_hobbies)}")
        
        if all_hobbies:
            from collections import Counter
            hobby_count = Counter(all_hobbies)
            most_common = hobby_count.most_common(3)
            print(f"\n Most Popular Hobbies:")
            for hobby, count in most_common:
                print(f"   - {hobby}: {count} person(s)")
    
    def run(self):
        """Main menu loop"""
        while True:
            print("\n" + "="*50)
            print("PERSONAL INFORMATION MANAGER")
            print("="*50)
            print("1. Add New Person")
            print("2. Display All Records")
            print("3. Search Person")
            print("4. Update Person")
            print("5. Delete Person")
            print("6. Show Statistics")
            print("7. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.add_person()
            elif choice == '2':
                self.display_all()
            elif choice == '3':
                self.search_person()
            elif choice == '4':
                self.update_person()
            elif choice == '5':
                self.delete_person()
            elif choice == '6':
                self.display_statistics()
            elif choice == '7':
                print("\n Thank you for using Personal Information Manager!")
                print("All data has been saved to", self.filename)
                break
            else:
                print("\n Invalid choice! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    manager = PersonalInfoManager()
    manager.run()