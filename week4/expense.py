from datetime import datetime

class Expense:
    """Represents a single expense with validation"""
    
    def __init__(self, date, amount, category, description, expense_id=None):
        self.id = expense_id if expense_id else datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.date = self._validate_date(date)
        self.amount = self._validate_amount(amount)
        self.category = category
        self.description = description
    
    def _validate_date(self, date_str):
        """Validate and parse date string"""
        try:
            if isinstance(date_str, str):
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            return date_str
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    def _validate_amount(self, amount):
        """Validate amount is positive number"""
        try:
            amt = float(amount)
            if amt <= 0:
                raise ValueError("Amount must be positive")
            return round(amt, 2)
        except (ValueError, TypeError):
            raise ValueError("Invalid amount. Must be a positive number")
    
    def to_dict(self):
        """Convert expense to dictionary"""
        return {
            'id': self.id,
            'date': str(self.date),
            'amount': self.amount,
            'category': self.category,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create expense from dictionary"""
        return cls(
            date=data['date'],
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            expense_id=data.get('id')
        )
    
    def __str__(self):
        return f"{self.date} | ${self.amount:,.2f} | {self.category} | {self.description}"