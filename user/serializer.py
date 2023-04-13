from rest_framework import serializers

from user.models import User, UserRating, UserInterest, FreelancerInterest


class UserDataSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username', 'name', 'user_image', 'phone', 'address', 'is_verified']


class UserNameSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name','user_image']


class Rating(serializers.ModelSerializer):
    rating_giver = UserNameSerial(read_only=True, many=False)

    class Meta:
        model = UserRating
        fields = ['rating_giver', 'rating', 'review']


class InterestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'


class FreelancerSerializer(serializers.ModelSerializer):
    interests = InterestDataSerializer(read_only=True, many=True)

    class Meta:
        model = FreelancerInterest
        fields = ['id', 'interests']
