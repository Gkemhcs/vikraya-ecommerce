from flask import Flask,request
from models.order_client import userOrders
from google.cloud import logging
app=Flask(__name__)
orderClient=userOrders(database="vikraya-ecommerce")
logging_client = logging.Client()
logger = logging_client.logger('order-manager')
@app.route("/")
def home():
   logger.log_text('Home route accessed', severity='INFO')
   return {"message":"i am running","status":200}
@app.route("/order/create",methods=["POST"])
def create_order():
      logger.log_text('Create order route accessed', severity='INFO')
      user_id=request.form.get("user_id")
      product_id=request.form.get("product_id")
     
      return orderClient.create_order(product_id,user_id)
@app.route("/orders")
def show_orders():
      logger.log_text('Show orders route accessed', severity='INFO')
      user_id=request.args.get("user_id")
      return orderClient.show_orders(user_id)
@app.route("/order/cancel",methods=["POST"])
def cancel_order():
       logger.log_text('Cancel order route accessed', severity='INFO')
       order_id=request.form.get("order_id")
       return orderClient.cancel_order(order_id)
if(__name__=="__main__"):
      app.run(port=8004)