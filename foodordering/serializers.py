from rest_framework import serializers
from .models import *

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name', 'creation_date']

class FoodSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source='category.category_name',read_only=True)
    image=serializers.ImageField(required=False)
    is_available=serializers.BooleanField(required=False,default=True)
    class Meta:
        model = food
        fields = '__all__'
class CartOrderSerializer(serializers.ModelSerializer):
    food=FoodSerializer()
    class Meta:
        model=Order
        fields=['id','food','quantity']