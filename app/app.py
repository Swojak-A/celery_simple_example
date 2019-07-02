import os

from flask import Flask, render_template, request, session, redirect, url_for
from celery import Celery
from flask_mail import Mail, Message

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

#Flask mail configuration  
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 465  
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

#instantiate the Mail class  
mail = Mail(app)  
  


# ROUTES
@app.route('/', methods=['GET', 'POST'])  
def index():
	if request.method == 'GET':
		return render_template('index.html')

	email = request.form['email']

	return redirect(url_for('index'))

    # recipient = "pilot.string@gmail.com"
    # msg = Message('subject', sender = 'pilot.string@gmail.com', recipients=[recipient])  
    # msg.body = 'hi, this is the mail sent by using the flask web application'  

    # mail.send(msg)

    # return "Mail Sent"  
  


if __name__ == '__main__':
	app.run()


