from django.shortcuts import render,redirect

from .models import Rating
from Product.models import Products
from rest_framework_mongoengine.generics import GenericAPIView,ValidationError
from rest_framework.response import Response
from rest_framework import status
from .serializers import RatingSerializer,DeleteSerializer,GetSerializer,serobj
from Users.auth import IsAuthenticated

class User_Review(GenericAPIView):
    """
    An API that takes reviews from the Customer about the stores.
    """
    permission_classes=(IsAuthenticated,)
    serializer_class=RatingSerializer

    def get_queryset(self):
        return Rating.objects.all()

    def post(self,request):
        """
        If the ID for user review already exists then it will return following response
        "Review already given for this store! You can update it or add for some other store."
        """
        data=request.data
        ID= update(request,data)
        if ID:
            return Response({"message":"Review already given for this Product! You can update it or add for some other Product."},status=status.HTTP_409_CONFLICT)
        serializer=RatingSerializer(data=data)
        if serializer.is_valid():
            '''
            If the ID for user review Doesn't exists
            then it will tell user that there record has been stored.
            '''
            data = AvgRating(data)
            rat = serializer.create(request,data)
            return Response(rat,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

""""
Function that calculate average rating(given by customer) of a store
"""
def AvgRating(data1):
    '''
            A function which calculates Average ratings
            and return ID to particular user's review.
    '''
    data=Products.objects.get(Productid=data1['Productid'])
    if data.count==None:
        data.count=int()
    if data.OverallRating==None:
        data.OverallRating=float()

    new_rating=float(data1['UserRating'])
    data.OverallRating=(((data.count*data.OverallRating)+new_rating)/(data.count+1))
    data.count += 1
    data.save()
    return data1
'''
A Function that allows you to Update the average rating.
'''
def UpdateAvgRating(data1,old_rating):
    data=Products.objects.get(id=data1['Productid'])
    new_rating=float(data1['UserRating'])
    data.OverallRating=(((data.count*data.OverallRating)+new_rating-old_rating)/(data.count))
    data.save()
    return data1

"""
A function to return ID to particular user's review
"""
def update(request,data):
    '''
        A function which takes the UserEmail and StoreEmail
        and return ID to particular user's review.
    '''
    UserEmail=request.user.email
    Productid=data.get("Productid")
    groups=Rating.objects.all()
    for group in groups:
        if UserEmail==group['UserEmail'] and Productid==group["Productid"]:
            ID=group['Productid']
            return ID

"""
A function to update review given by customer.
Customer can make changes to his/her already given Reviews about a product through this function.
"""
class Update_Review(GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=RatingSerializer

    def get_queryset(self):
        return Rating.objects.all()

    def post(self,request):
        data=request.data
        ID= update(request,data)
        try:
            group = Rating.objects.get(id=ID)
        except:
            return Response({"message":"No Review With this Email Found"}, status=status.HTTP_204_NO_CONTENT)

        old_rating = group['UserRating']
        serializer=RatingSerializer(instance=group, data=data)
        if serializer.is_valid():
            data=UpdateAvgRating(data,old_rating)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

"""
A function to delete review given by customer.
Customer can delete his/her Review of a store
"""
class delete_Review(GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=DeleteSerializer

    def get_queryset(self):
        return Rating.objects.all()

    def post(self,request):
        data=request.data
        ID= update(request,data)
        try:
            group=Rating.objects.get(id=ID)
        except ValidationError:
            return Response({"message":"No Review With this Email Found"}, status=status.HTTP_204_NO_CONTENT)
        serializer=DeleteSerializer(instance=group,data=data)
        if serializer.is_valid():
            data=AvgRating_del(group)
            group.delete()
            return Response({"message":"Your Review has been deleted."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

'''
A Function that Update average rating after a Review has been deleted .
'''
def AvgRating_del(data1):
    data=Products.objects.get(id=data1['Productid'])
    del_rating = data1['UserRating']
    if data.count==1:
        data.OverallRating=4.0
        data.count=0
    else:
        data.OverallRating=(((data.count*data.OverallRating)-del_rating)/(data.count-1))
        data.count-=1
    data.save()
    return data1

'''
An API to Show reviews given by user about a specific Store based on their Store Email.
'''
class Get_Review(GenericAPIView):
    serializer_class=GetSerializer

    def get_queryset(self):
        return Rating.objects.all()

    def post(self,request):

            data=request.data
            Productid=data.get("Productid")
            group=[]
            x={}
            content=[]
            groups=Rating.objects.all()
            for group1 in groups:
                if Productid==group1["Productid"]:
                    group.append(group1)

            serializer=GetSerializer(instance=group,data=data)
            if serializer.is_valid():
                for group1 in group:
                    x=serobj(group1)
                    content.append(x)
                if content:
                    return Response(content,status=status.HTTP_200_OK)
                else:
                    return Response({"message":"No Review With this Email Found"},status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
