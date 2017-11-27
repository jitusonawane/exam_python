from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import User, Quote
# Create your views here.

def logincheck(session):
    if 'id' not in session:
        return False
    return True    

def index(request):
    if logincheck(request.session):
        return redirect('/quotes')
    else:
        return render(request, 'main/index.html')

def register(request):
    errors  = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():            
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        print "here"
        rg = User.objects.get(email = request.POST['email'])
        request.session['id'] = rg.id   
        return redirect('/quotes')


def login(request):    
    errors  = User.objects.login_valiator(request.POST)
    if len(errors):              
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:        
        lg =  User.objects.get(email = request.POST['email'])
        request.session['id'] = lg.id
        return redirect('/quotes')


def logout(request):
    del request.session['id']
    return redirect('/')
  

def quotes(request):    
    if logincheck(request.session):
        quotes= Quote.objects.all().exclude(favourite__id=request.session['id'])        
        favourites= Quote.objects.filter(favourite__id=request.session['id'])
        user= User.objects.get(id=request.session['id'])
        notfav= Quote.objects.exclude(favourite__id=request.session['id'])        
        others= Quote.objects.all().exclude(favourite__id=request.session['id'])
        
        context = {
            "user": user,
            "quotes": quotes,
            "favourites": favourites,
            "others": others
        }

        # context = {

        #     'favourites': User.objects.filter(favourite__id=request.session['id']),
        #     'user': User.objects.get(id=request.session['id']),
        #     'notfav': User.objects.exclude(favourite__id=request.session['id']),      
        #     'others' : Quote.objects.all().exclude(favourite__id=request.session['id'])
        # }


               
        return render(request, 'main/quotes.html', context)
    else:
        return redirect('/')

def createquote(request):
    if request.method != 'POST':
        messages.error(request, "Please insert item in Field")
        return redirect ("/quotes")
    newquote= Quote.objects.quoteval(request.POST, request.session["id"])
    
    if newquote[0]== False:
            for each in newquote[1]:
                messages.add_message(request, messages.INFO, each)
            return redirect('/quotes')
    
    else:
        return redirect('/quotes')

def show(request, quote_id):
    creator= User.objects.filter(quoter__id= quote_id)
    quotes= Quote.objects.filter(favourite=creator)
    count= Quote.objects.filter(favourite=creator).count()
    print quotes
    
    context={
        "count": count,
        "quotes": quotes,
        "creator": creator
        
    }
    return render(request, 'main/show.html', context)

def addfav(request, quote_id):
    if request.method != "POST":
        messages.error(request,"What Item?")
        return redirect('/')
    else:
        add_fav= Quote.objects.addfav(request.session['id'],quote_id)
        if 'errors' in add_fav:
            messages.error(request, add_fav['errors'])
        return redirect('/quotes')

def removefav(request, quote_id):
    if request.method != "GET":
        messages.error(request,"")
        return redirect('/')
    else:
        remove_fav= Quote.objects.removefav(request.session['id'],quote_id)
        if 'errors' in remove_fav:
            messages.error(request, remove_fav['errors'])
            return redirect('/quotes')
        else:
            return redirect('/quotes')