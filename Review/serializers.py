from rest_framework_mongoengine import serializers,generics
from django_mongoengine import fields
from .models import Rating

'''This serializer class is used to create a User Rating
and store it in the database'''
class RatingSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Rating
        fields = ('Productid','Review_Title','UserReview','UserRating')

    '''This function is used to create a Rating object
    and store it in the database'''
    def create(self,request,data):
        rat_obj = Rating(
        Productid = data.get('Productid'),
        Review_Title = data.get('Review_Title'),
        UserReview = data.get('UserReview'),
        UserRating = data.get('UserRating'),
        UserEmail = request.user.email,
        User_FirstName = request.user.first_name,
        User_LastName = request.user.last_name
        ).save()
        return serobj(rat_obj)

'''This serializer class is used to delete the User Rating
already stored it in the database'''
class DeleteSerializer(serializers.DocumentSerializer):
    class Meta:
        model= Rating
        fields = ('Productid',)

'''This serializer class is used to get all the User Ratings
for a particular store stored in the database'''
class GetSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Rating
        fields= ('Productid',)

'''This function is used to convert rating object in json form'''
def serobj(validated_data):

    jsondata = {

    "User_FirstName" : validated_data['User_FirstName'],
    "User_LastName" : validated_data['User_LastName'],
    "Productid" : validated_data['Productid'],
    "UserEmail" : validated_data['UserEmail'],
    "Review_Title" : validated_data['Review_Title'],
    "UserReview" : validated_data['UserReview'],
    "UserRating" : validated_data['UserRating'],
    }

    return jsondata
