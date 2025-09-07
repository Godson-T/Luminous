
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'orders'
urlpatterns = [
    path("cart/",views.show_cart,name='cart'),
    path("add_to_cart/",views.add_to_cart,name='add_to_cart'),
    path("checkout",views.checkout_cart,name='checkout'),
    path("remove_item/<pk>",views.remove_item_from_cart,name='remove_item'),
    path("orders/",views.show_orders,name='orders'),
]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)