from django.shortcuts import render
from .serializers import AddcartSerializer,DeleteSerializer ,PlaceOrderSerializer
from .models import Cart,OrderDetails
from Product.models import Products
from rest_framework.response import Response
from rest_framework import status
from rest_framework_mongoengine.generics import GenericAPIView,ValidationError
from Users.auth import IsAuthenticated

class Add_to_cart(GenericAPIView):
    serializer_class = AddcartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.all()

    def post(self,request):
        data = request.data
        useremail = request.user.email
        Productid = data.get('Productid')
        q = data.get('Quantity')
        obj = Cart.objects.filter(useremail=useremail, Productid=Productid,status = 'Cart')
        if not obj:
            serializer = AddcartSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.create(request,data,'Cart'),status = status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            if int(q)>0:
                obj.update(Quantity=int(q))
            else:
                obj.delete()
            return Response({"message":"Cart Updated"},status=status.HTTP_200_OK)

def cartjson(prod,q):
    form_dict = {
        "Productid" : prod["Productid"],
        "product_name": prod["product_name"],
        "Description": prod["Description"],
        "Quantity": q,
        "Price": prod["Price"],
        "Category": prod["Category"],
        "Discount": prod["Discount"],
        "Brand": prod["Brand"],
        "Model": prod["Model"],
        "FrontPic": prod["FrontPic"],
        "BackPic": prod["BackPic"],
    }
    return form_dict

class getcart(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        useremail = request.user.email
        cart = []
        groups = Cart.objects.all()
        for group in groups:
            if group["useremail"] == useremail and group['status'] == 'Cart':
                prod = Products.objects.get(Productid= group['Productid'])
                cart.append(cartjson(prod,group["Quantity"]))
        if cart:
            return Response(cart,status = status.HTTP_200_OK)
        else:
            return Response({"message":"No Products in your cart!"},status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Cart.objects.all()

class Remove_from_cart(GenericAPIView):
    serializer_class = DeleteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.all()

    def post(self, request):
        data = request.data
        useremail = request.user.email
        Productid = data.get('Productid')
        serializer = DeleteSerializer(data = data)
        if serializer.is_valid():
            obj = Cart.objects.filter(useremail=useremail, Productid=Productid, status = 'Cart')
            if obj:
                obj.delete()
                return Response({"message":"Product removed from cart."},status=status.HTTP_200_OK)
            else:
                return Response({"message":"No product with this product id found."},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaceOrder(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaceOrderSerializer

    def get_queryset(self):
        return OrderDetails.objects.all()

    def post(self,request):
        data = request.data
        serializer = PlaceOrderSerializer(data = data)
        if serializer.is_valid():
            return Response(serializer.create(request,data,'Order Placed'),status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetMyOrders(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaceOrderSerializer

    def get_queryset(self):
        return OrderDetails.objects.all()

    def get(self,request):
        useremail = request.user.email
        orders = []
        groups = OrderDetails.objects.all()
        for group in groups:
            if group['useremail'] == useremail:
                prod = Products.objects.get(Productid=group['Productid'])
                orders.append(group)
        if orders:
            return Response(orders,status=status.HTTP_200_OK)
        else:
            return Response({"message":"You have no orders placed yet"},status =status.HTTP_204_NO_CONTENT)

class Add_to_Wishlist(GenericAPIView):
    serializer_class = AddcartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.all()

    def post(self,request):
        data = request.data
        useremail = request.user.email
        Productid = data.get('Productid')
        obj = Cart.objects.filter(useremail=useremail, Productid=Productid,status = 'Wishlist')
        if not obj:
            serializer = AddcartSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.create(request,data,'Wishlist'),status = status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Item Already in Wishlist"},status=status.HTTP_200_OK)

class getWishlist(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        useremail = request.user.email
        cart = []
        groups = Cart.objects.all()
        for group in groups:
            if group["useremail"] == useremail and group['status'] == 'Wishlist':
                prod = Products.objects.get(Productid= group['Productid'])
                cart.append(cartjson(prod,group["Quantity"]))
        if cart:
            return Response(cart,status = status.HTTP_200_OK)
        else:
            return Response({"message":"No Products in your cart!"},status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Cart.objects.all()

class Remove_from_Wishlist(GenericAPIView):
    serializer_class = DeleteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.all()

    def post(self, request):
        data = request.data
        useremail = request.user.email
        Productid = data.get('Productid')
        serializer = DeleteSerializer(data = data)
        if serializer.is_valid():
            obj = Cart.objects.filter(useremail=useremail, Productid=Productid, status = 'Wishlist')
            if obj:
                obj.delete()
                return Response({"message":"Product removed from cart."},status=status.HTTP_200_OK)
            else:
                return Response({"message":"No product with this product id found."},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)