import os
import sys
import pandas as pd
import importlib.util
import subprocess

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

    # 2. Now import test_cases (which depends on student)
    from test_cases import test_suite

    # 3. Run tests manually (no pytest)
    results = {}
    for tc_id, (test_func, max_score) in test_suite.items():
        try:
            passed = test_func()  # Assume test_func returns True on success
            results[tc_id] = max_score if passed else 0
            status = "✅ Passed" if passed else "❌ Failed"
            print(f"  - {tc_id}: {status} ({results[tc_id]}/{max_score})")
        except Exception as e:
            print(f"  - {tc_id}: ❌ Failed (0/{max_score}) - Error: {str(e)}")
            results[tc_id] = 0

    total_score = sum(results.values())
    print(f"🏁 Total score for {student_id}: {total_score} / {sum(m for _, m in test_suite.values())}")
    return results, total_score

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
