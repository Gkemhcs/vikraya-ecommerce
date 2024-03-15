from flask import Flask
from models.firestore_client import Firestore
from google.cloud import logging
client=Firestore(database="vikraya-ecommerce")
logging_client = logging.Client()
logger = logging_client.logger('catalog-service')
app=Flask(__name__)
@app.route("/")
def home():
      logger.log_text('Home route accessed', severity='INFO')
      return {"status":200,"message":"i am working"}
@app.route("/products")
def get_catalog():
     logger.log_text('Get catalog route accessed', severity='INFO')
     data=client.get_all()
     return data
@app.route("/categories/<category>")

def get_category(category):
      logger.log_text('Get category route accessed', severity='INFO')
      data=client.get_category(category)
      return data
@app.route("/products/<id>")
def get_produt_info(id):
        logger.log_text('Get product info route accessed', severity='INFO')
        data=client.get_product_info(id)
        return data
if(__name__=="__main__"):
        app.run(port=8001)
