from flask_security import auth_required, roles_required ,current_user, login_user, logout_user, login_required
from flask_restful import Resource, marshal_with, fields, reqparse, abort
import json
from main import cache
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import *
from flask import current_app as app




# _________________User(LOGIN, LOGOUT)_________________
class Login(Resource):
    user_login_parser = reqparse.RequestParser()
    user_login_parser.add_argument("email_address", type=str, required=True)
    user_login_parser.add_argument("password", type=str, required=True)
    
    def post(self):
        data = self.user_login_parser.parse_args()
        user = User.query.filter_by(email_address = data["email_address"].lower()).first()

        if user:
            if not user.active :
                return {"message" : "You have been deactivated by the admin, please contact him for re-activation"}, 403

            if check_password_hash(user.password, data['password']):
                auth = user.get_auth_token()
                login_user(user)
                return {
                    "message": "Logged in successfully ",
                    "auth_token": auth, 
                    "username": user.username,
                    "role":user.roles[-1].name,
                    "user_id" : user.id
                    }, 200
            return {"message": "Wrong password! "}, 401
            
            
        return {"message": "Email is not registered. Please register first."}, 401

class Logout(Resource):
    def post(self):
        try:
            try:
                user = User.query.get(current_user.id)
                if user:
                    user.lastlogin = datetime.utcnow()
                    db.session.commit()
            finally:
                logout_user()
            return {"message": "Logged out successfully."}, 200
        except:
            return {"message": "Logged out successfully."}, 200


# _________________SHOW USERS ORDER HISTORY DATA_________________
class OrderHistory(Resource):

    order_table_marshal={
        "id": fields.Integer,
        "user_id": fields.Integer,
        "product_id": fields.Integer,
        "item_name": fields.String,
        "item_quantity": fields.Integer,
        "item_total": fields.Integer,
        "purchase_date": fields.DateTime(dt_format='rfc822'),
    }
    @marshal_with(order_table_marshal)
    def get(self, user_id):
        orders = OrderItem.query.filter_by(user_id= user_id).all()
        if orders:
            return orders, 200
        return {"message" : "Plesae order Something first"}, 404

# _________________SENDING USER EMAIL DATA_________________
class SendingConfidentialData(Resource):
    @auth_required('token')
    @login_required
    def get(self):
        user_info = {
            "username": current_user.username,
            "email_address": current_user.email_address,
            "user_id" : current_user.id,
        }
        return jsonify(user_info)
    
# _________________ACTIVATE/ DEACVTIVATE ANY USER_________________
class ToggleUser(Resource):
    @auth_required('token')
    @cache.cached(timeout=20)
    def post(self):
        args =reqparse.RequestParser()
        args.add_argument("email_address", type= str, required = True)
        data = args.parse_args()

        email_address = data["email_address"]
        user = User.query.filter_by(email_address = email_address).first()
        if user:
            with app.app_context():
                datastore = app.security.datastore
            datastore.toggle_active(user)
            try:
                db.session.commit()
                return{"message" : "Done successfully!"} ,200
            except:
                db.session.rollback()
                return {'message' : 'Error!'}, 500
        return {'message' : 'User not found!'}, 404

# _________________User(REGISTER, CHANGE PASSWORD, SIGNUP,PROFILE)_________________
class UserResource(Resource):
    user_res_parser = reqparse.RequestParser()
    user_res_parser.add_argument(
        "username", help="Please enter username", required=True)
    user_res_parser.add_argument(
        "email_address", help="Please enter email_address", required=True)
    user_res_parser.add_argument(
        "password", help="Please enter password", required=True)
    user_res_parser.add_argument(
        "contact_number", help="Please enter contact_number", required=True)
    user_res_parser.add_argument(
        "home_address", help="Please enter home_address", required=True)


    allusers = {
        "username": fields.String,
        "email_address": fields.String,
        "active": fields.Boolean,
         'roles' : fields.List(fields.Nested({
             "name" : fields.String
         }
         )) }

    @marshal_with(allusers)
    def get(self):
        all_users = User.query.all()
        if all_users != []:
            return all_users, 200
        return {"message": "No user found."}, 404


    #register
    def post(self):
        args = self.user_res_parser.parse_args()
        username = args.get("username").title()
        email_address = args.get("email_address").lower()
        password = args.get("password")
        contact_number = args.get("contact_number")
        home_address = args.get("home_address")

        ifuser = User.query.filter_by(email_address=email_address).first()
        if ifuser:
            return {"message": "email already exists!"},  401
        if User.query.get(contact_number):
            return {"message": "Phone Number already exists!"},  401

        try:
            with app.app_context():
                datastore = app.security.datastore
                datastore.create_user(username=username.title(), email_address=email_address.lower(), password=generate_password_hash(password),contact_number=contact_number, home_address=home_address, roles=["user"])
                db.session.commit()
            return {"message": "User added Successfully!"}, 200
        except Exception as e:
            print(e)
            return {"message": "Couldn't add User. Try again later!"}, 400

    # get the username and the oldpassword and then change then new password
    @auth_required("token")
    def put(self):
        change_pswd_parser = reqparse.RequestParser()
        change_pswd_parser.add_argument("username", required=False)
        change_pswd_parser.add_argument(
            "email_address", help="Please enter the username", required=True)
        change_pswd_parser.add_argument(
            "old_password", help="Please enter the old_password", required=True)
        change_pswd_parser.add_argument(
            "new_password", help="Please enter the new_password", required=True)

        args = change_pswd_parser.parse_args()
        email_address = args["email_address"].lower()
        old_password = args["old_password"]
        new_password = args["new_password"]

        user = User.query.filter_by(email_address=email_address).first()

        if not user:
            return {'message': 'No user with the credentials. Please make an account first.'}, 404
        
        # check_password_hash, generate_password_hash

        if not check_password_hash(user.password, old_password):
            return {'message': 'Wrong password.'}, 404

        if check_password_hash(user.password, new_password):
            return {'message': 'New password is the same as the old passsword'}, 401

        user.password = generate_password_hash(new_password) # Replace with hashed password if necessary
        db.session.commit()
        return {"message": "Password updated successfully"}, 200
    
    @auth_required("token")
    def delete(self):
        user_delete_parser = reqparse.RequestParser()
        user_delete_parser.add_argument(
            "username", help="Please enter username", required=True)
        user_delete_parser.add_argument(
            "email_address", help="Please enter email_address", required=True)
        user_delete_parser.add_argument(
            "password", help="Please enter password", required=True)

        args = user_delete_parser.parse_args()
        username = args["username"].title()
        email_address = args["email_address"].lower()
        password = args["password"]

        user = User.query.filter_by(email_address=email_address).first()
        if not user:
            return {'message': 'User not found'}, 404

        if not check_password_hash(user.password, password):
            return {'message': 'Wrong password.'}, 404

        try:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Could not delete user. Please try again later.'}, 500

# _________________User(LOGIN, SIGNUP,PROFILE)_________________
class BecomeStoreManager(Resource):

    @auth_required("token")
    def post(self):
        user_id = current_user.id
        user = User.query.get(user_id)
        if user and not "manager" in user.roles:
            become_manager_req = Request(user_id = user.id, type="storeManager_add")
            try:
                db.session.add(become_manager_req)
                db.session.commit()
                return {'message':'Request to become a Store-Manager has been sent to Authorities'}, 200
            except:
                pass    
        return {'message': 'No user found!'}, 400             

# _________________LOAD DUMMY DATA_________________
class LoadData(Resource):
    def add_dummy_user():
        c1 = Category(category_name="Fruits")
        c2 = Category(category_name="Beverages")
        p1 = Product(product_name="Apple", product_price=123,
                     stock_quantity=100, category_id=1, imageUrl = "/static/Apple.png")
        p2 = Product(product_name="Mango", product_price=100,
                     stock_quantity=400, category_id= 1, imageUrl = "/static/Mango.png")
        p3 = Product(product_name="Water", product_price=100, imageUrl = "/static/Water.png",
                     stock_quantity=400, category_id=2)
        p4 = Product(product_name="Tea", product_price=100, imageUrl = "/static/Tea.png",
                     stock_quantity=400, category_id=2)
        cart1 = CartItem(item_name = "Apple",item_quantity = 12,item_total = 2460,user_id = 1,product_id = 1)
        cart2 = CartItem(item_name = "Apple",item_quantity = 12,item_total = 2460,user_id = 2,product_id = 1)
        cart3 = CartItem(item_name = "Apple",item_quantity = 12,item_total = 2460,user_id = 3,product_id = 1)
        scart1 = ShoppingCart(user_id= 1, itemcart_id= 1)
        scart2 = ShoppingCart(user_id= 2, itemcart_id= 2)
        scart3 = ShoppingCart(user_id= 3, itemcart_id= 3)
        
        
        try:
            db.session.add_all([c1, c2, p1, p2, p3, p4])
            db.session.add_all([cart1,cart2,cart3])
            db.session.add_all([scart1,scart2,scart3])
            db.session.commit()
            return True
        except :
            return False
        
    def get(self):
        if LoadData.add_dummy_user():
            return {'message': 'Dummy data added successfully'}, 200
        return {"message":  "Failed to add data"}, 400

# _________________CATEGORIES(SEARCH BY NAME / CATEGORY)_________________
class SearchFunctionality(Resource):
    category_marshal = {
        "category_id": fields.Integer,
        "category_name": fields.String,
        'linked_products': fields.List(fields.Nested({
            "product_id": fields.Integer,
            "product_name": fields.String,
            "product_price": fields.Integer,
            "imageUrl": fields.String,
            "stock_quantity": fields.Integer,
            "manufacture_date": fields.DateTime(dt_format='rfc822'),
            "expiry_date": fields.DateTime(dt_format='rfc822')
        }))
    }
    # TODO:in home page add the show my price and show my manufacture date, in addain to showing them by the categories 
    @marshal_with(category_marshal)
    # @cache.cached(timeout=20)
    def get(self, search_string=None):
        search_type = request.args.get("searchneighbourbutton")

        if search_string:
            if search_type == "Category":
                cat = Category.query.filter(
                    Category.category_name.ilike(f"%{search_string}%")).all()
                if cat:
                    return cat
                else:
                    return abort(404, description='No Categories found, Try looking in Products')
            elif search_type == "Price":
                try:
                    search_price = int(search_string)
                except ValueError:
                    return abort(400, description='Invalid price value')

                # Query products based on the provided price
                prod = Product.query.filter(Product.product_price == search_price).all()
                if prod:
                    categories_with_products = []
                    for product in prod:
                        categories_with_products.append({
                            "category_id": product.category.category_id,
                            "category_name": product.category.category_name,
                            "linked_products": [product]
                        })
                    return categories_with_products
                else:
                    return abort(404, description='No Results found for the provided search price')
            else:
                prod = Product.query.filter(
                    Product.product_name.ilike(f"%{search_string}%")).all()
                if prod:
                    categories_with_products = []
                    for product in prod:
                        categories_with_products.append({
                            "category_id": product.category.category_id,
                            "category_name": product.category.category_name,
                            "linked_products": [product]
                        })
                    return categories_with_products
                else:
                    return abort(404, description='No Results found for the provided search string')
        
        return Category.query.all()

# _________________PRODUCTS(MADE BY THAT PARTICULAR USER BY ID)_________________
class UserProducts(Resource):

    product_fields = {
        'product_id': fields.Integer,
        'product_name': fields.String,
        'product_price': fields.Float,
        'stock_quantity': fields.Integer,
        'category_id': fields.Integer,
        'imageUrl': fields.String,
        'creator_id': fields.Integer,
        "manufacture_date":fields.DateTime(dt_format='rfc822'),
        "expiry_date":fields.DateTime(dt_format='rfc822'),
    }

    @marshal_with(product_fields)
    def get(self, creator_id):
        products = Product.query.filter_by(creator_id=creator_id).all()
        if not products:
            return {'message': 'No products found for the given user.'}, 404
        return products, 200

# _________________CATEGORIES(MADE BY THAT PARTICULAR USER BY ID)_________________
class UserCategories(Resource):
    
    category_fields = {
    'category_id': fields.Integer,
    'category_name': fields.String,
    'creator_id': fields.Integer
}

    @marshal_with(category_fields)
    def get(self, creator_id):
        categories = Category.query.filter_by(creator_id=creator_id).all()
        if not categories:
            return {'message': 'No categories found for the given user.'}, 404
        return categories, 200

# _________________CATEGORIES(SEARCH, ADD, UPDATE, PUT, DELETE PRODUCTS) _________________
class CategoriesResource(Resource):
    # ONLY ADMIN , manager CAN CHANGE THE CATEGORIES HERE......SO ADD THAT LOGIN , ROLE REQUIRED HERE
    # @auth_required("token")
    # @roles_required("Admin", "manager")
    def post(self):
        category_parser = reqparse.RequestParser()
        category_parser.add_argument(
            "category_name", required=True, help="Category name cannot be blank")
        args = category_parser.parse_args()

        input_category = args["category_name"].title()
        x = Category.query.filter_by(category_name=input_category).first()
        if x:
            return {"message": "Category is already present!"}, 400

        # if all is okay then send the cateogory to the admin for addition ?
        # ##c = Category(category_name=input_category)
        # ##db.session.add(c)
        # ##db.session.commit()

        # till then reply that cateogry has been sent for addition , chillout store manager
        new_request_for_category = Request(user_id = current_user.id, type="category_add", details = json.dumps({"category_name": input_category.title()}))
        db.session.add(new_request_for_category)
        db.session.commit()
        
        return {"message": "Request to admin sent Successfully!"}, 200

    # the databse wont consider the names as same if there is any change in the letter_CASE of the name , this allows the users to enter {Sea Food}and{Sea food} as well
    # inorder to solve this error, when we will provide the responses we can submit them in Title case only ! ####
    # ONLY ADMIN CAN CHANGE THE CATEGORIES HERE......SO ADD THAT LOGIN , ROLE REQUIRED HERE
    # get the categ_id and see if the n
    def put(self, category_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type=str,
                            required=True, help="Name cannot be blank!")
        parser.add_argument('old_category_name', type=str,
                            required=True, help="Old Category Name cannot be blank!")
        parser.add_argument('category_id', type=int,
                            required=False, help="ID cannot be blank!")
        data = parser.parse_args()

      
        manual_cat_id = data["category_id"]
        manual_cat = Category.query.filter_by(
            category_id=manual_cat_id).first()
        if not manual_cat:
            return {"message": "No category found ! with the id"}, 404
        # checking if there is any other category with the same name
        dulplicate_cat_check = Category.query.filter_by(
            category_name=data["category_name"].title()).first()
        if dulplicate_cat_check:
            return {"message": "There is already a category with the same name"}, 400
        
        cat_update_req = Request(user_id = current_user.id, type='category_update',details = json.dumps({"category_name":data['category_name'].title(),"old_category_name":data['old_category_name'].title(), "category_id": manual_cat_id}))
    
        db.session.add(cat_update_req)
        db.session.commit()
        return {"message": "Category updatation request sent to admin successfully"}, 200

    # ONLY ADMIN CAN CHANGE THE CATEGORIES HERE......SO ADD THAT LOGIN , ROLE REQUIRED HERE

    def delete(self, category_id):
        category = Category.query.get(category_id)
        if category:
            request_for_category_delete = Request(user_id = current_user.id,  type="category_delete", details= json.dumps({"category_id": category_id, "category_name":category.category_name}))
            db.session.add(request_for_category_delete)
            db.session.commit()
            return {"message": "Category deletetion request sent successfully"}, 200
        return {"message": "Category not found"}, 404

# _________________PRODUCTS(SEARCH, ADD, UPDATE, PUT, DELETE PRODUCTS) _________________
class ProductResource(Resource):
    # ONLY ADMIN CAN CHANGE THE products HERE......SO ADD THAT LOGIN , ROLE REQUIRED HERE
    def post(self):
        product_parser = reqparse.RequestParser()
        product_parser.add_argument("product_id", type=int)
        product_parser.add_argument(
            "product_name", type=str, required=True, help="Product name cannot be blank")
        product_parser.add_argument("product_price", type=int, required=True,
                                    help="Product price is required and should be a number")
        product_parser.add_argument("stock_quantity", type=int, required=True,
                                    help="Stock quantity is required and should be an integer")
        product_parser.add_argument("category_id", type=int, required=True,
                                    help="Category ID is required and should be an integer")
        product_parser.add_argument("manufacture_date", required=False,
                                    help="manufacture_date is required")
        product_parser.add_argument("expiry_date", required=False,
                                    help="expiry_date is required")
        product_parser.add_argument("imageUrl", required=True,
                                    help="Image Url  is required")
        args = product_parser.parse_args()

        product_id = args['product_id']
        product_name = args["product_name"].title()
        product_price = args['product_price']
        stock_quantity = args['stock_quantity']
        category_id = args['category_id']
        imageUrl = args['imageUrl']

        manufacture_date = None
        expiry_date = None
        if args["expiry_date"]:
            # expiry_date = datetime.strftime(args["expiry_date"], '%Y-%m-%dT%H:%M')
            expiry_date = args["expiry_date"]

        if args["manufacture_date"]:
            # manufacture_date = datetime.strftime(args["manufacture_date"], '%Y-%m-%dT%H:%M')
            manufacture_date = args["manufacture_date"]
        x = Product.query.filter_by(product_name=product_name).first()
        if x:
            return {"message": "Product is already present!"}, 400
        
        new_prod_request = Request(
            user_id= current_user.id,
            type= "product_add",
                        details = json.dumps({
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price,
        'stock_quantity': stock_quantity,
        'manufacture_date': manufacture_date,
        "imageUrl": imageUrl,
        'expiry_date': expiry_date,
        'category_id': category_id})) 
        try:
            db.session.add(new_prod_request)
            db.session.commit()
            return {"message": "Product sent to admin Successfully!"}, 200
        except:
            return  {"message": "Bad Request!"}, 400

    # ONLY ADMIN CAN CHANGE THE Product HERE......SO ADD THAT LOGIN , ROLE REQUIRED HERE
    # get the categ_id and see if the n

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int, required=True, help="The product id has to be sent by the server!")
        parser.add_argument("product_name", type=str)
        parser.add_argument("product_price", type=int)
        parser.add_argument("stock_quantity", type=int)
        parser.add_argument("category_id", type=int)
        parser.add_argument("manufacture_date")
        parser.add_argument("expiry_date")
        parser.add_argument("imageUrl")
        data = parser.parse_args()

        product_id = data['product_id']
        product = Product.query.get(product_id)
        
        if product:
            de2tails = {"category_id" : product.category.category_id,"category_name" : product.category.category_name,"product_old_name": product.product_name,}
            if data['product_id'] is not None:
                de2tails['product_id'] = data['product_id']
                # product.product_id = data['product_id']
            if data['product_name'] is not None:
                de2tails['product_name'] = data['product_name']
                # product.product_name = data['product_name']
            if data['imageUrl'] is not None:
                de2tails['imageUrl'] = data['imageUrl']
                # product.imageUrl = data['imageUrl']
            if data['product_price'] is not None:
                de2tails['product_price'] = data['product_price']
                # product.product_price = data['product_price']
            if data['stock_quantity'] is not None:
                de2tails['stock_quantity'] = data['stock_quantity']
                # product.stock_quantity = data['stock_quantity']
            if data['category_id'] is not None:
                de2tails['category_id'] = data['category_id']
                # product.category_id = data['category_id']
            if data['manufacture_date'] is not None:
                de2tails['manufacture_date'] = data['manufacture_date']
                # product.manufacture_date = data['manufacture_date']
            if data['expiry_date'] is not None:
                de2tails['expiry_date'] = data['expiry_date']
                # product.expiry_date = data['expiry_date']

            prod_update_req = Request(user_id = current_user.id, type='product_update',details= json.dumps(de2tails))
            db.session.add(prod_update_req)
            db.session.commit()
            return {"message": "Product update sent to admin successfully"}, 200
        else:
            return {"message": "Product not found"}, 404

    # ONLY ADMIN CAN CHANGE THE Product HERE......SO ADD THAT LOGIN , ROLE REQUIRED HERE
    def delete(self, product_id):
        product = Product.query.get(product_id)

        if product:
            request_for_product_delete = Request(user_id = current_user.id,  type="product_delete", details=json.dumps({"category_id" : product.category.category_id,"category_name" : product.category.category_name,"product_id": product_id, "product_name":product.product_name}))
            db.session.add(request_for_product_delete)
            db.session.commit()
            return {"message": "Product deletetion request sent successfully"}, 200
        return {"message": "Product not found"}, 404

## ________________CART RESOURCE________________##
class CartAPI(Resource):
    user_cart_item_marshal ={
    "cart_id" : fields.Integer,
    "user_id" : fields.Integer,
    "product_id" : fields.Integer,
    "item_name" : fields.String,
    "item_quantity" : fields.Integer,
    "item_total" : fields.Integer,
}
    user_shopping_cart_marshal = {
        'shopping_cart_id' : fields.Integer,
        'user_id' : fields.Integer,
        'itemcart_id' : fields.Integer,
        "cart_items" : fields.List(fields.Nested(user_cart_item_marshal))
    }
  

    @marshal_with(user_shopping_cart_marshal)
    def get(self):
        user_id = current_user.id
        user_shopping_cart = ShoppingCart.query.filter_by(user_id=user_id).first()
        user_item_cart = CartItem.query.filter_by(user_id = user_id).all()
        if user_item_cart:
            res_cart = []
            for item in user_item_cart:
                res_cart.append({
                    'shopping_cart_id' : user_shopping_cart.shopping_cart_id,
                    'user_id' : item.user_id, 
                    'itemcart_id' : item.cart_id, 
                    "cart_items" : [item], 
                })
            return res_cart
        return abort(404, description=  "No items in cart yet!")
    #adding item to cart 
    def post(self):
        cart_item_parser = reqparse.RequestParser()
        user_id = current_user.id
        cart_item_parser.add_argument("quantity", type =int, required =True, help = "quantity asked for can't be empty!")
        cart_item_parser.add_argument("product_id", type =int, required =True, help = "product_id can't be empty!")
        data = cart_item_parser.parse_args()

        quantity = data["quantity"]
        product_id = data['product_id']


        product = Product.query.get(product_id)
        if not product or product.stock_quantity < quantity or quantity <=0:
            return abort(400, description = "Not enough quantity for requested item.")

        check_user_cart = ShoppingCart.query.filter_by(user_id = user_id).first()
        if not check_user_cart:
            cart = ShoppingCart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
            check_user_cart = cart
       
        cart_item_check = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item_check:
            cart_item_check.item_quantity += quantity
            cart_item_check.item_total = cart_item_check.item_quantity * product.product_price

        else:
            item_total = quantity * product.product_price
            add_cart_item = CartItem(
                item_name=product.product_name,
                item_quantity=quantity,
                item_total=item_total,
                user_id=user_id,
                product_id=product_id
            )
            db.session.add(add_cart_item)

        product.stock_quantity -= quantity

        try:
            db.session.commit()
            return {'message': f"{product.product_name} added to cart!"}, 200
        except:
            return {"message": "Error adding item to cart"}, 500


    def delete(self):
        cart_item_delete_parser = reqparse.RequestParser()
        cart_item_delete_parser.add_argument("product_id", type=int, required=True, help="product_id can't be empty!")
        cart_item_delete_parser.add_argument("quantity", type=int, required=True, help="Quantity to remove can't be empty!")
        data = cart_item_delete_parser.parse_args()

        user_id = current_user.id
        product_id = data['product_id']
        quantity_to_remove = data['quantity']

        cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not cart_item:
            return {"message": "Item not found in cart"}, 404

        if quantity_to_remove <= 0 or quantity_to_remove > cart_item.item_quantity:
            return {"message": "Invalid quantity to remove"}, 400

        product = Product.query.get(product_id)
        if not product:
            return abort(400, description="Product not found.")

        try:
            if quantity_to_remove == cart_item.item_quantity:
                db.session.delete(cart_item)
            else:
                cart_item.item_quantity -= quantity_to_remove
                cart_item.item_total = cart_item.item_quantity * product.product_price

            product.stock_quantity += quantity_to_remove

            db.session.commit()
            return {"message": f" {quantity_to_remove} {product.product_name} quantity removed from the cart"}, 200
        except:
            return {"message": "Error updating item in cart"}, 400

## ________________CART CHECKOUT RESOURCE________________##
class CheckoutResource(Resource):
    order_item_marshal = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'product_id': fields.Integer,
        'item_name': fields.String,
        'item_quantity': fields.Integer,
        'item_total': fields.Integer,
        'associated_product' : fields.List(fields.Nested({
            "product_price":fields.Integer,
            'manufacture_date' : fields.DateTime(dt_format='rfc822'),
            'expiry_date' : fields.DateTime(dt_format='rfc822')
        }))
    }

    @marshal_with(order_item_marshal)
    def post(self):
        user_id = current_user.id
        user_cart = ShoppingCart.query.filter_by(user_id=user_id).first()
        if not user_cart:
            abort(404, description="Cart not found.")

        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            abort(400, description="Cart is empty.")

        order_items = []
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if not product :
                abort(400, description=f"Insufficient stock for {product.product_name}.")

            # Create an OrderItem
            order_item = OrderItem(
                user_id=user_id,
                product_id=item.product_id,
                item_name=item.item_name,
                item_quantity=item.item_quantity,
                item_total=item.item_total
            )
            db.session.add(order_item)
            order_items.append(order_item)

            # Update product stock
            product.stock_quantity -= item.item_quantity

            # Remove item from cart
            db.session.delete(item)

        # Commit the transaction
        try:
            db.session.commit()
            return order_items, 200
        except:
            abort(500, description="Error during checkout")

# ___________________________Admin to view all the request and approve / reject it ______________________________
'''all the request that come to admin must fullfill all the requirements beforehand {shoudln't be empty, should be unique etc etc}'''

'''allocate definitons for if they wana add the thing , update the thing , or delete the thing ........else if the user says no then reject the thing '''
class AdminResource(Resource):
    def product_function(what_action, details, creator_id):
        if what_action == "Add":
            p = Product.query.filter_by(product_name = details['product_name'].title()).first()
            if p:
                details['product_id'] = p.product_id
                addtoupdate = AdminResource.product_function('Update', details= details, creator_id=creator_id)
                if addtoupdate['status']=='ok':
                    return {'message': f"Product {details['product_name']} has been added sucsessfully"
                        ,"status" : "ok"}
                else:
                    return {'message': f"Product {details['product_name']} ERROR!","status" : "not_ok"}

            new_product = Product(
                product_name = details['product_name'].title(),
                product_price=details['product_price'],
                imageUrl=details['imageUrl'],
                stock_quantity=details['stock_quantity'],
                creator_id = creator_id,
                category_id=details['category_id'])
            
            if 'manufacture_date' in details.keys():
                try:
                    new_product.manufacture_date =datetime.strptime(str(details['manufacture_date']), "%Y-%m-%dT%H:%M") 
                except:
                    pass

            if 'expiry_date' in details.keys():
                try:
                    new_product.expiry_date = datetime.strptime(str(details['expiry_date']),"%Y-%m-%dT%H:%M") 
                except:
                    pass
            try:
                db.session.add(new_product)
                db.session.commit()
                return {'message': f"Product {details['product_name']} has been added sucsessfully"
                        ,"status" : "ok"}
            except:
                return {'message': f"Product {details['product_name']} ERROR!","status" : "not_ok"}

        elif what_action == "Update":
            # Update product details
            product = Product.query.filter_by(product_id=int(details['product_id'])).first()
            if product:
                product.product_name = details.get('product_name', product.product_name).title()
                product.product_price = details.get('product_price', product.product_price)
                product.imageUrl = details.get('imageUrl', product.imageUrl)
                product.stock_quantity = details.get('stock_quantity', product.stock_quantity)
                product.category_id = details.get('category_id', product.category_id)

                if 'manufacture_date' in details:
                    try:
                        product.manufacture_date = datetime.strptime(str(details['manufacture_date']), "%Y-%m-%dT%H:%M")
                    except :
                        product.manufacture_date = datetime.utcnow()
                       
                if 'expiry_date' in details:
                    try:
                        product.expiry_date = datetime.strptime(str(details['expiry_date']), "%Y-%m-%dT%H:%M")
                    except:
                       abort(404, description= 'error in manufacture date')
                try:
                    db.session.commit()
                    return {'message': f"Product {details['product_name']} has been Updated successfully","status" : "ok"}
                except:
                    pass
                    return {'message': f"Product {details['product_name']} ERROR!","status" : "not_ok"}
            else:
                return {'message': 'Product not found',"status" : "not_ok"}, 404

        elif what_action == "Delete":
            product = Product.query.filter_by(product_id=int(details['product_id'])).first()
            if product:
                prodname = product.product_name.title()
                cartitem_product = CartItem.query.filter_by(product_id=int(details['product_id'])).all()
                if cartitem_product:
                    for each_item in cartitem_product:
                        try:
                            db.session.delete(each_item)
                        except:
                            pass
                try:
                    db.session.delete(product)
                    db.session.commit()
                    return {'message': f"Product {prodname} has been deleted successfully","status" : "ok"}
                except:
                    return {'message': f"Product {details['product_name'].title()} ERROR!","status" : "not_ok"}

            else:
                return {'message': 'Product not found',"status" : "not_ok"}, 404
        return {'message': 'Wrong action given!',"status" : "not_ok"}
    def category_function(what_action, details, creator_id):
        if what_action=="Add":
            new_categ = Category(category_name = details['category_name'].title(), creator_id = creator_id)
            try:
                db.session.add(new_categ)
                db.session.commit()
                return {'message': f"{details['category_name']} has been added successfully","status" : "ok"}
            except:
                return {'message': f"{details['category_name']} ERROR (Category already Exists)","status" : "not_ok"}
        
        elif what_action=="Update":
            cat = Category.query.filter_by(category_id = int(details['category_id'])).first()
            cat.category_name = details['category_name'].title()
            try:
                db.session.commit()
                return {'message': f"{details['category_name']} has been changed successfully","status" : "ok"}
            except:
                return {'message': f"{details['category_name']} ERROR","status" : "not_ok"}
        
        elif what_action=="Delete":
            cat = Category.query.filter_by(category_id =int(details['category_id'])).first()
            cat_items = cat.linked_products
            for cat_item in cat_items:
                d = {"product_id":cat_item.category_id}
                try:
                    AdminResource.product_function("Delete", d, creator_id=creator_id)
                except:
                    pass
            try:
                db.session.delete(cat)
                db.session.commit()
                return {'message': f"{details['category_name']} has been Deleted successfully","status" : "ok"}
            except:
                return {'message': f"{details['category_name']} ERROR!","status" : "not_ok"}
        return {'message': 'Wrong action given!',"status" : "not_ok"}
    def storemanager_function(what_action, requesting_user_ki_id):
        """I can also send role as a parameter and then update to any role! if time permits ill do it ! Fingers Crossed !"""
        user = User.query.get(requesting_user_ki_id)
        if user:
            if what_action == "Add":
                with app.app_context():
                    datastore = app.security.datastore
                try:
                    datastore.add_role_to_user(user, "manager")
                    db.session.commit()
                    return {'message': f'{user.username} is now Manager!',"status" : "ok"}
                except:
                    pass
        return {'message': 'Could not find user.',"status" : "not_ok"}
       
    def rejected_request(req):
        req.status = "Rejected"
        req.request_change_done_by_admin = datetime.utcnow()
        try:   
            db.session.commit()
            print(f"Request to {req.type} has been rejected")
        except:
            pass
    
    def change_status(req):
        req.status = "Approved!"
        req.request_change_done_by_admin = datetime.utcnow()
        try:   
            db.session.commit()
            print(f"Request to {req.type} has been Approved!")
        except:
            pass

    @auth_required("token")
    @roles_required("admin")
    def get(self):
        '''view all the pending requests that he has'''
        # get the name of the person
        pending_requests = Request.query.filter_by(status='pending').all()
        if not pending_requests:
            return {"message":"no requests found"},404
        
        requests_data= []
        for req in pending_requests:
            requesting_user = User.query.get(req.user_id)
            requests_data.append({
                'request_id': req.id,
                'request_type' : req.type,
                'username': requesting_user.username,
                'user_id': requesting_user.id,
                'details': json.loads(req.details) if req.details is not None else None
            })
        return jsonify(requests_data)
    
    @auth_required("token")
    @roles_required("admin")
    def post(self):
        admin_parser = reqparse.RequestParser()
        admin_parser.add_argument("request_id", type=int, help = "Please enter the request id by the server !")
        admin_parser.add_argument("what_action", type=str, help = "Please enter the Action to be taken Mr.Admin !!")
        data = admin_parser.parse_args()

        request_id = data['request_id']
        what_action = data['what_action']

        req = Request.query.filter_by(id= int(request_id)).first()
        # what_action = req.type category_add
        '''split the whataaction and use listing for checcking the methds to be done !'''
        if req: 
            if what_action == "Reject":
                AdminResource.rejected_request(req)
                return {"message": "The request was rejected."},500

            elif "storeManager" in req.type:
                store_manager_returns = AdminResource.storemanager_function(what_action, req.user_id)
                if store_manager_returns["status"] == "ok":
                    AdminResource.change_status(req)
                    return {"message" : store_manager_returns["message"]}, 200

            details = json.loads(req.details)
            if "product" in req.type:
                product_returns = AdminResource.product_function(what_action, details,req.user_id)
                if product_returns["status"] == "ok":
                    AdminResource.change_status(req)
                    return {"message" : product_returns["message"]}, 200
                return {"message": product_returns["message"]},404
            
            elif "category" in req.type:

                category_returns = AdminResource.category_function(what_action, details, req.user_id)
                if category_returns['status'] == 'ok':
                    AdminResource.change_status(req)
                    return {"message" : category_returns["message"]}, 200
                return {"message": category_returns["message"]}, 404
            

            
            

            else:
                return {"message": "Bad Request!"}, 500
    


