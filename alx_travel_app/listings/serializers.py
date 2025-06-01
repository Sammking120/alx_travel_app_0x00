from rest_framework import serializers
from .models import Listing, Booking
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ListingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'owner', 'title', 'description', 'address', 'city', 'country',
            'price_per_night', 'max_guests', 'bedrooms', 'bathrooms',
            'created_at', 'updated_at', 'is_active', 'average_rating'
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return None

class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), source='listing', write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_id', 'guest', 'check_in', 'check_out',
            'total_price', 'status', 'created_at', 'updated_at'
        ]

    def validate(self, attrs):
        if attrs['check_out'] <= attrs['check_in']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return attrs