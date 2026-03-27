from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from store.models import Product
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def dashboard_fn(request):
    user = request.user

    # Admin dashboard
    if user.is_superuser:
        total_users = User.objects.count()
        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        total_revenue = sum(o.total_price for o in Order.objects.all())
        recent_orders = Order.objects.order_by('-created_at')[:10]
        context = {
            'total_users': total_users,
            'total_orders': total_orders,
            'total_products': total_products,
            'total_revenue': total_revenue,
            'recent_orders': recent_orders,
            'role': 'admin',
        }
        return render(request, 'dashboard/dashboard.html', context)

    # Baker dashboard
    elif user.profile.is_baker():
        orders = Order.objects.filter(product__baker=user)
        total_orders = orders.count()
        total_revenue = sum(o.total_price for o in orders)
        pending_orders = orders.filter(status='pending').count()
        delivered_orders = orders.filter(status='delivered').count()
        total_products = Product.objects.filter(baker=user).count()
        recent_orders = orders.order_by('-created_at')[:5]
        context = {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'pending_orders': pending_orders,
            'delivered_orders': delivered_orders,
            'total_products': total_products,
            'recent_orders': recent_orders,
            'role': 'baker',
        }
        return render(request, 'dashboard/dashboard.html', context)

    # Customer dashboard
    else:
        orders = Order.objects.filter(customer=user)
        total_orders = orders.count()
        total_spent = sum(o.total_price for o in orders)
        pending_orders = orders.filter(status='pending').count()
        delivered_orders = orders.filter(status='delivered').count()
        recent_orders = orders.order_by('-created_at')[:5]
        context = {
            'total_orders': total_orders,
            'total_spent': total_spent,
            'pending_orders': pending_orders,
            'delivered_orders': delivered_orders,
            'recent_orders': recent_orders,
            'role': 'customer',
        }
        return render(request, 'dashboard/dashboard.html', context)