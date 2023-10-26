from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from .forms import *
from django.http import Http404
from .models import Food
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Case, When
import pandas as pd

# Create your views here.

def index(request):
    food = Food.objects.all()
    query = request.GET.get('q')

    if query:
        food= Food.objects.filter(Q(title__icontains=query)).distinct()
        return render(request, 'home.html', {'foods': food})

    return render(request, 'home.html', {'foods': food})

def about(request):
    return render(request,'aboutus.html')


# Show details of the food
def detail(request, food_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    food = get_object_or_404(Food, id=food_id)
    food = Food.objects.get(id=food_id)
    
    temp = list(MyList.objects.all().values().filter(food_id=food_id,user=request.user))
    if temp:
        update = temp[0]['watch']
    else:
        update = False
    if request.method == "POST":

        # For my list
        if 'watch' in request.POST:
            watch_flag = request.POST['watch']
            if watch_flag == 'on':
                update = True
            else:
                update = False
            if MyList.objects.all().values().filter(food_id=food_id,user=request.user):
                MyList.objects.all().values().filter(food_id=food_id,user=request.user).update(watch=update)
            else:
                q=MyList(user=request.user,food=food,watch=update)
                q.save()
            if update:
                messages.success(request, "Food added to your list!")
            else:
                messages.success(request, "Food removed from your list!")

            
        # For rating
        else:
            rate = request.POST['rating']
            if Myrating.objects.all().values().filter(food_id=food_id,user=request.user):
                Myrating.objects.all().values().filter(food_id=food_id,user=request.user).update(rating=rate)
            else:
                q=Myrating(user=request.user,food=food,rating=rate)
                q.save()

            messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    out = list(Myrating.objects.filter(user=request.user.id).values())

    # To display ratings in the movie detail page
    food_rating = 0
    rate_flag = False
    for each in out:
        if each['food_id'] == food_id:
            food_rating_rating = each['rating']
            rate_flag = True
            break

    context = {'food': food,'food_rating':food_rating,'rate_flag':rate_flag,'update':update}
    return render(request, 'review.html', context)


# MyList functionality
def watch(request):

    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404

    food = Food.objects.filter(mylist_watch=True,mylist_user=request.user)
    query = request.GET.get('q')

    if query:
        food = Food.objects.filter(Q(title__icontains=query)).distinct()
        return render(request, 'watch.html', {'food': food})

    return render(request, 'watch.html', {'food': food})


# To get similar food based on user rating
def get_similar(food_name,rating,corrMatrix):
    similar_ratings = corrMatrix[food_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

# Recommendation Algorithm
def recommend(request):
    return render(request,'recommend.html')

def recommendation(request):
    return render(request,'rcommendation.html')


# Register user
def signUp(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")

    context = {'form': form}

    return render(request, 'signUp.html', context)


# Login User
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            else:
                return render(request, 'login.html', {'error_message': 'Your account disable'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid Login'})

    return render(request, 'login.html')


# Logout user
def Logout(request):
    logout(request)
    return redirect("login")