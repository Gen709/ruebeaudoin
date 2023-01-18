from django.urls import path
from .views import index, grocery_list_view, grocery_store_create_view, grocery_store_list_view, \
    groceryitem_delete_view, grocery_store_delete_view, grocery_store_list_update_view

urlpatterns = [
    path('', index, name='index'),
    path('wishlist/', grocery_list_view, name='wishlist'),
    path('wishlist/update/', grocery_store_list_update_view, name='wishlist-update'),
    path('store/create/', grocery_store_create_view, name='grocery-store-create'),
    path('store/list/', grocery_store_list_view, name='grocery-store-list'),
    
    path('store/delete/<int:pk>', grocery_store_delete_view, name='grocery-store-delete'),
    path('groceryitem/delete/<int:pk>/', groceryitem_delete_view, name='groceryitem-delete')
    
    ]