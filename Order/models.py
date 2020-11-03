from django_mongoengine import fields,DynamicDocument

class OrderDetails(DynamicDocument):
    Order_date = fields.StringField(max_length=100)
    Orderid = fields.StringField(max_length=100)
    Total_Price = fields.FloatField()
    Shipping_Address = fields.StringField(max_length = 500)
    Payment_type = fields.StringField(max_length=100)
    Quantity = fields.IntField()
    Price = fields.FloatField()

class Order(DynamicDocument):
    Userid = fields.StringField(max_length=255)
    ProductID = fields.IntField(max_length=255)
    Tracking_Number = fields.IntField(unique = True)
    status = fields.StringField()