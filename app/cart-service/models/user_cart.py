from google.cloud import firestore,logging
class UserCart:
      def __init__(self,**kwargs):
        self.logger = logging.Client().logger('cart-service')
        self.cartClient=firestore.Client(**kwargs)
      def check_cart(self,product_id,user_id):
           self.logger.log_text('Checking cart for user %s and product %s' % (user_id, product_id), severity='INFO')
           product=self.cartClient.collection("users").document(user_id).collection("cart").document(product_id).get()._data
         
           if(product is None):
              return True
           else:
             return False
      
      
      def add_to_cart(self,product_id,user_id):
          self.logger.log_text('Adding to cart for user %s and product %s' % (user_id, product_id), severity='INFO')
          if(self.check_cart(product_id,user_id)):
             
              product_info=self.cartClient.collection("catalog").document(product_id).get().to_dict()
            
              self.cartClient.collection("users").document(user_id).collection("cart").document(f"{product_id}").set(product_info)
              response= {"status":200,"message":"added to cart"}
          else:
            
            response= {"status":409,"message":"already present in cart"}
          self.logger.log_text('Response: %s' % response, severity='ERROR' if response['status'] > 400 else 'INFO')
          return response
      def delete_from_cart(self,product_id,user_id):
          self.logger.log_text('Deleting from cart for user %s and product %s' % (user_id, product_id), severity='INFO')
          self.cartClient.collection("users").document(user_id).collection("cart").document(product_id).delete()
       
          
          return {"status":200,"message":"deleted from cart"}
      def to_dict(self,obj):
        product=obj._data
        
        product["id"]=obj.id
        return product
      def get_cart(self,user_id):
        self.logger.log_text('Getting cart for user %s' % user_id, severity='INFO')
        products=self.cartClient.collection("users").document(user_id).collection("cart").stream()
        products=list(map(self.to_dict,products))
        return products
      def  empty_cart(self,user_id):
         self.logger.log_text('Emptying cart for user %s' % user_id, severity='INFO')
         for doc in self.cartClient.collection("users").document(user_id).collection("cart").list_documents():
              doc.delete()
         return {"message":"succesfully cleared the cart","status":200}
