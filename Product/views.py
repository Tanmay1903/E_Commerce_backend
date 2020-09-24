from django.shortcuts import render
from .serializers import ProductsSerializer
from .models import Products
from rest_framework.response import Response
from rest_framework import status
from rest_framework_mongoengine.generics import CreateAPIView,GenericAPIView

class Add_Products(GenericAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Products.objects.all()

    def post(self,request):
        data = request.data
        print(data)
        serializer = ProductsSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.create(data),status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
