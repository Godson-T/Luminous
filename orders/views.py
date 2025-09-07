from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderedItem
from django.contrib import messages
from products.models import Product 
from django.contrib.auth.decorators import login_required


def checkout_cart(request):
    if request.method == "POST":
        try:
            user = request.user
            customer = user.customer_profile
            total = float(request.POST.get('total', 0))

            order_obj = Order.objects.filter(
                owner=customer,
                order_status=Order.CART_STAGE
            ).first()

            if order_obj:
                order_obj.order_status = Order.ORDER_CONFORMED
                order_obj.save()
                messages.success(
                    request, 
                    "Your order is processed. Your item will be delivered within two days."
                )
            else:
                messages.error(request, "Unable to process. No items in cart.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('orders:cart')


def show_cart(request):
    user = request.user
    customer = user.customer_profile 
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )
    context = {'cart': cart_obj}
    return render(request, 'cart.html', context)


def remove_item_from_cart(request, pk):
    item = get_object_or_404(OrderedItem, pk=pk)
    item.delete()
    return redirect('orders:cart')


@login_required(login_url='account')
def show_orders(request):
    user = request.user
    customer = user.customer_profile 
    all_orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context = {
        'orders': all_orders,
        'hide_blog_and_contact': True
    }
    return render(request, 'orders.html', context)


@login_required(login_url='account')
def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        try:
            customer = user.customer_profile
        except Exception:
            messages.error(request, "User profile not found. Please complete your profile before adding items to cart.")
            return redirect('orders:cart')

        quantity = int(request.POST.get('quantity', 1))  
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')  # If you use size later

        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        product = get_object_or_404(Product, pk=product_id)

        ordered_item, created = OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj,
        )
        if created:
            ordered_item.quantity = quantity
        else:
            ordered_item.quantity += quantity
        ordered_item.save()
        
        messages.success(request, f"{product.title} added to cart!")

    return redirect('orders:cart')
