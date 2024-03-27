from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timedelta
db = SQLAlchemy()

#------------------ db Models ------------------>

# Association table for roles and users
user_roles = db.Table('user_roles',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

# User model
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    contact_number = db.Column(db.Integer, unique=True, nullable=False)
    home_address = db.Column(db.String, nullable=True)
    lastlogin = db.Column(db.DateTime, default=datetime.utcnow())

    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

# Role model
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# Category model
class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String, nullable=False, unique = True)
    linked_products = db.relationship("Product", backref='category', cascade="all, delete-orphan")
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), default=1 )

# Product model
class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    manufacture_date = db.Column(db.DateTime(timezone= True), default=datetime.utcnow(), nullable=False)
    expiry_date = db.Column(db.DateTime(timezone= True), default=lambda: datetime.utcnow() + timedelta(days=100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), default=1 )

# Cart item model
class CartItem(db.Model):
    __tablename__ = "cart_item"
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_total = db.Column(db.Integer, nullable=False, default = 0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    linked_product = db.relationship("Product")


# Cart model
class ShoppingCart(db.Model):
    __tablename__ = "shopping_cart"
    shopping_cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    itemcart_id = db.Column(db.Integer, db.ForeignKey("cart_item.cart_id"), nullable=True)
    cart_items = db.relationship("CartItem", backref="shopping_cart", cascade="all, delete-orphan", single_parent=True)

# Order items model
class OrderItem(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    item_name = db.Column(db.String, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_total = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, default= datetime.utcnow())

    associated_product = db.relationship("Product")

# Admin Request Model
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50))  # 'category_add', 'category_edit', 'category_delete'
    request_time_added  = db.Column(db.DateTime, default= datetime.utcnow())
    request_change_done_by_admin  = db.Column(db.DateTime, default= datetime.utcnow())

    details = db.Column(db.Text)  # JSON or similar structured data
    ###detials will look like this = {
                                        # category_id:int,
                                        # category_name:str,
                                        # linked_products.product_id: <any>,
                                        # prlinked_products.oduct_name: <any>,
                                        # prolinked_products.duct_price: <any>,
                                        # stoclinked_products.k_quantity: <any>,
                                        # manufalinked_products.cture_date: <any>,
                                        # elinked_products.xpiry_date: <any>,
                                        # }
    # They have asked for only categories so ill keep categories modification only
    status = db.Column(db.String(50), default='pending')  # 'pending', 'approved', 'rejected'
