import os

from flask import Flask, render_template, request, session, redirect, url_for, flash
from celery import Celery
from celery.schedules import crontab
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] =  'thi$-i$-$ecret'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
app.config['CELERY_TIMEZONE'] = 'Europe/Warsaw'
app.config['CELERYBEAT_SCHEDULE'] = {
    'test-celery': {
        'task': 'app.send_async_email',
        # Every minute
        'schedule': crontab(minute="*"),
    }
}


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
def send_async_email(recipient=None):
    # print(f"user:{app.config['MAIL_USERNAME']} pass: {app.config['MAIL_PASSWORD']}") # for possibly quick debug
    if recipient == None:
        recipient = 'pilot.string@gmail.com'

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
        recipient = request.form['email']
        send_async_email.delay(recipient)
        flash(f"An email was sent to {recipient}")
    if request.form['submit'] == 'Send in 1 minute':
        recipient = request.form['email']
        countdown = 20
        send_async_email.apply_async(args=[recipient], countdown=countdown)
        flash(f"An email to {recipient} will be sent in {countdown} seconds.")

    return redirect(url_for('index'))

  


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


