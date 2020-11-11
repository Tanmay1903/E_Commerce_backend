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
    Useremail = fields.StringField(max_length=255)
    Productid = fields.IntField()
    Tracking_Number = fields.IntField(unique = True)
    status = fields.StringField()

class Cart(DynamicDocument):
    useremail = fields.StringField(max_length=255)
    Productid = fields.IntField()
    Quantity = fields.IntField()

    def json(self):
        form_dict = {
            "useremail" : self.useremail,
            "Productid" : self.Productid,
            "Quantity" : self.Quantity
        }
        return form_dict