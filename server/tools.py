COURSES = {
    1: [("MS-251", "Probability & Statistics", 3.0), ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0), ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5), ("GE-190", "Functional English", 3.0)],
    2: [("CC-112", "Programming Fundamentals", 3.0), ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0), ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0), ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0), ("HQ-002", "Quran Translation - II", 0.5)],
    3: [("CC-211", "Object Oriented Programming", 3.0), ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0), ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0), ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5)],
    4: [("CC-213", "Data Structures", 3.0), ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0), ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0), ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5)],
    5: [("CC-313", "Analysis of Algorithms", 3.0), ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0), ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0), ("HQ-005", "Quran Translation - V", 0.5)],
    6: [("CC-311", "Operating Systems", 3.0), ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0), ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0), ("HQ-006", "Quran Translation - VI", 0.5)],
    7: [("CC-411", "Final Year Project - I", 2.0), ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0), ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0), ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0), ("HQ-007", "Quran Translation - VII", 0.5)],
    8: [("CC-412", "Final Year Project - II", 4.0), ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0), ("HQ-008", "Quran Translation - VIII", 0.5)],
}


def marks_to_grades(marks: int) -> float:
    """Convert student marks (0-100) into a grade value (0-4)."""
    if marks < 0 or marks > 100:
        return -1.0
    if marks >= 85: return 4.0
    if marks >= 80: return 3.7
    if marks >= 75: return 3.3
    if marks >= 70: return 3.0
    if marks >= 65: return 2.7
    if marks >= 61: return 2.3
    if marks >= 58: return 2.0
    if marks >= 55: return 1.7
    if marks >= 50: return 1.0
    return 0.0


def calculate_semester_gpa(grade_points: list[float], credit_hours: list[float]) -> float | str:
    """Compute weighted GPA for one semester."""
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours lists cannot be empty."
    if len(grade_points) != len(credit_hours):
        return f"Error: Mismatch in input lengths. There are {len(grade_points)} grade points and {len(credit_hours)} credit hours."
    if any(gp < 0.0 or gp > 4.0 for gp in grade_points):
        return "Error: grade points must be between 0.0 and 4.0."
    if any(ch <= 0 for ch in credit_hours):
        return "Error: credit hours must be positive."
    total = sum(credit_hours)
    return round(sum(gp * ch for gp, ch in zip(grade_points, credit_hours)) / total, 2)


def calculate_new_cgpa(current_cgpa: float, completed_credit_hours: float, semester_gpa: float, semester_credit_hours: float) -> float | str:
    """Project CGPA after adding one semester."""
    if not 0 <= current_cgpa <= 4: return "Error: current_cgpa must be between 0.0 and 4.0."
    if not 0 <= semester_gpa <= 4: return "Error: semester_gpa must be between 0.0 and 4.0."
    if completed_credit_hours < 0: return "Error: completed_credit_hours cannot be negative."
    if semester_credit_hours <= 0: return "Error: semester_credit_hours must be greater than zero."
    total = completed_credit_hours + semester_credit_hours
    return round((current_cgpa * completed_credit_hours + semester_gpa * semester_credit_hours) / total, 2)


def required_gpa_for_target(target_cgpa: float, current_cgpa: float, completed_credit_hours: float, remaining_credit_hours: float) -> float | str:
    """Calculate the GPA needed across remaining credit hours to reach a target CGPA."""
    if not 0 <= target_cgpa <= 4: return "Error: target_cgpa must be between 0.0 and 4.0."
    if not 0 <= current_cgpa <= 4: return "Error: current_cgpa must be between 0.0 and 4.0."
    if completed_credit_hours < 0: return "Error: completed_credit_hours cannot be negative."
    if remaining_credit_hours <= 0: return "Error: remaining_credit_hours must be greater than zero."
    total = completed_credit_hours + remaining_credit_hours
    needed = target_cgpa * total - current_cgpa * completed_credit_hours
    return round(needed / remaining_credit_hours, 2)


def marks_to_grade_points(marks: int) -> float | str:
    """Convert percentage marks to a 4.0-scale grade point."""
    gp = marks_to_grades(marks)
    return "Error: marks must be between 0 and 100." if gp == -1.0 else gp


def get_semester_courses(semester: int) -> str:
    """Return courses and credit hours for semester 1 through 8."""
    if semester < 1 or semester > 8:
        return "Error: semester must be between 1 and 8."
    lines = [f"Semester {semester} Courses:"]
    total = 0.0
    for code, title, hours in COURSES.get(semester, []):
        lines.append(f"- {code}: {title} ({hours} Credit Hours)")
        total += hours
    lines.append(f"Total Semester Credit Hours: {total}")
    return "\n".join(lines)


def get_credit_hours(semesters: list[int]) -> float | str:
    """Return the total credit hours for one or more semesters."""
    if not semesters:
        return "Error: semesters list cannot be empty."
    total = 0.0
    for semester in semesters:
        if semester < 1 or semester > 8:
            return "Error: semesters must be between 1 and 8."
        total += sum(hours for _, _, hours in COURSES.get(semester, []))
    return round(total, 1)


def get_remaining_credit_hours(current_semester: int) -> float | str:
    """Calculate credit hours remaining after the current semester through semester 8."""
    if current_semester < 1 or current_semester > 8:
        return "Error: current_semester must be between 1 and 8."
    return round(sum(hours for semester in range(current_semester + 1, 9)
                     for _, _, hours in COURSES.get(semester, [])), 1)


def save_report(filename: str, content: str) -> str:
    """Write a text report or study plan to the workspace."""
    if not filename or not content:
        return "Error: filename and content cannot be empty."
    if not filename.endswith(".txt"):
        filename += ".txt"
    try:
        with open(filename, "w", encoding="utf-8") as report:
            report.write(content)
        return f"Report successfully saved to '{filename}'."
    except Exception as exc:
        return f"Error: Failed to save report. Details: {exc}"
