import os

from flask import Flask, render_template, request, session, redirect, url_for
from celery import Celery
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] =  'thi$-i$-$ecret'

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



# Celery tasks
@celery.task
def send_async_email():
    # sending the mail
    recipient = "pilot.string@gmail.com"
    msg = Message('subject', sender = 'pilot.string@gmail.com', recipients=[recipient])
    msg.body = 'hi, this is the mail sent by using the celery app'  

    with app.app_context():
        mail.send(msg)

# Routes
@app.route('/', methods=['GET', 'POST'])  
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))

    email = request.form['email']
    # session['email'] = email

    if request.form['submit'] == 'Send':
        send_async_email()

    return redirect(url_for('index'))

  


if __name__ == '__main__':
    app.run()


