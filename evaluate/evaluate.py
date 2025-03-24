import importlib.util
import os
import pandas as pd
from test_cases import test_suite
from report_generator import generate_reports

def evaluate_student_code(student_id, local_path):
    spec = importlib.util.spec_from_file_location("student", os.path.join(local_path, "student.py"))
    student = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student)

    results = {}
    for tc_id, (test_fn, marks) in test_suite.items():
        try:
            passed = test_fn()
            results[tc_id] = marks if passed else 0
        except Exception:
            results[tc_id] = 0
    return results, sum(results.values())

def run_all():
    df = pd.read_csv("evaluator/students.csv")
    results = {}

    for _, row in df.iterrows():
        student_id = row["student_name"].replace(" ", "_")
        ip = row["ip_address"]

        print(f"📥 Pulling code from {student_id} at {ip}")
        os.makedirs(f"student_repos/{student_id}", exist_ok=True)
        scp_command = f"scp -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa ubuntu@{ip}:/home/ubuntu/python-mini-grocery/student.py student_repos/{student_id}/"
        os.system(scp_command)

        if not os.path.exists(f"student_repos/{student_id}/student.py"):
            print(f"❌ student.py missing for {student_id}")
            continue

        res, total = evaluate_student_code(student_id, f"student_repos/{student_id}")
        results[student_id] = {
            "name": row["student_name"],
            "email": row["email"],
            "test_results": res,
            "total": total
        }

    generate_reports(results)

if __name__ == "__main__":
    run_all()
