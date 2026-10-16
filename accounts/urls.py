from django.urls import path
from .views import (
    RegisterView,
    login_view,
    UserLogoutView,
    verify_otp_view,
    resend_otp_view,
    profile_dashboard_view,
    checkout_view,
)

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path("verify/", verify_otp_view, name="verify_otp"),
    path('verify/resend/', resend_otp_view, name='resend_otp'),

    # مسیرهای مربوط به داشبورد
    path('dashboard/profile/', profile_dashboard_view, name='profile_dashboard'),

    # مسیر جدید فرم تکمیل اطلاعات کاربری قبل از پرداخت
    path('dashboard/checkout/<str:plan_id>/', checkout_view, name='dashboard_checkout'),
]
