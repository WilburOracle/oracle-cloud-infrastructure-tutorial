# python script for sending SMTP configuration with Oracle Cloud Infrastructure Email Delivery
import smtplib 
import email.utils
from email.message import EmailMessage
import ssl

# Replace sender@example.com with your "From" address.
# This address must be verified.
# this is the approved sender email
SENDER = 'admin@oracle-work.com'
SENDERNAME = 'Admin OrcWrk'

FROM = 'chenwb2019@gmail.com'
FROMNAME = 'chenwb2019 (sent by admin@oracle-work.com on behalf of chenwb2019@gmail.com)'
 
# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
#RECIPIENT = 'wenbin.chen@oracle.com'
RECIPIENT = '1064068030@qq.com'
 
# Replace the USERNAME_SMTP value with your Email Delivery SMTP username.
#USERNAME_SMTP = 'ocid1.user.oc1..aaaaaaaa54m6kfigxatlwnhqsh5dby7e4laxz557at3srexq3dpsyfmqax7a@ocid1.tenancy.oc1..aaaaaaaaro7aox2fclu4urtpgsbacnrmjv46e7n4fw3sc2wbq24l7dzf3kba'
USERNAME_SMTP = 'ocid1.user.oc1..aaaaaaaa54m6kfigxatlwnhqsh5dby7e4laxz557at3srexq3dpsyfmqax7a@ocid1.tenancy.oc1..aaaaaaaaro7aox2fclu4urtpgsbacnrmjv46e7n4fw3sc2wbq24l7dzf3kba.jj.com'


# Put the PASSWORD value from your Email Delivery SMTP password into the following file.
PASSWORD_SMTP_FILE = 'ociemail.config'
 
# If you're using Email Delivery in a different region, replace the HOST value with an appropriate SMTP endpoint.
# Use port 25 or 587 to connect to the SMTP endpoint.
HOST = "smtp.email.ap-tokyo-1.oci.oraclecloud.com"
PORT = 587
 
# The subject line of the email.
SUBJECT = 'Shenzhen Convention and Exhibition Center ticket verification code'
 
# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Email Delivery Test\r\n"
             "This email was sent through the Email Delivery SMTP "
             "Interface using the Python smtplib package."
            )
 
# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
   <p> Hi, Chenwb</p>
   <br/>
   <p>I'm glad you can attend this conference. 
    <br/>Your ticket verification code is: <b>ef-ha20543</b>.Please attend the conference at Shenzhen Convention and Exhibition Center on 10/22/2022. Please show your verification code when you enter</p>
    <br/>
     <br/>
      <br/>
</body>
</html>"""

# get the password from a named config file ociemail.config
with open(PASSWORD_SMTP_FILE) as f:
    password_smtp = f.readline().strip()

# create message container
msg = EmailMessage()
msg['Subject'] = SUBJECT
#msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['From'] = email.utils.formataddr((FROMNAME, FROM))
msg['To'] = RECIPIENT

# make the message multi-part alternative, making the content the first part
msg.add_alternative(BODY_TEXT, subtype='text')
# this adds the additional part to the message
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.add_alternative(BODY_HTML, subtype='html')

# Try to send the message.
try: 
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    # most python runtimes default to a set of trusted public CAs that will include the CA used by OCI Email Delivery.
    # However, on platforms lacking that default (or with an outdated set of CAs), customers may need to provide a capath that includes our public CA.
    server.starttls(context=ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None))
    # smtplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, password_smtp)
    # our requirement is that SENDER is the same as From address set previously
    server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()
# Display an error message if something goes wrong.
except Exception as e:
    print(f"Error: {e}")
else:
    print("Email successfully sent!")