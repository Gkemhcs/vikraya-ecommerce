from google.cloud import firestore
import json 
db=firestore.Client("vikraya-ecommerce",database="vikraya-ecommerce")
with open("new-local-catalog.json") as file:
      data=file.read()
json_catalog=json.loads(data)["data"]
id=100
batch=db.batch()
for product in json_catalog:
      doc=db.collection("product_catalog").document(f"product-{id+1}")
      id+=1
      batch.set(doc,product)
batch.commit()
print("DATA IMPORTED SUCCESSFULLY")
