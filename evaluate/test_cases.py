

import pytest
import os
import sys
import importlib


# # Add the student's directory to Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from student_repos.Anil.student import GroceryManager

# #from student import GroceryManager

# Dynamically import the student module
def import_student_module():
    # The current directory of test_cases.py
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Parent directory (where student_repos is located)
    parent_dir = os.path.dirname(test_dir)
    
    # Attempt to find the student module dynamically
    current_student_dir = os.path.join(parent_dir, os.environ.get('CURRENT_STUDENT_DIR', ''))
    
    if not os.path.exists(current_student_dir):
        raise ValueError(f"Student directory not found: {current_student_dir}")
    
    # Add the parent directory to Python path to ensure imports work
    sys.path.insert(0, parent_dir)
    
    # Dynamically import the student module
    student_module_path = os.path.join(current_student_dir, "student.py")
    spec = importlib.util.spec_from_file_location("student", student_module_path)
    student_module = importlib.util.module_from_spec(spec)
    sys.modules["student"] = student_module
    spec.loader.exec_module(student_module)
    
    return student_module

# Import the student module dynamically
StudentModule = import_student_module()
GroceryManager = StudentModule.GroceryManager


@pytest.fixture
def sample_products():
    return [
        {"name": "Apples", "price": 3.0, "quantity": 5, "category": "Fruits"},
        {"name": "Bread", "price": 2.0, "quantity": 1, "category": "Bakery"},
        {"name": "Milk", "price": 2.0, "quantity": 3, "category": "Dairy"},
        {"name": "Eggs", "price": 0.5, "quantity": 12, "category": "Dairy"}
    ]

def test_add_product(sample_products):
    gm = GroceryManager()
    new_product = {"name": "Rice", "price": 1.0, "quantity": 10, "category": "Grains"}
    gm.add_product(sample_products, **new_product)
    assert len(sample_products) == 5
    assert sample_products[-1] == new_product

def test_total_inventory_value(sample_products):
    gm = GroceryManager()
    total_value = gm.total_inventory_value(sample_products)
    assert total_value == pytest.approx(29.0, 0.01)  # Corrected expected value

def test_total_inventory_value_with_discount(sample_products):
    gm = GroceryManager()
    total_value = gm.total_inventory_value(sample_products, price_modifier=lambda p: p["price"] * 0.9)
    assert total_value == pytest.approx(26.1, 0.01)  # Corrected expected value


# Test suite with test case functions and weights
test_suite = {
    "test_add_product": (test_add_product, 2.5),
    "test_total_inventory_value": (test_total_inventory_value, 2.5),
    "test_total_inventory_value_with_discount": (test_total_inventory_value_with_discount, 2.5),
}

def run_tests():
    import subprocess
    import sys

    # Run pytest programmatically and capture the output
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--tb=short", "-q"],
        capture_output=True,
        text=True
    )

    # Print the results of the test suite
    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    run_tests()
