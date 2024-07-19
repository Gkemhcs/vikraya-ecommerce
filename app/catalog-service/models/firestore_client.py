from google.cloud import firestore,logging


class Firestore:
      def __init__(self,**kwargs):
        self.client=firestore.Client(**kwargs)
        self.logging_client = logging.Client()
        self.logger = self.logging_client.logger('catalog-service')
      def to_dict(self,product):
        obj=product._data
        obj["id"]=product.id
        return obj

      def get_all(self):
        self.logger.log_text('Getting all products', severity='INFO')
        docs=self.client.collection("product_catalog").order_by("price").stream()
        catalog=list(map(self.to_dict,docs))
        return catalog
      def get_category(self,category):
          self.logger.log_text('Getting category: %s' % category, severity='INFO')
          docs=self.client.collection("product_catalog").where(filter=firestore.FieldFilter("category","==",category)).stream()
          catalog=list(map(self.to_dict,docs))
          return catalog
      def get_product_info(self,id):
          self.logger.log_text('Getting product info for id: %s' % id, severity='INFO')
          doc=self.client.collection("product_catalog").document(str(id)).get()
          product=doc._data
          product["id"]=doc.id
          return product
