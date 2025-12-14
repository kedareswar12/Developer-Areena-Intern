
class GradeCalculator:
    def __init__(self):

        self.student_records = []
    
    def evaluate_performance(self, score):

        if score >= 90:
            return ('A+', 'Outstanding! Exceptional mastery of the subject.')
        elif score >= 80:
            return ('A', 'Excellent work! Strong understanding demonstrated.')
        elif score >= 70:
            return ('B', 'Good performance! Above average achievement.')
        elif score >= 60:
            return ('C', 'Satisfactory. Meets basic requirements.')
        elif score >= 50:
            return ('D', 'Passing grade. Significant improvement needed.')
        else:
            return ('F', 'Unsuccessful. Additional support required.')
    
    def add_student_result(self, name, marks):

        if marks < 0 or marks > 100:
            print("Error: Marks must be between 0 and 100")
            return False
        

        grade, comment = self.evaluate_performance(marks)
        
        
        record = {
            'name': name,
            'marks': marks,
            'grade': grade,
            'feedback': comment
        }
        
        
        self.student_records.append(record)
        

        print(f"\n{'='*50}")
        print(f"Student: {name}")
        print(f"Marks: {marks}/100")
        print(f"Grade: {grade}")
        print(f"Comment: {comment}")
        print(f"{'='*50}")
        
        return True
    
    def show_all_records(self):

        if not self.student_records:
            print("\nNo records available yet.")
            return
        
        print(f"\n{'='*60}")
        print(f"{'STUDENT RECORDS':^60}")
        print(f"{'='*60}")
        
        for idx, record in enumerate(self.student_records, 1):
            print(f"\n{idx}. Name: {record['name']}")
            print(f"   Marks: {record['marks']}/100 | Grade: {record['grade']}")
            print(f"   Feedback: {record['feedback']}")
        
        print(f"\n{'='*60}")
        print(f"Total Students: {len(self.student_records)}")
        print(f"{'='*60}")



def main():
    calculator = GradeCalculator()
    
    print("=" * 60)
    print("STUDENT GRADE CALCULATOR - VERSION 1".center(60))
    print("=" * 60)
    
    while True:
        print("\n--- Menu ---")
        print("1. Add Student Grade")
        print("2. View All Records")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            name = input("Enter student name: ")
            try:
                marks = float(input("Enter marks (0-100): "))
                calculator.add_student_result(name, marks)
            except ValueError:
                print("Error: Please enter valid numeric marks")
        
        elif choice == '2':
            calculator.show_all_records()
        
        elif choice == '3':
            print("\nThank you for using the Grade Calculator!")
            break
        
        else:
            print("Invalid choice! Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()