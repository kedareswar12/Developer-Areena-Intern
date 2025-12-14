class Member:
    
    
    def __init__(self, name, member_id, email=""):
        self.name = name
        self.member_id = member_id
        self.email = email
        self.borrowed_books = []
        self.max_borrow_limit = 5
        self.join_date = datetime.now().strftime('%Y-%m-%d')
    
    def can_borrow(self):
        
        return len(self.borrowed_books) < self.max_borrow_limit
    
    def borrow_book(self, isbn):
        
        if not self.can_borrow():
            return False, "Borrow limit reached"
        
        self.borrowed_books.append(isbn)
        return True, "Book added to member's list"
    
    def return_book(self, isbn):

        if isbn not in self.borrowed_books:
            return False, "Book not found in member's borrowed list"
        
        self.borrowed_books.remove(isbn)
        return True, "Book removed from member's list"
    
    def to_dict(self):

        return {
            'name': self.name,
            'member_id': self.member_id,
            'email': self.email,
            'borrowed_books': self.borrowed_books,
            'max_borrow_limit': self.max_borrow_limit,
            'join_date': self.join_date
        }
    
    @classmethod
    def from_dict(cls, data):
        member = cls(
            name=data['name'],
            member_id=data['member_id'],
            email=data.get('email', '')
        )
        member.borrowed_books = data.get('borrowed_books', [])
        member.max_borrow_limit = data.get('max_borrow_limit', 5)
        member.join_date = data.get('join_date', datetime.now().strftime('%Y-%m-%d'))
        return member
    
    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) - {len(self.borrowed_books)}/{self.max_borrow_limit} books borrowed"