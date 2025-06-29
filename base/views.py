from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from decimal import Decimal
from base.models import Product, AddCard, Buy, Address, Delivery

# Global variables for order processing
order_address = None
payment_mode = None
payment_value = Decimal('0.00')

def home(request):
    category_nav = True
    brand_nav = False
    count = 0
    
    if request.user.is_authenticated:
        count = AddCard.objects.filter(host=request.user).count()
    
    products = Product.objects.all()
    
    # Filter products based on GET parameters
    if 'trending' in request.GET:
        products = Product.objects.filter(trending=True)
    elif 'sale' in request.GET:
        products = Product.objects.filter(sale=True)
    elif 'query' in request.GET:
        s = request.GET['query']
        category_nav = False
        brand_nav = True
        products = Product.objects.filter(
            Q(category__icontains=s) | 
            Q(name__icontains=s) | 
            Q(desc__icontains=s)
        )
    elif 'brand' in request.GET:
        s = request.GET['brand']
        brand_nav = True
        category_nav = False
        products = Product.objects.filter(
            Q(category__icontains=s) | 
            Q(name__icontains=s) | 
            Q(desc__icontains=s)
        )
    elif 'category' in request.GET:
        category_nav = False
        brand_nav = True
        category = request.GET['category']
        products = Product.objects.filter(category=category)
    
    # Handle product creation (admin functionality)
    if request.method == "POST":
        category = request.POST['cat']
        name = request.POST['name']
        desc = request.POST['desc']
        price = Decimal(request.POST['price'])
        img = request.FILES['img']
        Product.objects.create(
            category=category, 
            name=name, 
            desc=desc, 
            price=price, 
            img=img
        )
        return redirect('home')
    
    # Get unique categories
    products_category = list(set(product.category for product in products))
    
    context = {
        'products': products,
        'products_category': products_category,
        'category_nav': category_nav,
        'brand_nav': brand_nav,
        'count': count
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
def Details(request, id):
    product = get_object_or_404(Product, id=id)
    count = AddCard.objects.filter(host=request.user).count()
    return render(request, 'details.html', {'data': product, 'count': count})

@login_required(login_url='login')
def Cart(request):
    count = AddCard.objects.filter(host=request.user).count()
    cart_items = AddCard.objects.filter(host=request.user)
    buy_products = Buy.objects.filter(host=request.user)
    
    total_cart = sum(Decimal(str(item.totalprice)) for item in cart_items)
    total_order = sum(Decimal(str(item.totalprice)) for item in buy_products)
    
    context = {
        'data': cart_items,
        'count': count,
        'buyproducts': buy_products,
        'totalcart': total_cart,
        'totalorder': total_order
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def Addcart(request, id):
    product = get_object_or_404(Product, id=id)
    
    cart_item, created = AddCard.objects.get_or_create(
        name=product.name,
        host=request.user,
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
        cart_item.totalprice = Decimal(str(cart_item.price)) * cart_item.quantity
        cart_item.save()
    
    return redirect('home')

def Know(request):
    return render(request, 'know.html', {'log_nav': True})

def Support(request):
    return render(request, 'support.html', {'log_nav': True})

@login_required
def Remove(request, id):
    cart_item = get_object_or_404(AddCard, id=id, host=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def Buyproduct(request, id):
    cart_item = get_object_or_404(AddCard, id=id, host=request.user)
    
    buy_item, created = Buy.objects.get_or_create(
        name=cart_item.name,
        host=cart_item.host,
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
        buy_item.totalprice = Decimal(str(buy_item.price)) * buy_item.quantity
        buy_item.save()
    
    return redirect('cart')

@login_required
def ByeDelete(request, id):
    buy_item = get_object_or_404(Buy, id=id, host=request.user)
    buy_item.delete()
    return redirect('cart')

@login_required
def ByeDeleteAll(request):
    if 'del' in request.GET and request.GET['del']:
        Buy.objects.filter(host=request.user).delete()
        return redirect('cart')
    return render(request, 'conf.html')

@login_required
def Reduce(request, id):
    cart_item = get_object_or_404(AddCard, id=id, host=request.user)
    
    if cart_item.quantity <= 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.totalprice = Decimal(str(cart_item.price)) * cart_item.quantity
        cart_item.save()
    
    return redirect('cart')

@login_required
def Increse(request, id):
    cart_item = get_object_or_404(AddCard, id=id, host=request.user)
    cart_item.quantity += 1
    cart_item.totalprice = Decimal(str(cart_item.price)) * cart_item.quantity
    cart_item.save()
    return redirect('cart')

@login_required
def Reduce1(request, id):
    buy_item = get_object_or_404(Buy, id=id, host=request.user)
    
    if buy_item.quantity <= 1:
        buy_item.delete()
    else:
        buy_item.quantity -= 1
        buy_item.totalprice = Decimal(str(buy_item.price)) * buy_item.quantity
        buy_item.save()
    
    return redirect('cart')

@login_required
def Increse1(request, id):
    buy_item = get_object_or_404(Buy, id=id, host=request.user)
    buy_item.quantity += 1
    buy_item.totalprice = Decimal(str(buy_item.price)) * buy_item.quantity
    buy_item.save()
    return redirect('cart')

@login_required
def Checkout(request):
    addresses = Address.objects.filter(host=request.user)
    
    if request.method == "POST":
        global order_address
        address_id = request.POST["selected_address"]
        order_address = get_object_or_404(Address, id=address_id, host=request.user)
        return redirect('payment')
    
    return render(request, 'checkout.html', {'addresses': addresses})

@login_required
def AddAddress(request):
    if request.method == "POST":
        Address.objects.create(
            host=request.user,
            country=request.POST["country"],
            name=request.POST["name"],
            phone=request.POST["phone"],
            house=request.POST["house"],
            street=request.POST["street"],
            land=request.POST["land"],
            city=request.POST["city"],
            state=request.POST["state"],
            pincode=request.POST["pin"],
            instructions=request.POST.get("inst", "")
        )
        return redirect("ch")
    
    return render(request, "checkout1.html")

@login_required
def Edit_address(request, id):
    address = get_object_or_404(Address, id=id, host=request.user)
    
    if request.method == "POST":
        address.country = request.POST["country"]
        address.name = request.POST["name"]
        address.phone = request.POST["phone"]
        address.house = request.POST["house"]
        address.street = request.POST["street"]
        address.land = request.POST["land"]
        address.city = request.POST["city"]
        address.state = request.POST["state"]
        address.pincode = request.POST["pin"]
        address.instructions = request.POST.get("inst", "")
        address.save()
        return redirect("ch")
    
    return render(request, "editaddress.html", {'address': address})

@login_required
def Delete_address(request, id):
    address = get_object_or_404(Address, id=id, host=request.user)
    address.delete()
    return redirect("ch")

@login_required
def Payment_method(request):
    if request.method == "POST":
        global payment_mode, payment_value
        payment_mode = request.POST['paymentt']
        
        delivery = Delivery.objects.first()
        if delivery:
            payment_value = Decimal(str(getattr(delivery, payment_mode, 0)))
            
        return redirect('order')
    
    return render(request, 'checkout2.html')

# @login_required
# def Order_view(request):
#     delivery_type_price = Decimal('0.00')
    
#     if 'f' in request.GET:
#         delivery_type = request.GET['f']
#         delivery_type_price = Decimal('79.00') if delivery_type == 'Oneday' else Decimal('0.00')
    
#     count = AddCard.objects.filter(host=request.user).count()
#     buy_count = Buy.objects.filter(host=request.user).count()
#     buy_products = Buy.objects.filter(host=request.user)
    
#     total_order = sum(Decimal(str(item.totalprice)) for item in buy_products)
#     delivery_charge = Decimal('49.50')
#     final_total = total_order + payment_value + delivery_charge + delivery_type_price
    
#     context = {
#         'count': count,
#         'buycount': buy_count,
#         'buyproducts': buy_products,
#         'delivery_charge': delivery_charge,
#         'total': total_order,
#         'payment_value': payment_value,
#         'payment_mode': payment_mode,
#         'final_total': final_total,
#         'Delivery_type_price': delivery_type_price,
#         'order_address': order_address,
#     }
    
#     return render(request, 'checkoutmain.html', context)

# Add this at the top of your views.py file
from datetime import datetime, timedelta

# Delivery configuration - easy to modify
DELIVERY_CONFIG = {
    'Free': {
        'label': 'Free Delivery',
        'price': 0.00,
        'days': 5
    },
    'Oneday': {
        'label': 'One-Day Delivery', 
        'price': 79.00,
        'days': 1
    }
}

# Then modify just the Order_view function:
@login_required
def Order_view(request):
    # Get selected delivery type and calculate price and date
    selected_delivery = request.GET.get('f', 'Free')
    delivery_config = DELIVERY_CONFIG.get(selected_delivery, DELIVERY_CONFIG['Free'])
    
    delivery_type_price = Decimal(str(delivery_config['price']))
    delivery_date = (datetime.now() + timedelta(days=delivery_config['days'])).strftime('%B %d')
    
    count = AddCard.objects.filter(host=request.user).count()
    buy_count = Buy.objects.filter(host=request.user).count()
    buy_products = Buy.objects.filter(host=request.user)
    
    total_order = sum(Decimal(str(item.totalprice)) for item in buy_products)
    delivery_charge = Decimal('49.50')
    final_total = total_order + payment_value + delivery_charge + delivery_type_price
    
    context = {
        'count': count,
        'buycount': buy_count,
        'buyproducts': buy_products,
        'delivery_charge': delivery_charge,
        'total': total_order,
        'payment_value': payment_value,
        'payment_mode': payment_mode,
        'final_total': final_total,
        'delivery_type_price': delivery_type_price,
        'order_address': order_address,
        'delivery_config': DELIVERY_CONFIG,  # Add this
        'selected_delivery': selected_delivery,
        'delivery_date': delivery_date,  # Add this
    }
    
    return render(request, 'checkoutmain.html', context)


def OrderPlaced(request):
    return render(request, 'ordersuccess.html')

# AJAX Views - UPDATED WITH PROPER CART COUNT HANDLING
@login_required
def add_to_cart_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = AddCard.objects.get_or_create(
            host=request.user,
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
            cart_item.totalprice = Decimal(str(cart_item.price)) * cart_item.quantity
            cart_item.save()

        cart_count = AddCard.objects.filter(host=request.user).count()
        return JsonResponse({'status': 'success', 'cartCount': cart_count})

@login_required
def update_quantity_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(AddCard, id=item_id, host=request.user)

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                cart_count = AddCard.objects.filter(host=request.user).count()
                total_cart = sum(Decimal(str(item.totalprice)) for item in AddCard.objects.filter(host=request.user))
                return JsonResponse({
                    'deleted': True,
                    'cartCount': cart_count,
                    'totalCart': float(total_cart)
                })

        cart_item.totalprice = Decimal(str(cart_item.price)) * cart_item.quantity
        cart_item.save()

        cart_count = AddCard.objects.filter(host=request.user).count()
        total_cart = sum(Decimal(str(item.totalprice)) for item in AddCard.objects.filter(host=request.user))
        
        return JsonResponse({
            'qty': cart_item.quantity, 
            'subtotal': float(cart_item.totalprice), 
            'totalCart': float(total_cart),
            'cartCount': cart_count
        })

@login_required
def remove_from_cart_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        cart_item = get_object_or_404(AddCard, id=item_id, host=request.user)
        cart_item.delete()
        
        cart_items = AddCard.objects.filter(host=request.user)
        total_cart = sum(Decimal(str(item.totalprice)) for item in cart_items)
        cart_count = cart_items.count()
        
        return JsonResponse({
            'status': 'success',
            'totalCart': float(total_cart),
            'cartCount': cart_count
        })

@login_required
def remove_from_buy_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        buy_item = get_object_or_404(Buy, id=item_id, host=request.user)
        buy_item.delete()
        
        buy_items = Buy.objects.filter(host=request.user)
        total_order = sum(Decimal(str(item.totalprice)) for item in buy_items)
        
        return JsonResponse({
            'status': 'success',
            'totalOrder': float(total_order)
        })

@login_required
def update_buy_quantity_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        action = request.POST.get('action')
        buy_item = get_object_or_404(Buy, id=item_id, host=request.user)
        
        if action == 'increase':
            buy_item.quantity += 1
        elif action == 'decrease':
            buy_item.quantity -= 1
            if buy_item.quantity <= 0:
                buy_item.delete()
                buy_items = Buy.objects.filter(host=request.user)
                total_order = sum(Decimal(str(item.totalprice)) for item in buy_items)
                return JsonResponse({
                    'deleted': True,
                    'totalOrder': float(total_order)
                })
        
        buy_item.totalprice = Decimal(str(buy_item.price)) * buy_item.quantity
        buy_item.save()
        
        buy_items = Buy.objects.filter(host=request.user)
        total_order = sum(Decimal(str(item.totalprice)) for item in buy_items)
        
        return JsonResponse({
            'qty': buy_item.quantity,
            'subtotal': float(buy_item.totalprice),
            'totalOrder': float(total_order)
        })

@login_required
def buy_item_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        cart_item = get_object_or_404(AddCard, id=item_id, host=request.user)
        
        buy_item, created = Buy.objects.get_or_create(
            host=request.user,
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
            buy_item.totalprice = Decimal(str(buy_item.price)) * buy_item.quantity
            buy_item.save()
        
        # Remove from cart after adding to buy list
        cart_item.delete()
        
        # Calculate new totals
        cart_items = AddCard.objects.filter(host=request.user)
        buy_items = Buy.objects.filter(host=request.user)
        total_cart = sum(Decimal(str(item.totalprice)) for item in cart_items)
        total_order = sum(Decimal(str(item.totalprice)) for item in buy_items)
        cart_count = cart_items.count()
        
        # Return properly formatted response with item details
        return JsonResponse({
            'status': 'success',  # Changed from 'success' to 'status'
            'buyItem': {
                'id': buy_item.id,
                'name': buy_item.name,
                'desc': buy_item.desc,
                'price': float(buy_item.price),
                'img': buy_item.img.url,
                'quantity': buy_item.quantity,
                'totalprice': float(buy_item.totalprice)
            },
            'totalCart': float(total_cart),
            'totalOrder': float(total_order),
            'cartCount': cart_count
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

@login_required
def clear_buy_list_ajax(request):
    if request.method == 'POST':
        Buy.objects.filter(host=request.user).delete()
        return JsonResponse({
            'status': 'success',
            'totalOrder': 0
        })

