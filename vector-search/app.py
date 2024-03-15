from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Annoy
from flask import Flask ,request

def convert_to_dict(doc):
       doc=doc.metadata
       jsondata={}
       jsondata["id"]=doc["id"]
       jsondata["category"]=doc["category"]
       jsondata["price"]=doc["price"]
       jsondata["product_name"]=doc["product_name"]
       return jsondata
embeddings = VertexAIEmbeddings()
db=Annoy.load_local(
    "./vikraya_ecommerce_index", embeddings=embeddings,allow_dangerous_deserialization=True
)
app=Flask(__name__)
@app.route("/")
def home():
      return {"message":"WELCOME TO LANGSEARCH VERTEX AI SEARCH","status_code":200}

@app.route("/query")

def query():
      query=db.similarity_search(request.args.get("query"),k=6)
      search_results=list(map(convert_to_dict,query))
      
      return  search_results
if(__name__=="__main__"):
      app.run()