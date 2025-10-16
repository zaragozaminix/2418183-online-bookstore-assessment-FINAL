import bcrypt
import datetime
import random
import time


class Book:
    def __init__(self, title, category, price, image):
        self.title = title
        self.category = category
        self.price = price
        self.image = image


class CartItem:
    def __init__(self, book, quantity=1):
        self.book = book
        self.quantity = quantity

    def get_total_price(self):
        return self.book.price * self.quantity


class Cart:
    """
    A shopping cart class that holds book items and their quantities.
    """

    def __init__(self):
        self.items = {}

    def add_book(self, book, quantity=1):
        if book.title in self.items:
            self.items[book.title].quantity += quantity
        else:
            self.items[book.title] = CartItem(book, quantity)

    def remove_book(self, book_title):
        if book_title in self.items:
            del self.items[book_title]

    def update_quantity(self, book_title, quantity):
        if book_title in self.items:
            if quantity > 0:
                self.items[book_title].quantity = quantity
            else:
                self.remove_book(book_title)

    # FIX for Inefficiency #1: Use 'direct multiplication' instead of a loop
    def get_total_price(self):
        return sum(item.book.price * item.quantity for item in self.items.values())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.values())

    def clear(self):
        self.items = {}

    def get_items(self):
        return list(self.items.values())

    def is_empty(self):
        return len(self.items) == 0

# ## --- START: UPDATED User CLASS --- ##
# This is the new User class with password hashing and email normalisation.

class User:
    """User account management class with password hashing."""

    def __init__(self, email, password, name="", address=""):
        # FIX for Bug #6: Store email as lowercase for case-insensitive checks
        self.email = email.lower()
        # FIX for Security Issue #1: Hash the password, don't store it in plain text
        self.password_hash = self.set_password(password)
        self.name = name
        self.address = address
        self.orders = []

    # New method to hash passwords
    def set_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # New method to check passwords against the hash
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def add_order(self, order):
        self.orders.append(order)
        self.orders.sort(key=lambda x: x.order_date)

    def get_order_history(self):
        return [order for order in self.orders]

# ## --- END: UPDATED User CLASS --- ##

class Order:
    """Order management class"""

    def __init__(self, order_id, user_email, items, shipping_info, payment_info, total_amount):
        self.order_id = order_id
        self.user_email = user_email
        self.items = items.copy()
        self.shipping_info = shipping_info
        self.payment_info = payment_info
        self.total_amount = total_amount
        self.order_date = datetime.datetime.now()
        self.status = "Confirmed"

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_email': self.user_email,
            'items': [{'title': item.book.title, 'quantity': item.quantity, 'price': item.book.price} for item in
                      self.items],
            'shipping_info': self.shipping_info,
            'total_amount': self.total_amount,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }


class PaymentGateway:
    """Mock payment gateway for processing payments"""

    @staticmethod
    def process_payment(payment_info):
        """Mock payment processing - returns success/failure with mock logic"""
        payment_method = payment_info.get('payment_method')
        card_number = payment_info.get('card_number', '')

        if payment_method == 'credit_card' and not card_number:
            return {
                'success': False,
                'message': 'Payment failed: Invalid card number',
                'transaction_id': None
            }

        if card_number.endswith('1111'):
            return {
                'success': False,
                'message': 'Payment failed: Invalid card number',
                'transaction_id': None
            }

        transaction_id = f"TXN{random.randint(100000, 999999)}"

        if payment_method == 'paypal':
            return {
                'success': True,
                'message': 'Payment with PayPal processed successfully',
                'transaction_id': transaction_id
            }

        return {
            'success': True,
            'message': 'Payment processed successfully',
            'transaction_id': transaction_id
        }


class EmailService:
    """Mock email service for sending order confirmations"""

    @staticmethod
    def send_order_confirmation(user_email, order):
        """Mock email sending - just prints to console in this implementation"""
        print(f"\n=== EMAIL SENT ===")
        print(f"To: {user_email}")
        print(f"Subject: Order Confirmation - Order #{order.order_id}")
        print(f"Order Date: {order.order_date}")
        print(f"Total Amount: ${order.total_amount:.2f}")
        print(f"Items:")
        for item in order.items:
            print(f"  - {item.book.title} x{item.quantity} @ ${item.book.price:.2f}")
        print(f"Shipping Address: {order.shipping_info.get('address', 'N/A')}")
        print(f"==================\n")

        return True