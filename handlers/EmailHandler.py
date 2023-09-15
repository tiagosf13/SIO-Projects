from handlers.DataBaseCoordinator import read_json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib



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