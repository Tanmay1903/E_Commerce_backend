from django.contrib import messages
from django.shortcuts import render
from .serializers import ProductsSerializer,create, ProductlistSerializer, SearchSerializer, SearchProductSerializer
from .models import Products,Analysis
from rest_framework.response import Response
from rest_framework import status
from rest_framework_mongoengine.generics import GenericAPIView,ValidationError
import uuid
from django.core.files.storage import default_storage
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from Users.auth import IsAuthenticated
from django.contrib.auth import login,logout
from django.shortcuts import redirect
from django_mongoengine.mongo_auth.managers import get_user_document
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

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


class get_product(GenericAPIView):

    def get(self,request,a):
        prod = Products.objects.get(Productid = int(a))
        if prod:
            return Response(prod.json(),status=status.HTTP_200_OK)
        else:
            return Response("No Product with this productid Found",status=status.HTTP_400_BAD_REQUEST)

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

class Search_product(GenericAPIView):
    serializer_class = SearchSerializer
    def get_queryset(self):
        return Products.objects.all()

    def post(self,request):
        data = request.data
        Category = data.get("Category")
        content = []
        serializer = SearchSerializer(data = data)
        if serializer.is_valid():
            groups = Products.objects.all()
            for group in groups:
                if group['Category'] == Category:
                    content.append(group.json())
            if content:
                return Response(content,status = status.HTTP_200_OK)
            else:
                return Response("No Products in this Category Found", status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

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

class searchproduct(GenericAPIView):
    serializer_class = SearchProductSerializer

    def get_queryset(self):
        return Products.objects.all()

    def post(self, request):
        data = request.data
        print(data)
        search = request.data.get('Search')
        import re
        serializer = SearchProductSerializer(data=data)
        if serializer.is_valid():
            try:
                loc = {"product_name": re.compile(search, re.IGNORECASE)}
                loc1 = {"Category": re.compile(search, re.IGNORECASE)}
                groups = Products._get_collection()
                y = groups.find(loc)
                z = groups.find(loc1)
                y = list(y)
                y.extend(list(z))
                res = []
                for i in y:
                    del (i['_id'])
                    if i not in res:
                        res.append(i)
                if res:
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "No Products Found"}, status=status.HTTP_204_NO_CONTENT)
            except ValidationError as e:
                return Response("Something Went Wrong", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

def return_driver():
    from pyvirtualdisplay import Display
    from selenium import webdriver
    from fake_useragent import UserAgent
    display = Display(visible=0, size=(800, 600))
    display.start()

    chrome_options = webdriver.ChromeOptions()
    ua = UserAgent()
    userAgent = ua.random
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument(f'user-agent={userAgent}')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome()

    return driver

def create_dict(name,price,percentage,accuracy):
    form_dict = {
        "Name" : name,
        "Price" : price,
        "Percentage" : percentage,
        "Accuracy" : accuracy
    }
    return form_dict

def check(a,site):
    try:
        prod = Analysis.objects.all()
        print(site)
        for i in prod:
            if i['site'] == site and i['Productid'] == int(a):
                print(i['site'])
                datetime_now = datetime.now(timezone.utc)
                diff = (datetime_now - i['date_time']).total_seconds() / 60
                print(diff)
                if diff < 10080:
                    return i["Analysis_Result"]
                else:
                    prod.delete()
                    return {}
        return {}
    except:
        return {}

class Sentiment_Analysis_Amazon(GenericAPIView):

    def get(self,request,a):
        prod = Products.objects.get(Productid=int(a))
        name = prod['product_name']
        dict = check(int(a),site = "Amazon")
        if dict:
            return Response(dict,status=status.HTTP_200_OK)
        else:
            driver = return_driver()

            df = pd.DataFrame([], columns=list(['Titles']))
            import Product.clean_review as ct
            dfx = pd.read_csv("amazonReviews.csv")  # to remove 'nan'
            dfx.dropna(subset=['reviews.rating'], inplace=True)

            # to remove integer values
            # In the regular expression \d stands for "any digit" and + stands for "one or more".
            dfx['reviews.title'] = dfx['reviews.title'].str.replace('\d+', ' ')

            x = dfx['reviews.title'].tolist()
            y = dfx["reviews.rating"].tolist()

            y = np.array(y)

            for i in range(0, 1177):
                if y[i] > 3:
                    y[i] = 1
                else:
                    y[i] = 0

            x_clean = [ct.getStemmedReview(i) for i in x]
            cv = CountVectorizer()
            x_vec = cv.fit_transform(x_clean).toarray()
            mnb = MultinomialNB()
            mnb.fit(x_vec, y)  # Training

            driver.get("https://www.amazon.in/")
            value = driver.find_element_by_xpath('//*[@id="nav-link-accountList"]/div/span').text
            '''
            #time.sleep(5)
            search = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(name)
            #time.sleep(4)
            ent = driver.find_element_by_xpath('//*[@id="nav-search-submit-text"]/input').click()
            time.sleep(5)
            try:
                try:
                    ent = driver.find_element_by_xpath('//*[@class="a-size-medium a-color-base a-text-normal"]').click()
                except:
                    ent = driver.find_element_by_xpath('//*[@class="a-size-base-plus a-color-base a-text-normal"]').click()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[-1])
                #time.sleep(2)
                amaz_name = driver.find_element_by_xpath('//*[@id="productTitle"]').text
                amaz_price = driver.find_element_by_xpath('//*[@class="a-span12"]/span[1]').text
                ent = driver.find_element_by_xpath('//*[@id="reviews-medley-footer"]/div[2]/a').click()
                time.sleep(2)
                titles = []
                while len(titles) < 10:
                    values = driver.find_elements_by_xpath('//*[@class="a-row"]/a/span')
                    for i in values:
                        titles.append(i.text)
                        df1 = pd.DataFrame({"Titles": [i.text]})
                        df = pd.concat([df, df1])
                    try:
                        ent = driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
                        #time.sleep(5)
                    except:
                        break
            except:
                driver.quit()
                return Response({"message": "Oops! Something went Wrong! Check your Internet Connection."},
                                status=status.HTTP_409_CONFLICT)
            if df.empty:
                data = {"Amazon": {"message": "Not Enough Reviews for Analysis Found!"}}
            else:
                dfxt = df
                x_test = dfxt["Titles"]
                xt_clean = [ct.getStemmedReview(i) for i in x_test]

                ## Vectorization on the test set
                xt_vec = cv.transform(xt_clean).toarray()
                cv.get_feature_names()
                overall = np.array(mnb.predict(xt_vec))
                overall = np.average(overall)
                Percentage = (overall * 100)
                Accuracy = mnb.score(x_vec, y)
                data = {"Amazon": create_dict(amaz_name, amaz_price, Percentage, Accuracy)}
            driver.quit()

            Analysis(
                Productid=int(a),
                date_time=datetime.now(timezone.utc),
                site = "Amazon",
                Analysis_Result=data
            ).save()
            '''
            return Response(value, status=status.HTTP_200_OK)

class Sentiment_Analysis_Flipkart(GenericAPIView):

    def get(self,request,a):
        prod = Products.objects.get(Productid=int(a))
        name = prod['product_name']
        dict = check(int(a),site = "Flipkart")
        if dict:
            return Response(dict,status=status.HTTP_200_OK)
        else:
            driver = return_driver()
            df = pd.DataFrame([], columns=list(['Titles']))
            import Product.clean_review as ct
            dfx = pd.read_csv("amazonReviews.csv")  # to remove 'nan'
            dfx.dropna(subset=['reviews.rating'], inplace=True)

            # to remove integer values
            # In the regular expression \d stands for "any digit" and + stands for "one or more".
            dfx['reviews.title'] = dfx['reviews.title'].str.replace('\d+', ' ')

            x = dfx['reviews.title'].tolist()
            y = dfx["reviews.rating"].tolist()

            y = np.array(y)

            for i in range(0, 1177):
                if y[i] > 3:
                    y[i] = 1
                else:
                    y[i] = 0

            x_clean = [ct.getStemmedReview(i) for i in x]
            cv = CountVectorizer()
            x_vec = cv.fit_transform(x_clean).toarray()
            mnb = MultinomialNB()
            mnb.fit(x_vec, y)
            driver.get("https://www.flipkart.com/")
            time.sleep(5)
            try:
                ent = driver.find_element_by_xpath('/html/body/div[2]/div/div/button').click()
                time.sleep(2)
            except:
                pass
            search = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input').send_keys(name)
            time.sleep(4)
            ent = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/button').click()
            time.sleep(5)
            try:
                try:
                    ent = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[1]/div[1]').click()
                except:
                    ent = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div/a[2]').click()
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                flip_name = driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span').text
                flip_price = driver.find_element_by_xpath('//*[@class="_30jeq3 _16Jk6d"]').text
                try:
                    ent = driver.find_element_by_xpath('//*[@class="_3UAT2v _16PBlm"]/span').click()
                except:
                    pass
                time.sleep(5)
                titles = []
                while len(titles) < 10:
                    values = driver.find_elements_by_class_name("_2-N8zT")
                    for i in values:
                        titles.append(i.text)
                        df1 = pd.DataFrame({"Titles": [i.text]})
                        df = pd.concat([df, df1])
                    try:
                        ent = driver.find_elements_by_xpath('//*[@class="_1LKTO3"]')
                        ent[-1].click()
                        time.sleep(5)
                    except:
                        break
            except:
                driver.quit()
                return Response({"message": "Oops! Something went Wrong! Check your Internet Connection."},
                                status=status.HTTP_409_CONFLICT)
            if df.empty:
                data={"Flipkart":  {"message": "Not Enough Reviews for Analysis Found!"}}
            else:
                dfxt = df
                x_test = dfxt["Titles"]
                xt_clean = [ct.getStemmedReview(i) for i in x_test]
                xt_vec = cv.transform(xt_clean).toarray()
                cv.get_feature_names()
                overall = np.array(mnb.predict(xt_vec))
                overall = np.average(overall)
                Percentage = (overall * 100)
                Accuracy = mnb.score(x_vec, y)
                data= {'Flipkart': create_dict(flip_name, flip_price, Percentage, Accuracy)}

            driver.quit()

            Analysis(
                Productid=int(a),
                date_time=datetime.now(timezone.utc),
                site = "Flipkart",
                Analysis_Result=data
            ).save()
            return Response(data, status=status.HTTP_200_OK)
