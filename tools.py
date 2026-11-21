from langchain_core.tools import tool

COURSES = {
    1: [
        ("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0),
    ],
    2: [
        ("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5),
    ],
    3: [
        ("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5),
    ],
    4: [
        ("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5),
    ],
    5: [
        ("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5),
    ],
    6: [
        ("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5),
    ],
    7: [
        ("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5),
    ],
    8: [
        ("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5),
    ],
}


def marks_to_grades(marks: int) -> float:
    """Convert student marks (0-100) into a grade value (0-4)"""
    if marks < 0 or marks > 100:
        return -1.0
    if marks >= 85:
        return 4.0
    elif marks >= 80:
        return 3.7
    elif marks >= 75:
        return 3.3
    elif marks >= 70:
        return 3.0
    elif marks >= 65:
        return 2.7
    elif marks >= 61:
        return 2.3
    elif marks >= 58:
        return 2.0
    elif marks >= 55:
        return 1.7
    elif marks >= 50:
        return 1.0
    return 0.0


@tool
def calculate_semester_gpa(
    grade_points: list[float], credit_hours: list[float]
) -> float | str:
    """Compute the weighted GPA for one semester using a student's grade points and credit hours.

    This function multiplies each grade point by its corresponding course credit hour,
    sums the weighted values, and divides by the total credit hours. It returns the
    result rounded to two decimals, or an error message when inputs are invalid.
    """
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours lists cannot be empty."

    if len(grade_points) != len(credit_hours):
        return f"Error: Mismatch in input lengths. There are {len(grade_points)} grade points and {len(credit_hours)} credit hours."

    for gp in grade_points:
        if gp < 0.0 or gp > 4.0:
            return f"Error: Invalid grade point {gp}. Must be between 0.0 and 4.0"

    for ch in credit_hours:
        if ch <= 0:
            return f"Error: Invalid credit hour {ch}. Credit hours must be positive."

    total_credit_hours = sum(credit_hours)
    if total_credit_hours == 0:
        return "Error: Total credit hours cannot be zero."

    weighted_points = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
    semester_gpa = weighted_points / total_credit_hours
    return round(semester_gpa, 2)


@tool
def calculate_new_cgpa(
    current_cgpa: float,
    completed_credit_hours: float,
    semester_gpa: float,
    semester_credit_hours: float,
) -> float | str:
    """Project the updated cumulative GPA after including one semester's performance.

    The function uses the current CGPA, previously completed credit hours, the semester GPA,
    and the current semester's credit hours to estimate the new cumulative result. It returns
    the new CGPA rounded to two decimals, or a validation error if any value is invalid.
    """
    if current_cgpa < 0.0 or current_cgpa > 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0."
    if semester_gpa < 0.0 or semester_gpa > 4.0:
        return "Error: semester_gpa must be between 0.0 and 4.0."
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative."
    if semester_credit_hours <= 0:
        return "Error: semester_credit_hours must be greater than zero."

    total_credit_hours = completed_credit_hours + semester_credit_hours
    if total_credit_hours == 0:
        return "Error: Total combined credit hours cannot be zero."

    total_quality_points = (current_cgpa * completed_credit_hours) + (
        semester_gpa * semester_credit_hours
    )
    new_cgpa = total_quality_points / total_credit_hours
    return round(new_cgpa, 2)


@tool
def required_gpa_for_target(
    target_cgpa: float,
    current_cgpa: float,
    completed_credit_hours: float,
    remaining_credit_hours: float,
) -> float | str:
    """Calculate the GPA required in the remaining credit hours to achieve a target CGPA.

    This tool estimates the average grade point needed across the remaining courses to reach
    the desired cumulative GPA. It returns the required GPA rounded to two decimals or an
    error string when the provided values are invalid.
    """
    if target_cgpa < 0.0 or target_cgpa > 4.0:
        return "Error: target_cgpa must be between 0.0 and 4.0."
    if current_cgpa < 0.0 or current_cgpa > 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0."
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative."
    if remaining_credit_hours <= 0:
        return "Error: remaining_credit_hours must be greater than zero."

    current_quality_points = current_cgpa * completed_credit_hours
    total_credit_hours = completed_credit_hours + remaining_credit_hours
    required_total_quality_points = target_cgpa * total_credit_hours
    needed_quality_points = required_total_quality_points - current_quality_points
    required_gpa = needed_quality_points / remaining_credit_hours
    return round(required_gpa, 2)


@tool
def marks_to_grade_points(marks: int) -> float | str:
    """Convert percentage marks into the equivalent grade point used in the GPA scale.

    Values from 0 to 100 are mapped to the university's grade-point system, such as 4.0 for
    85+ and 0.0 for failing marks. If the input is outside the valid range, it returns an error.
    """
    gp = marks_to_grades(marks)
    if gp == -1.0:
        return "Error: marks must be between 0 and 100."
    return gp


@tool
def get_semester_courses(semester: int) -> str:
    """Return all course codes, names, and credit hours for a specific semester.

    This tool fetches the curriculum data for semesters 1 through 8 and includes the total
    credit hours for that semester. It returns a clear error message if the semester is invalid
    or no courses are available for it.
    """
    if semester < 1 or semester > 8:
        return "Error: semester must be between 1 and 8."

    courses_list = COURSES.get(semester, [])
    if not courses_list:
        return f"Error: No courses found for semester {semester}."

    output = [f"Semester {semester} Courses:"]
    total_ch = 0.0
    for code, title, ch in courses_list:
        output.append(f"- {code}: {title} ({ch} Credit Hours)")
        total_ch += ch
    output.append(f"Total Semester Credit Hours: {total_ch}")
    return "\n".join(output)


@tool
def get_remaining_credit_hours(current_semester: int) -> float | str:
    """Calculate the total credit hours remaining from the next semester through semester 8.

    This function sums the credit hours of all future semesters and returns the remaining load as
    a rounded value. It raises an error if the provided semester number is outside the valid range.
    """
    if current_semester < 1 or current_semester > 8:
        return "Error: current_semester must be between 1 and 8."

    remaining_hours = 0.0
    for sem in range(current_semester + 1, 9):
        for _, _, ch in COURSES.get(sem, []):
            remaining_hours += ch
    return round(remaining_hours, 1)


@tool
def save_report(filename: str, content: str) -> str:
    """Write a report or study plan to a local text file in the workspace.

    The function ensures the file ends with a .txt extension, saves the provided content,
    and returns a confirmation message. If the filename or content is empty, or the file cannot
    be written, it returns a descriptive error message.
    """
    if not filename or not content:
        return "Error: filename and content cannot be empty."
    if not filename.endswith(".txt"):
        filename += ".txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Report successfully saved to '{filename}'."
    except Exception as e:
        return f"Error: Failed to save report. Details: {str(e)}"


TOOLS = [
    marks_to_grade_points,
    calculate_semester_gpa,
    calculate_new_cgpa,
    required_gpa_for_target,
    get_semester_courses,
    get_remaining_credit_hours,
    save_report,
]
