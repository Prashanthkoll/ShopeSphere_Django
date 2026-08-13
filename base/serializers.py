# Create this new file: serializers.py
from rest_framework import serializers
from .models import Product, AddCard, Buy, Address

class ProductSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'desc', 'price', 'img_url', 'sale', 'trending']
    
    def get_img_url(self, obj):
        if obj.img:
            return obj.img.url
        return '/media/default.png'

class CartItemSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    price_float = serializers.SerializerMethodField()
    totalprice_float = serializers.SerializerMethodField()
    
    class Meta:
        model = AddCard
        fields = ['id', 'category', 'name', 'desc', 'price', 'price_float', 'img_url', 'quantity', 'totalprice', 'totalprice_float']
    
    def get_img_url(self, obj):
        return obj.img.url if obj.img else '/media/default.png'
    
    def get_price_float(self, obj):
        return float(obj.price)
    
    def get_totalprice_float(self, obj):
        return float(obj.totalprice)

class BuyItemSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    price_float = serializers.SerializerMethodField()
    totalprice_float = serializers.SerializerMethodField()
    
    class Meta:
        model = Buy
        fields = ['id', 'category', 'name', 'desc', 'price', 'price_float', 'img_url', 'quantity', 'totalprice', 'totalprice_float']
    
    def get_img_url(self, obj):
        return obj.img.url if obj.img else '/media/default.png'
    
    def get_price_float(self, obj):
        return float(obj.price)
    
    def get_totalprice_float(self, obj):
        return float(obj.totalprice)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'phone', 'house', 'street', 'land', 'city', 'state', 'pincode', 'country', 'instructions']