import os

class Library:
    
    def __init__(self):
        self.books = {}  # ISBN -> Book object
        self.members = {}  # member_id -> Member object
    
    def add_book(self, book):
        if book.isbn in self.books:
            return False, "Book with this ISBN already exists"
        
        self.books[book.isbn] = book
        return True, "Book added successfully"
    
    def remove_book(self, isbn):
        if isbn not in self.books:
            return False, "Book not found"
        
        if not self.books[isbn].available:
            return False, "Cannot remove a borrowed book"
        
        del self.books[isbn]
        return True, "Book removed successfully"
    
    def find_book(self, isbn):
        return self.books.get(isbn)
    
    def register_member(self, member):
        if member.member_id in self.members:
            return False, "Member ID already exists"
        
        self.members[member.member_id] = member
        return True, "Member registered successfully"
    
    def find_member(self, member_id):
        return self.members.get(member_id)
    
    def borrow_book(self, isbn, member_id):
        book = self.find_book(isbn)
        member = self.find_member(member_id)
        
        if not book:
            return False, "Book not found"
        
        if not member:
            return False, "Member not found"
        
        if not member.can_borrow():
            return False, f"Member has reached borrow limit ({member.max_borrow_limit} books)"
        
        # Check out the book
        success, message = book.check_out(member_id)
        if not success:
            return False, message
        
        # Add to member's borrowed list
        member.borrow_book(isbn)
        return True, message
    
    def return_book(self, isbn):
        book = self.find_book(isbn)
        
        if not book:
            return False, "Book not found"
        
        member_id = book.borrowed_by
        success, message = book.return_book()
        
        if success and member_id:
            member = self.find_member(member_id)
            if member:
                member.return_book(isbn)
        
        return success, message
    
    def search_books(self, query, search_by='title'):
        results = []
        query = query.lower()
        
        for book in self.books.values():
            if search_by == 'title' and query in book.title.lower():
                results.append(book)
            elif search_by == 'author' and query in book.author.lower():
                results.append(book)
            elif search_by == 'isbn' and query in book.isbn.lower():
                results.append(book)
        
        return results
    
    def get_available_books(self):
        return [book for book in self.books.values() if book.available]
    
    def get_overdue_books(self):
        return [book for book in self.books.values() if book.is_overdue()]
    
    def get_statistics(self):
        total_books = len(self.books)
        available_books = len(self.get_available_books())
        borrowed_books = total_books - available_books
        overdue_books = len(self.get_overdue_books())
        total_members = len(self.members)
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'overdue_books': overdue_books,
            'total_members': total_members
        }
    
    def save_data(self, books_file='data/books.json', members_file='data/members.json'):
        try:
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            # Save books
            books_data = {isbn: book.to_dict() for isbn, book in self.books.items()}
            with open(books_file, 'w') as f:
                json.dump(books_data, f, indent=2)
            
            # Save members
            members_data = {mid: member.to_dict() for mid, member in self.members.items()}
            with open(members_file, 'w') as f:
                json.dump(members_data, f, indent=2)
            
            return True, "Data saved successfully"
        except Exception as e:
            return False, f"Error saving data: {str(e)}"
    
    def load_data(self, books_file='data/books.json', members_file='data/members.json'):
        try:
            # Load books
            if os.path.exists(books_file):
                with open(books_file, 'r') as f:
                    books_data = json.load(f)
                    self.books = {isbn: Book.from_dict(data) for isbn, data in books_data.items()}
            
            # Load members
            if os.path.exists(members_file):
                with open(members_file, 'r') as f:
                    members_data = json.load(f)
                    self.members = {mid: Member.from_dict(data) for mid, data in members_data.items()}
            
            return True, f"Loaded {len(self.books)} books and {len(self.members)} members"
        except Exception as e:
            return False, f"Error loading data: {str(e)}"