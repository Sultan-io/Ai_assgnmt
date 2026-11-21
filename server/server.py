import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from fastmcp import FastMCP
from tools import (
    calculate_semester_gpa,
    calculate_new_cgpa,
    required_gpa_for_target,
    marks_to_grade_points,
    get_semester_courses,
    get_credit_hours,
    get_remaining_credit_hours,
    save_report,
)

mcp = FastMCP("cgpa")

for tool in (
    marks_to_grade_points,
    calculate_semester_gpa,
    calculate_new_cgpa,
    required_gpa_for_target,
    get_semester_courses,
    get_credit_hours,
    get_remaining_credit_hours,
    save_report,
):
    mcp.tool(tool)

if __name__ == "__main__":
        import os
        # Bind to 0.0.0.0 in the cloud so Render can route traffic, or 127.0.0.1 locally
        default_host = "0.0.0.0" if os.getenv("PORT") else "127.0.0.1"
        host = os.getenv("HOST", default_host)
        port = int(os.getenv("PORT", "8000"))
        
        print(f"Starting server on http://{host}:{port}/mcp ...")
        mcp.run(transport="http", host=host, port=port)
