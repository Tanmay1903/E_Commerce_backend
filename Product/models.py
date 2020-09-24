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
    product_name = fields.StringField(max_length=255)
    Description  = fields.StringField(max_length=255)
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
