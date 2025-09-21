# Prerequisite Violations Checker

A Python tool that analyzes student enrollment data to identify prerequisite violations for Fall 2025 and Spring 2026 terms. This tool helps academic institutions ensure students have completed required prerequisite courses before enrolling in advanced coursework.

## Features

- ✅ Analyzes student enrollment data against prerequisite requirements
- ✅ Identifies students enrolled in courses without completing prerequisites
- ✅ **Recognizes in-progress prerequisites** with 'N' or 'A' status and blank grades
- ✅ **Smart concurrent enrollment detection** for same-semester prerequisites
- ✅ Generates comprehensive violation reports
- ✅ Exports detailed CSV reports for further analysis
- ✅ Provides executive summary with violation statistics
- ✅ Highlights students with multiple violations

## Key Logic Features

### Prerequisite Recognition
The tool recognizes prerequisites as satisfied in the following scenarios:

1. **Completed Prerequisites**: Courses taken in previous terms with verified grades
2. **In-Progress Prerequisites**: Courses taken in previous terms or concurrently with:
   - Current Status of 'N' (enrolled) or 'A' (active)
   - Blank or empty Verified Grade field

This ensures students are not flagged when they are legitimately taking prerequisites and follow-up courses in logical sequence (e.g., taking CSC-113 in Fall 2025 and CSC-114 in Spring 2026).

## Requirements

- Python 3.6 or higher
- pandas
- openpyxl

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install pandas openpyxl
```

## Required Data Files

The tool requires two data files to be placed in the same directory as the script:

1. **Student Enrollment Data (CSV)**
   - Filename: `ST.csv`
   - Contains student enrollment records with course history

2. **Prerequisites Data (Excel)**
   - Filename: `Prerequisites.xlsx`
   - Contains prerequisite requirements for IT and AI degree courses
   - Must have a sheet named 'Prerequisites'

### Data File Formats

#### Student Enrollment CSV Expected Columns:
- `Student Id`: Unique student identifier
- `First Name`: Student's first name
- `Last Name`: Student's last name
- `Student Email`: Student's email address
- `Term`: Academic term (format: YYYYFA/YYYYSP, e.g., 2025FA, 2026SP)
- `Course Name`: Name of the course
- `Verified Grade`: Grade received (if completed, may be blank for in-progress courses)
- `Current Status`: Current enrollment status ('N' for enrolled, 'A' for active, etc.)

#### Prerequisites Excel Expected Columns:
- Column B (index 1): Course Prefix & Course Number
- Column D (index 3): Prerequisite course (LOCAL ADD)

## Usage

1. Ensure all required data files are in the same directory as `prereq-checker.py`
2. Run the script:

```bash
python prereq-checker.py
```

The tool will:
1. Load and validate the data files
2. Build a map of prerequisite requirements
3. Analyze enrollments for violations
4. Display a comprehensive report to the console
5. Generate a CSV file with detailed violation data

## Output

### Console Report
The tool generates a detailed console report including:

- **Executive Summary**: Total violations, affected students, terms analyzed
- **Prerequisites Analyzed**: List of course → prerequisite relationships
- **Most Common Violations**: Top 10 violation types by frequency
- **Students with 4+ Violations**: Detailed list of heavily affected students
- **Detailed Violation List**: Complete list of all violations organized by student

### CSV Export
A CSV file named `prerequisite_violations_report.csv` is generated containing:
- Student ID and contact information
- Term and course details
- Missing prerequisite information
- Current enrollment status

## Example Output

```
================================================================================
PREREQUISITE VIOLATIONS REPORT
Students Enrolled in 2025FA & 2026SP Without Meeting Prerequisites
================================================================================

EXECUTIVE SUMMARY:
Total Violations Found: 38
Students Affected: 30
Terms Analyzed: 2025FA (Fall 2025) and 2026SP (Spring 2026)

PREREQUISITE REQUIREMENTS ANALYZED:
  CSC-115 → requires CSC-112
  CSC-215 → requires CSC-115
  CSC-161 → requires CSC-215
  CSC-162 → requires CSC-161
  CSC-114 → requires CSC-113
  CSC-214 → requires CSC-114
  CSC-128 → requires CSC-121
  CSC-228 → requires CSC-128
  WEB-140 → requires WEB-110

MOST COMMON VIOLATIONS:
  1. CSC-115 without CSC-112: 9 violations
  2. CSC-114 without CSC-113: 8 violations
  3. CSC-162 without CSC-161: 8 violations
```

## How It Works

1. **Data Loading**: Reads student enrollment CSV and prerequisites Excel files
2. **Prerequisites Mapping**: Creates a dictionary mapping courses to their prerequisites
3. **Term Comparison**: Implements chronological term ordering (SP < SU < FA)
4. **Violation Detection**: For each enrollment in target terms (2025FA, 2026SP):
   - Checks if the course has prerequisites
   - Verifies if the student completed prerequisites through:
     - **Completed courses**: Previous terms with verified grades
     - **In-progress courses**: Previous or same term with 'N'/'A' status and blank grades
   - Records violations only when prerequisites are truly missing
5. **Report Generation**: Organizes and presents findings in multiple formats

### Smart Prerequisite Logic

The tool uses intelligent logic to avoid false positives:

- **Concurrent Enrollment**: Students taking a prerequisite and follow-up course in the same semester are not flagged
- **In-Progress Recognition**: Prerequisites with 'N' or 'A' status and blank grades are considered valid
- **Sequential Planning**: Students who took prerequisites in Fall 2025 are not flagged for follow-up courses in Spring 2026

This ensures the tool identifies true violations while respecting normal academic progression patterns.

## Troubleshooting

### Common Issues

**File Not Found Error**
```
Error: Could not find required file: ...
```
- Ensure both data files are in the same directory as the script
- Check that filenames match exactly (including spaces and capitalization)

**Empty or Fewer Results Than Expected**
- The tool now uses smart logic to avoid false positives
- Students taking prerequisites concurrently or in logical sequence are not flagged
- Verify that actual prerequisite violations exist in your data
- Check that Current Status values include 'N' and 'A' for enrolled students

**Data Loading Errors**
- Verify CSV file is properly formatted and not corrupted
- Check Excel file has the 'Prerequisites' sheet
- Ensure required columns are present in both files

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is provided as-is for educational and administrative purposes.

---

*Last updated: September 21, 2025*
*Recent updates: Enhanced prerequisite logic to handle in-progress courses and concurrent enrollment*