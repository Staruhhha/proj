from django import forms
from .models import *
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = (
            'name',
            'agent_firstname',
            'agent_name',
            'agent_patronymic',
            'agent_telephone',
            'address'
        )

    def clean_agent_phone(self):
        agent_phone = self.cleaned_data['agent_telephone']

        if re.match(r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}', agent_phone):
            return agent_phone
        raise ValidationError('Телефон должке быть прописа в формате +7(___)___-__-__')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'photo',
            'exists',
            'category',
            'tag'
        )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'title',
            'description'
        )


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2
    )
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', }),
    )
    password1 = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
    password2 = forms.CharField(
        label='Повторите паролm',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )


class ContactForm(forms.Form):
    recipient = forms.EmailField(
        label='Получатель',
        widget=forms.EmailInput(
            attrs={'class': 'form-control',},
        ),
    )
    subject = forms.CharField(
        label='Тема письма',
        widget=forms.TextInput(
            attrs={'class': 'form-control',},
        ),
    )
    content = forms.CharField(
        label='Текст письма',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 11}
        )
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'FIO_customer',
            'delivery_address',
            'delivery_type'
        )
