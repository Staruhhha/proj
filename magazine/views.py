from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    return render(request, 'index.html')

# Create your views here.

def catalog_product(request):
    product_list = Product.objects.filter(exists=True).order_by('-name')
    context = {
        'list_object': product_list
    }
    return render(request, 'product/catalog.html', context)

from basket.forms import BasketAddProductForm

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'form_basket': BasketAddProductForm
    }
    return render(request, 'product/detail.html', context)




@permission_required('magazine.view_supplier')
def catalog_supplier(request):
    supplier_list = Supplier.objects.order_by('-name')
    context = {
        'list_sup': supplier_list
    }
    return render(request, 'supplier/catalog.html', context)

@permission_required('magazine.view_supplier')
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    context = {
        'supplier': supplier
    }
    return render(request, 'supplier/detail.html', context)


@permission_required('magazine.add_supplier')
def supplier_create(request):
    if request.method == "POST":
        form_supplier = SupplierForm(request.POST)
        if form_supplier.is_valid():
            form_supplier.save()
            messages.success(request, 'Поставщик успешно добавлен')
            return redirect('catalog_suppliers_page')

        messages.error(request, 'Неверно заполнены поля')

    else:
        form_supplier = SupplierForm()

        context = {
            'form': form_supplier
        }
        return render(request, 'supplier/create.html', context)



@permission_required('magazine.add_product')
def product_create(request):
    if request.method == "POST":
        form_product = ProductForm(request.POST)
        if form_product.is_valid():
            form_product.save()
            messages.success(request, 'Продукт успешно добавлен')
            return redirect('catalog_product_page')
        messages.error(request, 'неправильно заполнены поля')
    else:
        form_product = ProductForm()
    context = {
        'form': form_product
    }
    return render(request, 'product/create.html', context)




#------------------------авторизация в приложении-------------------------

def user_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            print(user)

            login(request, user)

            messages.success(request, 'успешная регистрация')
            return redirect('home_page')

        messages.error(request, "Произошла проблема")

    else:
        form = RegistrationForm()
    return render(request, 'auth/registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            print('is_anon:', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)

            login(request, user)

            print('is_anon:', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            print(user)

            messages.success(request, 'Вы успешно авторизовались')
            return redirect('home_page')

        messages.error(request, "ой, ошибка")
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.warning(request, 'вы вышли из аккаунта')
    return redirect('log in')


def anon(request):
    print('is_active:', request.user.is_active)
    print('is_anonymous:',request.user.is_anonymous)
    print('is_authenticated:',request.user.is_authenticated)
    print('is_staff:', request.user.is_staff)
    print('is_superuser:', request.user.is_superuser)

    print('может добавлять товар?',request.user.has_perm('magazine.add_product'))
    print('может добавлять или изменять товар', request.user.has_perms(['magazine.add_product', 'magazine.change_product']))
    print('может менять способ доставки', request.user.has_perm('magazine.change_delivery_type'))

    return render(request, 'test/anon.html')


@login_required()
def auth(request):
    return render(request, 'test/auth.html')


@permission_required('magazine.add_product')
def can_add_product(request):
    return render(request, 'test/can_add_product.html')


@permission_required(['magazine.add_product', 'magazine.change_prodcut'])
def can_add_and_change_product(request):
    return render(request, 'test/can_change_and_add_product.html')

@permission_required('magazine.change_delivery_type')
def change_delivery(request):
    return render(request, 'test/change_delivery_type.html')


#--------------------------View Generic-----------------------

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy

class CategoryList(ListView):
    model = Category
    template_name = 'category/category_list.html'
    extra_context = {
        'title': 'Список книг из класса'
    }

    allow_empty = True

    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


    def get_queryset(self):
        return Category.objects.all()


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm

    extra_context = {
        'action': 'Создать',
    }
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('get_category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UpdateCategory(UpdateView):
    model = Category
    form_class = CategoryForm

    extra_context = {
        'action': 'Изменить',
    }

    template_name = 'category/category_form.html'
    success_url = reverse_lazy('get_category')

    @method_decorator(permission_required('magazine.change_product'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('get_category')

    @method_decorator(permission_required('magazine.delete_product'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



#-----------------API--------------------------
from django.http import JsonResponse

from .serializer import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets


def test_json(request):
    supplier = get_object_or_404(Supplier, pk=1)
    return JsonResponse(
        {
            'message': supplier.name
        }
    )


#GET - получение
#POST - добавление
#DELETE - удаление
#PUT - обновление
@api_view(['GET', 'POST'])
def order_api_list(request, format=None):

    if request.method == 'GET':
        order_list = Order.objects.all()
        serializer = OrderSerializer(order_list, many=True)
        print(serializer.data)
        return Response({'orders': serializer.data})

    elif request.method == 'POST':

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_api_detail(request, pk, format=None):
    order_obj = get_object_or_404(Order, pk=pk)
    if order_obj:
        if request.method == 'GET':
            serializer = OrderSerializer(order_obj)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = OrderSerializer(order_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно обновлены', 'order': serializer.data})

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            order_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProductViewSet(viewsets.ModelViewSet):
        queryset = Product.objects.filter(exists=True)
        serializer_class = ProductSerializer

from django.core.mail import send_mail, send_mass_mail
from django.conf import settings

def contact_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['recipient']],
                fail_silently=True
            )
            if mail:
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('home_page')
            else:
                messages.error(request, 'Ошибка в отправке письма')
        else:
            messages.warning(request, 'неверно заполнены поля')
    else:
        form = ContactForm()

    return render(request, 'email.html', {'form': form})



#--------------------Prac 1-----------------------

class OrderList(ListView):
    model = Order
    template_name = 'order/order_list.html'

    extra_context = {
        'title': 'Список заказов'
    }
    allow_empty = True
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Order.objects.all()


class OrderDetail(DetailView):
    model = Order
    template_name = 'order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    extra_context = {
        'action': 'Добавить'
    }
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('get_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    extra_context = {
        'action': 'Изменить'
    }
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('get_order')
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class OrderDelere(DeleteView):
    model = Order
    template_name = 'order/order_conf_delete.html'
    success_url = reverse_lazy('get_order')
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer


def error_404(request, exception):
    return render(
        request,
        'error/404.html',
        {
            'title': 'Страница не найдена',
            'exception': exception
        },
        status=404
    )


import datetime


def template_start(request):
    context = {
        'current_page': request.GET.get('curr_page')
    }
    return render(request, 'templates/index.html', context=context)


def template_filter(request):
    context = {
        'digit': 84,
        'string': "I'm\ using Django",
        'string2': "im using Django",
        'bool': True,
        'datetime': datetime.datetime.now(),
        'var1': 'Var',
        'var2': '',
        'var3': None,
        'dict_col': [
            {'name': 'Samsung', 'price': 1300},
            {'name': 'Apple', 'price': 2000},
            {'name': 'Google', 'price': 1670}
        ],
        'some_list': ['firstdfsdfsdfs', 'second', 'third', 'last', 'ultra last',
                      'ultra last', 'ultra last', 'ultra last', 'ultra last', 'ultra last',
                      'final final v2.0'],
        'floatdig': 34.232425
    }
    return render(request, 'templates/filters.html', context=context)


def template_tag(request):
    context={
        'html_code': '<a class="btn btn-warning">sdfsdfsd</a>',
        'some_list': ['fiasdsadarst', 'second', 'third', 'last', 'ultra last',
                      'ultra last', 'ultra last', 'ultra last', 'ultra last', 'ultra last',
                      'final final v2.0'],
        'var1': None,
        'var2': False,
        'var3': 0,
        'var4': '',
        'var5': 'some str',
        'obj': Product.objects.get(pk=2)
    }
    return render(request, 'templates/tags.html', context=context)