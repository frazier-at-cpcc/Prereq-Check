#!/usr/bin/env python3
"""
Prerequisite Violations Checker
Analyzes student enrollment data to identify prerequisite violations for 2025FA and 2026SP terms.

Requirements:
- pandas
- openpyxl

Install with: pip install pandas openpyxl

Usage:
python prerequisite_checker.py
"""

import pandas as pd
import sys
from pathlib import Path
from collections import defaultdict

def load_data():
    """Load the CSV and Excel files."""
    try:
        # Load student enrollment data
        csv_file = "ST.csv"
        df_students = pd.read_csv(csv_file)
        
        # Clean column names (remove extra spaces)
        df_students.columns = df_students.columns.str.strip()
        
        # Load prerequisites data
        excel_file = "Prerequisites.xlsx"
        df_prereqs = pd.read_excel(excel_file, sheet_name='Prerequisites')
        
        return df_students, df_prereqs
        
    except FileNotFoundError as e:
        print(f"Error: Could not find required file: {e}")
        print("\nPlease ensure the following files are in the same directory as this script:")
        print("1. ST STC List students enrolled in a term taking a certain class list their history of course records RISE.csv")
        print("2. Prerequisites  IT and AI Degrees.xlsx")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def build_prerequisites_map(df_prereqs):
    """Build a dictionary mapping courses to their prerequisites."""
    prerequisites = {}
    
    # Skip header row and process each prerequisite
    for idx, row in df_prereqs.iterrows():
        if idx == 0:  # Skip header row
            continue
            
        course = row.iloc[1]  # Course Prefix & Course Number
        prerequisite = row.iloc[3]  # LOCAL ADD
        
        if pd.notna(course) and pd.notna(prerequisite):
            prerequisites[course.strip()] = prerequisite.strip()
    
    return prerequisites

def is_term_before(term1, term2):
    """Check if term1 comes before term2 chronologically."""
    if pd.isna(term1) or pd.isna(term2):
        return False
    
    def get_term_value(term):
        """Convert term to numeric value for comparison."""
        year = int(term[:4])
        semester = term[4:]
        semester_values = {'SP': 1, 'SU': 2, 'FA': 3}
        return year * 10 + semester_values.get(semester, 0)
    
    return get_term_value(term1) < get_term_value(term2)

def has_completed_prerequisite(student_id, prerequisite_course, before_term, df_students):
    """Check if a student has completed a prerequisite course before a given term."""
    student_records = df_students[df_students['Student Id'] == student_id]
    
    # Find records where student took the prerequisite course before the target term with verified grades
    prereq_records_with_grade = student_records[
        (student_records['Course Name'] == prerequisite_course) &
        (student_records['Verified Grade'].notna()) &
        (student_records['Verified Grade'] != '') &
        (student_records['Term'].apply(lambda x: is_term_before(x, before_term)))
    ]
    
    # Also check for prerequisites taken before or in the same semester with 'N' or 'A' status and blank grade
    prereq_records_n_a_status = student_records[
        (student_records['Course Name'] == prerequisite_course) &
        (student_records['Current Status'].isin(['N', 'A'])) &
        ((student_records['Verified Grade'].isna()) | (student_records['Verified Grade'] == '')) &
        ((student_records['Term'].apply(lambda x: is_term_before(x, before_term))) | 
         (student_records['Term'] == before_term))
    ]
    
    return len(prereq_records_with_grade) > 0 or len(prereq_records_n_a_status) > 0

def analyze_violations(df_students, prerequisites):
    """Analyze prerequisite violations for target terms."""
    target_terms = ['2025FA', '2026SP']
    
    # Filter students in target terms
    target_enrollments = df_students[df_students['Term'].isin(target_terms)]
    
    # Filter for courses that have prerequisites
    courses_with_prereqs = target_enrollments[
        target_enrollments['Course Name'].isin(prerequisites.keys())
    ]
    
    violations = []
    
    for idx, record in courses_with_prereqs.iterrows():
        course = record['Course Name']
        prerequisite = prerequisites[course]
        student_id = record['Student Id']
        student_name = f"{record['First Name']} {record['Last Name']}"
        term = record['Term']
        email = record.get('Student Email', '')
        
        # Check if prerequisite was completed
        if not has_completed_prerequisite(student_id, prerequisite, term, df_students):
            violations.append({
                'student_id': student_id,
                'student_name': student_name,
                'email': email,
                'term': term,
                'course': course,
                'missing_prerequisite': prerequisite,
                'current_status': record.get('Current Status', ''),
                'verified_grade': record.get('Verified Grade', '')
            })
    
    return violations

def generate_report(violations, prerequisites):
    """Generate and print the violations report."""
    print("=" * 80)
    print("PREREQUISITE VIOLATIONS REPORT")
    print("Students Enrolled in 2025FA & 2026SP Without Meeting Prerequisites")
    print("=" * 80)
    
    print(f"\nEXECUTIVE SUMMARY:")
    print(f"Total Violations Found: {len(violations)}")
    
    # Count unique students
    unique_students = len(set(v['student_id'] for v in violations))
    print(f"Students Affected: {unique_students}")
    print(f"Terms Analyzed: 2025FA (Fall 2025) and 2026SP (Spring 2026)")
    
    print(f"\nPREREQUITE REQUIREMENTS ANALYZED:")
    for course, prereq in prerequisites.items():
        print(f"  {course} → requires {prereq}")
    
    # Count violations by type
    violation_counts = defaultdict(int)
    for v in violations:
        violation_key = f"{v['course']} without {v['missing_prerequisite']}"
        violation_counts[violation_key] += 1
    
    print(f"\nMOST COMMON VIOLATIONS:")
    sorted_violations = sorted(violation_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (violation_type, count) in enumerate(sorted_violations[:10], 1):
        print(f"  {i}. {violation_type}: {count} violations")
    
    # Group violations by student
    violations_by_student = defaultdict(list)
    for v in violations:
        violations_by_student[v['student_id']].append(v)
    
    # Students with multiple violations
    multi_violations = {sid: viols for sid, viols in violations_by_student.items() if len(viols) >= 4}
    
    if multi_violations:
        print(f"\nSTUDENTS WITH 4+ VIOLATIONS:")
        for student_id, student_violations in sorted(multi_violations.items(), 
                                                   key=lambda x: len(x[1]), reverse=True):
            student = student_violations[0]
            print(f"\n{student['student_name']} (ID: {student_id})")
            print(f"Email: {student['email']}")
            print(f"Total violations: {len(student_violations)}")
            for v in student_violations:
                print(f"  • {v['term']}: {v['course']} without {v['missing_prerequisite']}")
    
    print(f"\n" + "=" * 80)
    print("DETAILED VIOLATION LIST")
    print("=" * 80)
    
    # Sort students by number of violations (descending), then by name
    sorted_students = sorted(violations_by_student.items(), 
                           key=lambda x: (-len(x[1]), x[1][0]['student_name']))
    
    for student_id, student_violations in sorted_students:
        student = student_violations[0]
        print(f"\n{student['student_name']} (ID: {student_id})")
        print(f"Email: {student['email']}")
        print(f"Violations: {len(student_violations)}")
        
        for v in sorted(student_violations, key=lambda x: (x['term'], x['course'])):
            print(f"  • {v['term']}: Enrolled in {v['course']} without completing {v['missing_prerequisite']}")

def save_csv_report(violations):
    """Save violations to a CSV file for further analysis."""
    if violations:
        df_violations = pd.DataFrame(violations)
        output_file = "prerequisite_violations_report.csv"
        df_violations.to_csv(output_file, index=False)
        print(f"\nDetailed report saved to: {output_file}")

def main():
    """Main function to run the prerequisite violations analysis."""
    print("Loading data...")
    df_students, df_prereqs = load_data()
    
    print("Building prerequisites map...")
    prerequisites = build_prerequisites_map(df_prereqs)
    
    print(f"Found {len(prerequisites)} prerequisite requirements")
    print("Analyzing violations...")
    
    violations = analyze_violations(df_students, prerequisites)
    
    generate_report(violations, prerequisites)
    save_csv_report(violations)
    
    print(f"\nAnalysis complete!")

if __name__ == "__main__":
    main()