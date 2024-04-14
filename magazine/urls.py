from django.urls import path, include
from django.conf.urls.static import static
from .views import *

urlpatterns_template = [
    path('', template_start, name='template_start'),
    path('tag/', template_tag, name='template_tag'),
    path('filter/', template_filter, name='template_filter')
]

urlpatterns = [
    path ('template/', include(urlpatterns_template)),
    path ('index/', home, name='home_page'),
    path('catalog/', catalog_product, name='catalog_product_page'),
    path('product/<int:pk>/', product_detail, name='detail_product_page'),

    path('suppliers/', catalog_supplier, name='catalog_supplier_page'),
    path('supplier/<int:pk>', supplier_detail, name='detail_supplier_page'),
    path('supplier/create', supplier_create, name='create_supplier_page'),


    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),

    path('anon/', anon, name='anon'),
    path('auth/',auth, name='auth'),
    path('can_add/', can_add_product, name='can_add'),
    path('can_add_change/', can_add_and_change_product, name='can_add_change'),
    path('can_change_del/', change_delivery, name='can_change_del'),

    path('product/create', product_create, name='create_product_page'),

    path('category/', CategoryList.as_view(), name='get_category'),
    path('category/<int:pk>/detail', CategoryDetail.as_view(), name='category_detail'),
    path('category/create/', CategoryCreate.as_view(), name='category_create'),
    path('category/<int:pk>/update/', UpdateCategory.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='delete_category'),
    path('contact/', contact_email, name='email_page'),
    path('api/orders/', order_api_list, name='api_order_list'),
    path('api/orders/<int:pk>/', order_api_detail, name='api_order_detail'),
    path('order/', OrderList.as_view(), name='get_order'),
    path('order/<int:pk>/detail', OrderDetail.as_view(), name='order_detail'),
    path('order/<int:pk>/delete', OrderDelere.as_view(), name='order_delete'),
    path('order/create', OrderCreate.as_view(), name='order_create'),
    path('order/<int:pk>/update', OrderUpdate.as_view(), name='order_update')

]

from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'api/products', ProductViewSet, basename='product')
router.register(r'api/supplier', SupplierViewSet, basename='supplier')
router.register(r'api/supply', SupplyViewSet, basename='supply')
urlpatterns += router.urls
