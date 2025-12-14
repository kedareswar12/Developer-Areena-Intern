import json
import csv
import os
from datetime import datetime
import shutil

class FileHandler:
    """Handles file operations for expense data"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.expenses_file = os.path.join(data_dir, 'expenses.json')
        self.backup_dir = os.path.join(data_dir, 'backup')
        self.export_dir = os.path.join(data_dir, 'exports')
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.export_dir, exist_ok=True)
    
    def save_expenses(self, expenses):
        """Save expenses to JSON file"""
        try:
            data = [e.to_dict() for e in expenses]
            with open(self.expenses_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving expenses: {e}")
            return False
    
    def load_expenses(self):
        """Load expenses from JSON file"""
        try:
            if not os.path.exists(self.expenses_file):
                return []
            
            with open(self.expenses_file, 'r') as f:
                data = json.load(f)
            
            from expense import Expense
            return [Expense.from_dict(item) for item in data]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading expenses: {e}")
            return []
    
    def backup_data(self):
        """Create backup of current data"""
        try:
            if not os.path.exists(self.expenses_file):
                print("No data to backup")
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f'expenses_backup_{timestamp}.json')
            shutil.copy2(self.expenses_file, backup_file)
            print(f"Backup created: {backup_file}")
            return True
        except IOError as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore_from_backup(self, backup_filename):
        """Restore data from backup file"""
        try:
            backup_path = os.path.join(self.backup_dir, backup_filename)
            if not os.path.exists(backup_path):
                print("Backup file not found")
                return False
            
            shutil.copy2(backup_path, self.expenses_file)
            print("Data restored successfully")
            return True
        except IOError as e:
            print(f"Error restoring backup: {e}")
            return False
    
    def list_backups(self):
        """List available backup files"""
        try:
            backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            return sorted(backups, reverse=True)
        except OSError:
            return []
    
    def export_to_csv(self, expenses, filename=None):
        """Export expenses to CSV file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f'expenses_export_{timestamp}.csv'
            
            filepath = os.path.join(self.export_dir, filename)
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Amount', 'Category', 'Description'])
                for expense in expenses:
                    writer.writerow([expense.date, expense.amount, 
                                   expense.category, expense.description])
            
            print(f"Data exported to: {filepath}")
            return True
        except IOError as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def import_from_csv(self, filename):
        """Import expenses from CSV file"""
        try:
            filepath = os.path.join(self.export_dir, filename)
            if not os.path.exists(filepath):
                print("CSV file not found")
                return []
            
            from expense import Expense
            expenses = []
            
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        expense = Expense(
                            date=row['Date'],
                            amount=row['Amount'],
                            category=row['Category'],
                            description=row['Description']
                        )
                        expenses.append(expense)
                    except (ValueError, KeyError) as e:
                        print(f"Skipping invalid row: {e}")
            
            return expenses
        except IOError as e:
            print(f"Error importing from CSV: {e}")
            return []
