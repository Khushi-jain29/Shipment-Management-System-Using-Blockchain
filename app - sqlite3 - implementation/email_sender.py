import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Replace the below details with your own
sender_email = "tamanagementsuite@gmail.com" # TA app official email
app_password = "jwvctuybkduuvnic" # app password (without spaces)


def send_email(receiver_email, subject, body):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to the email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP session for sending the mail
        server = smtplib.SMTP('smtp.gmail.com', 587) # Use 465 for SSL
        server.starttls() # Enable security
        server.login(sender_email, app_password) # Login with your Gmail and app password
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

