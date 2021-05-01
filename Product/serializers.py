from rest_framework_mongoengine import serializers,generics
from .models import Products,Manufact_details,Ship_details
from datetime import datetime
from rest_framework import serializers as ser

class ManufacSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Manufact_details

class ShipSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Ship_details


class ProductsSerializer(serializers.DynamicDocumentSerializer):
    #manufacturing_details = ManufacSerializer(many = True)
    #Shipping_details = ShipSerializer(many = True)
    class Meta:
        model = Products
        fields = ("product_name","Description","Quantity","Price","Category","Discount","Brand","Model")
        depth = 2

def create(data,FP,BP):
    prod_obj = Products(
    product_name = data["product_name"],
    Description = data["Description"],
    Quantity = data["Quantity"],
    Inventory_ID = "1", #data["Inventory_ID"],
    Price = float(data["Price"]),
    Category = data["Category"],
    Discount = float(data["Discount"]),
    Brand = data["Brand"],
    Model = data["Model"]
    )
    m = Manufact_details(
    Model_no = data["Model_no"],
    Release_date = data["Release_date"],
    Batch_no = data["Batch_no"]
    )
    s = Ship_details(
    Weight = data["Weight"],
    Height = data["Height"],
    Width = data["Width"],
    Depth = data["Depth"]
    )
    prod_obj.FrontPic = FP
    prod_obj.BackPic = BP
    prod_obj.manufacturing_details.append(m)
    prod_obj.manufacturing_details.append(m)
    prod_obj.Shipping_details.append(s)
    prod_obj.Date_added = str(datetime.now())
    prod_obj.Date_modified = None
    return prod_obj

class ProductlistSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = Products
        fields = ("Productid","product_name", "Description","manufacturing_details","Shipping_details", "Price", "Category","FrontPic","BackPic", "Discount", "Brand", "Model","OverallRating")

class SearchSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = Products
        fields = ("Category",)

class SearchProductSerializer(serializers.DocumentSerializer):
    Search = ser.CharField()
    class Meta():
        model = Products
        fields = ('Search',)