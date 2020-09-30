from django_mongoengine.forms import DocumentForm
from django.forms import FileField, Form, CharField, IntegerField, FloatField,ImageField, ChoiceField, ModelForm
from .models import Products

class UpdateForm(DocumentForm):
    BackPic = ImageField(required=False)
    FrontPic = ImageField(required=False)
    Model_no = CharField(max_length = 200,required=False)
    Release_date = CharField(max_length = 200,required=False)
    Batch_no = IntegerField(required = False)
    Weight = FloatField(required = False)
    Height = FloatField(required = False)
    Width = FloatField(required = False)
    Depth = FloatField(required = False)
    class Meta():
        document=Products
        fields = ("product_name","Description","Quantity","FrontPic","BackPic","Price","Category","Discount","Brand","Model","Model_no","Release_date","Batch_no","Weight","Height","Width","Depth")
