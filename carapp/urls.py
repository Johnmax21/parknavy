"""
URL configuration for parknavi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .  import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index,name='index'),
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register_user/',views.register_user,name='register_user'),
    path('userlist/',views.userlist,name='userlist'),
    path('delete_user/<int:id>/',views.delete_user,name='delete_user'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('proupdate/',views.proupdate,name='proupdate'),
    path('user_home/',views.user_home,name='user_home'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('feedback_rate/',views.feedback_rate,name='feedback_rate'),
    path('feedback_success/',views.feedback_success,name='feedback_success'),
    path('feedbacklist/',views.feedbacklist,name='feedbacklist'),
    path('delete_feedback/<int:id>/',views.delete_feedback,name='delete_feedback'),
    path('area/',views.area,name='area'),
    path('arealist/',views.arealist,name='arealist'),
    path('delete_area/<int:id>/',views.delete_area,name='delete_area'),
    path('update_area/<int:id>/',views.update_area,name='update_area'),
    path('editarea/<int:id>/',views.editarea,name='editarea'),
    path('area_list/<int:id>/', views.area_list, name='area_list'),
    path('addbook/<int:id>/', views.addbook, name='addbook'),
    path('add_book/', views.add_book, name="add_book"),
    path('update_status/', views.update_status, name="update_status"),
    path('book_list/', views.book_list, name="book_list"),
    path('payment/',views.payment,name='payment'),
    path('paymenthandler/',views.paymenthandler,name='paymenthandler'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('area_details/',views.area_details,name='area_details'),
    path('view_details/<int:id>/',views.view_details,name='view_details'),
    path('userbookings/', views.userbookings, name='userbookings'),
    # path('edit_booking/<int:id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:id>/', views.delete_booking, name='delete_booking'),
    # path('slotfeedback/<int:id>/', views.slotfeedback, name='slotfeedback'),
    path('slotfeedback/<int:slot_id>/', views.save_feedback, name='save_feedback'),
 # Optional success page
    path('add_favourites/<int:id>/', views.add_favourites, name='add_favourites'),
    path('remove_wishlist/<int:id>/', views.remove_wishlist, name='remove_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    # path('recurring/', views.recurring, name='recurring'),
    path('parking-spaces-map/', views.parking_spaces_map, name='parking_spaces_map'),
    path('get_nearby_shops/', views.get_nearby_shops, name='get_nearby_shops'),
    path('add_cart/<int:pid>/',views.add_cart,name='add_cart'),
    path('cart_list/',views.cart_list,name='cart_list'),
    path('initiate-payment/<cid>/', views.initiate_payment, name='initiate-payment'),
    path('confirm-payment/<order_id>/<payment_id>/<crti_id>/', views.confirm_payment, name='confirm-payment'),
    path('trans_history/', views.trans_history, name='trans_history'),
    path('transhistory/', views.transhistory, name='transhistory'),
    path('recur_list/', views.recur_list, name='recur_list'),
    path('logout/', views.logout, name='logout'),
    path('show_map/', views.show_map, name='mapp'),
    path('about/', views.about, name='about'),
    path('extrapay/<int:transaction_id>/', views.xtrapay, name='extrapay'),
    path('xrepay/', views.xrepay, name='xrepay'),
    path('update-payment-status/', views.update_payment_status, name='update_payment_status'),
    path('slotfeed/', views.slotfeed, name='slotfeed'),
    path('refundrequests/', views.refund_requests, name='refund_requests'),
    path("refund-requests/", views.refund_requests, name="refund_requests"),
    path("update-refund-status/<int:transaction_id>/<str:status>/", views.update_refund_status, name="update_refund_status"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path('request_refund/<int:transaction_id>/', views.request_refund, name='requestrefund'),
    path("approved-requests/", views.approvedrequests, name="approved_requests"),
    path('delete_cartlist/<int:id>/', views.delete_cart_item, name='delete_cart_item'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
        path('ride/', views.ride, name='ride'),
        path('solo/', views.solo, name='solo-ride'),

    

    
]


    




    # path('slotfeedback',views.slotfeedback,name='slotfeedback'),




