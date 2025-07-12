from app import db
from models import User, Category, Product
import logging

def init_sample_data():
    """Initialize sample data if database is empty"""
    try:
        # Check if we already have data
        if Product.query.count() > 0:
            return
        
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@techkart.com',
                full_name='Admin User',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create categories
        categories_data = [
            {'name': 'Smartphones', 'description': 'Latest smartphones and mobile devices'},
            {'name': 'Laptops', 'description': 'High-performance laptops and notebooks'},
            {'name': 'Tablets', 'description': 'Tablets and e-readers'},
            {'name': 'Accessories', 'description': 'Tech accessories and gadgets'},
            {'name': 'Audio', 'description': 'Headphones, speakers, and audio equipment'},
            {'name': 'Smart Home', 'description': 'Smart home devices and IoT products'}
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(name=cat_data['name'], description=cat_data['description'])
                db.session.add(category)
                db.session.commit()
            categories[cat_data['name']] = category
        
        # Sample products with real stock photo URLs
        products_data = [
            {
                'name': 'Premium Smartphone X1',
                'description': 'Latest flagship smartphone with advanced camera and AI features',
                'price': 899.99,
                'stock_quantity': 50,
                'category': 'Smartphones',
                'image_url': 'https://pixabay.com/get/g86e6014041987793ab0b902e7904a54724054e6ed803ef6c9c406a1e3e027d97493823938f980e506c494410216f4edc7587591915e821742b003ff3625cd4d0_1280.jpg',
                'is_featured': True
            },
            {
                'name': 'Ultra Gaming Laptop Pro',
                'description': 'High-performance gaming laptop with RTX graphics and RGB keyboard',
                'price': 1299.99,
                'stock_quantity': 25,
                'category': 'Laptops',
                'image_url': 'https://pixabay.com/get/gdc89b0b8ba1123f804d96d6fd40656c314843fef3bdeeb40296196c584a8074d93330ea3dec8f4800682f3d70b22856ab91123a516668237296b7f93d0a10386_1280.jpg',
                'is_featured': True
            },
            {
                'name': 'Wireless Earbuds Elite',
                'description': 'Premium wireless earbuds with active noise cancellation',
                'price': 199.99,
                'stock_quantity': 100,
                'category': 'Audio',
                'image_url': 'https://pixabay.com/get/gfa084e555dd702d14f4223a109099cb66eb34d7d1d1a4edad66916f14752d893342936050b401c8ae5191b7a0a5331c30d57c59964e708a94a85773a075fa9ad_1280.jpg',
                'is_featured': True
            },
            {
                'name': 'Smart Watch Series 5',
                'description': 'Advanced smartwatch with health monitoring and GPS',
                'price': 349.99,
                'stock_quantity': 75,
                'category': 'Accessories',
                'image_url': 'https://pixabay.com/get/g68dc1ba3e4012eaee0f044e07e1966438d5f0fcb64b1cfc26c75062be2dc72add6a3f5c45ac4a1b94a7e968dfe8c7ced5eaa862460521c94c3237cc175f244ca_1280.jpg',
                'is_featured': True
            },
            {
                'name': 'Professional Tablet 12"',
                'description': 'Large tablet perfect for creative work and productivity',
                'price': 649.99,
                'stock_quantity': 40,
                'category': 'Tablets',
                'image_url': 'https://pixabay.com/get/gb612744cc0597b353acbfc1fcde1a00013a15d6d9ca31c333759f434dd718fbe680ffee75d2049a8e90f15115f69ca9cf110e1889860cc2f2d0995211e51df05_1280.jpg',
                'is_featured': True
            },
            {
                'name': 'Mechanical Gaming Keyboard',
                'description': 'RGB mechanical keyboard with customizable keys',
                'price': 129.99,
                'stock_quantity': 60,
                'category': 'Accessories',
                'image_url': 'https://pixabay.com/get/g1f6850eb994c13b237dfe640d4f0fdbc118aafcd0c91ff5cff2459c233a229e36772b63af26dc40b288e31682d7d2a5b9c4d7b61177e08b073db69e4c3197c71_1280.jpg',
                'is_featured': True
            },
            {
                'name': 'Ultra-Wide Monitor 34"',
                'description': 'Curved ultra-wide monitor for immersive gaming and work',
                'price': 599.99,
                'stock_quantity': 20,
                'category': 'Accessories',
                'image_url': 'https://pixabay.com/get/ga1bcfac67f44876c3001cc8567af53f603700f5749e8e42029916075296e3be0a5d4f14e83592eee22f83ff1956ceec67dc14a34569cddee1588320711a82eed_1280.jpg',
                'is_featured': True
            },
            {
                'name': 'Smart Home Hub',
                'description': 'Central hub for all your smart home devices',
                'price': 99.99,
                'stock_quantity': 80,
                'category': 'Smart Home',
                'image_url': 'https://pixabay.com/get/gaf88bc977a91f874baf84af1b961095e5fa62a5ab3245dcceba359d52f5ef0a6eb8dd31c7fe1707588db821929b7ed1638ff59d88c7f813b3632dfbefa45fab3_1280.jpg',
                'is_featured': True
            }
        ]
        
        for product_data in products_data:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock_quantity=product_data['stock_quantity'],
                category_id=categories[product_data['category']].id,
                image_url=product_data['image_url'],
                is_featured=product_data['is_featured']
            )
            db.session.add(product)
        
        db.session.commit()
        logging.info("Sample data initialized successfully")
        
    except Exception as e:
        logging.error(f"Error initializing sample data: {e}")
        db.session.rollback()
