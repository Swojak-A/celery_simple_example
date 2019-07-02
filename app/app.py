import os

from flask import Flask
from celery import Celery
from flask_mail import Mail, Message

app = Flask(__name__)


#Flask mail configuration  
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 465  
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True


#instantiate the Mail class  
mail = Mail(app)  
  
#configure the Message class object and send the mail from a URL  
@app.route('/')  
def index():  
    recipient = "pilot.string@gmail.com"
    msg = Message('subject', sender = 'pilot.string@gmail.com', recipients=[recipient])  
    msg.body = 'hi, this is the mail sent by using the flask web application'  



    mail.send(msg)

    return "Mail Sent"  
  
if __name__ == '__main__':
	app.run()


