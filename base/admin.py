from django.contrib import admin
from base.models import Product,AddCard
# Register your models here.

class DisplayProducts(admin.ModelAdmin):
    list_display=['category','name','desc','price','sale','trending','img']
    list_display_links=['name']


admin.site.register(Product,DisplayProducts)

class DisplayAddCard(admin.ModelAdmin):
    list_display=['category','name','desc','price','img']
    list_display_links=['name']
admin.site.register(AddCard,DisplayAddCard)