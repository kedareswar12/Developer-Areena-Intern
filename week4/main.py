from datetime import datetime
from expense import Expense
from expense_manager import ExpenseManager
from file_handler import FileHandler
from reports import ReportGenerator

class FinanceTracker:
    """Main application class"""
    
    CATEGORIES = ['Food', 'Transport', 'Shopping', 'Bills', 
                  'Entertainment', 'Healthcare', 'Other']
    
    def __init__(self):
        self.manager = ExpenseManager()
        self.file_handler = FileHandler()
        self.report_gen = ReportGenerator(self.manager)
        self.budgets = {}
        self._load_data()
    
    def _load_data(self):
        """Load expenses from file"""
        expenses = self.file_handler.load_expenses()
        for expense in expenses:
            self.manager.add_expense(expense)
    
    def _save_data(self):
        """Save expenses to file"""
        self.file_handler.save_expenses(self.manager.get_all_expenses())
    
    def run(self):
        """Main application loop"""
        print("=" * 60)
        print("          PERSONAL FINANCE TRACKER")
        print("=" * 60)
        
        while True:
            print("\n" + "=" * 40)
            print("              MAIN MENU")
            print("=" * 40)
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. Search Expenses")
            print("4. Generate Monthly Report")
            print("5. View Category Breakdown")
            print("6. Set/Update Budget")
            print("7. Export Data to CSV")
            print("8. View Statistics")
            print("9. Backup/Restore Data")
            print("0. Exit")
            print("=" * 40)
            
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.search_expenses()
            elif choice == '4':
                self.generate_monthly_report()
            elif choice == '5':
                self.view_category_breakdown()
            elif choice == '6':
                self.set_budget()
            elif choice == '7':
                self.export_data()
            elif choice == '8':
                self.view_statistics()
            elif choice == '9':
                self.backup_restore()
            elif choice == '0':
                self._save_data()
                print("\n" + "=" * 60)
                print("Thank you for using Personal Finance Tracker!")
                print("Data saved successfully.")
                print("=" * 60)
                break
            else:
                print("Invalid choice! Please enter 0-9.")
    
    def add_expense(self):
        """Add new expense"""
        print("\n" + "=" * 60)
        print("  ADD NEW EXPENSE")
        print("=" * 60)
        
        try:
            date_str = input("Date (YYYY-MM-DD) [Enter for today]: ").strip()
            if not date_str:
                date_str = datetime.now().strftime("%Y-%m-%d")
            
            amount = input("Amount: $").strip()
            
            print("\nCategories:")
            for i, cat in enumerate(self.CATEGORIES, 1):
                print(f"{i}. {cat}")
            
            cat_choice = input(f"Select category (1-{len(self.CATEGORIES)}): ").strip()
            try:
                category = self.CATEGORIES[int(cat_choice) - 1]
            except (ValueError, IndexError):
                print(" Invalid category. Using 'Other'")
                category = 'Other'
            
            description = input("Description: ").strip()
            
            expense = Expense(date_str, amount, category, description)
            self.manager.add_expense(expense)
            self._save_data()
            
            print(f"\n Expense added successfully!")
            print(f"   {expense}")
            
        except ValueError as e:
            print(f" Error: {e}")
    
    def view_expenses(self):
        """View all expenses"""
        print("\n" + "=" * 60)
        print("  ALL EXPENSES")
        print("=" * 60)
        
        expenses = self.manager.get_all_expenses()
        
        if not expenses:
            print("\nNo expenses recorded yet.")
            return
        
        print(f"\n{'Date':<12} {'Amount':>10} {'Category':<15} {'Description'}")
        print("-" * 60)
        
        for expense in expenses:
            print(f"{str(expense.date):<12} ${expense.amount:>9,.2f} "
                  f"{expense.category:<15} {expense.description}")
        
        print("-" * 60)
        print(f"{'TOTAL:':<12} ${self.manager.get_total():>9,.2f}")
        print("=" * 60)
    
    def search_expenses(self):
        """Search expenses"""
        print("\n" + "=" * 60)
        print("  SEARCH EXPENSES")
        print("=" * 60)
        print("\n1. Search by Category")
        print("2. Search by Date Range")
        print("3. Search by Description")
        print("4. Back to Menu")
        
        choice = input("\nSelect search type (1-4): ").strip()
        
        criteria = {}
        
        if choice == '1':
            print("\nCategories:")
            for i, cat in enumerate(self.CATEGORIES, 1):
                print(f"{i}. {cat}")
            cat_choice = input("Select category: ").strip()
            try:
                criteria['category'] = self.CATEGORIES[int(cat_choice) - 1]
            except (ValueError, IndexError):
                print(" Invalid category")
                return
        
        elif choice == '2':
            criteria['date_from'] = input("From date (YYYY-MM-DD): ").strip()
            criteria['date_to'] = input("To date (YYYY-MM-DD): ").strip()
        
        elif choice == '3':
            criteria['description'] = input("Search keyword: ").strip()
        
        elif choice == '4':
            return
        
        else:
            print(" Invalid choice")
            return
        
        results = self.manager.search_expenses(**criteria)
        
        if not results:
            print("\nNo expenses found matching criteria.")
            return
        
        print(f"\nFound {len(results)} expense(s):")
        print(f"\n{'Date':<12} {'Amount':>10} {'Category':<15} {'Description'}")
        print("-" * 60)
        
        for expense in results:
            print(f"{str(expense.date):<12} ${expense.amount:>9,.2f} "
                  f"{expense.category:<15} {expense.description}")
    
    def generate_monthly_report(self):
        """Generate monthly report"""
        print("\n" + "=" * 60)
        print("  MONTHLY REPORT")
        print("=" * 60)
        
        try:
            year = int(input("Year (YYYY): ").strip())
            month = int(input("Month (1-12): ").strip())
            
            report = self.report_gen.monthly_report(year, month)
            print(report)
            
        except ValueError:
            print(" Invalid year or month")
    
    def view_category_breakdown(self):
        """View category breakdown"""
        report = self.report_gen.category_breakdown()
        print(report)
    
    def set_budget(self):
        """Set or update budget"""
        print("\n" + "=" * 60)
        print("  SET/UPDATE BUDGET")
        print("=" * 60)
        
        print("\nCategories:")
        for i, cat in enumerate(self.CATEGORIES, 1):
            current = self.budgets.get(cat, 0)
            print(f"{i}. {cat} (Current: ${current:,.2f})")
        
        try:
            cat_choice = input(f"\nSelect category (1-{len(self.CATEGORIES)}): ").strip()
            category = self.CATEGORIES[int(cat_choice) - 1]
            amount = float(input(f"Budget amount for {category}: $").strip())
            
            self.budgets[category] = amount
            print(f"\n Budget for {category} set to ${amount:,.2f}")
            
            # Check current spending
            totals = self.manager.get_category_totals()
            spent = totals.get(category, 0)
            remaining = amount - spent
            
            print(f"   Spent so far: ${spent:,.2f}")
            print(f"   Remaining: ${remaining:,.2f}")
            
            if remaining < 0:
                print(f"     Over budget by ${abs(remaining):,.2f}!")
            
        except (ValueError, IndexError) as e:
            print(f" Error: {e}")
    
    def export_data(self):
        """Export data to CSV"""
        print("\n" + "=" * 60)
        print("  EXPORT DATA")
        print("=" * 60)
        
        expenses = self.manager.get_all_expenses()
        
        if not expenses:
            print("\nNo data to export.")
            return
        
        filename = input("\nFilename (leave blank for auto): ").strip()
        filename = filename if filename else None
        
        if self.file_handler.export_to_csv(expenses, filename):
            print(" Data exported successfully!")
    
    def view_statistics(self):
        """View statistics"""
        report = self.report_gen.statistics()
        print(report)
    
    def backup_restore(self):
        """Backup or restore data"""
        print("\n" + "=" * 60)
        print("  BACKUP/RESTORE")
        print("=" * 60)
        print("\n1. Create Backup")
        print("2. Restore from Backup")
        print("3. List Backups")
        print("4. Back to Menu")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            if self.file_handler.backup_data():
                print(" Backup created successfully!")
        
        elif choice == '2':
            backups = self.file_handler.list_backups()
            if not backups:
                print("No backups available.")
                return
            
            print("\nAvailable backups:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup}")
            
            try:
                idx = int(input("\nSelect backup to restore: ").strip()) - 1
                if self.file_handler.restore_from_backup(backups[idx]):
                    print(" Data restored! Reloading...")
                    self.manager.expenses.clear()
                    self._load_data()
            except (ValueError, IndexError):
                print(" Invalid selection")
        
        elif choice == '3':
            backups = self.file_handler.list_backups()
            if not backups:
                print("No backups available.")
            else:
                print("\nAvailable backups:")
                for backup in backups:
                    print(f"  • {backup}")
        
        elif choice == '4':
            return
        
        else:
            print(" Invalid choice")


def main():
    """Application entry point"""
    tracker = FinanceTracker()
    tracker.run()


if __name__ == "__main__":
    main()