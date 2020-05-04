from django.urls import path
from . import views
print("Payement Called")
urlpatterns = [

    path('',views.index,name='index'),
    path('iphone/',views.iphone,name='iphone'),
    path('redmi/',views.redmi,name='redmi'),
    path('samsung/',views.samsung,name='samsung'),
    path('sale/',views.sale,name='sale'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('signup_user/',views.signup_user,name='signup_user'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout/',views.logout,name='logout'),
    path('detail/<int:pk>/',views.detail,name='detail'),
    path('feedback/<int:pk1>/<int:pk2>/',views.feedback,name='feedback'),
    path('submit_feedback/<int:pk1>/<int:pk2>/',views.submit_feedback,name='submit_feedback'),
    path('add_to_cart/<int:pk1>/<int:pk2>/',views.add_to_cart,name='add_to_cart'),
    path('mycart/',views.mycart,name='mycart'),
    path('remove_cart/<int:pk>/',views.remove_cart,name='remove_cart'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('verify_email/',views.verify_email,name='verify_email'),
    path('update_password/',views.update_password,name='update_password'),
    path('payment/', views.payment, name='payment'),
    path('myorder/',views.myorder,name='myorder'),
]