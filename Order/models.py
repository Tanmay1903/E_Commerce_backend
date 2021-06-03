from django_mongoengine import fields,DynamicDocument

class OrderDetails(DynamicDocument):
    Useremail = fields.StringField(max_length=255)
    Productid = fields.ListField()
    Order_date = fields.StringField(max_length=100)
    Tracking_Number = fields.IntField(unique=True)
    status = fields.StringField()
    Total_Price = fields.FloatField()
    Amount_Payable = fields.FloatField()
    Shipping_Address = fields.StringField(max_length = 500)
    Payment_type = fields.StringField(max_length=100)
    Quantity = fields.IntField()

    def json(self,products):
        form_dict = {
            "Productid" : products,
            "Order_date": self.Order_date,
            "Tracking_Number": self.Tracking_Number,
            "status" : self.status,
            "Total_Price": self.Total_Price,
            "Shipping_Address": self.Shipping_Address,
            "Payment_type": self.Payment_type,
            "Quantity": self.Quantity
        }
        return form_dict


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