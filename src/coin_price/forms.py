from django import forms
from .models import Coin
from pycoingecko import CoinGeckoAPI
from decimal import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


cg = CoinGeckoAPI()
coins_dict = cg.get_coins_list()


class Email_as_usernameForm(UserCreationForm):
    username = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ('username', )
        labels = {
           'username' : 'Email'
        }

    def save(self, commit = True):
        user = super(Email_as_usernameForm, self).save(commit = False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user
    
    def clean_username(self, *args, **kwargs):
        value = self.cleaned_data['username']
        return value
    

class InputForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = '__all__'
        labels = {
            'name': 'Coin',
            'price_guess': 'Price'
        }
    
    def clean_price_guess(self, *args, **kwargs):
        value = self.cleaned_data.get("price_guess")
        if value <= 0:
            raise forms.ValidationError('Price cannot be negative or zero!')
        return value

    
    def clean_name(self):
        user_input_name = self.cleaned_data["name"]
        #compare user_input_name with id and name data from gecko, if correct, proceed with return, lowercase the names from the coin_dictionary when comparing
        for coin in coins_dict:
            if (coin['symbol'].lower() == user_input_name.lower()) or (coin['name'].lower() == user_input_name.lower()) or (coin['id'].lower() == user_input_name.lower()):
                self.cleaned_data["name"] = coin["name"]
                return self.cleaned_data["name"]
        raise forms.ValidationError("Coin does not exist!")

    def compare_price(self, actual_price):
        value = self.cleaned_data.get("price_guess")
        value = Decimal(value)
        if value < actual_price:
            return 'Actual price is higher!'
        elif value > actual_price:
            return 'Actual price is lower!'
        else:
            return 'Price is correct!'

class SearchForm(forms.Form):
    searched = forms.CharField(max_length = 255)

    def clean_searched(self):
        searched = self.cleaned_data['searched']
        return searched


    

