import pytest

def run_test_suite(student_module):
    GroceryManager = student_module.GroceryManager

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
        assert total_value == pytest.approx(29.0, 0.01)

    def test_total_inventory_value_with_discount(sample_products):
        gm = GroceryManager()
        total_value = gm.total_inventory_value(sample_products, price_modifier=lambda p: p["price"] * 0.9)
        assert total_value == pytest.approx(26.1, 0.01)

    test_suite = {
        "test_add_product": (test_add_product, 2.5),
        "test_total_inventory_value": (test_total_inventory_value, 2.5),
        "test_total_inventory_value_with_discount": (test_total_inventory_value_with_discount, 2.5),
    }

    results = {}
    for name, (test_fn, weight) in test_suite.items():
        try:
            test_fn()
            print(f"✅ {name} passed ({weight} pts)")
            results[name] = weight
        except AssertionError as e:
            print(f"❌ {name} failed ({weight} pts): {e}")
            results[name] = 0

    total_score = sum(results.values())
    return results, total_score, test_suite
