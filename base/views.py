from django.shortcuts import render,redirect
from base.models import Product,AddCard,Buy,Address,Delivery
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    category_nav=True
    brand_nav=False
    # count=AddCard.objects.filter(host=request.user).count()
    products=Product.objects.all()
    if 'trending' in request.GET:
        trendingproducts=Product.objects.filter(trending=1)
        products=trendingproducts
    if 'sale' in request.GET:
        saleproducts=Product.objects.filter(sale=1)
        products=saleproducts

    if 'query' in request.GET:
        s=request.GET['query']
        category_nav=False
        brand_nav=True
        products=Product.objects.filter(Q(category__icontains=s) | Q(name__icontains=s) |Q(desc__icontains=s))
    if 'brand' in request.GET:
        s=request.GET['brand']
        brand_nav=True
        category_nav=False
        products=Product.objects.filter(Q(category__icontains=s) | Q(name__icontains=s) |Q(desc__icontains=s))

    if request.method=="POST":
        category=request.POST['cat']
        name=request.POST['name']
        desc=request.POST['desc']
        price=request.POST['price']
        img=request.FILES['img']
        Product.objects.create(category=category,name=name,desc=desc,price=price,img=img)
        return redirect('home')
    
    products_category=[]
    for i in products:
        if i.category not in products_category:
            products_category+=[i.category]

    if 'category' in request.GET:
        category_nav=False
        brand_nav=True
        a=request.GET['category']
        products=Product.objects.filter(category=a)
        return render(request,'home.html',{'products':products,'products_category':products_category,'category_nav':category_nav,'brand_nav':brand_nav})
    return render(request,'home.html',{'products':products,'products_category':products_category,'category_nav':category_nav,'brand_nav':brand_nav})


def Details(request,id):
    a=Product.objects.get(id=id)
    count=AddCard.objects.filter(host=request.user).count()
    return render(request,'details.html',{'data':a,'count':count})

@login_required(login_url='login')
def Cart(request):
    count=AddCard.objects.filter(host=request.user).count()
    a=AddCard.objects.filter(host=request.user)
    buyproducts=Buy.objects.filter(host=request.user)
    totalcart=sum(i.totalprice for i in a)
    totalorder=sum(i.totalprice for i in buyproducts)
    return render(request,'cart.html',{'data':a,'count':count,'buyproducts':buyproducts,'totalcart':totalcart,'totalorder':totalorder})

@login_required(login_url='login')
def Addcart(request,id):
    a=Product.objects.get(id=id)
    try:
        item_exist=AddCard.objects.filter(Q(name=a.name) & Q(host=request.user)).first()
        item_exist.quantity+=1
        item_exist.totalprice+=item_exist.price
        item_exist.save()

    except:
        AddCard.objects.create(category=a.category,name=a.name,desc=a.desc,price=a.price,img=a.img,totalprice=a.price,host=request.user)
    return redirect('home')


def Know(request):
    log_nav=True
    return render(request,'know.html',{'log_nav':log_nav})

def Support(request):
    log_nav=True
    return render(request,'support.html',{'log_nav':log_nav})




def Remove(request,id):
    a=AddCard.objects.get(id=id)
    a.delete()
    return redirect('cart')

def Buyproduct(request,id):
    a=AddCard.objects.get(id=id)
    try:
        item_exist=Buy.objects.filter(Q(name=a.name) & Q(host=a.host)).first()
        item_exist.quantity+=1
        item_exist.totalprice+=item_exist.price
        item_exist.save()
    except:
        Buy.objects.create(category=a.category,name=a.name,desc=a.desc,price=a.price,img=a.img,totalprice=a.totalprice,host=a.host,quantity=a.quantity)
    return redirect('cart')

def ByeDelete(request,id):
    a=Buy.objects.get(id=id)
    a.delete()
    return redirect('cart')

def ByeDeleteAll(request):
    a=Buy.objects.filter(host=request.user)
    if 'del' in request.GET:
        del_value=request.GET['del']
        if del_value:
            a.delete()
        return redirect('cart')
    return render(request,'conf.html')

def Reduce(request,id):
    a=AddCard.objects.get(id=id)
    if a.quantity==1:
        a.delete()
    else:
        a.quantity-=1
        a.totalprice-=a.price
        a.save()
    return redirect('cart')
def Increse(request,id):
    a=AddCard.objects.get(id=id)
    a.quantity+=1
    a.totalprice+=a.price
    a.save()
    return redirect('cart')


def Reduce1(request,id):
    a=Buy.objects.get(id=id)
    if a.quantity==1:
        a.delete()
    else:
        a.quantity-=1
        a.totalprice-=a.price
        a.save()
    return redirect('cart')
def Increse1(request,id):
    a=Buy.objects.get(id=id)
    a.quantity+=1
    a.totalprice+=a.price
    a.save()
    return redirect('cart')


def Checkout(request):
    addresses = Address.objects.filter(host=request.user)
    if request.method == "POST":
        global order_address
        a=request.POST["selected_address"]
        order_address=Address.objects.filter(Q(id=a) & Q(host=request.user)).first()
        return redirect('payment')
    return render(request,'checkout.html',{'addresses': addresses})


@login_required
def AddAddress(request):
    if request.method == "POST":
        country = request.POST["country"]
        name = request.POST["name"]
        phone = request.POST["phone"]
        house = request.POST["house"]
        street = request.POST["street"]
        land = request.POST["land"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pin"]
        instructions = request.POST.get("inst","")
        Address.objects.create(host=request.user,country = country,name = name,phone = phone,house = house,street = street,land = land,city = city,state = state,pincode = pincode,instructions = instructions)
        return redirect("ch")

    return render(request,"checkout1.html")



@login_required
def Edit_address(request,id):
    try:
        address = Address.objects.get(id=id, host=request.user)
    except Address.DoesNotExist:
        return redirect("ch")
    
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
        address.instructions = request.POST.get("inst","")
        address.save()
        return redirect("ch")
    return render(request,"editaddress.html",{'address':address})


@login_required
def Delete_address(request,id):
    try:
        address = Address.objects.get(id=id, host=request.user)
        address.delete()
        return redirect("ch")
    except Address.DoesNotExist:
        return redirect("ch")

def Payment_method(request):
    if request.method == "POST":
        global payment_mode
        payment_mode=request.POST['paymentt']
        delivery = Delivery.objects.first()
        if delivery:
            global payment_value
            payment_value = getattr(delivery,payment_mode,0)
            print("Payment Mode Value:",payment_value)
        return redirect('order')
    return render(request,'checkout2.html')


def Order_view(request):
    Delivery_type_price=0
    if 'f' in request.GET:
        Delivery_type=request.GET['f']
        if Delivery_type=='Oneday':
            Delivery_type_price=79
        else:
            Delivery_type_price=0
    count=AddCard.objects.filter(host=request.user).count()
    buycount=Buy.objects.filter(host=request.user).count()
    buyproducts=Buy.objects.filter(host=request.user)
    totalorder=sum(i.totalprice for i in buyproducts)
    delivery_charge=49.5
    final_total=totalorder+payment_value+delivery_charge+Delivery_type_price
    
    context={
        'count':count,
        'buycount':buycount,
        'buyproducts':buyproducts,
        'delivery_charge':delivery_charge,
        'total':totalorder,
        'payment_value':payment_value,
        'payment_mode':payment_mode,
        'final_total':final_total,
        'Delivery_type_price':Delivery_type_price,
        'order_address':order_address,
    }
    totalorder=sum(i.totalprice for i in buyproducts)
    return render(request,'checkoutmain.html',context)

def OrderPlaced(request):
    return render(request,'ordersuccess.html')