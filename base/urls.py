from django.urls import path
from . import views
urlpatterns = [
   
    path('',views.home,name='home'),
    path('cart',views.Cart,name='cart'),
    path('addcart/<int:id>',views.Addcart,name='addcart'),
    path('details/<int:id>',views.Details,name='details'),
    path('know',views.Know,name='know'),
    path('support',views.Support,name='support'),
    path('remove/<int:id>',views.Remove,name='remove'),
    path('buy/<int:id>',views.Buyproduct,name='buy'),
    path('buydelete/<int:id>',views.ByeDelete,name='buydelete'),
    path('buydeleteall',views.ByeDeleteAll,name='buydeleteall'),
    path('reduce/<int:id>',views.Reduce,name='reduce'),
    path('increse/<int:id>',views.Increse,name='increse'),
    path('reduce1/<int:id>',views.Reduce1,name='reduce1'),
    path('increse1/<int:id>',views.Increse1,name='increse1'),
    path('ch',views.Checkout,name='ch'),
    path('ch1',views.AddAddress,name='ch1'),
    path('editaddress/<int:id>',views.Edit_address,name='editaddress'),
    path('deleteaddress/<int:id>',views.Delete_address,name='deleteaddress'),
    path('payment',views.Payment_method, name='payment'),
    path('order',views.Order_view, name='order'),
    path('ordersuccess',views.OrderPlaced, name='ordersuccess'),
    # AJAX URLs
    path('add-to-cart-ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('update-quantity-ajax/', views.update_quantity_ajax, name='update_quantity_ajax'),
    path('update-buy-quantity-ajax/', views.update_buy_quantity_ajax, name='update_buy_quantity_ajax'),
    path('remove-from-cart-ajax/', views.remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path('remove-from-buy-ajax/', views.remove_from_buy_ajax, name='remove_from_buy_ajax'),
    path('buy-item-ajax/', views.buy_item_ajax, name='buy_item_ajax'),
    path('clear-buy-list-ajax/', views.clear_buy_list_ajax, name='clear_buy_list_ajax'),
]