from django.contrib.auth import authenticate

from app.utils.cart_utils import create_customer


def authenticate_user(form):
    """
    Аутентифицировать пользователя
    """
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    authenticate(username=username, password=password)


def register_user(form):
    """
    Зарегистрировать пользователя
    """
    user = form.save(commit=False)
    user.username = form.cleaned_data['username']
    user.set_password(form.cleaned_data['password'])
    user.address = form.cleaned_data['address']
    user.phone = form.cleaned_data['phone']
    user.save()
    create_customer(user)
    return user
