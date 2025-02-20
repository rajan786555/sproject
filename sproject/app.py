from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail
import os

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Sample menu data
menu = {
    '1': {'name': 'Crispy Burger', 'price': 10.99},
    '2': {'name': 'Aloo Tikki Burger', 'price': 5.99},
    '3': {'name': 'Cheese Burger', 'price': 8.99},
    '4': {'name': 'Double Tikki Burger', 'price': 4.99},
    '5': {'name': 'Veggie Pizza', 'price': 7.99},
    '6': {'name': 'Pasta', 'price': 6.99},
    '7': {'name': 'Fries', 'price': 2.99},
    '8': {'name': 'Soda', 'price': 1.99},
    '9': {'name': 'Ice Cream', 'price': 3.99},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def show_menu():
    return render_template('menu.html', menu=menu)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    if 'cart' not in session:
        session['cart'] = {}
    if item_id in session['cart']:
        session['cart'][item_id]['quantity'] += 1
    else:
        session['cart'][item_id] = {
            'name': menu[item_id]['name'],
            'price': menu[item_id]['price'],
            'quantity': 1
        }
    return redirect(url_for('show_cart'))

@app.route('/cart')
def show_cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty. Please add items to your cart before placing an order.')
        return redirect(url_for('show_menu'))
    
    # Here you would typically process the order (e.g., save to a database)
    session.pop('cart', None)  # Clear the cart after placing the order
    return render_template('order_confirmation.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        flash(f"Welcome {user.name}! Login successful.", "success")
        return redirect(url_for('hotels'))
    
    flash("Invalid email or password.", "error")
    return redirect(url_for('hotels'))


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists. Please login.", "error")
        return redirect(url_for('home'))

    # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    hashed_password = generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("Signup successful! Please login.", "success")
    return redirect(url_for('hotels'))

@app.route('/order')
def order():
    return render_template('order.html')

if __name__ == '__main__':
    app.run(debug=True)