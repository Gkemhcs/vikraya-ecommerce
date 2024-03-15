from flask import  Blueprint,render_template,url_for,redirect,request
import os,time,requests,json
from google.cloud import logging
from flask_login import login_required
def create_products_route(counter,gauge,histogram,summary):
      
      products=Blueprint("products",__name__,static_folder="static",template_folder="templates")
      logging_client = logging.Client()
      logger = logging_client.logger('frontend_product_routes')
      catalog_service_endpoint=os.getenv("CATALOG_SERVICE_ENDPOINT")
      product_search_endpoint=os.getenv("VECTOR_SEARCH_API_ENDPOINT")
      product_search_api_key=os.getenv("VECTOR_SEARCH_API_KEY")
      @products.route("/")
      @login_required
      def show_products():
            counter.labels("GET","/products","product_route").inc()
            start_time=time.time()
            logger.log_text('show_products route accessed', severity='INFO')
            catalog_service_url=catalog_service_endpoint+"/products"
            request=requests.get(catalog_service_url)
            catalog=json.loads(request.content)
            response_time=time.time()-start_time
            gauge.labels("GET","/products","product_route").set(response_time)
            histogram.labels("GET","/products","product_route").observe(response_time)
            summary.labels("GET","/products","product_route").observe(response_time)
            return render_template("products.html",catalog=catalog)

      @products.route("/categories/<category>")
      @login_required
      def show_categories(category):
            counter.labels("GET","/categories","product_route").inc()
            start_time=time.time()
            logger.log_text('show_categories route accessed', severity='INFO')
            catalog_service_url=catalog_service_endpoint+f"/categories/{category}"
            request=requests.get(catalog_service_url)
            catalog=json.loads(request.content)
            response_time=time.time()-start_time
            gauge.labels("GET","/categories","product_route").set(response_time)
            histogram.labels("GET","/categories","product_route").observe(response_time)
            summary.labels("GET","/categories","product_route").observe(response_time)
            return render_template("products.html",catalog=catalog)
      @products.route("/search",methods=["POST"])
      def search_products():
            start_time=time.time()
            search_query=request.form.get("search")
            response=requests.get(product_search_endpoint+"/query",params={"query":search_query,"key":product_search_api_key})
            response_time=time.time()-start_time
            gauge.labels("GET","/categories","product_route").set(response_time)
            histogram.labels("GET","/categories","product_route").observe(response_time)
            summary.labels("GET","/categories","product_route").observe(response_time)
            print(json.loads(response.content))
            return render_template("products.html",catalog=json.loads(response.content))
            
      @products.route("/<product_id>")
      @login_required
      def get_product(product_id):
            counter.labels("GET","/product","product_route").inc()
            start_time=time.time()
            logger.log_text('get_product route accessed', severity='INFO')
            catalog_service_url=catalog_service_endpoint+f"/products/{product_id}"
            request=requests.get(catalog_service_url)
            product=json.loads(request.content)
            response_time=time.time()-start_time
            gauge.labels("GET","/product","product_route").set(response_time)
            histogram.labels("GET","/product","product_route").observe(response_time)
            summary.labels("GET","/product","product_route").observe(response_time)
            return render_template("product_info.html",product=product)
      return products
