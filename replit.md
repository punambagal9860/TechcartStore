# TechKart E-commerce Platform

## Overview

TechKart is a Flask-based e-commerce platform for selling tech products and electronics. The application provides a complete online shopping experience with product browsing, shopping cart functionality, user authentication, and administrative features for managing products and orders.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (default) or PostgreSQL support
- **Authentication**: Session-based authentication with password hashing
- **Architecture Pattern**: MVC (Model-View-Controller) pattern

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating)
- **CSS Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Font Awesome 6.4.0 for UI icons
- **JavaScript**: Vanilla JavaScript for client-side interactions

### Database Schema
- **User Model**: User accounts with roles (admin/regular users)
- **Product Model**: Product catalog with categories, pricing, and inventory
- **Category Model**: Product categorization system
- **Order/OrderItem Models**: Order management system (referenced but not fully implemented)

## Key Components

### Models (models.py)
- **User**: Handles user authentication, profiles, and admin privileges
- **Product**: Manages product information, pricing, and inventory
- **Category**: Organizes products into categories
- **Order/OrderItem**: Shopping cart and order management (partial implementation)

### Routes (routes.py)
- **Public Routes**: Home page, product listings, product details
- **Authentication Routes**: Login, registration, logout
- **Shopping Cart**: Add/remove items, checkout process
- **Admin Routes**: Product management, dashboard, CRUD operations

### Templates
- **Base Template**: Common layout with navigation and styling
- **Public Pages**: Home, products, product details, cart, checkout
- **Authentication Pages**: Login and registration forms
- **Admin Pages**: Dashboard, product management, add/edit products

### Static Assets
- **CSS**: Custom styling complementing Bootstrap
- **JavaScript**: Client-side functionality for cart operations and UI enhancements

## Data Flow

1. **User Registration/Login**: Users create accounts or authenticate via session-based login
2. **Product Browse**: Users browse products with search and category filtering
3. **Shopping Cart**: Session-based cart management before user authentication
4. **Checkout Process**: Authenticated users complete purchases with shipping information
5. **Admin Management**: Admin users manage products, categories, and view orders

## External Dependencies

### Frontend Libraries
- **Bootstrap 5.3.0**: Responsive CSS framework
- **Font Awesome 6.4.0**: Icon library
- **CDN Delivery**: External CSS/JS assets loaded via CDN

### Backend Dependencies
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Werkzeug**: Password hashing and security utilities
- **Flask-Login**: User session management (referenced but not fully implemented)

### Development Dependencies
- **SQLite**: Default database for development
- **PostgreSQL**: Production database option via DATABASE_URL environment variable

## Deployment Strategy

### Environment Configuration
- **Development**: SQLite database, debug mode enabled
- **Production**: PostgreSQL database via DATABASE_URL environment variable
- **Session Management**: Configurable session secret via SESSION_SECRET environment variable

### Application Structure
- **Entry Point**: main.py imports and runs the Flask application
- **Application Factory**: app.py initializes Flask app, database, and routes
- **Database Initialization**: Automatic table creation and sample data population
- **Static File Serving**: Flask serves CSS, JS, and other static assets

### Security Considerations
- **Password Hashing**: Werkzeug's secure password hashing
- **Session Security**: Configurable session secret keys
- **Input Validation**: Form validation and CSRF protection
- **Admin Access Control**: Role-based access control for administrative functions

### Notable Implementation Details
- **Sample Data**: Automatic initialization of sample products and admin user
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Search and Filtering**: Product search with category and price filtering
- **Image Handling**: External image URLs for product photos
- **Cart Persistence**: Session-based cart management
- **Admin Interface**: Comprehensive product management system

The application follows Flask best practices with clear separation of concerns, secure authentication, and a user-friendly interface suitable for both customers and administrators.