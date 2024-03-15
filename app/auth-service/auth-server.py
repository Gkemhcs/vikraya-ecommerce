from flask import Flask,request
from utils.user_management import User
from google.cloud import logging
client = logging.Client()
logger = client.logger('auth-server')
app=Flask(__name__)
user_db=User(database="vikraya-ecommerce")
@app.route("/")
def home():
      logger.log_text('Home route accessed', severity='INFO')
      return {"status":200,"message":"i am running"}
@app.route("/register",methods=["POST"])
def register_user():
    logger.log_text('Register route accessed', severity='INFO')
    name=request.form.get("name")
    email=request.form.get("email")
    phonenumber=request.form.get("email")
    passwordhash=request.form.get("passwordhash")
    
    return user_db.register(name,email,phonenumber,passwordhash)
@app.route("/login",methods=["POST"])
def validate_login():
    logger.log_text('Login route accessed', severity='INFO')
    email=request.form.get("email")
    return user_db.validate_login(email)
@app.route("/user_info")
def get_user_info():
        user_id=request.args.get("user_id")
        return user_db.user_info(user_id)
if(__name__=="__main__"):
      logger.log_text('Starting application', severity='INFO')
      app.run(port=8002)