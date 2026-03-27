from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .models import *
from .forms import *
# Create your views here.


@login_required(login_url='/login/')
def place_orderfn(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user == product.baker:
        messages.error(request, "You cannot order your own product.")
        return redirect(f'/product_detail/{product.id}/')

    if request.method == 'POST':
        form = OrderQuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if quantity > product.stock:
                messages.error(request, f'Only {product.stock} items available.')
                return render(request, 'orders/order_confirm.html', {'product': product, 'form': form})

            # Save to session and go to checkout
            request.session['order_quantity'] = quantity
            request.session['order_product_id'] = product.id
            return redirect('/checkout/')
    else:
        form = OrderQuantityForm()

    return render(request, 'orders/order_confirm.html', {'product': product, 'form': form})


@login_required(login_url='/login/')
def order_checkoutfn(request):
    product_id = request.session.get('order_product_id')
    quantity = request.session.get('order_quantity')

    if not product_id or not quantity:
        messages.error(request, 'No active order. Please select a product first.')
        return redirect('/')

    product = get_object_or_404(Product, id=product_id)
    total_price = product.price * quantity
    profile = request.user.profile

    if request.method == 'POST':
        form = OrderCheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.product = product
            order.quantity = quantity
            order.total_price = total_price
            order.status = 'pending'
            order.save()

            # Reduce stock
            product.stock -= quantity
            product.save()

            # Clear session
            del request.session['order_quantity']
            del request.session['order_product_id']

            messages.success(request, 'Order placed successfully!')
            return redirect(f'/order-success/{order.id}/')
        else:
            messages.error(request, 'Please fill all delivery details.')
    else:
        # Pre-fill form from profile
        form = OrderCheckoutForm(initial={
            'delivery_name': request.user.get_full_name() or request.user.username,
            'delivery_phone': profile.phone,
            'delivery_address': profile.address,
            'delivery_city': profile.city,
            'delivery_state': profile.state,
            'delivery_pincode': profile.pincode,
        })

    return render(request, 'orders/order_checkout.html', {
        'product': product,
        'quantity': quantity,
        'total_price': total_price,
        'form': form,
    })


@login_required(login_url='/login/')
def order_successfn(request, id):
    order = get_object_or_404(Order, id=id, customer=request.user)
    return render(request, 'orders/order_success.html', {'order': order})



@login_required(login_url='/login/')
def baker_ordersfn(request):

    if not request.user.profile.is_baker():
        messages.error(request, "Access denied.")
        return redirect('/')
    orders = Order.objects.filter(product__baker=request.user).order_by('-created_at')
    return render(request, 'orders/baker_orders.html', {'orders': orders})


@login_required(login_url='/login/')
def ordersfn(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required(login_url='/login/')
def cancel_order_fn(request, id):
    order = get_object_or_404(Order, id=id, customer=request.user)
    
    if order.status != 'pending':
        messages.error(request, "Only pending orders can be cancelled.")
        return redirect('/orders/')
    

    order.product.stock += order.quantity
    order.product.save()
    
    order.status = 'cancelled'
    order.save()
    
    messages.success(request, f'Order {order.product.name} has been cancelled.')
    return redirect('/my-orders/')



@login_required(login_url='/login/')
def update_order_statusfn(request, id):
    order = get_object_or_404(Order, id=id, product__baker=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order.id} status updated to {new_status}.')
    return redirect('/baker-orders/')



@login_required(login_url='/login/')
def add_review_fn(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    has_ordered = Order.objects.filter(
        customer=request.user,
        product=product,
        status='delivered'
    ).exists()

    if not has_ordered:
        messages.error(request, 'You can only review products you have received.')
        return redirect(f'/product_detail/{product_id}/')

    already_reviewed = Review.objects.filter(
        customer=request.user,
        product=product
    ).exists()

    if already_reviewed:
        messages.error(request, 'You have already reviewed this product.')
        return redirect(f'/product_detail/{product_id}/')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.product = product
            review.save()
            messages.success(request, 'Review submitted successfully!')
        else:
            messages.error(request, 'Please fill all fields.')

    return redirect(f'/product_detail/{product_id}/')


@login_required(login_url='/login/')
def edit_review_fn(request, review_id):
    review = get_object_or_404(Review, id=review_id, customer=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
        else:
            messages.error(request, 'Please fill all fields.')

    return redirect(f'/product_detail/{review.product.id}/')


@login_required(login_url='/login/')
def delete_review_fn(request, review_id):
    review = get_object_or_404(Review, id=review_id, customer=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect(f'/product_detail/{product_id}/')
