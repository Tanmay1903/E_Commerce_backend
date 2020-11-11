from rest_framework_mongoengine import serializers
from .models import OrderDetails,Order,Cart
from datetime import datetime

class AddcartSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = Cart
        fields = ("Productid","Quantity")

    def create(self,request, validated_data):
        cart_obj = Cart(
            useremail = request.user.email,
            Productid = validated_data["Productid"],
            Quantity = validated_data["Quantity"]
        )
        cart_obj.save()
        return cart_obj.json()


class DeleteSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = Cart
        fields = ("Productid",)