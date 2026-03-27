from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import UserProfile
from .forms import *
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.


def registerfn(request):

    if request.method == 'POST':
        form= RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password1=form.cleaned_data['password1']
            password2=form.cleaned_data['password2']

            if password1 != password2:
                messages.error(request,'Password does not match')
                return render(request, 'accounts/register.html', {'form': form})


            if User.objects.filter(username=username).exists():
                messages.error(request,'username Already exists')
                return render(request, 'accounts/register.html', {'form': form})

            user=User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            user.save()
            messages.success(request,'Account Created! Please login')
            return redirect('/login/')
        
        else:
            messages.error(request, 'Fill the form correctly')
            return render(request, 'accounts/register.html', {'form': form})
            
    
    else:
        form=RegisterForm() 
        return render(request,'accounts/register.html',{'form': form })






def loginfn(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user:
            auth.login(request,user)
            messages.success(request,'Login Successfull')
            return redirect('/')
        
        else:
            messages.error(request,'Invalid Credentials, Try Again')
            return render(request,'accounts/login.html')
        
    else:
        return render(request,'accounts/login.html')


@login_required(login_url='/login')

def logoutfn(request):
    auth.logout(request)
    messages.success(request,'You are Logged out ')
    return redirect('/login/')


@login_required(login_url='/login')

def profilefn(request):
    return render(request, 'accounts/profile.html')
    

@login_required(login_url='/login')
def become_bakerfn(request):
        profile= UserProfile.objects.get(user=request.user)
        
        if profile.is_baker():
            messages.error(request,"You are already a baker.")
            baker = BakerProfile.objects.get(user=request.user)
            return redirect(f'/my-store/{baker.id}/')
        
        if request.method == 'POST':
            form= BecomeBakerForm(request.POST, request.FILES)
            if form.is_valid():
                form=form.save(commit=False)
                form.user=request.user
                form.save()

                profile.role='baker'
                profile.save()


                baker = BakerProfile.objects.get(user=request.user)
                messages.success(request, "You are now a Baker on Dessert Hub!")
                return redirect(f'/my-store/{baker.id}/')
            
            else:
                messages.error(request,"Please correct the errors below.")
                return render(request, 'accounts/become_baker.html', {'form': form})
            

        else:
            form= BecomeBakerForm()
            return render(request, 'accounts/become_baker.html', {'form': form})






def edit_profilefn(request):
    profile = get_object_or_404 (UserProfile, user=request.user)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
         

        if form.is_valid():
            form.save()

            request.user.username = request.POST.get('username')
            request.user.email = request.POST.get('email')
            request.user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('/profile/')
        else:
            messages.error(request, 'Complete the form with valid details')
            return render(request, 'accounts/editprofile.html', {'form': form, 'profile': profile})
        
    else:
        form = CustomerProfileForm(instance=profile)
        return render(request, 'accounts/editprofile.html', {'form': form, 'profile': profile})


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin, login_url='/login/')
def admin_panel_fn(request):
    from accounts.models import BakerProfile
    bakers = BakerProfile.objects.all().order_by('-created_at')
    total_users = User.objects.count()
    total_bakers = bakers.count()
    verified_bakers = bakers.filter(is_verified=True).count()
    pending_bakers = bakers.filter(is_verified=False).count()

    context = {
        'bakers': bakers,
        'total_users': total_users,
        'total_bakers': total_bakers,
        'verified_bakers': verified_bakers,
        'pending_bakers': pending_bakers,
    }
    return render(request, 'accounts/admin_panel.html', context)


@user_passes_test(is_admin, login_url='/login/')
def verify_baker_fn(request, id):
    from accounts.models import BakerProfile
    baker = get_object_or_404(BakerProfile, id=id)
    baker.is_verified = not baker.is_verified  # toggle
    baker.save()
    status = "verified" if baker.is_verified else "unverified"
    messages.success(request, f'{baker.store_name} has been {status}.')
    return redirect('/admin-panel/')