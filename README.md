# Prerequisite Violations Checker

A Python tool that analyzes student enrollment data to identify prerequisite violations for Fall 2025 and Spring 2026 terms. This tool helps academic institutions ensure students have completed required prerequisite courses before enrolling in advanced coursework.

## Features

- ✅ Analyzes student enrollment data against prerequisite requirements
- ✅ Identifies students enrolled in courses without completing prerequisites
- ✅ Generates comprehensive violation reports
- ✅ Exports detailed CSV reports for further analysis
- ✅ Provides executive summary with violation statistics
- ✅ Highlights students with multiple violations

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
- `Verified Grade`: Grade received (if completed)
- `Current Status`: Current enrollment status

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
Total Violations Found: 45
Students Affected: 23
Terms Analyzed: 2025FA (Fall 2025) and 2026SP (Spring 2026)

PREREQUISITE REQUIREMENTS ANALYZED:
  Advanced Programming → requires Introduction to Programming
  Database Design → requires Data Structures
  ...

MOST COMMON VIOLATIONS:
  1. Advanced Programming without Introduction to Programming: 12 violations
  2. Database Design without Data Structures: 8 violations
  ...
```

## How It Works

1. **Data Loading**: Reads student enrollment CSV and prerequisites Excel files
2. **Prerequisites Mapping**: Creates a dictionary mapping courses to their prerequisites
3. **Term Comparison**: Implements chronological term ordering (SP < SU < FA)
4. **Violation Detection**: For each enrollment in target terms (2025FA, 2026SP):
   - Checks if the course has prerequisites
   - Verifies if the student completed prerequisites before enrollment
   - Records violations where prerequisites are missing
5. **Report Generation**: Organizes and presents findings in multiple formats

## Troubleshooting

### Common Issues

**File Not Found Error**
```
Error: Could not find required file: ...
```
- Ensure both data files are in the same directory as the script
- Check that filenames match exactly (including spaces and capitalization)

**Empty Results**
- Verify data file formats match expected column structures
- Check that term values follow the YYYYFA/YYYYSP format
- Ensure prerequisite data is properly formatted in the Excel file

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