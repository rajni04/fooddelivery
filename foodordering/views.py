from django.shortcuts import render
from rest_framework.decorators import api_view,parser_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .models import *
from .serializers import *
import random
from django.db.models import Q
from django.contrib.auth.hashers import check_password


from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
@api_view(['POST'])
# Create your views here.
def admin_login_api(request):
    username=request.data.get('username')
    password=request.data.get('password')
    user=authenticate(username=username, password=password)
    if user is not None and user.is_staff:
        return Response({"message":"Login successful","username":username}, status=200)

    return Response({"message":"Invalid credentials"}, status=401)

@api_view(['POST'])
def add_category(request):
    category_name=request.data.get('category_name')
    Category.objects.create(category_name=category_name)
    return Response({"message":"Category created successful","category":category_name}, status=201)

@api_view(['GET'])
def list_categories(request):
    categories=Category.objects.all()
    serializer=categorySerializer(categories, many=True)
    return Response(serializers.data)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_food_item(request):
    serializers=FoodSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response({"message":"Food created successful"}, status=201)
    return Response({"message":"Something went wrong"}, status=400)

@api_view(['GET'])
def list_food(request):
    foods=food.objects.all()
    serializer=FoodSerializer(foods, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def food_search(request):
    query=request.GET.get('q','')
    foods=food.objects.filter(item_name__icontains=query)
    serializer=FoodSerializer(foods, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def random_foods(request):
    foods=list(food.objects.all())
    random.shuffle(foods)
    limited_food=foods[0:9]
    serializers=FoodSerializer(limited_food, many=True)
    return Response(serializers.data)


@api_view(['POST'])
def register_user(request):
    firstname=request.data.get('firstname')
    lastname=request.data.get('lastname')
    mobile=request.data.get('mobile_num')
    eml=request.data.get('email')
    passw=request.data.get('password')

    if User.objects.filter(email=eml).exists() or User.objects.filter(mobile=mobile).exists():
        return Response({"message":"Email or mobile already exists"}, status=400)

    User.objects.create(first_name=firstname,last_name=lastname,email=eml,mobile=mobile,password=make_password(passw))
    return Response({"message":"Successfully created user"}, status=201)
@api_view(['POST'])
def login_user(request):
    identifier=request.data.get('emailcont')
    password=request.data.get('password')

    try:
        user=User.objects.get(Q(email=identifier)|Q(moile=identifier))
        if check_password(password=user.password):
            return Response({"message":"Login successful", "userId":user.id,"username":f"{user.first_name}{user.last_name}"}, status=200)
        else:
            return Response({"message":"Invalid credentials"}, status=401)

    except:
            return Response({"message":"Invalid credentials"}, status=401)


@api_view(['GET'])
def food_detail(request, id):
    f=food.objects.get(id=id)
    print(food)
    
    serializers=FoodSerializer(f)
    return Response(serializers.data)

@api_view(['POST'])
def add_to_cart(request):
    user_id=request.data.get('userID')
    food_id=request.data.get('foodID')
    try:
        user=User.objects.get(id=user_id)
        f=food.objects.get(id=food_id)
        order, created=Order.objects.get_or_create(
            user=user,
            food=f,
            is_order_placed=False,
            defaults={'quantity':1}


        )
        if not created:
            order.quantity+=1
            order.save()
        return Response({"message":"food added to cart"}, status=200)

    except:
        return Response({"message":"Something went wrong"}, status=401)

@api_view(['GET'])

def get_cart_items(request, user_id):
    orders=Order.objects.filter(user_id=user_id,is_order_placed=False).select_related('food')
    serializers=CartOrderSerializer(orders, many=True)
    return Response(serializers.data)

@api_view(['PUT'])
def update_cart_quantity(request):
    order_id=request.data.get('orderID')
    quantity=request.data.get('quantity')
    try:

        order=Order.objects.get(id=order_id, is_order_placed=False)
        order.quantity=quantity
        return Response({"message","quantity updated"}, status=200)
    except:
        return Response({"message":"something went wrong"}, status =404)


@api_view(['DELETE'])
def delete_cart_items(request):
    order_id=request.data.get('orderID')
    try:

        order=Order.objects.get(id=order_id, is_order_placed=False)
        order.delete()
        return Response({"message","order deleted"}, status=200)
    except:
        return Response({"message":"something went wrong"}, status =404)


