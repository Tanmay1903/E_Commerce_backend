from django_mongoengine import fields,Document

class Rating(Document):
    User_FirstName= fields.StringField(
        max_length=255,
    )
    User_LastName= fields.StringField(
        max_length=255,
    )
    Productid=fields.StringField(
        max_length=255,
    )
    UserEmail=fields.EmailField(
        max_length=255,
        unique=False
    )
    UserReview=fields.StringField(max_length=500)
    Review_Title=fields.StringField(max_length=500)
    UserRating=fields.FloatField()
