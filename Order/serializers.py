from rest_framework_mongoengine import serializers
from .models import OrderDetails,Cart
from datetime import datetime
import uuid

class AddcartSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = Cart
        fields = ("Productid","Quantity")

    def create(self,request, validated_data, status):
        cart_obj = Cart(
            useremail = request.user.email,
            Productid = validated_data["Productid"],
            Quantity = validated_data["Quantity"],
            status = status
        )
        cart_obj.save()
        return cart_obj.json()


class DeleteSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = Cart
        fields = ("Productid",)


class PlaceOrderSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = OrderDetails
        fields = ("Productid","Total_Price","Amount_Payable","Shipping_Address","Payment_type","Quantity")

    def create(self,request,data,status):
        order_obj = OrderDetails(
            Useremail = request.user.email,
            Productid = data['Productid'],
            Order_date = str(datetime.now()),
            Tracking_Number = uuid.uuid1().time_low,
            status = status,
            Total_Price = data['Total_Price'],
            Amount_Payable = data['Amount_Payable'],
            Shipping_Address = data['Shipping_Address'],
            Payment_type = data['Payment_type'],
            Quantity = data['Quantity']
        )
        order_obj.save()
        return order_obj
