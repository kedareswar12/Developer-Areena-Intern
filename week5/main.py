def print_header():
    """Print application header"""
    print("\n" + "=" * 50)
    print("      LIBRARY MANAGEMENT SYSTEM")
    print("=" * 50)

def print_menu():
    """Print main menu"""
    print("\n--- MAIN MENU ---")
    print("1. Add New Book")
    print("2. Register New Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. View All Books")
    print("7. View All Members")
    print("8. View Overdue Books")
    print("9. View Statistics")
    print("10. Save & Exit")
    print("0. Exit Without Saving")

def add_book_menu(library):
    """Add a new book"""
    print("\n--- ADD NEW BOOK ---")
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    isbn = input("Enter ISBN: ").strip()
    year = input("Enter publication year (optional): ").strip()
    
    year = int(year) if year.isdigit() else None
    book = Book(title, author, isbn, year)
    
    success, message = library.add_book(book)
    print(f"\n{'correct' if success else 'false'} {message}")

def register_member_menu(library):
    """Register a new member"""
    print("\n--- REGISTER NEW MEMBER ---")
    name = input("Enter member name: ").strip()
    member_id = input("Enter member ID: ").strip()
    email = input("Enter email (optional): ").strip()
    
    member = Member(name, member_id, email)
    success, message = library.register_member(member)
    print(f"\n{'correct ' if success else 'false '} {message}")

def borrow_book_menu(library):
    """Borrow a book"""
    print("\n--- BORROW BOOK ---")
    isbn = input("Enter book ISBN: ").strip()
    member_id = input("Enter member ID: ").strip()
    
    success, message = library.borrow_book(isbn, member_id)
    print(f"\n{'correct' if success else 'flase'} {message}")

def return_book_menu(library):
    """Return a book"""
    print("\n--- RETURN BOOK ---")
    isbn = input("Enter book ISBN: ").strip()
    
    success, message = library.return_book(isbn)
    print(f"\n{'correct' if success else 'false'} {message}")

def search_books_menu(library):
    """Search for books"""
    print("\n--- SEARCH BOOKS ---")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by ISBN")
    print("4. Show All Available Books")
    
    choice = input("\nEnter search option: ").strip()
    
    if choice == '4':
        results = library.get_available_books()
        print(f"\n--- AVAILABLE BOOKS ({len(results)}) ---")
    else:
        search_map = {'1': 'title', '2': 'author', '3': 'isbn'}
        search_by = search_map.get(choice, 'title')
        query = input(f"Enter {search_by} to search: ").strip()
        results = library.search_books(query, search_by)
        print(f"\n--- SEARCH RESULTS ({len(results)} found) ---")
    
    if results:
        for i, book in enumerate(results, 1):
            status = "Available" if book.available else f"Borrowed (Due: {book.due_date})"
            print(f"\n{i}. {book.title}")
            print(f"   Author: {book.author}")
            print(f"   ISBN: {book.isbn}")
            if book.year:
                print(f"   Year: {book.year}")
            print(f"   Status: {status}")
            if book.is_overdue():
                print(f"    OVERDUE by {book.days_overdue()} days")
    else:
        print("No books found.")

def view_all_books(library):
    """View all books in the library"""
    print(f"\n--- ALL BOOKS ({len(library.books)}) ---")
    
    if not library.books:
        print("No books in the library.")
        return
    
    for i, book in enumerate(library.books.values(), 1):
        status = "Available" if book.available else f"Borrowed by {book.borrowed_by}"
        print(f"\n{i}. {book.title} by {book.author}")
        print(f"   ISBN: {book.isbn} | Year: {book.year or 'N/A'}")
        print(f"   Status: {status}")
        if book.due_date:
            print(f"   Due Date: {book.due_date}")
        if book.is_overdue():
            print(f"    OVERDUE by {book.days_overdue()} days")

def view_all_members(library):
    """View all library members"""
    print(f"\n--- ALL MEMBERS ({len(library.members)}) ---")
    
    if not library.members:
        print("No members registered.")
        return
    
    for i, member in enumerate(library.members.values(), 1):
        print(f"\n{i}. {member.name}")
        print(f"   ID: {member.member_id}")
        print(f"   Email: {member.email or 'N/A'}")
        print(f"   Borrowed Books: {len(member.borrowed_books)}/{member.max_borrow_limit}")
        print(f"   Join Date: {member.join_date}")
        
        if member.borrowed_books:
            print("   Currently Borrowed:")
            for isbn in member.borrowed_books:
                book = library.find_book(isbn)
                if book:
                    print(f"     - {book.title} (Due: {book.due_date})")

def view_overdue_books(library):
    """View overdue books"""
    overdue = library.get_overdue_books()
    print(f"\n--- OVERDUE BOOKS ({len(overdue)}) ---")
    
    if not overdue:
        print("No overdue books! ")
        return
    
    for i, book in enumerate(overdue, 1):
        print(f"\n{i}. {book.title} by {book.author}")
        print(f"   ISBN: {book.isbn}")
        print(f"   Borrowed by: {book.borrowed_by}")
        print(f"   Due Date: {book.due_date}")
        print(f"    {book.days_overdue()} days overdue")

def view_statistics(library):
    """View library statistics"""
    stats = library.get_statistics()
    
    print("\n--- LIBRARY STATISTICS ---")
    print(f"Total Books: {stats['total_books']}")
    print(f"Available Books: {stats['available_books']}")
    print(f"Borrowed Books: {stats['borrowed_books']}")
    print(f"Overdue Books: {stats['overdue_books']}")
    print(f"Total Members: {stats['total_members']}")

def main():
    """Main application loop"""
    library = Library()
    
    # Try to load existing data
    success, message = library.load_data()
    if success:
        print(f"✓ {message}")
    
    # Add sample data if library is empty
    if not library.books:
        sample_books = [
            Book("Python Crash Course", "Eric Matthes", "9781593279288", 2019),
            Book("Clean Code", "Robert Martin", "9780132350884", 2008),
            Book("The Pragmatic Programmer", "Hunt & Thomas", "9780135957059", 2019),
        ]
        for book in sample_books:
            library.add_book(book)
        
        sample_members = [
            Member("Alice Johnson", "MEM001", "alice@email.com"),
            Member("Bob Smith", "MEM002", "bob@email.com"),
        ]
        for member in sample_members:
            library.register_member(member)
        
        print("✓ Sample data loaded")
    
    print_header()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            add_book_menu(library)
        elif choice == '2':
            register_member_menu(library)
        elif choice == '3':
            borrow_book_menu(library)
        elif choice == '4':
            return_book_menu(library)
        elif choice == '5':
            search_books_menu(library)
        elif choice == '6':
            view_all_books(library)
        elif choice == '7':
            view_all_members(library)
        elif choice == '8':
            view_overdue_books(library)
        elif choice == '9':
            view_statistics(library)
        elif choice == '10':
            success, message = library.save_data()
            print(f"\n{'✓' if success else '✗'} {message}")
            print("\nThank you for using Library Management System!")
            break
        elif choice == '0':
            confirm = input("\nExit without saving? (y/n): ").strip().lower()
            if confirm == 'y':
                print("\nThank you for using Library Management System!")
                break
        else:
            print("\n✗ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()