from flask import Flask,render_template,url_for,redirect,Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_session import Session  # Import Session
from users.user_routes import create_auth_route,User
from products.product_routes import create_products_route
from prometheus_client import Gauge,Counter,Histogram,Summary,CollectorRegistry,generate_latest, CONTENT_TYPE_LATEST
import os,redis,json,requests,time
from datetime import timedelta
app=Flask(__name__)

AUTH_SERVICE_ENDPOINT=os.getenv("AUTH_SERVICE_ENDPOINT")

app.config['SECRET_KEY'] = 'vikretha-ecommerce'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False  # Session is not permanent
app.config['SESSION_USE_SIGNER'] = True  # Secure cookies with a secret key
app.config['SESSION_KEY_PREFIX'] = 'session:'  # Prefix for storing session
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) 
app.config['SESSION_REDIS'] = redis.Redis(host=os.getenv("REDIS_SERVER_IP_ADDRESS"), port=os.getenv("REDIS_SERVER_PORT"),password=os.getenv("REDIS_SERVER_AUTH_STRING"))  

Session(app)

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)
# creating prometheus metric variables 
registry=CollectorRegistry()
counter=Counter("request_count","COUNTER METRIC SHOWING NO.OF  REQUESTS",["method","path","route"],registry=registry)
gauge=Gauge("response_time","GAUGE METRIC SHOWING AMOUNT OF TIME  TOOK BY SERVIE TO PROCESS AND SEND THE RESPONSE",["method","path","route"],registry=registry)
buckets = [0.1, 0.2, 0.5, 1.0, 2.0,3.0, 5.0]
histogram=Histogram("summary_of_response_times","SUMMARY  METRIC SHOWING SUMMARY OF  RESPONSE TIME",["method","path","route"],registry=registry,buckets=buckets)

summary=Summary("response_time_quantile","QUANTILE METRIC SHOWING QUANTILES OF RESPONSE TIME",["method","path","route"],registry=registry)


auth_route=create_auth_route(counter,gauge,histogram,summary)
app.register_blueprint(auth_route,url_prefix="/user")
products_route=create_products_route(counter,gauge,histogram,summary)
app.register_blueprint(products_route,url_prefix="/products")

@login_manager.user_loader
def load_user(user_id):
   auth_service_user_info_url=AUTH_SERVICE_ENDPOINT+"/user_info"
   response=requests.get(auth_service_user_info_url,params={"user_id":user_id})
   if(response.status_code==200):
      user_data=json.loads(response.content)
      return User(user_data["id"],user_data["name"],user_data["email"])

@app.route("/")
def home():
        return redirect(url_for("products.show_products"))
@app.route("/load")
def load():
          time.sleep(2)
          return "working"
@app.route("/metrics")
def metrics():
        return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)


if(__name__=="__main__"):
      app.run(debug=True,port=8080)