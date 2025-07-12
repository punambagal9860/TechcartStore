from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import User, Product, Category, Order, OrderItem
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import logging

# Decorator for admin required routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

# Decorator for login required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page with featured products"""
    featured_products = Product.query.filter_by(is_featured=True).limit(8).all()
    return render_template('index.html', products=featured_products)

@app.route('/products')
def products():
    """Product listing page with search and filters"""
    # Get search and filter parameters
    search = request.args.get('search', '')
    category_id = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    
    # Build query
    query = Product.query
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if min_price:
        try:
            query = query.filter(Product.price >= float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            query = query.filter(Product.price <= float(max_price))
        except ValueError:
            pass
    
    products = query.all()
    categories = Category.query.all()
    
    return render_template('products.html', products=products, categories=categories,
                         search=search, selected_category=category_id,
                         min_price=min_price, max_price=max_price)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Add product to cart"""
    product = Product.query.get_or_404(product_id)
    
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    # Add or update product in cart
    product_id_str = str(product_id)
    if product_id_str in session['cart']:
        session['cart'][product_id_str]['quantity'] += 1
    else:
        session['cart'][product_id_str] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'image_url': product.image_url
        }
    
    session.modified = True
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
def cart():
    """Shopping cart page"""
    if 'cart' not in session:
        session['cart'] = {}
    
    cart_items = []
    total = 0
    
    for product_id, item in session['cart'].items():
        cart_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': item['price'] * item['quantity'],
            'image_url': item['image_url']
        })
        total += item['price'] * item['quantity']
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:product_id>')
def update_cart(product_id):
    """Update cart item quantity"""
    quantity = request.args.get('quantity', 1, type=int)
    
    if 'cart' in session:
        product_id_str = str(product_id)
        if product_id_str in session['cart']:
            if quantity > 0:
                session['cart'][product_id_str]['quantity'] = quantity
            else:
                del session['cart'][product_id_str]
            session.modified = True
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from cart"""
    if 'cart' in session:
        product_id_str = str(product_id)
        if product_id_str in session['cart']:
            del session['cart'][product_id_str]
            session.modified = True
            flash('Item removed from cart.', 'info')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        # Process checkout
        user = User.query.get(session['user_id'])
        
        # Calculate total
        total = 0
        for item in session['cart'].values():
            total += item['price'] * item['quantity']
        
        # Create order
        order = Order(
            user_id=user.id,
            total_amount=total,
            shipping_address=request.form.get('address'),
            payment_method=request.form.get('payment_method')
        )
        db.session.add(order)
        db.session.commit()
        
        # Create order items
        for product_id, item in session['cart'].items():
            order_item = OrderItem(
                order_id=order.id,
                product_id=int(product_id),
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        # Clear cart
        session.pop('cart', None)
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('index'))
    
    # GET request - show checkout form
    cart_items = []
    total = 0
    
    for product_id, item in session['cart'].items():
        cart_items.append({
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': item['price'] * item['quantity']
        })
        total += item['price'] * item['quantity']
    
    user = User.query.get(session['user_id'])
    return render_template('checkout.html', cart_items=cart_items, total=total, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            flash('Login successful!', 'success')
            
            # Redirect to admin dashboard if admin
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        # Validation
        if not username or not email or not password:
            flash('Please fill in all required fields.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         recent_orders=recent_orders)

@app.route('/admin/products')
@admin_required
def admin_products():
    """Admin product management"""
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock_quantity = int(request.form.get('stock_quantity'))
        category_id = int(request.form.get('category_id'))
        image_url = request.form.get('image_url')
        is_featured = 'is_featured' in request.form
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            category_id=category_id,
            image_url=image_url,
            is_featured=is_featured
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit product"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock_quantity = int(request.form.get('stock_quantity'))
        product.category_id = int(request.form.get('category_id'))
        product.image_url = request.form.get('image_url')
        product.is_featured = 'is_featured' in request.form
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/products/delete/<int:product_id>')
@admin_required
def admin_delete_product(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))

# Context processors for templates
@app.context_processor
def inject_cart_count():
    """Inject cart count into all templates"""
    cart_count = 0
    if 'cart' in session:
        cart_count = sum(item['quantity'] for item in session['cart'].values())
    return {'cart_count': cart_count}

@app.context_processor
def inject_user():
    """Inject current user into all templates"""
    current_user = None
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])
    return {'current_user': current_user}
