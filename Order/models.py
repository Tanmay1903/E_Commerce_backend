from django_mongoengine import fields,DynamicDocument

class OrderDetails(DynamicDocument):
    Useremail = fields.StringField(max_length=255)
    Productid = fields.IntField()
    Order_date = fields.StringField(max_length=100)
    Tracking_Number = fields.StringField(unique=True)
    status = fields.StringField()
    Total_Price = fields.FloatField()
    Shipping_Address = fields.StringField(max_length = 500)
    Payment_type = fields.StringField(max_length=100)
    Quantity = fields.IntField()


class Cart(DynamicDocument):
    useremail = fields.StringField(max_length=255)
    Productid = fields.IntField()
    Quantity = fields.IntField()
    status = fields.StringField()

    def json(self):
        form_dict = {
            "useremail" : self.useremail,
            "Productid" : self.Productid,
            "Quantity" : self.Quantity,
            "status" : self.status
        }
        return form_dict