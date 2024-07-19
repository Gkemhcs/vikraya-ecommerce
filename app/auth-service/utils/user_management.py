from google.cloud import firestore,logging

class User:
     def __init__(self,**kwargs):
        self.client=firestore.Client(**kwargs)
        self.logger = logging.Client().logger('auth-service')
     def validate_registration(self,email):
       
        self.logger.log_text('Validating registration for email %s' % email, severity='INFO')
        if(len(self.client.collection("users").where(filter=firestore.FieldFilter("email","==",email)).get())!=0):
            return False
        else: 
            return True

     def validate_login(self,email):
        self.logger.log_text('Validating login for email %s' % email, severity='INFO')
        docs=self.client.collection("users").where(filter=firestore.FieldFilter("email","==",email)).get()
        if(len(docs)!=0):
             user=docs[0]
             user_info=user._data
             user_info["id"]=user.id
             response=user_info
             response["status"]=200
        else:
           response={"status":400}
        return response
     def register(self,name,email,phonenumber,passwordhash):
        self.logger.log_text('Registering user with email %s' % email, severity='INFO')
        if self.validate_registration(email):
          doc=self.client.collection("users").document().set({"name":name,"email":email,"phonenumber":phonenumber,"passwordhash":passwordhash})
          return {"status":200,"message":"user succesfully created"}
        else:
              return {"status":404,"message":"user already exists"} 
                      
     def  user_info(self,user_id):
         doc=self.client.collection("users").document(user_id).get()
         user_info=doc._data 
         user_info["id"]=doc.id
         return  user_info
           
          
