from google.cloud import firestore,logging
class userOrders:
      def __init__(self,**kwargs):
        self.userClient=firestore.Client(**kwargs)
        self.logging_client = logging.Client()
        self.logger = self.logging_client.logger('order-service')
      def create_order(self,product_id,user_id):
        user_ref=self.userClient.collection("users").document(user_id)
        product_ref=self.userClient.collection("product_catalog").document(product_id)
        order_ref=self.userClient.collection("orders").document().set({"user_ref":user_ref,"product_ref":product_ref,"status":"ready to dispatch","order_time":firestore.SERVER_TIMESTAMP})
        response={"status":200,'message':"order created successfully"}
        self.logger.log_text('Create order response: %s' % response, severity='INFO')
        return  response
      def get_product_info(self,order):
        product_ref=order._data["product_ref"]
        product_info=product_ref.get()._data
        order_formatted={**product_info,"order_id":order.id,"status":order._data["status"]}
        return order_formatted
 
      def show_orders(self,user_id):
          user_ref=self.userClient.collection("users").document(user_id)
          orders=self.userClient.collection("orders").where(filter=firestore.FieldFilter("user_ref","==",user_ref)).get()
          orders_formatted=list(map(self.get_product_info,orders))
          self.logger.log_text('Show orders response: %s' % orders_formatted, severity='INFO')
          return orders_formatted
      def cancel_order(self,order_id):
          self.userClient.collection("orders").document(order_id).delete()
          response={"status":200,"message":"ORDER CANCELED SUCCESSFULLY"}
          self.logger.log_text('Cancel order response: %s' % response, severity='INFO')
          return  response