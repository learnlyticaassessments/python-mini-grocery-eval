from student import GroceryManager

def test_add_full():
    products = []
    gm = GroceryManager()
    gm.add_product(products, "Apples", 3.0, 5, category="Fruits")
    return products == [{'name': 'Apples', 'price': 3.0, 'quantity': 5, 'category': 'Fruits'}]

def test_default_qty():
    products = []
    gm = GroceryManager()
    gm.add_product(products, "Bread", 2.0, category="Bakery")
    return products == [{'name': 'Bread', 'price': 2.0, 'quantity': 1, 'category': 'Bakery'}]

def test_discount():
    products = []
    gm = GroceryManager()
    gm.add_product(products, "Milk", 2.0, 3, category="Dairy")
    gm.add_product(products, "Eggs", 0.5, 12, category="Dairy")
    return gm.total_inventory_value(products, lambda p: p["price"] * 0.9) == 8.46

def test_tax():
    products = [{"name": "Rice", "price": 1.0, "quantity": 10, "category": "Grains"}]
    gm = GroceryManager()
    return gm.total_inventory_value(products, lambda p: p["price"] * 1.15) == 11.5

test_suite = {
    "TC1": (test_add_full, 2.5),
    "TC2": (test_default_qty, 2.5),
    "TC3": (test_discount, 2.5),
    "HTC1": (test_tax, 2.5)
}
