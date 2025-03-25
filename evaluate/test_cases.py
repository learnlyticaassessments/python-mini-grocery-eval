import pytest
from student import GroceryManager

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
