from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages   

from store.forms import AddProductForm
from .models import *

from django.shortcuts import get_object_or_404 
from django.contrib.auth.decorators import login_required

from accounts.models import BakerProfile
from accounts.forms import BecomeBakerForm
from orders.models import Review
# Create your views here.


@login_required(login_url='/login')
def homefn(request):
    products=Product.objects.filter(is_available=True )
    category = Category.objects.all()
    return render (request,'store/home.html',{'products':products, 'categories': category})


@login_required(login_url='/login')
def product_detailfn(request, id):
    from orders.models import Review
    product = get_object_or_404(Product, id=id)
    images = ProductImage.objects.filter(product=product)
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    # Check if current user already reviewed this product
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            customer=request.user,
            product=product
        ).first()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'images': images,
        'reviews': reviews,
        'user_review': user_review,
    })


@login_required(login_url='/login/')
def category_fn(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category, is_available=True)
    categories = Category.objects.all()
    return render(request, 'store/category.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })


@login_required(login_url='/login/')
def all_products_fn(request):
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'store/all_products.html', {
        'products': products,
        'categories': categories,
    })


@login_required(login_url='/login')
def baker_storefn(request, id):
    baker= get_object_or_404(BakerProfile, id=id)
    products= Product.objects.filter(baker=baker.user, is_available=True)
    return render (request, 'store/baker_store.html', {'baker': baker, 'products': products})




@login_required(login_url='/login')
def editstorefn(request):
    baker = get_object_or_404(BakerProfile, user=request.user)
    
    if request.method == 'POST':
        form = BecomeBakerForm(request.POST,request.FILES, instance=baker)
        if form.is_valid():
            form.save()

            messages.success(request, 'Store details updated successfully!')
            return redirect ( f'/my-store/{baker.id}/')
        else:
            messages.error(request, 'Complete the form with valid details')
            return render(request, 'store/edit_store.html', {'form': form ,'baker': baker })
        
    else:
        form = BecomeBakerForm(instance=baker)
        return render(request, 'store/edit_store.html', {'form': form ,'baker': baker })
    

@login_required(login_url='/login')        
def add_productfn(request):
    category=Category.objects.all()
    if request.method == 'POST':
        form = AddProductForm(request.POST,request.FILES)

        if form.is_valid():
            product =  form.save(commit=False)
            product.baker = request.user
            product.save()
            
            for i in range(1,7):
                image = request.FILES.get(f'image_{i}')
                if image:
                    ProductImage.objects.create(
                        product=product,
                        image=image
                    )

            messages.success(request, 'Product added successfully!')
            return redirect(f'/my-store/{request.user.baker_profile.id}/')
        else:
            messages.error(request, 'Complete the form with valid details') 
            return render(request, 'store/add_product.html', {'form': form, 'categories': category})
    else:
        form = AddProductForm()        
        return render(request, 'store/add_product.html', {'form': form, 'categories': category})
    


@login_required(login_url='/login/')
def edit_productfn(request, id):
    product = get_object_or_404(Product, id=id, baker=request.user)
    categories = Category.objects.all()

    # Calculate remaining image slots
    current_image_count = product.images.count()
    remaining_count = max(0, 6 - current_image_count)
    remaining_slots = range(1, remaining_count + 1)  

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            product.delete()
            messages.success(request, 'Product deleted successfully.')
            return redirect(f'/my-store/{request.user.baker_profile.id}/')

        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            delete_ids = request.POST.getlist('delete_image')
            if delete_ids:
                ProductImage.objects.filter(id__in=delete_ids).delete()

            # Save only remaining slots
            for i in range(1, remaining_count + 1):
                image = request.FILES.get(f'new_image_{i}')
                if image:
                    ProductImage.objects.create(product=product, image=image)

            messages.success(request, 'Product updated successfully!')
            return redirect(f'/my-store/{request.user.baker_profile.id}/')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'store/edit_product.html', {
                'form': form,
                'product': product,
                'categories': categories,
                'remaining_slots': remaining_slots
            })

    else:
        form = AddProductForm(instance=product)
        return render(request, 'store/edit_product.html', {
            'form': form,
            'product': product,
            'categories': categories,
            'remaining_slots': remaining_slots  
        })
