from main import app
from application.models import db
from werkzeug.security import generate_password_hash
from application.sec import datastore

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name="admin", description="User is an Admin")
    datastore.find_or_create_role(name="manager", description="User is a Store-Manager")
    datastore.find_or_create_role(name="user", description="User is a User")

    db.session.commit()
    if not datastore.find_user(email_address="admin@email.com"):
        datastore.create_user(email_address="admin@email.com", home_address= "Apt. 865 60964 Pouros Mill, Janettafort, WY 79450", username = "Admin",contact_number = "7827335933", password=generate_password_hash("1234"), roles=["admin"])

    if not datastore.find_user(email_address="manager1@email.com"):
        datastore.create_user(email_address="manager1@email.com", home_address= "Apt. 519 379 Andre Prairie, New Celindaville, MD 03878-0282", username = "Store Manager 1",contact_number = "3433649506",password=generate_password_hash("1234"), roles=["manager"], active=False)
    if not datastore.find_user(email_address="user1@email.com"):
        datastore.create_user(email_address="user1@email.com", home_address= "Jl. Gatot Soebroto No. 60, Purwakarta, SG 95029", username = "User 1",contact_number = "2079076657",password=generate_password_hash("1234"), roles=["user"])
    if not datastore.find_user(email_address="user2@email.com"):
        datastore.create_user(email_address="user2@email.com",home_address= "Esc. 945 Monte Antonia Naranjo, 93, Roquetas de Mar, Bal 73300",  username = "User 2",contact_number = "7756290441",password=generate_password_hash("1234"), roles=["user"])
    db.session.commit()
