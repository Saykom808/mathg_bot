import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase


email_sender = 'Your mail'
email_password = 'Your pass'
email_receiver = 'Mail Receiver'

def send_email(message, sender, receiver,  password):
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls() 


  try:                      
    with open('index.html', 'r') as file:
      template = file.read()
  except IOError:
    return "Template file doesn't found"
  

  try:                   # Mail sending
    server.login(sender, password)
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email_receiver
    msg['Subject'] = '2024 Soundmains beats'

    msg.attach(MIMEText('Whats good'))
    msg.attach(MIMEText(template, 'html'))

    for file in os.listdir("beats"):
      filename = os.path.basename(file)
      ftype, encoding = mimetypes.guess_type(file)
      file_type, subtype = ftype.split('/')
      

      if file_type == "text":
        with open(f"beats/{file}") as f:
          file = MIMEText(f.read(), subtype)
      elif file_type == 'application':
        with open(f"beats/{file}", 'rb') as f:
          file = MIMEApplication(f.read(), subtype)
      elif file_type == 'audio':
        with open(f"beats/{file}", 'rb') as f:
          file = MIMEAudio(f.read(), subtype)
      elif file_type == 'audio':
        with open(f"beats/{file}", 'rb') as f:
          file = MIMEBase(f.read(), subtype)
      else:
        continue

      file.add_header('content-disposition', 'attachment', filename=filename)
      msg.attach(file)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    return "Message sent successfully"
  except Exception as _ex:
    return f"{_ex}\nCheck your email address or password"

def main():
  
  result = send_email(None , email_sender, email_receiver, email_password)
  print(result)

if __name__ == '__main__':
  main()
