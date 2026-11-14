from django.urls import path
from .views import *

urlpatterns =[    path('admin-login/', admin_login_api),
              path('add_cat/', add_category),
              path('categories/', list_categories),
              path('add_food/', add_food_item),
               path('list_food/', list_food),
               path('random_foods/', random_foods),
                path('register/', register_user),
                path('login/', login_user),
                path('foods/<int:id>/', food_detail),
                path('addtocart/', add_to_cart),
                path('get_cart_items/<int:user_id>/', get_cart_items),

                path('cart/update_quantity/', update_cart_quantity),
                path('delete_cart_items/', delete_cart_items),
                path('place_order/', place_order),
                path('order/<int:user_id>/', user_orders),
                



] 
    