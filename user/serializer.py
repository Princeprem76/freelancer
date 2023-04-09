from rest_framework import serializers

from user.models import User, UserRating, UserInterest, FreelancerInterest


class UserDataSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'user_image', 'phone', 'address', 'is_verified']


class Rating(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['rating_giver.username', 'rating', 'review']


class InterestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'


class FreelancerSerializer(serializers.ModelSerializer):
    interests = InterestDataSerializer(read_only=True, many=True)

    class Meta:
        model = FreelancerInterest
        fields = ['interests']
