from django.shortcuts import render,redirect
from base.models import Product,AddCard,Buy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    category_nav=True
    brand_nav=False
    count=AddCard.objects.filter(host=request.user).count()
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

    # if request.method=="POST":
    #     category=request.POST['cat']
    #     name=request.POST['name']
    #     desc=request.POST['desc']
    #     price=request.POST['price']
    #     img=request.FILES['img']
    #     Product.objects.create(category=category,name=name,desc=desc,price=price,img=img)
    #     return redirect('home')
    products_category=[]
    for i in products:
        if i.category not in products_category:
            products_category+=[i.category]
    if 'category' in request.GET:
        category_nav=False
        brand_nav=True
        a=request.GET['category']
        products=Product.objects.filter(category=a)
        return render(request,'home.html',{'products':products,'products_category':products_category,'category_nav':category_nav,'brand_nav':brand_nav,'count':count})
    return render(request,'home.html',{'products':products,'products_category':products_category,'category_nav':category_nav,'brand_nav':brand_nav,'count':count})


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




# def Add(request):
#     c = Addcard.objects.filter(host=request.user)
#     count=Addcard.objects.filter(host=request.user).count()
#     a = Buy.objects.filter(host=request.user)
#     ttcost=sum(i.cost*i.quantity for i in c)
#     totalcost=sum(i.cost*i.quantity for i in a)
#     return render(request, 'addcard.html',{'products': c,'count':count,'buyproducts': a,'totalcost':totalcost,'ttcost':ttcost})


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