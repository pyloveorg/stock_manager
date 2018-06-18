from flask import Flask
from flask_mail import Mail, Message
from config_deployment import MAIL


app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']=MAIL.MAIL_SERVER
app.config['MAIL_PORT'] = MAIL.MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL.MAIL_USE_SSL
app.config['MAIL_ASCII_ATTACHMENTS'] = MAIL.MAIL_ASCII_ATTACHMENTS


mail = Mail(app)