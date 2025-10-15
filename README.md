# Online Bookstore Flask Application

## Academic Project – Software Testing Learning

**ACADEMIC USE ONLY — FOR EDUCATIONAL PURPOSES**

## Overview
The Online Bookstore is a small Flask e-commerce demo used to practice software testing. It includes cart, checkout, mock payment, user accounts, and order confirmation flows.

## Note for Testers
This application intentionally contains bugs and edge cases to create realistic testing scenarios. Your tasks:
- Find defects (functional, performance, security, UX, edge cases)
- Write clear bug reports
- Propose fixes and improvements
- Consider performance and security implications

## Features

### Book Catalog (FR-001)
- Featured books with title, category, price, cover image
- Simple catalog browsing

### Shopping Cart (FR-002)
- Add to cart with quantity
- View, update quantities, remove items, clear cart
- Dynamic totals calculation

### Checkout (FR-003)
- Order summary
- Shipping form (name, email, address, city, zip)
- Payment method: Credit Card or PayPal (mock)
- Discount codes: `SAVE10`, `WELCOME20`
- Basic validation and messages

### Mock Payment (FR-004)
- Simulated gateway result
- Transaction IDs on success
- Failure scenario (e.g., card ending in `1111`)

### Order Confirmation (FR-005)
- Mock email service (console output)
- Confirmation page with order details and ID

### User Accounts (FR-006)
- Register / Login / Logout
- Profile update (name, address, password)
- In-memory order history (demo)
- Session-based authentication

### Responsive UI (FR-007)
- Mobile/tablet/desktop friendly HTML/CSS

---

## Technology
- Backend: Python 3.11+, Flask, Jinja2, Flask sessions
- Frontend: HTML5, CSS3
- Storage: In-memory (demo only)
- Mocks: Payment gateway and Email service

## Project Structure
online-bookstore-final-assessment/
│
├── app.py
├── models.py
├── requirements.txt
├── pytest.ini
├── README.md
│
├── static/
│ ├── styles.css
│ ├── logo.png
│ └── images/
│ └── books/
│ ├── the_great_gatsby.jpg
│ ├── 1984.jpg
│ ├── I-Ching.jpg
│ └── moby_dick.jpg
│
└── templates/
├── index.html
├── cart.html
├── checkout.html
├── order_confirmation.html
├── login.html
├── register.html
└── account.html

---

## What to Test
- Authentication:  
  Demo account → email `demo@bookstore.com`, password `demo123`.  
  Register / Login / Logout / Update profile.

- Checkout and Payments:  
  Any card passes except those ending in `1111` (simulated failure).

- Discounts:  
  `SAVE10` → 10% off  
  `WELCOME20` → 20% off  
  Invalid codes → proper error message.

- Validation:  
  Required fields, email format, payment inputs.

- Responsive UI:  
  Test on mobile, tablet, and desktop widths.

---

## Setup and Run (Windows / Git Bash)
```bash
cd /c/Users/USER/projects/online-bookstore-final-assessment
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python -m pytest -q     # expect 9 passed
python app.py           # then open http://127.0.0.1:5000
::contentReference[oaicite:0]{index=0}
