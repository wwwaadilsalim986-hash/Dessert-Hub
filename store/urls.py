from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
      path('',views.homefn),
      path('product_detail/<int:id>/', views.product_detailfn, name='product_detail'),
      path('my-store/<int:id>/',views.baker_storefn, name='my_store'),
      path('edit-store/', views.editstorefn, name='edit_store'),
      path('add-product/', views.add_productfn, name='add_product'),
      path('edit-product/<int:id>/', views.edit_productfn, name='edit_product'),
      path('category/<int:id>/', views.category_fn, name='category'),
      path('all-products/', views.all_products_fn, name='all_products'),

      



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)