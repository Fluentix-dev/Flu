import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, code, subject="Your Fluentix vertification code."):

    body = f"""Hello, here is your vertification code: {code}
By the way, thanks for using our language Fluentix, it's a language that with a plan to replace the coding industry.
Please note that this language is still in early development, so bugs/issues are expected.
You can freely reply to this email to report a bug.

From, Lam, one of the developers of Fluentix:

http://fluentix.dev"""

    from_email = "nglamdztop1ff@gmail.com"
    app_password = "tril mcas htbk wqyp"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(from_email, app_password)  # Log in to your email account
            server.send_message(msg)  # Send the email
            #print("Email sent successfully!")
            return ""
    except Exception as e:
        exit()