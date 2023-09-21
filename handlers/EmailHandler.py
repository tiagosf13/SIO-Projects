from handlers.DataBaseCoordinator import read_json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak
from handlers.DataBaseCoordinator import db_query
from handlers.Retrievers import get_product_by_id
import os
from datetime import datetime

def get_id_by_username(username):
    # Construct the SQL query
    # Secure Query
    # query = "SELECT id FROM users WHERE username = %s"
    # result = db_query(query, (username,))
    
    query = "SELECT id FROM users WHERE username = " + username
    result = db_query(query)

    # Check if 
    if result:
        return str(result[0][0])
    else:
        return None

def sql_to_pdf(username, output_path):

    # Secure Query
    # query = "SELECT * FROM %s_cart"
    # result = db_query(query, (username,))

    query = "SELECT * FROM " + username + "_cart"
    result = db_query(query)

    id = get_id_by_username(username.capitalize())
    lst = []
    for element in result:
        product_id = element[0]
        quantity = element[1]
        product = get_product_by_id(product_id)
        product_name = product["name"]
        price = product["price"]
        price = round(float(price) * int(quantity), 2)
        price = str(price) + " €"
        lst.append((product_id, product_name, quantity, price))

    lst = sorted(lst, key=lambda x: x[0])
    result = lst
    result.insert(0, ("Product ID", "Product Name", "Quantity", "Price"))

    
    # Read the CSV file and convert it to a list of rows
    rows = result

    # Define the table style
    style = TableStyle([
        # Header row style
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(77/255, 155/255, 75/255)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 14),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        # Data rows style
        ("BACKGROUND", (0, 1), (-1, -1), colors.Color(102/255, 102/255, 102/255)),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.whitesmoke),
        ("ALIGN", (0, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ])

    # Create the table object
    table = Table(rows)

    # Apply the table style
    table.setStyle(style)

    # Create the PDF document and add the table to it
    doc = SimpleDocTemplate(output_path, pagesize=letter, encoding="utf-8")


    # Create the username and ID paragraph
    username_style = ParagraphStyle(
        name='UsernameStyle',
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.black,
        alignment=TA_CENTER
    )
    username_text = f"{username.capitalize()} ({id})"
    username_para = Paragraph(username_text, username_style)

    # Create the date and time paragraph
    datetime_style = ParagraphStyle(
        name='DateTimeStyle',
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.black,
        alignment=TA_CENTER
    )
    now = datetime.now()
    datetime_text = f"Date: {now.strftime('%d-%m-%Y %H:%M:%S')}"
    datetime_para = Paragraph(datetime_text, datetime_style)

    # Add the spacer, username/ID paragraph, table, and datetime paragraph to the PDF document
    elements = [
        username_para,
        Spacer(width=0, height=0.2*inch),
        table,
        Spacer(width=0, height=0.2*inch),
        datetime_para
    ]

    doc.build(elements)
    return True



def send_email_with_attachment(to, subject, body, attachment_path):
    # Read Email credentials file
    credentials = read_json("/credentials/EmailCredentials.json")

    # Create a MIMEText object to represent the email body
    msg = MIMEMultipart()
    msg['From'] = credentials["email"]
    msg['To'] = to
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'html'))

    # Attach the PDF file as an attachment
    with open(attachment_path, "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")

    pdf_attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
    msg.attach(pdf_attachment)

    # Connect to the SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your email provider's SMTP server

    try:
        # Login to your email account
        server.login(credentials["email"], credentials["password"])

        # Send the email with attachment
        server.sendmail(credentials["email"], to, msg.as_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()

    # Return True to indicate the email was sent successfully
    return True




def send_email(to, subject, body):

    # Read Email credentials file
    credentials = read_json("/credentials/EmailCredentials.json")

    # Create a MIMEText object to represent the email body
    msg = MIMEMultipart()
    msg['From'] = credentials["email"]
    msg['To'] = to
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your email provider's SMTP server

    try:
        # Login to your email account
        server.login(credentials["email"], credentials["password"])

        # Send the email
        server.sendmail(credentials["email"], to, msg.as_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the connection to the SMTP server
        server.quit()

    # Return True to indicate the email was sent successfully
    return True