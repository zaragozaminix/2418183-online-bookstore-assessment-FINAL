# Test Plan: Online Bookstore Application

This document outlines the testing strategy for the Online Bookstore application, aligning with the project requirements. The plan covers functional, performance, and security testing to ensure comprehensive quality assurance.

---

## 1. Functional Testing (Unit & Integration)

This section covers the core features of the application as described in the project documentation.

### FR-002: Shopping Cart Functionality
- **TC-CART-01 (Positive)**: Verify a book can be added to the cart and the total price is calculated correctly.
- **TC-CART-02 (Positive)**: Verify updating a book's quantity correctly adjusts the cart total.
- **TC-CART-03 (Boundary)**: Verify updating a book's quantity to **0** removes the item from the cart.
- **TC-CART-04 (Negative)**: Verify updating a book's quantity to a **negative number** removes the item.
- **TC-CART-05 (Negative)**: Verify the application handles a **non-numeric quantity** input gracefully without crashing when adding to the cart.

### FR-003 & FR-004: Checkout and Payment
- **TC-CHECKOUT-01 (Positive)**: Verify a valid discount code (`SAVE10`) is applied correctly.
- **TC-CHECKOUT-02 (Boundary)**: Verify a discount code works irrespective of its case (e.g., `save10`).
- **TC-CHECKOUT-03 (Positive)**: Verify a successful checkout with a valid credit card.
- **TC-CHECKOUT-04 (Negative)**: Verify a failed checkout with a card number known to fail (ending in `1111`).
- **TC-CHECKOUT-05 (Negative)**: Verify how the system handles the **PayPal** payment method during checkout.

### FR-006: User Account Management
- **TC-USER-01 (Positive)**: Verify successful user registration with a unique, valid email.
- **TC-USER-02 (Negative)**: Verify the system rejects registration with an **invalid email format**.
- **TC-USER-03 (Boundary)**: Verify the system prevents creating duplicate accounts using the **same email with different casing** (e.g., `user@example.com` vs. `User@example.com`).
- **TC-USER-04 (Security)**: Verify user passwords are **not stored in plain text** after the security fix is implemented.

---

## 2. Performance Testing

This section focuses on identifying and measuring code inefficiencies.

- **PT-01**: Profile the `Cart.get_total_price()` method to measure its performance, especially with a large item quantity, to identify the impact of its nested loop algorithm.
- **PT-02**: Profile the `User.add_order()` method to analyze the efficiency of sorting the order list on every addition.
- **PT-03**: Measure the response time of the `/add-to-cart` route to identify the performance impact of its linear book search.

---

## 3. Security Testing

This section focuses on identifying key security vulnerabilities.

- **ST-01 (Authentication)**: Verify that user passwords are securely hashed during registration and that the hash is verified during login.
- **ST-02 (Input Sanitization)**: Test key input fields (e.g., registration name, checkout address) for Cross-Site Scripting (XSS) vulnerabilities by attempting to inject simple HTML or script tags.