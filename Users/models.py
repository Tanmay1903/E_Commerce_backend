from django_mongoengine import fields,Document
from datetime import datetime
import os
from django_mongoengine.mongo_auth.models import User

class CustomUser(User):
    address=fields.DictField(max_length=100,blank=True)
    phone_no=fields.StringField(blank=True)
    provider = fields.StringField(max_length=255, blank=True)
    access_token = fields.StringField(max_length=4096, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def authenticate(self, email ,password):
        email=self.email
        password=self.password
        return(email,password)

    def json(self,userid):
        form_dict= {
        "userid":userid,
        "username": self.username,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email,
        "phone_no":self.phone_no,
        "address": self.address
        }
        return form_dict
