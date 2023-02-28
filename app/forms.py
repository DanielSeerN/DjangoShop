from django import forms
from .models import Order, User


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_receiveing'].label = 'Дата получения заказа'

    date_of_receiveing = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('customer_name', 'customer_last_name', 'phone', 'adress', 'type_of_order', 'comment',
                  'date_of_receiveing')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username)
        if not user.exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не существует')
        if user.first():
            if not user.first().check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password')


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField()
    address = forms.CharField()

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
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        user_email = User.objects.filter(email=email).exists()
        if user_email:
            raise forms.ValidationError('Этот электронный адрес почты уже существует')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        username_check = User.objects.filter(username=username).exists()
        if username_check:
            raise forms.ValidationError('Имя пользователя уже существует')
        return username

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email')


class SendQuestionMail(forms.Form):
    first_name = forms.CharField(max_length=255, label='Ваше имя')
    last_name = forms.CharField(max_length=255, label='Ваша Фамилия')
    user_mail = forms.EmailField(max_length=255, label='Укажите почту, на которую хотите получить ответ')
    question = forms.CharField(widget=forms.Textarea, label='Опишите свою проблему')


class ReviewForm(forms.Form):
    score = forms.IntegerField(max_value=5, label="Ваша оценка продукта от 1 до 5")
    text = forms.CharField(widget=forms.Textarea, label="Опишите продукт")
