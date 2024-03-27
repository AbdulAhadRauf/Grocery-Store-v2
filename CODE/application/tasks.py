import time
from fpdf import FPDF
from matplotlib import pyplot as plt
from sqlalchemy import desc, func
from application.workers import cel_app
from datetime import datetime, timedelta
from celery.schedules import crontab
from jinja2 import Template
from application.tosendmail import send_email
from application.models import Product, User, OrderItem, Category, db
import os
import csv
import zipfile
from flask import jsonify, render_template
from weasyprint import HTML

'''celery commands
celery -A main.celery worker -l info
celery -A main.celery beat --max-interval 1 -l info

~/go/bin/MailHog
to send a mial using mail hog '''


@cel_app.on_after_finalize.connect
def set_up_daily_task(sender, **kwargs):
    sender.add_periodic_task(crontab(
        hour=5, minute=34), send_dailyvisit_email.s(), name="send_dailyemail_task")


@cel_app.on_after_finalize.connect
def set_up_monthly_task(sender, **kwargs):
    sender.add_periodic_task(crontab(day_of_month='18', hour=5, minute=34),
                             send_monthlyreport_email.s(), name="send_monthly_emailtask")



# create admin report analysis
@cel_app.task()
def create_admin_report():
    def sales_and_revenue_analysis():
        daily_sales_data = db.session.query(
            func.date(OrderItem.purchase_date).label('date'),
            func.sum(OrderItem.item_total).label('total_sales')
        ).group_by(func.date(OrderItem.purchase_date)).all()

        # Processing the results to prepare for plotting
        dates = [result.date for result in daily_sales_data]
        sales = [float(result.total_sales) for result in daily_sales_data]

        # Plotting the results
        plt.figure(figsize=(6, 9))
        plt.plot(dates, sales, marker='o')
        plt.title('Daily Sales')
        plt.xlabel('Date')
        plt.ylabel('Total Sales')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('./static/daily_sales.png')

        # Cumulative revenue
        daily_sales_data = db.session.query(
            func.date(OrderItem.purchase_date).label('date'),
            func.sum(OrderItem.item_total).label('total_sales')
        ).group_by(func.date(OrderItem.purchase_date)).order_by(desc('date')).all()

        # Sort the sales data by date
        daily_sales_data = sorted(daily_sales_data, key=lambda x: x.date)

        # Calculate cumulative sales
        dates = [result.date for result in daily_sales_data]
        daily_sales = [float(result.total_sales)
                       for result in daily_sales_data]
        cumulative_sales = [sum(daily_sales[:i+1])
                            for i in range(len(daily_sales))]

        # Plotting the results
        plt.figure(figsize=(6, 9))
        plt.plot(dates, cumulative_sales, marker='o')
        plt.title('Cumulative Sales Over Time')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Sales')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('./static/cumulative_revenue.png')

    def pie_chart_products():
        all_products = Product.query.all()
        product_names = [product.product_name for product in all_products]
        product_quantities = [float(product.stock_quantity)
                              for product in all_products]
        plt.figure(figsize=(6, 6))
        plt.pie(product_quantities, labels=product_names, autopct='%1.1f%%')
        plt.title('Items by Size')
        plt.savefig('./static/pchart_items.png')

    def pie_chart_categories():
        all_categories = Category.query.all()
        category_sizes = {}

        for category in all_categories:
            category_size = sum(float(product.stock_quantity)
                                for product in category.linked_products)
            category_sizes[category.category_name] = category_size

        plt.figure(figsize=(6, 6))
        plt.pie(list(category_sizes.values()), labels=list(
            category_sizes.keys()), autopct='%1.1f%%')
        plt.title('Category by Size')
        plt.savefig('./static/pchart_category.png')

    sales_and_revenue_analysis()
    pie_chart_products()
    pie_chart_categories()

    time.sleep(5)

    html_content = render_template("analysis.html")
    html = HTML(string=html_content)

    pdf_filename = "Admin_report.pdf"
    downloads_folder = "./MADDownloads"
    pdf_file_path_in_folder = f'{downloads_folder}/{pdf_filename}'
    html_file_path_in_folder = f"{downloads_folder}/{pdf_filename.replace('.pdf', '.html')}"

    with open(html_file_path_in_folder, "w") as html_fil:
        html_fil.write(html_content)

    img_height = 200
    img_width = 180
# generating pdf usinf fpdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(40, 10, "Analysis")
    pdf.ln(20)
    pdf.cell(40, 10, 'Pie Chart by Category')
    pdf.image("static/pchart_category.png", 10, 30, img_height, img_width)
    
    pdf.add_page()
    pdf.cell(40, 10, 'Pie Chart by Items')
    pdf.image("static/pchart_items.png", 10, 30, img_height, img_width)

    pdf.add_page()
    pdf.cell(40, 10, 'Daily Sales')
    pdf.image("static/daily_sales.png", 10, 30, img_height, img_width)

    pdf.add_page()
    pdf.cell(40, 10, 'Cumulative Revenue')
    pdf.image("static/cumulative_revenue.png", 10, 30, img_height, img_width)

    pdf.output(pdf_file_path_in_folder, "F")

    with open('templates/adminreport.html') as file_:
        template = Template(file_.read())
        message = template.render()
    send_email(
        to="admin@email.com",
        subject="Analysis of the Grocery Store",
        message=message,
        file=pdf_file_path_in_folder
    )

    return "Email with analysis report sent successfully."


# send monthly report to user
@cel_app.task()
def send_dailyvisit_email():
    all_users = User.query.all()
    for user in all_users:

        if datetime.now() - user.lastlogin >= timedelta(minutes=0):
            with open('templates/visit24houralert.html') as file_:
                visit_alert_template = Template(file_.read())
                message = visit_alert_template.render(username=user.username)

            send_email(
                to=user.email_address,
                subject="Visit Alert",
                message=message
            )

    return " Alert emails have been sent to users who have not logged in in 24 hours!"

# monthly report to all users


@cel_app.task()
def send_monthlyreport_email():
    users = User.query.all()
    data = db.session.query(User.id, User.username, User.email_address, OrderItem.item_name, OrderItem.item_quantity, OrderItem.item_total).join(
        OrderItem, User.id == OrderItem.user_id
    ).all()

    for user in users:
        list = []
        final_sum = 0
        for i in data:
            if user.id == i.id:
                final_sum += i.item_total
                detail = {"productname": i.item_name,
                          "quantity": i.item_quantity, "total": i.item_total}
                list.append(detail)
        with open('templates/Monthlypurchasereport.html') as file_:
            template = Template(file_.read())
            message = template.render(
                name=user.username, details=list, totalprice=final_sum)

        send_email(
            to=user.email_address,
            subject="Monthly Alert",
            message=message
        )
    return "Monthly Emails sent to all users"


# send a categoery report to store manager
@cel_app.task()
def generate_report(category_id, store_manager_email):
    cat = Category.query.get(category_id)
    if cat:
        products = cat.linked_products
        csv_data = [
            ["Category Name", "Product Name", "Quantity", "Time_of_Issue", "Price", "Expiry_Date", "Manufacture_Date"]
        ]
        for j in products:
            csv_data.append([
                j.category.category_name, j.product_name, j.stock_quantity, datetime.utcnow(), j.product_price, j.expiry_date, j.manufacture_date])

        categname_cleaned = cat.category_name.replace(" ", "_")
        downloads_folder = "./MADDownloads"
        csv_file_path = os.path.join(
            downloads_folder, f'{categname_cleaned}.csv')

        with open(csv_file_path, 'a', newline='') as csvfile:
            data_writer = csv.writer(csvfile)
            data_writer.writerows(csv_data)

        zip_file_path = os.path.join(
            downloads_folder, f'{categname_cleaned}.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            zipf.write(csv_file_path, arcname=f'{categname_cleaned}.csv')

        with open('templates/CSVsendingcard.html') as file_:
            template = Template(file_.read())
            message = template.render()

        send_email(
            to=store_manager_email,
            subject="Export CSV",  # Fixed sub to subject
            message=message,
            file=zip_file_path  # Use files instead of file
        )
        return "Mail Sent to User!!"

    return jsonify({"message": "category not found"})


@cel_app.task()
def user_requested_report(user_id):
    users = User.query.get(user_id)
    users = [users]
    data = db.session.query(User.id, User.username, User.email_address,
                            OrderItem.item_name, OrderItem.item_quantity, OrderItem.item_total, OrderItem.purchase_date
                            ).join(
        OrderItem, User.id == OrderItem.user_id
    ).all()

    for user in users:
        list = []
        final_sum = 0
        for i in data:
            if user.id == i.id:
                final_sum += i.item_total
                detail = {"productname": i.item_name, "quantity": i.item_quantity,
                          "total": i.item_total, "purchase_date": i.purchase_date}
                list.append(detail)
        with open('templates/Monthlypurchasereport.html') as file_:
            template = Template(file_.read())
            message = template.render(
                name=user.username, details=list, totalprice=final_sum)

        send_email(
            to=user.email_address,
            subject="Your order history till now",
            message=message
        )
    return f"Mail to {user.username} has been sent !"
