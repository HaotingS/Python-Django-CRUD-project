from django.shortcuts import render, redirect
from coin_price.forms import InputForm, Email_as_usernameForm, SearchForm
from coin_price.models import Coin
from pycoingecko import CoinGeckoAPI
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.

cg = CoinGeckoAPI()
coins_dict = cg.get_coins_list()



def home(request):
    return render(request, 'home.html',{})

def register(request):
    if request.method == "POST":
        form = Email_as_usernameForm(request.POST)        
        if form.is_valid():
            form.save()
            return redirect("login")
    form = Email_as_usernameForm()
    return render(request, "register.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request)
                return redirect("input")
            else:
                messages.error(request, "Invalid username or password")
    else:
        messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})


def logout(request):
    logout(request)
    messages.info(request, "Logged out!")
    return redirect("logout")

def input_view(request, *args, **kwargs):
    if request.method == "GET":
        form = InputForm()
        context = {
        'form': form
        }
        return render(request, 'input.html', context)
    else:
        form = InputForm(request.POST)
        if form.is_valid():
            coin_name = form.cleaned_data['name']
            coin_holder = next(coin for coin in coins_dict if coin['name'] == coin_name)
            coin_id = coin_holder['id']
            actual_price = cg.get_price(ids = coin_id, vs_currencies='usd')[coin_id]
            result = form.compare_price(actual_price['usd'])
            form.cleaned_data['result'] = result
            to_display = form.cleaned_data['result']
            form.save()
            messages.success(request, to_display)
        
            return redirect('/input/')
        else:
            context = {
                'form' : form
            }
            return render(request, 'input.html', context)

def list_view(request, *args, **kwargs):
    input_coins = Coin.objects.all()
    paginator = Paginator(input_coins, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'page_obj': page_obj}
    return render(request, 'list.html', context)

def search(request, *args, **kwargs):
    form = SearchForm()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            searched = form.cleaned_data['searched']
            for coin in coins_dict:
                if (coin['symbol'].lower() == searched.lower()) or (coin['name'].lower() == searched.lower()) or (coin['id'].lower() == searched.lower()):
                    form.cleaned_data['searched'] = coin["name"]
                    searched = form.cleaned_data['searched']
            context= {
                'searched': searched,
                'list': Coin.objects.all()
            }    
            return render(request, 'search_results.html', context)
        else:
            form = SearchForm()
            print(form.is_valid())
            context = {
                'form': form
            }
            return render(request, 'search_results.html', context)

def delete_coin(request, id):
    coin = Coin.objects.get(pk = id)
    coin.delete()
    return redirect('list')



    




    
        
