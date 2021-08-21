from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import uploads


def index(request):
    ik=Closebid.objects.all()
    ima = auction.objects.all()
    return render(request, "auctions/index.html",{
        'ima' : ima,
        'ik': ik
    })

def watch(request,id):
    commente = comment.objects.filter(listid=id)
    auct =  auction.objects.filter(id=id)
    return render(request, "auctions/watch.html",{
       "auctions": auct,
        "commente": commente,
        "error": request.COOKIES.get('error')
    })

def login_view(request):
   if request.method == "POST":

       # Attempt to sign user in
       username = request.POST["username"]
       password = request.POST["password"]
       user = authenticate(request, username=username, password=password)

       # Check if authentication successful
       if user is not None:
           login(request, user)
           return HttpResponseRedirect(reverse("index"))
       else:
           return render(request, "auctions/login.html", {
               "message": "Invalid username and/or password."
           })
   else:
       return render(request, "auctions/login.html")


def logout_view(request):
   logout(request)
   return HttpResponseRedirect(reverse("index"))


def register(request):
   if request.method == "POST":
       username = request.POST["username"]
       email = request.POST["email"]

       # Ensure password matches confirmation
       password = request.POST["password"]
       confirmation = request.POST["confirmation"]
       if password != confirmation:
           return render(request, "auctions/register.html", {
               "message": "Passwords must match."
           })

       # Attempt to create new user
       try:
           user = User.objects.create_user(username, email, password)
           user.save()
       except IntegrityError:
           return render(request, "auctions/register.html", {
               "message": "Username already taken."
           })
       login(request, user)
       return HttpResponseRedirect(reverse("index"))
   else:
       return render(request, "auctions/register.html")

@login_required(login_url='/login')

def upload(request):

   if request.method == 'POST':
       form = uploads(request.POST,request.FILES)
       if form.is_valid():
           ok=form.save(commit=False)
           ok.user=request.user
           ok.save()
           return redirect(index)
   else:
       form = uploads()
       all = auction.objects.all()
       return render(request,'auctions/form.html',{
           'form' : form, 'all' : all
       })
@login_required(login_url='/login')
def watchlist(request,productid):
   obj = watchs.objects.filter(
       auctionh=productid, user=request.user.username)
   if obj:
       obj.delete()
       product = auction.objects.filter(id=productid)
       added = watchs.objects.filter(
           auctionh=productid, user=request.user.username)
       return HttpResponseRedirect(reverse("index"))

   else:
       obj = watchs()
       obj.user = request.user.username
       obj.auctionh = productid
       obj.save()
       product = auction.objects.get(id=productid)
       added = watchs.objects.filter(
           auctionh=productid, user=request.user.username)
       return render(request,"auctions/watchlist.html",{
           "i" : product,
           "added" : added
       })

@login_required(login_url='/login')
def update(request):
   lst = watchs.objects.filter(user=request.user.username)
   # list of products available in WinnerModel
   present = False
   prodlst = []
   i = 0
   if lst:
       present = True
       for item in lst:
           product = auction.objects.get(id=item.auctionh)
           prodlst.append(product)
   print(prodlst)
   return render(request, "auctions/cart.html", {
       "product_list": prodlst,
       "present": present
   })
@login_required(login_url='/login')
def bids(request,bidid):
   if request.method == "POST":
       item = auction.objects.get(id=bidid)
       new = int(request.POST.get('new'))
       if item.bid>=new :
           product = auction.objects.get(id=bidid)
           response = redirect('watch', id=bidid)
           response.set_cookie('error', 'bid should be greater than previous one', max_age=3)
           return response
       else:
           item.bid = new
           item.save()
           bids = bid.objects.filter(id=bidid)
           if bids:
               bids.delete()
           k = bid()
           k.user = request.user.username
           k.title = item.title
           k.id = bidid
           k.bid = new
           k.save()
           product = auction.objects.get(id=bidid)
           return redirect('watch', id=bidid)

   else:
       product = auction.objects.get(id=bidid)
       ok = bid.objects.filter(id=bidid)
       added = watchlist.objects.filter(
           auctionh=bidid, user=request.user.username)
       return render(request, "auctions/watch.html", {
           "i": product,
           "added": added,
           "ok":ok
       })
@login_required(login_url='/login')
def comments(request,pid):
   if request.method == "POST":
       c = comment()
       c.commentsa = request.POST.get('commentsa')
       c.user = request.user.username
       c.listid = pid
       c.save()
       return redirect('watch', id=pid)
   else :
       return redirect('index')
@login_required(login_url='/login')
def close(request,cid):
    c= Closebid()
    x = auction.objects.get(id=cid)
    bids = bid.objects.filter(id=cid)

    c.user = request.user.username
    c.listid = x.id
    c.bidprice = x.bid
    c.title = x.title
    c.image1 = x.image
    c.save()
    message = "bid closed"

    if auction.objects.filter(id=cid):
        a = auction.objects.filter(id=cid)
        a.delete()
    if comment.objects.filter(id=cid):
        f= comment.objects.filter(id=cid)
        f.delete()
    return redirect('index')

def win(request,title):
    ok=bid.objects.filter(title=title)
    print(ok)
    win = Closebid.objects.filter(title=title)
    return render(request, "auctions/close.html", {
        "ok": ok,
        "winner": win
    })

def category(request):

    categories = list(set([auction.category for auction in auction.objects.all() if auction.category]))
    return render(request, "auctions/categories.html", {
        'categories': categories
    })
def filtered(request, category):
    return render(request, "auctions/index.html", {
        'ima': auction.objects.filter(category=category)
    })