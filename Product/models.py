from django_mongoengine import fields,DynamicDocument,EmbeddedDocument
from django_mongoengine.fields import EmbeddedDocumentField

class Manufact_details(EmbeddedDocument):
    Model_no = fields.StringField(max_length=200,blank = True)
    Release_date = fields.StringField(max_length=200,blank = True)
    Batch_no = fields.IntField(blank = True)

    def json(self):
        m_dict = {
        "Model_no":self.Model_no,
        "Release_date": self.Release_date,
        "Batch_no": self.Batch_no
        }
        return m_dict

class Ship_details(EmbeddedDocument):
    Weight = fields.FloatField(blank = True)
    Height = fields.FloatField(blank = True)
    Width = fields.FloatField(blank = True)
    Depth = fields.FloatField(blank = True)

    def json(self):
        s_dict = {
        "Weight":self.Weight,
        "Height": self.Height,
        "Width": self.Width,
        "Depth": self.Depth
        }
        return s_dict

class Products(DynamicDocument):
    Productid = fields.IntField(unique = True)
    product_name = fields.StringField(max_length=255)
    Description  = fields.StringField(max_length=600)
    manufacturing_details = fields.ListField(EmbeddedDocumentField(Manufact_details),blank=True)
    Shipping_details = fields.ListField(EmbeddedDocumentField(Ship_details),blank=True)
    Quantity = fields.IntField()
    Inventory_ID = fields.StringField(max_length=100)
    Price = fields.FloatField()
    Date_added = fields.StringField(max_length=255,blank=True)
    Date_modified = fields.StringField(max_length=255,default = None,blank=True)
    OverallRating = fields.FloatField(default=4.0 , blank=True)
    Category = fields.StringField(max_length = 255)
    FrontPic = fields.StringField(max_length = 255, blank = True)
    BackPic = fields.StringField(max_length = 255, blank = True)
    Images = fields.ListField(fields.StringField(),blank=True)
    Discount = fields.FloatField(blank = True)
    Brand = fields.StringField(max_length=255)
    Model = fields.StringField(max_length=255)
    OverallRating = fields.FloatField(blank = True)
    count = fields.IntField(blank = True)

    def json(self):
        form_dict = {
        "id" : str(self.id),
        "Productid" : self.Productid,
        "product_name" : self.product_name,
        "Description" : self.Description,
        "Price" : self.Price,
        "Category" : self.Category,
        "Discount" : self.Discount,
        "Brand" : self.Brand,
        "Model" : self.Model,
        "FrontPic" : self.FrontPic,
        "BackPic" : self.BackPic,
        "OverallRating": self.OverallRating,
        "manufacturing_details" : {
                                    "Model_no" : self.manufacturing_details[0]["Model_no"],
                                    "Release_date" : self.manufacturing_details[0]["Release_date"],
                                    "Batch_no" : self.manufacturing_details[0]["Batch_no"]
                                    },
        "Shipping_details" : {
                            "Weight" : self.Shipping_details[0]["Weight"],
                            "Height" : self.Shipping_details[0]["Height"],
                            "Width" : self.Shipping_details[0]["Width"],
                            "Depth" : self.Shipping_details[0]["Depth"]
                                },
        }
        return form_dict

class Analysis(DynamicDocument):
    Productid = fields.IntField()
    date_time = fields.DateTimeField()
    site = fields.StringField()
