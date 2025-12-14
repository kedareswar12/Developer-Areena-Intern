from datetime import datetime
from collections import defaultdict

class ReportGenerator:
    """Generate various reports and statistics"""
    
    def __init__(self, expense_manager):
        self.manager = expense_manager
    
    def monthly_report(self, year, month):
        """Generate monthly summary report"""
        expenses = self.manager.get_monthly_expenses(year, month)
        
        if not expenses:
            return "No expenses found for this month."
        
        total = sum(e.amount for e in expenses)
        category_totals = defaultdict(float)
        
        for expense in expenses:
            category_totals[expense.category] += expense.amount
        
        report = f"\n{'='*60}\n"
        report += f"  MONTHLY REPORT - {datetime(year, month, 1).strftime('%B %Y')}\n"
        report += f"{'='*60}\n\n"
        report += f"Total Expenses: ${total:,.2f}\n"
        report += f"Number of Transactions: {len(expenses)}\n"
        report += f"Average per Transaction: ${total/len(expenses):,.2f}\n\n"
        report += f"{'='*60}\n"
        report += "CATEGORY BREAKDOWN:\n"
        report += f"{'='*60}\n"
        
        for category, amount in sorted(category_totals.items(), 
                                      key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100
            report += f"{category:.<20} ${amount:>10,.2f} ({percentage:>5.1f}%)\n"
        
        return report
    
    def category_breakdown(self):
        """Generate category-wise breakdown"""
        totals = self.manager.get_category_totals()
        total = sum(totals.values())
        
        if total == 0:
            return "No expenses recorded."
        
        report = f"\n{'='*60}\n"
        report += "  CATEGORY BREAKDOWN\n"
        report += f"{'='*60}\n\n"
        
        for category, amount in sorted(totals.items(), 
                                      key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100
            bar_length = int(percentage / 2)
            bar = 'bar ' * bar_length
            report += f"{category:.<15} ${amount:>10,.2f} ({percentage:>5.1f}%) {bar}\n"
        
        report += f"\n{'='*60}\n"
        report += f"TOTAL: ${total:,.2f}\n"
        report += f"{'='*60}\n"
        
        return report
    
    def statistics(self):
        """Generate overall statistics"""
        expenses = self.manager.get_all_expenses()
        
        if not expenses:
            return "No expenses recorded."
        
        total = sum(e.amount for e in expenses)
        avg = total / len(expenses)
        max_expense = max(expenses, key=lambda x: x.amount)
        min_expense = min(expenses, key=lambda x: x.amount)
        
        # Monthly averages
        monthly_totals = defaultdict(float)
        for expense in expenses:
            key = (expense.date.year, expense.date.month)
            monthly_totals[key] += expense.amount
        
        avg_monthly = sum(monthly_totals.values()) / len(monthly_totals) if monthly_totals else 0
        
        report = f"\n{'='*60}\n"
        report += "  STATISTICS\n"
        report += f"{'='*60}\n\n"
        report += f"Total Expenses: ${total:,.2f}\n"
        report += f"Total Transactions: {len(expenses)}\n"
        report += f"Average per Transaction: ${avg:,.2f}\n"
        report += f"Average Monthly Spending: ${avg_monthly:,.2f}\n\n"
        report += f"Highest Expense: ${max_expense.amount:,.2f} ({max_expense.category})\n"
        report += f"  Date: {max_expense.date} - {max_expense.description}\n\n"
        report += f"Lowest Expense: ${min_expense.amount:,.2f} ({min_expense.category})\n"
        report += f"  Date: {min_expense.date} - {min_expense.description}\n"
        report += f"\n{'='*60}\n"
        
        return report
