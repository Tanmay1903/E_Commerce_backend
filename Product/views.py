from django.shortcuts import render
from .serializers import ProductsSerializer,create
from .models import Products,Manufact_details,Ship_details
from rest_framework.response import Response
from rest_framework import status
from rest_framework_mongoengine.generics import CreateAPIView,GenericAPIView
import uuid
from django.core.files.storage import default_storage
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
from .forms import UpdateForm
from django.http import HttpResponseRedirect
from Users.auth import IsAuthenticated
from django.contrib.auth import login,logout

class Add_Products(GenericAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Products.objects.all()

    def post(self,request):
        data = request.data
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
            create(data=data,FP = filename2, BP = filename1)
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
                if data.BackPic==None:
                    data.BackPic = unique_filename
                if data.BackPic is not  None:
                    path1 = 'back_pic/' + data.BackPic
                    default_storage.delete(path1)
                path1='back_pic/' + data.BackPic.rsplit('.', 1)[0].lower()+'.'+ext
                data.BackPic=data.BackPic.rsplit('.', 1)[0].lower()+'.'+ext
                default_storage.save(path1, ImageFile(newdoc1))
                data.save()
            if request.FILES.get('FrontPic'):
                newdoc2 = request.FILES['FrontPic']
                ext = str(newdoc2).rsplit('.', 1)[1].lower()
                if data.FrontPic==None:
                    data.FrontPic = unique_filename
                if data.FrontPic is not  None:
                    path2 = 'front_pic/' + data.FrontPic
                    default_storage.delete(path2)
                path2 = 'front_pic/' + data.FrontPic.rsplit('.', 1)[0].lower()+'.' + ext
                data.FrontPic = data.FrontPic.rsplit('.', 1)[0].lower() + '.' + ext
                default_storage.save(path2, ImageFile(newdoc2))
                data.save()
            create(data=data1, FP = data.FrontPic, BP = data.BackPic)
            data.delete()
            return Response({"message":"Product updated successfully"},status=status.HTTP_201_CREATED)
        context = {'data': data.json()}
        return render(request, 'Product/update_products.html', context)

def update_product(request,a):
    data = Products.objects.get(id=a)
    context = {'data': data.json()}
    return render(request, 'Product/update_products.html', context)

permission_classes = (IsAuthenticated)
def user_logout(request):
    '''
    A simple logout function for the staff memebers(crm users)
    to logout themselves
    '''
    logout(request)

    return render(request,'Product/index.html')
