# performance_analysis.py
import timeit
from models import Cart, Book

def setup_cart_with_many_items():
    """Creates a cart with a large quantity of one book to test performance."""
    cart = Cart()
    book = Book("Performance Test Book", "Test", 10.00, "")
    # The large quantity will exaggerate the inefficiency of the loop
    cart.add_book(book, 10000)
    return cart

def measure_get_total_price():
    """Function to be measured by timeit."""
    cart = setup_cart_with_many_items()
    cart.get_total_price()

# Run the measurement 100 times and get the total time
execution_time = timeit.timeit(measure_get_total_price, number=100)
print(f"Inefficient version took: {execution_time:.6f} seconds for 100 runs.")