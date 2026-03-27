from django.urls import path
from . import views

urlpatterns = [

      path('register/',views.registerfn, name='register'),
      path('login/',views.loginfn, name='login'),
      path('logout/',views.logoutfn, name='logout'),
      path('profile/',views.profilefn, name='profile'),
      path('become-baker/',views.become_bakerfn, name='become_baker'),
      path('edit-profile/', views.edit_profilefn, name='edit_profile'),
      
      path('admin-panel/', views.admin_panel_fn, name='admin_panel'),
      path('verify-baker/<int:id>/', views.verify_baker_fn, name='verify_baker'),



]