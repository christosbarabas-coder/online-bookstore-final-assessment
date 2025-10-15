from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from models import Book, Cart, User, Order, PaymentGateway, EmailService
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# -------------------------
# In-memory storage (demo)
# -------------------------
users = {}   # email -> User
orders = {}  # order_id -> Order

# Demo user
demo_user = User("demo@bookstore.com", "demo123", "Demo User", "123 Demo Street, Demo City, DC 12345")
users["demo@bookstore.com"] = demo_user

# Cart instance
cart = Cart()

# Books
BOOKS = [
    Book("The Great Gatsby", "Fiction", 10.99, "images/books/the_great_gatsby.jpg"),
    Book("1984", "Dystopia", 8.99, "images/books/1984.jpg"),
    Book("I Ching", "Traditional", 18.99, "images/books/I-Ching.jpg"),
    Book("Moby Dick", "Adventure", 12.49, "images/books/moby_dick.jpg"),
]
# -------------------------
# Helpers
# -------------------------
def get_book_by_title(title):
    return next((book for book in BOOKS if book.title == title), None)

def get_current_user():
    if 'user_email' in session:
        return users.get(session['user_email'])
    return None

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---- Coupons registry ----
COUPONS = {
    "SALE10": 0.10,
    "SALE20": 0.20,
}

def compute_cart_totals_from_cart(c):
    """Υπολογισμός subtotal/discount/total από το αντικείμενο Cart."""
    items = c.get_items() if hasattr(c, "get_items") else []
    # Προσπάθησε να χρησιμοποιήσεις item.get_total_price(), αλλιώς υπολόγισε μόνος σου
    try:
        subtotal = sum(float(it.get_total_price()) for it in items)
    except Exception:
        subtotal = sum(float(it.book.price) * int(it.quantity) for it in items)
    rate = float(session.get("coupon_value") or 0.0)
    discount = round(subtotal * rate, 2)
    total = round(subtotal - discount, 2)
    return subtotal, discount, total

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    current_user = get_current_user()
    return render_template('index.html', books=BOOKS, cart=cart, current_user=current_user)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    book_title = request.form.get('title')
    quantity = int(request.form.get('quantity', 1))

    book = get_book_by_title(book_title)
    if book:
        cart.add_book(book, quantity)
        flash(f'Added {quantity} "{book.title}" to cart!', 'success')
    else:
        flash('Book not found!', 'error')

    return redirect(url_for('index'))

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    book_title = request.form.get('title')
    cart.remove_book(book_title)
    flash(f'Removed "{book_title}" from cart!', 'success')
    return redirect(url_for('view_cart'))

@app.route('/update-cart', methods=['POST'])
def update_cart():
    book_title = request.form.get('title')
    quantity = int(request.form.get('quantity', 1))
    cart.update_quantity(book_title, quantity)

    if quantity <= 0:
        flash(f'Removed "{book_title}" from cart!', 'success')
    else:
        flash(f'Updated "{book_title}" quantity to {quantity}!', 'success')

    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    current_user = get_current_user()
    subtotal, discount, total = compute_cart_totals_from_cart(cart)
    return render_template(
        'cart.html',
        cart=cart,
        subtotal=subtotal,
        discount=discount,
        total=total,
        coupon_code=session.get("coupon_code"),
        current_user=current_user
    )

@app.post("/apply-coupon")
def apply_coupon():
    code = (request.form.get("code") or "").strip().upper()
    if not code:
        flash("Please enter a coupon code.", "warning")
        return redirect(url_for("view_cart"))

    if code in COUPONS:
        session["coupon_code"] = code
        session["coupon_value"] = COUPONS[code]
        flash(f"Coupon {code} applied!", "success")
    else:
        session.pop("coupon_code", None)
        session.pop("coupon_value", None)
        flash("Invalid coupon code.", "error")

    return redirect(url_for("view_cart"))

@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    cart.clear()
    flash('Cart cleared!', 'success')
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    if cart.is_empty():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))

    current_user = get_current_user()
    total_price = cart.get_total_price()
    return render_template('checkout.html', cart=cart, total_price=total_price, current_user=current_user)

@app.route('/process-checkout', methods=['POST'])
def process_checkout():
    if cart.is_empty():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))

    # Shipping
    shipping_info = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'address': request.form.get('address'),
        'city': request.form.get('city'),
        'zip_code': request.form.get('zip_code')
    }

    # Payment
    payment_info = {
        'payment_method': request.form.get('payment_method'),
        'card_number': request.form.get('card_number'),
        'expiry_date': request.form.get('expiry_date'),
        'cvv': request.form.get('cvv')
    }

    discount_code = request.form.get('discount_code', '')

    # Base total
    total_amount = cart.get_total_price()
    discount_applied = 0.0

    if discount_code == 'SAVE10':
        discount_applied = total_amount * 0.10
        total_amount -= discount_applied
        flash(f'Discount applied! You saved ${discount_applied:.2f}', 'success')
    elif discount_code == 'WELCOME20':
        discount_applied = total_amount * 0.20
        total_amount -= discount_applied
        flash(f'Welcome discount applied! You saved ${discount_applied:.2f}', 'success')
    elif discount_code:
        flash('Invalid discount code', 'error')

    # Validate shipping
    required_fields = ['name', 'email', 'address', 'city', 'zip_code']
    for field in required_fields:
        if not shipping_info.get(field):
            flash(f'Please fill in the {field.replace("_", " ")} field', 'error')
            return redirect(url_for('checkout'))

    # Validate payment
    if payment_info['payment_method'] == 'credit_card':
        if not payment_info.get('card_number') or not payment_info.get('expiry_date') or not payment_info.get('cvv'):
            flash('Please fill in all credit card details', 'error')
            return redirect(url_for('checkout'))

    # Mock payment
    payment_result = PaymentGateway.process_payment(payment_info)
    if not payment_result['success']:
        flash(payment_result['message'], 'error')
        return redirect(url_for('checkout'))

    # Create order
    order_id = str(uuid.uuid4())[:8].upper()
    order = Order(
        order_id=order_id,
        user_email=shipping_info['email'],
        items=cart.get_items(),
        shipping_info=shipping_info,
        payment_info={
            'method': payment_info['payment_method'],
            'transaction_id': payment_result['transaction_id']
        },
        total_amount=total_amount
    )
    orders[order_id] = order

    # Attach to user
    current_user = get_current_user()
    if current_user:
        current_user.add_order(order)

    # Email (mock)
    EmailService.send_order_confirmation(shipping_info['email'], order)

    # Clear cart and store last order id
    cart.clear()
    session['last_order_id'] = order_id

    flash('Payment successful! Your order has been confirmed.', 'success')
    return redirect(url_for('order_confirmation', order_id=order_id))

@app.route('/order-confirmation/<order_id>')
def order_confirmation(order_id):
    order = orders.get(order_id)
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('index'))

    current_user = get_current_user()
    return render_template('order_confirmation.html', order=order, current_user=current_user)

# -------------------------
# Account
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        address = request.form.get('address', '')

        if not email or not password or not name:
            flash('Please fill in all required fields', 'error')
            return render_template('register.html')

        if email in users:
            flash('An account with this email already exists', 'error')
            return render_template('register.html')

        user = User(email, password, name, address)
        users[email] = user
        session['user_email'] = email
        flash('Account created successfully! You are now logged in.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = users.get(email)
        if user and user.password == password:
            session['user_email'] = email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
    current_user = get_current_user()
    return render_template('account.html', current_user=current_user)

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    current_user = get_current_user()
    current_user.name = request.form.get('name', current_user.name)
    current_user.address = request.form.get('address', current_user.address)

    new_password = request.form.get('new_password')
    if new_password:
        current_user.password = new_password
        flash('Password updated successfully!', 'success')
    else:
        flash('Profile updated successfully!', 'success')

    return redirect(url_for('account'))

# -------------------------
# Main
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
