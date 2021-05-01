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
        fields = ("Productid","Total_Price","Shipping_Address","Payment_type","Quantity")

    def create(self,request,data,status):
        order_obj = OrderDetails(
            useremail = request.user.email,
            Productid = data['Productid'],
            Order_date = datetime.now(),
            id = uuid.uuid1(),
            status = status,
            Total_Price = data['Total_Price'],
            Shipping_Address = data['Shipping_Address'],
            Payment_type = data['Payment_type'],
            Quantity = data['Quantity']
        )
        order_obj.save()
        return order_obj
