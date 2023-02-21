import email, smtplib, ssl
from dotenv import load_dotenv, find_dotenv
from os import getenv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ntpath
from paths import *

load_dotenv(find_dotenv())

def get_latest_file(path:str):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def send_email(endtime, timedelta):

    subject = "Daily backup report"
    body = "Report from backup program. Program ended "+str(endtime) + ". Runtime was "+str(timedelta)
    sender_email = getenv('EMAIL')
    receiver_email = getenv('TO_EMAIL')
    password = getenv('EMAIL_PASS')
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    latest_copied_file = get_latest_file(COPIED_FILES_PATH)
    latst_figures_file = get_latest_file(FIGUREPATH)
    filenames = [latest_copied_file, COMPRESSED_LOGS_24H_PATH, latst_figures_file]  # In same directory as script

    # Open PDF file in binary mode
    for filename in filenames:
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {ntpath.basename(filename)}",
            )
            # Add attachment to message and convert message to string
            message.attach(part)
            
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.gmx.net", 465) as server:
        #server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)