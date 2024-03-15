from flask import Flask,request
from models.user_cart import UserCart
from google.cloud import logging
cartClient=UserCart(database="vikraya-ecommerce")

client = logging.Client()
logger = client.logger('cart-service')
app=Flask(__name__)

@app.route("/")
def home():
     logger.log_text('Home route accessed', severity='INFO')
     return {"status":200,"message":"I AM RUNNING"}
@app.route("/cart/add",methods=["POST"])
def add_to_cart():
     logger.log_text('Add to cart route accessed', severity='INFO')

     return cartClient.add_to_cart(request.form.get("product_id"),request.form.get("user_id"))
@app.route("/cart/delete",methods=["POST"])
def delete_from_cart():

     logger.log_text('Delete from cart route accessed', severity='INFO')
     return cartClient.delete_from_cart(request.form.get("product_id"),request.form.get("user_id"))
@app.route("/cart")
def  show_cart():
     logger.log_text('Show cart route accessed', severity='INFO')
     return cartClient.get_cart(request.args.get("user_id"))
@app.route("/cart/clear",methods=["POST"])
def empty_cart():
     logger.log_text('Empty cart route accessed', severity='INFO')
     return cartClient.empty_cart(request.form.get("user_id"))

if(__name__=="__main__"):
       logger.log_text('Starting application', severity='INFO')
       app.run(port=8003)