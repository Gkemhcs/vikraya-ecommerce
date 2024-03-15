from flask import Blueprint,render_template,request,redirect,url_for,Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json,requests,os,time
from google.cloud import logging
from werkzeug.security import generate_password_hash, check_password_hash
logging_client = logging.Client()
logger = logging_client.logger('frontend_user_routes')


class User(UserMixin):
   

    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name  
        self.email = email

def create_auth_route(counter,gauge,histogram,summary):
      auth=Blueprint("users",__name__,template_folder="templates")
      AUTH_SERVICE_ENDPOINT=os.getenv("AUTH_SERVICE_ENDPOINT")
      CART_SERVICE_ENDPOINT=os.getenv("CART_SERVICE_ENDPOINT")
      ORDER_SERVICE_ENDPOINT=os.getenv("ORDER_SERVICE_ENDPOINT")
      @auth.route("/register",methods=["GET","POST"])
      def  register():
         logger.log_text('register route accessed', severity='INFO')
         auth_service_registration_url=AUTH_SERVICE_ENDPOINT+"/register"
         if(request.method=="GET"):
           return render_template("registration.html")
         if(request.method=="POST"):
               name=request.form.get("name")
               email=request.form.get("email")
               phonenumber=request.form.get("phonenumber")
               password=request.form.get("password")
               user={"name":name,"email":email,"phonenumber":phonenumber,"passwordhash":generate_password_hash(password)}
               req=requests.post(url=auth_service_registration_url,data=user)
               if(json.loads(req.content)["status"] >= 400):
                   
                 return redirect(url_for("users.login",message="USER ALREADY REGISTERED,JUST LOGIN"))
               else:
                return redirect(url_for("users.login",message="USER REGISTRATION COMPLETE,JUST LOGIN"))

      @auth.route("/login",methods=["POST","GET"])
      def login():
        logger.log_text('login route accessed', severity='INFO')
        if(request.method=="GET"):
         
          return render_template("login.html")
        if(request.method=="POST"):
            auth_service_login_url=AUTH_SERVICE_ENDPOINT+"/login"
            email=request.form.get("email")
            password=request.form.get("password")
            response=requests.post(auth_service_login_url,data={"email":email})
            user_info=json.loads(response.content)
            if(user_info["status"]==200):
               if check_password_hash(user_info['passwordhash'], password):
                  user=User(user_info['id'], user_info['name'], user_info['email'])
               
                  login_user(user)
                  return redirect(url_for("products.show_products"))
               else:
                  return redirect(url_for("users.login"))
            else:
               return redirect(url_for("users.register"))
      @auth.route("/cart/add/<product_id>",methods=["POST"])
      def add_to_cart(product_id):
         
         start_time=time.time()
         add_to_cart_url=CART_SERVICE_ENDPOINT+"/cart/add"
         response=requests.post(add_to_cart_url,data={"user_id":current_user.id,"product_id":product_id})
         response_time=time.time()-start_time
         gauge.labels("POST","/user/cart/add","user_route").set(response_time)
         histogram.labels("POST","/user/cart/add","user_route").observe(response_time)
         summary.labels("POST","/user/cart/add","user_route").observe(response_time)
         print(current_user.id,product_id)
         print(json.loads(response.content))
         return json.loads(response.content)

      @auth.route("/cart")
      @login_required
      def show_cart():
         start_time=time.time()
         logger.log_text('show cart route accessed', severity='INFO')
         cart_service_url=CART_SERVICE_ENDPOINT+"/cart"
         response=requests.get(cart_service_url,params={"user_id":current_user.id})
         response_time=time.time()-start_time
         gauge.labels("GET","/user/cart/","user_route").set(response_time)
         histogram.labels("GET","/user/cart/","user_route").observe(response_time)
         summary.labels("GET","/user/cart/","user_route").observe(response_time)
         return render_template("cart.html",products=json.loads(response.content))
      @auth.route("/cart/delete/product/<product_id>")
      @login_required
      def delete_from_cart(product_id):
         start_time=time.time()
         logger.log_text('delete route accessed', severity='INFO')
         cart_delete_service_url=CART_SERVICE_ENDPOINT+"/cart/delete"
         response=requests.post(cart_delete_service_url,data={"user_id":current_user.id,"product_id":product_id})
         response_time=time.time()-start_time
         gauge.labels("POST","/user/cart/delete/product","user_route").set(response_time)
         histogram.labels("POST","/user/cart/delete/product","user_route").observe(response_time)
         summary.labels("POST","/user/cart/delete/product","user_route").observe(response_time)
         print(response.json())

         return redirect(url_for("users.show_cart"))
      @auth.route("/cart/clear")
      @login_required
      def clear_cart():
         logger.log_text('clear cart route accessed', severity='INFO')
         cart_service_clear_url=CART_SERVICE_ENDPOINT+"/cart/clear"
         response=requests.post(cart_service_clear_url,data={"user_id":current_user.id})
         print(response.content)
         return redirect(url_for("users.show_cart"))
      @auth.route("/order/create/<product_id>")
      @login_required
      def create_order(product_id):
         start_time=time.time()
         logger.log_text('create order route accessed', severity='INFO')
         order_service__create_url=ORDER_SERVICE_ENDPOINT+"/order/create"
         response=requests.post(order_service__create_url,data={"product_id":product_id,"user_id":current_user.id})
         response_time=time.time()-start_time
         gauge.labels("GET","/user/order/create","user_route").set(response_time)
         histogram.labels("GET","/user/order/create","user_route").observe(response_time)
         summary.labels("GET","/user/order/create","user_route").observe(response_time)
         if(json.loads(response.content)["status"]==200):
            return redirect(url_for("users.show_orders"))
         else:
            return redirect(request.referrer)
      @auth.route("/orders")
      @login_required
      def show_orders():
         logger.log_text('show orders  route accessed', severity='INFO')
         order_service_url=ORDER_SERVICE_ENDPOINT+"/orders"
         response=requests.get(order_service_url,params={"user_id":current_user.id})
         return render_template("orders.html",orders=json.loads(response.content))
      @auth.route("/order/cancel/<order_id>")
      @login_required
      def cancel_order(order_id):
            start_time=time.time()
            logger.log_text('cancel order route accessed', severity='INFO')
            order_service_cancel_url=ORDER_SERVICE_ENDPOINT+"/order/cancel"
            response=requests.post(order_service_cancel_url,data={"order_id":order_id})
            response_time=time.time()-start_time
            gauge.labels("GET","/user/order/cancel","user_route").set(response_time)
            histogram.labels("GET","/user/order/cancel","user_route").observe(response_time)
            summary.labels("GET","/user/order/cancel","user_route").observe(response_time)
            if(json.loads(response.content)["status"]==200):
               return redirect(url_for("users.show_orders"))
      @auth.route('/logout')
      @login_required
      def logout():
         logger.log_text("user logged out",severity='INFO')
         logout_user()
         return redirect(url_for('users.login'))
      return auth