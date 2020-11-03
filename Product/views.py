from django.contrib import messages
from django.shortcuts import render
from .serializers import ProductsSerializer,create, ProductlistSerializer
from .models import Products,Manufact_details,Ship_details
from rest_framework.response import Response
from rest_framework import status
from rest_framework_mongoengine.generics import GenericAPIView
import uuid
from django.core.files.storage import default_storage
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from Users.auth import IsAuthenticated
from django.contrib.auth import login,logout
from django.shortcuts import redirect
from django_mongoengine.mongo_auth.managers import get_user_document

User = get_user_document()

class Add_Products(GenericAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Products.objects.all()

    def post(self,request):
        data = request.data
        id = uuid.uuid1()
        serializer = ProductsSerializer(data=data)
        if serializer.is_valid():
            unique_filename = str(uuid.uuid4())
            filename1=''
            filename2=''
            if request.FILES.get('BackPic'):
                newdoc1 = request.FILES['BackPic']
                ext = str(newdoc1).rsplit('.', 1)[1].lower()
                filename1 = unique_filename + '.' + ext
                path1 = 'back_pic/' + filename1
                default_storage.save(path1, ImageFile(newdoc1))
            if request.FILES.get('FrontPic'):
                newdoc2 = request.FILES['FrontPic']
                ext = str(newdoc2).rsplit('.', 1)[1].lower()
                filename2 = unique_filename + '.' + ext
                path2 = 'front_pic/' + filename2
                default_storage.save(path2, ImageFile(newdoc2))
            prod_obj = create(data=data,FP = filename2, BP = filename1)
            prod_obj.Productid = id.time_low
            prod_obj.OverallRating = 4.0
            prod_obj.count = 0
            prod_obj.save()
            return Response({"message":"Product uploaded successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

def welcome(request):
    if request.session._session:
        data=Products.objects.all()
        context={'data':data}
        return render(request,"Product/crm.html",context)
    else:
        return render(request,'Product/index.html')

class UpdateProduct(GenericAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Products.objects.all()

    def post(self,request,a):
        data = Products.objects.get(id=a)
        data1 = request.data
        unique_filename = str(uuid.uuid4())
        form = ProductsSerializer(data=data1,instance=data)
        if form.is_valid():
            if request.FILES.get('BackPic'):
                newdoc1 = request.FILES['BackPic']
                ext = str(newdoc1).rsplit('.', 1)[1].lower()
                if not data.BackPic:
                    data.BackPic = unique_filename
                if data.BackPic :
                    path1 = 'back_pic/' + data.BackPic
                    default_storage.delete(path1)
                path1='back_pic/' + data.BackPic.rsplit('.', 1)[0].lower()+'.'+ext
                data.BackPic=data.BackPic.rsplit('.', 1)[0].lower()+'.'+ext
                default_storage.save(path1, ImageFile(newdoc1))
                data.save()
            if request.FILES.get('FrontPic'):
                newdoc2 = request.FILES['FrontPic']
                ext = str(newdoc2).rsplit('.', 1)[1].lower()
                if not data.FrontPic:
                    data.FrontPic = unique_filename
                if data.FrontPic:
                    path2 = 'front_pic/' + data.FrontPic
                    default_storage.delete(path2)
                path2 = 'front_pic/' + data.FrontPic.rsplit('.', 1)[0].lower()+'.' + ext
                data.FrontPic = data.FrontPic.rsplit('.', 1)[0].lower() + '.' + ext
                default_storage.save(path2, ImageFile(newdoc2))
                data.save()
            prod_obj = create(data=data1, FP = data.FrontPic, BP = data.BackPic)
            prod_obj.Productid = data['Productid']
            prod_obj.OverallRating = data['OverallRating']
            prod_obj.count = data['count']
            data.delete()
            prod_obj.save()
            return Response({"message":"Product updated successfully"},status=status.HTTP_201_CREATED)
        context = {'data': data.json()}
        return render(request, 'Product/update_products.html', context)

def update_product(request,a):
    data = Products.objects.get(id=a)
    context = {'data': data.json()}
    return render(request, 'Product/update_products.html', context)

class product_list(GenericAPIView):

    def get(self, request):
        prod = Products.objects.all()
        serializer = ProductlistSerializer(prod,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def get_queryset(self):
        return Products.objects.all()

permission_classes = (IsAuthenticated)
def user_logout(request):
    '''
    A simple logout function for the staff memebers(crm users)
    to logout themselves
    '''
    logout(request)

    return render(request,'Product/index.html')

def user_login(request):
    '''
    A simple login function for the staff memebers(crm users)
    to login themselves.
    '''
    if request.method=="POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.is_active and user.is_staff:
                    user.backend = 'django_mongoengine.mongo_auth.backends.MongoEngineBackend'
                    login(request, user,backend=user.backend)
                    return redirect('../security/crm')
            else:
                messages.error(request,"Invalid Email or Password!")
                return render(request,'Product/index.html')
        except User.DoesNotExist:
            messages.warning(request,"Invalid Credentials!")
            return render(request,'Product/index.html')

    else:

        return render(request, 'Product/index.html')

def search(request):
    search_query = request.GET.get('search_box')
    import re
    try:
        loc={"product_name": re.compile(search_query, re.IGNORECASE)}
        loc1={"Category":re.compile(search_query,re.IGNORECASE)}
        groups=Products._get_collection()
        y=groups.find(loc)
        z=groups.find(loc1)
        y = list(y)
        z=list(z)
        for i in y:
            i["id"] = i["_id"]
        for i in z:
            i["id"] = i["_id"]
        y.extend(z)
        res = []
        for i in y:
            if i not in res:
                res.append(i)
        if res :
            return render(request,"Product/crm.html",{"data":res})
        else:
            return HttpResponse('No Product Found.')
    except:
        return HttpResponse("No Product Found.")



@login_required()
def delete_product(request, a):
    '''
    A function which allows the staff memebers(crm users)
    to delete the existing store data
    and then redirects to the crm page.
    '''
    order = Products.objects.get(id=a)
    if request.method == "POST":
        if order.BackPic:
            path1 = 'back_pic/' + order.BackPic
            default_storage.delete(path1)
        if order.FrontPic:
            path2 = 'front_pic/' + order.FrontPic
            default_storage.delete(path2)
        order.delete()
        return redirect('../security/crm')
    context = {'item': order}
    return render(request, 'Product/delete.html', context)

class DeleteFrontPic(GenericAPIView):

    def post(self,request):
        data=request.data
        id=request.data.get('obj_id')
        obj = Products.objects.get(pk=id)
        if obj.FrontPic == "":
            return Response({'message':'No Front Picture Found!'},status=status.HTTP_200_OK)
        else:
            path1 = 'front_pic/' + obj.FrontPic
            default_storage.delete(path1)
            del obj.FrontPic
            obj.FrontPic = ""
            obj.save()
            return Response({'message': 'Front Picture Deleted'}, status=status.HTTP_200_OK)
        return Response({'message':'Invalid ID'},status=status.HTTP_400_BAD_REQUEST)

class DeleteBackPic(GenericAPIView):

    def post(self,request):
        data=request.data
        id=request.data.get('obj_id')
        obj = Products.objects.get(pk=id)
        if obj.BackPic == "":
            return Response({'message':'No Back Picture Found!'},status=status.HTTP_200_OK)
        else:
            path1 = 'back_pic/' + obj.BackPic
            default_storage.delete(path1)
            del obj.BackPic
            obj.BackPic = ""
            obj.save()
            return Response({'message': 'Back Picture Deleted'}, status=status.HTTP_200_OK)
        return Response({'message':'Invalid ID'},status=status.HTTP_400_BAD_REQUEST)
