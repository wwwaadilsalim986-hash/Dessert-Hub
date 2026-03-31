from django.urls import path
from . import views

urlpatterns = [

    path('place_order/<int:id>/',views.place_orderfn,name='place_order'),
    path('checkout/',views.order_checkoutfn,name='checkout'),
    path('order-success/<int:id>/', views.order_successfn, name='order_success'),

    path('baker-orders/', views.baker_ordersfn, name='baker_orders'),
    path('my-orders/', views.ordersfn, name='my_orders'),
    path('update-order-status/<int:id>/', views.update_order_statusfn, name='update_order_status'),
    path('cancel-order/<int:id>/', views.cancel_order_fn, name='cancel_order'),

    path('add-review/<int:product_id>/', views.add_review_fn, name='add_review'),
    path('edit-review/<int:review_id>/', views.edit_review_fn, name='edit_review'),
    path('delete-review/<int:review_id>/', views.delete_review_fn, name='delete_review'),

    path('orders/<int:id>/', views.orderdetailfn, name='order_detail'),
    

]