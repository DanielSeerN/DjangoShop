from django import forms
from .models import Order, USER


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_receiveing'].label = 'Дата получения заказа'

    date_of_receiveing = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('customer_name', 'phone', 'adress', 'customer_last_name', 'order_status', 'type_of_order', 'comment',
                  'date_of_receiveing')


class LoginForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = USER.objects.filter(username=username)
        if not user.exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не существует')
        if user.first():
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = USER
        fields = ('username', 'password')


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердить пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['address'].label = 'Адрес'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'Электронная почта'

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirmed_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        user_email = USER.objects.filter(email=email).exists()
        if user_email:
            raise forms.ValidationError('Этот электронный адрес почты уже существует')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        username_check = USER.objects.filter(username=username).exists()
        if username_check:
            raise forms.ValidationError('Имя пользователя уже существует')
        return username

    class Meta:
        model = USER
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email')

