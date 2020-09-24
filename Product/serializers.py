from rest_framework_mongoengine import serializers,generics
from .models import Products,Manufact_details,Ship_details
from datetime import datetime
import json

class ManufacSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Manufact_details

class ShipSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Ship_details


class ProductsSerializer(serializers.DynamicDocumentSerializer):
    manufacturing_details = ManufacSerializer(many = True)
    Shipping_details = ShipSerializer(many = True)
    class Meta:
        model = Products
        fields = ("product_name","Description","manufacturing_details","Shipping_details","Quantity","Inventory_ID","Price","Category","Discount","Brand","Model")
        depth = 2

    def create(self,data):
        prod_obj = Products(
        product_name = data["product_name"],
        Description = data["Description"],
        Quantity = data["Quantity"],
        Inventory_ID = data["Inventory_ID"],
        Price = data["Price"],
        Category = data["Category"],
        Discount = data["Discount"],
        Brand = data["Brand"],
        Model = data["Model"]
        )
        m = Manufact_details(
        Model_no = data["manufacturing_details"][0]["Model_no"],
        Release_date = data["manufacturing_details"][0]["Release_date"],
        Batch_no = data["manufacturing_details"][0]["Batch_no"]
        )
        s = Ship_details(
        Weight = data["Shipping_details"][0]["Weight"],
        Height = data["Shipping_details"][0]["Height"],
        Width = data["Shipping_details"][0]["Width"],
        Depth = data["Shipping_details"][0]["Depth"]
        )
        prod_obj.manufacturing_details.append(m)
        prod_obj.Shipping_details.append(s)
        prod_obj.Date_added = str(datetime.now())
        prod_obj.Date_modified = None
        prod_obj.save()
        return data
