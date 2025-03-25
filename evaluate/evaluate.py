import os
import sys
import pandas as pd
import importlib.util
from test_cases import run_test_suite
from report_generator import generate_reports

def load_student_module(student_py_path):
    module_name = "student_submission"
    spec = importlib.util.spec_from_file_location(module_name, student_py_path)
    student_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = student_module
    spec.loader.exec_module(student_module)
    return student_module

def evaluate_student_code(student_id, local_path):
    print(f"\n🔍 Evaluating code for {student_id}...")

    student_file = os.path.join(local_path, "student.py")
    if not os.path.exists(student_file):
        print(f"❌ student.py missing for {student_id}. Skipping.")
        return {}, 0

    try:
        student_module = load_student_module(student_file)
        results, total_score, test_suite = run_test_suite(student_module)

        for name, score in results.items():
            status = "✅ Passed" if score > 0 else "❌ Failed"
            print(f"  - {name}: {status} ({score}/{test_suite[name][1]})")

        print(f"🏁 Total score for {student_id}: {total_score} / {sum(w for _, w in test_suite.values())}")
        return results, total_score
    except Exception as e:
        print(f"💥 Error evaluating {student_id}: {e}")
        return {}, 0

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
