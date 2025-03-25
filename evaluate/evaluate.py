import os
import sys
import pandas as pd
import importlib.util
import subprocess
from report_generator import generate_reports

def load_student_module(student_file):
    """Dynamically load student.py before anything else"""
    spec = importlib.util.spec_from_file_location("student", student_file)
    student_module = importlib.util.module_from_spec(spec)
    sys.modules["student"] = student_module  # Make it globally available
    spec.loader.exec_module(student_module)
    return student_module

def evaluate_student_code(student_id, local_path):
    print(f"🔍 Evaluating code for {student_id}...")
    student_file = os.path.join(local_path, "student.py")

    # 1. Load student.py FIRST
    load_student_module(student_file)

    # 2. Run tests using pytest
    print("Running pytest...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "evaluate/test_cases.py", "--tb=short", "-v"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )

    # 3. Parse pytest output
    results = {}
    total_score = 0
    from test_cases import test_suite

    # Parse console output for test results
    for line in result.stdout.split('\n'):
        for tc_id, (_, max_score) in test_suite.items():
            if tc_id in line:
                if "PASSED" in line:
                    results[tc_id] = max_score
                    total_score += max_score
                    print(f"  - {tc_id}: ✅ Passed ({max_score}/{max_score})")
                elif "FAILED" in line:
                    results[tc_id] = 0
                    print(f"  - {tc_id}: ❌ Failed (0/{max_score})")

    # If no results found, consider all tests failed
    if not results:
        for tc_id, (_, max_score) in test_suite.items():
            results[tc_id] = 0
            print(f"  - {tc_id}: ❌ Failed (0/{max_score})")

    # Print total score
    total_possible = sum(m for _, m in test_suite.values())
    print(f"🏁 Total score for {student_id}: {total_score} / {total_possible}")

    # Print error output for debugging
    if result.stderr:
        print("🚨 Pytest Error Output:")
        print(result.stderr)

    return results, total_score


# def evaluate_student_code(student_id, local_path):
#     print(f"🔍 Evaluating code for {student_id}...")
#     test_path = os.path.join(local_path, "test_cases.py")

#     # 1. Copy test_cases.py into the student's directory
#     if not os.path.exists(test_path):
#         import shutil
#         shutil.copy("test_cases.py", local_path)

#     # 2. Run pytest on the student's folder
#     result = subprocess.run(
#         ["pytest", test_path, "--tb=short", "-q"],
#         capture_output=True,
#         text=True,
#         cwd=local_path
#     )

#     output = result.stdout
#     print(output)

#     # 3. Parse test result lines
#     results = {}
#     total_score = 0
#     suite = {
#         "test_add_product": 2.5,
#         "test_total_inventory_value": 2.5,
#         "test_total_inventory_value_with_discount": 2.5
#     }

#     for line in output.splitlines():
#         for test_name in suite:
#             if test_name in line:
#                 passed = "PASSED" in line or "✓" in line
#                 score = suite[test_name] if passed else 0
#                 results[test_name] = score
#                 status = "✅ Passed" if passed else "❌ Failed"
#                 print(f"  - {test_name}: {status} ({score}/{suite[test_name]})")
#                 total_score += score

#     print(f"🏁 Total score for {student_id}: {total_score} / {sum(suite.values())}")
#     return results, total_score

# def evaluate_student_code(student_id, local_path):
#     print(f"🔍 Evaluating code for {student_id}...")
#     student_file = os.path.join(local_path, "student.py")

#     # 1. Load student.py FIRST
#     load_student_module(student_file)

#     # 2. Now import test_cases (which depends on student)
#     from test_cases import test_suite

#     # 3. Run tests manually (no pytest)
#     results = {}
#     for tc_id, (test_func, max_score) in test_suite.items():
#         try:
#             passed = test_func()  # Assume test_func returns True on success
#             results[tc_id] = max_score if passed else 0
#             status = "✅ Passed" if passed else "❌ Failed"
#             print(f"  - {tc_id}: {status} ({results[tc_id]}/{max_score})")
#         except Exception as e:
#             print(f"  - {tc_id}: ❌ Failed (0/{max_score}) - Error: {str(e)}")
#             results[tc_id] = 0

#     total_score = sum(results.values())
#     print(f"🏁 Total score for {student_id}: {total_score} / {sum(m for _, m in test_suite.values())}")
#     return results, total_score

def run_all():
    print("📄 Reading student list from evaluate/students.csv...")
    df = pd.read_csv("evaluate/students.csv")
    results = {}

    for _, row in df.iterrows():
        student_id = row["student_name"].replace(" ", "_")
        ip = row["ip_address"]
        print(f"\n========================================")
        print(f"📥 Pulling code from {student_id} ({ip})")

        student_dir = f"student_repos/{student_id}"
        os.makedirs(student_dir, exist_ok=True)

        scp_command = f"scp -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa ubuntu@{ip}:/home/ubuntu/python-mini-grocery/student.py {student_dir}/"
        print(f"🔄 Running SCP: {scp_command}")
        os.system(scp_command)

        student_file = os.path.join(student_dir, "student.py")
        if not os.path.exists(student_file):
            print(f"❌ student.py missing for {student_id}. Skipping.")
            continue

        res, total = evaluate_student_code(student_id, student_dir)
        results[student_id] = {
            "name": row["student_name"],
            "email": row["email"],
            "test_results": res,
            "total": total
        }

    print("\n📝 Generating final reports...")
    generate_reports(results)
    print("✅ Evaluation complete. Reports generated.")

if __name__ == "__main__":
    print("🚀 Starting student code evaluation...\n")
    run_all()
