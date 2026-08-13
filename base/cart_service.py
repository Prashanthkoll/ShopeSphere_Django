# Create this new file: cart_service.py
from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Product, AddCard, Buy
from .serializers import CartItemSerializer, BuyItemSerializer

class CartService:
    def __init__(self, user):
        self.user = user
    
    def get_cart_summary(self):
        """Get cart items count and total"""
        cart_items = AddCard.objects.filter(host=self.user)
        return {
            'count': cart_items.count(),
            'total': float(sum(item.totalprice for item in cart_items))
        }
    
    def get_buy_summary(self):
        """Get buy items total"""
        buy_items = Buy.objects.filter(host=self.user)
        return {
            'total': float(sum(item.totalprice for item in buy_items))
        }
    
    def add_to_cart(self, product_id):
        """Add product to cart"""
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = AddCard.objects.get_or_create(
            host=self.user,
            name=product.name,
            defaults={
                'category': product.category,
                'desc': product.desc,
                'price': product.price,
                'img': product.img,
                'quantity': 1,
                'totalprice': product.price
            }
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.totalprice = cart_item.price * cart_item.quantity
            cart_item.save()
        
        return cart_item
    
    def update_cart_quantity(self, item_id, action):
        """Update cart item quantity"""
        cart_item = get_object_or_404(AddCard, id=item_id, host=self.user)
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return None
        
        cart_item.totalprice = cart_item.price * cart_item.quantity
        cart_item.save()
        return cart_item
    
    def remove_from_cart(self, item_id):
        """Remove item from cart"""
        cart_item = get_object_or_404(AddCard, id=item_id, host=self.user)
        cart_item.delete()
    
    def move_to_buy_list(self, item_id):
        """Move cart item to buy list"""
        cart_item = get_object_or_404(AddCard, id=item_id, host=self.user)
        
        buy_item, created = Buy.objects.get_or_create(
            host=self.user,
            name=cart_item.name,
            defaults={
                'category': cart_item.category,
                'desc': cart_item.desc,
                'price': cart_item.price,
                'img': cart_item.img,
                'quantity': cart_item.quantity,
                'totalprice': cart_item.totalprice
            }
        )
        
        if not created:
            buy_item.quantity += cart_item.quantity
            buy_item.totalprice = buy_item.price * buy_item.quantity
            buy_item.save()
        
        cart_item.delete()
        return buy_item
    
    def update_buy_quantity(self, item_id, action):
        """Update buy item quantity"""
        buy_item = get_object_or_404(Buy, id=item_id, host=self.user)
        
        if action == 'increase':
            buy_item.quantity += 1
        elif action == 'decrease':
            buy_item.quantity -= 1
            if buy_item.quantity <= 0:
                buy_item.delete()
                return None
        
        buy_item.totalprice = buy_item.price * buy_item.quantity
        buy_item.save()
        return buy_item
    
    def remove_from_buy_list(self, item_id):
        """Remove item from buy list"""
        buy_item = get_object_or_404(Buy, id=item_id, host=self.user)
        buy_item.delete()
    
    def clear_buy_list(self):
        """Clear all buy items"""
        Buy.objects.filter(host=self.user).delete()