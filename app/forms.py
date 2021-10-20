from django import forms
from .models import Order, USER

class OrderForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_receiveing'].label = 'Дата получения заказа'
    date_of_receiveing = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Order
        fields = ('customer_name', 'phone', 'adress', 'customer_last_name', 'order_status','type_of_order', 'comment',  'date_of_receiveing')
# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = USER
#         fields = ('login', 'password')
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['login'] = 'Логин'
