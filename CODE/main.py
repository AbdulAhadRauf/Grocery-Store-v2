from flask import Flask
from flask_restful import Api
from flask_security import Security
from application.config import DevelopmentConfig
from application.models import db
from application.sec import datastore
import os
from application.workers import cel_app,ContextTask
from flask_caching import Cache


celery = None
cache = None

def create_app():
    app = Flask(__name__)
    if os.getenv("ENV", "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Staring Local Development")
        app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    api = Api(app)
    api.init_app(app)
    app.app_context().push()
    cache = Cache(app)
    cache.init_app(app)
    app.app_context().push()
    app.security = Security(app, datastore)
    cel=cel_app
    cel.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        timezone = 'Asia/Kolkata',
        broker_connection_retry_on_startup=True,
    )

    cel.Task=ContextTask
    app.app_context().push()
    
    return app, api, celery, cache

app, api, celery, cache  = create_app()




from application.views import *
from application.api import AdminResource
from application.api import ToggleUser
from application.api import UserResource
from application.api import LoadData
from application.api import CategoriesResource
from application.api import ProductResource
from application.api import CheckoutResource
from application.api import SearchFunctionality
from application.api import CartAPI
from application.api import Login
from application.api import Logout
from application.api import BecomeStoreManager
from application.api import UserProducts
from application.api import UserCategories
from application.api import SendingConfidentialData
from application.api import OrderHistory


api.add_resource(OrderHistory, '/orderhistory/<int:user_id>')
api.add_resource(AdminResource, "/admin")
api.add_resource(UserResource, "/user")
api.add_resource(LoadData, "/loaddummy")
api.add_resource(CategoriesResource, "/categories", "/categories/<int:category_id>")
api.add_resource(ProductResource, "/products","/products/<int:product_id>")
api.add_resource(CheckoutResource, '/checkout')
api.add_resource(CartAPI, "/cart")
api.add_resource(SendingConfidentialData,'/api/me')
api.add_resource(SearchFunctionality, "/search","/search/<string:search_string>")
api.add_resource(Login, '/user_login')
api.add_resource(Logout, '/user_logout')
api.add_resource(BecomeStoreManager, '/BecomeStoreManger')
api.add_resource(UserProducts, '/user/<int:creator_id>/products')
api.add_resource(UserCategories, '/user/<int:creator_id>/categories')
api.add_resource(ToggleUser, '/toggleuser')




@app.errorhandler(404)
def page_not_found(e):

    return {"message": "Not Found"}, 404

@app.errorhandler(403)
def not_authorized(e):
    return {"message" : "Not Authorized"}, 403



with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()