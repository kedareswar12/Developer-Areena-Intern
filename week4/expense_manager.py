from datetime import datetime

class ExpenseManager:
    """Manages collection of expenses"""
    
    def __init__(self):
        self.expenses = []
    
    def add_expense(self, expense):
        """Add expense to collection"""
        self.expenses.append(expense)
    
    def remove_expense(self, expense_id):
        """Remove expense by ID"""
        self.expenses = [e for e in self.expenses if e.id != expense_id]
    
    def get_expense(self, expense_id):
        """Get expense by ID"""
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None
    
    def update_expense(self, expense_id, **kwargs):
        """Update expense fields"""
        expense = self.get_expense(expense_id)
        if expense:
            if 'date' in kwargs:
                expense.date = expense._validate_date(kwargs['date'])
            if 'amount' in kwargs:
                expense.amount = expense._validate_amount(kwargs['amount'])
            if 'category' in kwargs:
                expense.category = kwargs['category']
            if 'description' in kwargs:
                expense.description = kwargs['description']
            return True
        return False
    
    def search_expenses(self, **criteria):
        """Search expenses by criteria"""
        results = self.expenses
        
        if 'category' in criteria:
            results = [e for e in results if e.category == criteria['category']]
        
        if 'date_from' in criteria:
            date_from = datetime.strptime(criteria['date_from'], "%Y-%m-%d").date()
            results = [e for e in results if e.date >= date_from]
        
        if 'date_to' in criteria:
            date_to = datetime.strptime(criteria['date_to'], "%Y-%m-%d").date()
            results = [e for e in results if e.date <= date_to]
        
        if 'description' in criteria:
            keyword = criteria['description'].lower()
            results = [e for e in results if keyword in e.description.lower()]
        
        return results
    
    def get_all_expenses(self):
        """Get all expenses sorted by date"""
        return sorted(self.expenses, key=lambda x: x.date, reverse=True)
    
    def get_total(self):
        """Get total of all expenses"""
        return sum(e.amount for e in self.expenses)
    
    def get_category_totals(self):
        """Get totals by category"""
        totals = {}
        for expense in self.expenses:
            totals[expense.category] = totals.get(expense.category, 0) + expense.amount
        return totals
    
    def get_monthly_expenses(self, year, month):
        """Get expenses for specific month"""
        return [e for e in self.expenses 
                if e.date.year == year and e.date.month == month]
