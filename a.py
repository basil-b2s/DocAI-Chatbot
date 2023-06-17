# import json
# import requests
# headers = {
#     "Authorization":"ya29.a0AWY7CkmPFtQcCCwEsPQQi9JszdzVKppXzahZdQDY-3wCTO9S2iuq1N_aaRXWIfODumI4Rd3R3DKy4YAKyQDKu_ki-GWz2Rn3yhRafnSpTxhBhk62ptfExY25pp4I4XhcMSJHDDnzN5xoSdHNkzF2xosXliQRaCgYKASgSARESFQG1tDrprSGjJN0Y9GVvxEBXzWcWXQ0163"
# }

# para = {
#     "name" : "appointment.pdf"
# }

# files = {
#     'data':('metadata',json.dumps(para),'application/json;charset=UTF-8'),
#     'file':open('./appointment.pdf','rb')
# }

# r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
#     headers=headers,
#     files=files
# )

import email
from email.message import EmailMessage
import ssl
import smtplib

email_sender = "basilsaji2206@gmail.com"
email_password = "memh hopr ndym pqrz"


email_receiver = "basilsaji222@gmail.com"

subject = "This is a test mail"

body = "this is a test mail"

em = EmailMessage()
em["From"] = email_sender
em['To'] = email_receiver
em["subject"] = subject
em.set_content(body)


with open('appointment.pdf', 'rb') as content_file:
    content = content_file.read()
    em.add_attachment(content, maintype='application', subtype='pdf', filename='appointment.pdf')

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

