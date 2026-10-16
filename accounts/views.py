from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.views import View
from django.contrib.auth import logout, authenticate
from .forms import RegisterForm, LoginForm
from .utils import generate_otp_code, send_otp_sms
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.http import JsonResponse
import random
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import PricingPlan
from django.utils.http import url_has_allowed_host_and_scheme

User = get_user_model()


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "شما از قبل وارد حساب کاربری خود شده‌اید.")
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)

    # 🚀 این متد اضافه شد تا ارور VariableDoesNotExist کلا نابود بشه!
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # استخراج ایمن next از GET یا POST و ارسال به عنوان یه متغیر ساده به تمپلیت
        context['next_url'] = self.request.POST.get('next') or self.request.GET.get('next') or ''
        return context

    def form_valid(self, form):
        # کاربر ذخیره میشه اما دیگه لاگین نمیشه تا مجبور بشه پروسه احراز هویت رو طی کنه
        form.save()

        messages.success(self.request, "ثبت‌نام با موفقیت انجام شد! لطفاً برای ادامه وارد حساب کاربری خود شوید.")

        # استخراج next به صورت ایمن
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        login_url = reverse('accounts:login')

        # اگر next وجود داشت، کاربر رو با همون next می‌فرستیم صفحه لاگین
        if next_url:
            return redirect(f"{login_url}?next={next_url}")
        else:
            return redirect(login_url)

    def form_invalid(self, form):
        messages.error(self.request, "ثبت‌نام با خطا مواجه شد. لطفاً فرم را با دقت بررسی کنید.")
        return super().form_invalid(form)


def login_view(request):
    # اگر کاربر لاگین است، مستقیماً به صفحه اصلی هدایت شود
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            # استخراج دیتای تمیز شده از فرم
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = None
            try:
                # ۱. جستجوی مستقیم کاربر با نام کاربری
                user_obj = User.objects.get(username=username)

                # ۲. بررسی امن و رمزنگاری‌شده پسورد
                if user_obj.check_password(password):
                    user = user_obj
                    # 🔥 نکته فوق‌حیاتی: برای اینکه تابع login() در مرحله بعد (verify_otp)
                    # دچار ارور نشود، باید backend را به صورت دستی ست کنیم:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
            except User.DoesNotExist:
                # اگر کاربری با این نام کاربری اصلاً وجود نداشت
                pass

            if user is not None:

                # 💥 احراز هویت مرحله اول موفق بود 💥

                # ۱. تولید کد تایید ۵ رقمی
                otp_code = generate_otp_code()

                # ۲. استخراج شماره موبایل کاربر از دیتابیس (چون کاربر با username لاگین کرده است)
                user_phone = user.phone

                # ۳. ارسال پیامک به شماره موبایل کاربر
                sms_sent = send_otp_sms(user_phone, otp_code)

                if sms_sent:
                    masked_phone = f"{user_phone[:4]}***{user_phone[-4:]}"

                    request.session['auth_user_id'] = str(user.id)
                    request.session['otp_code'] = otp_code
                    request.session['masked_phone'] = masked_phone

                    # 🔥 تغییر حیاتی: ذخیره next_url در سشن برای استفاده در صفحه verify_otp 🔥
                    # دقت کن که باید قبل از این خط، next_url رو استخراج کرده باشی
                    current_next_url = request.POST.get('next') or request.GET.get('next')
                    if current_next_url:
                        request.session['next_url'] = current_next_url

                    return redirect('accounts:verify_otp')
                else:
                    messages.error(request, "متأسفانه در ارسال پیامک مشکلی رخ داد. لطفاً دوباره تلاش کنید.")
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")

        else:
            # اگر فرم ولید نباشد
            messages.error(request, "لطفاً اطلاعات را با فرمت صحیح وارد کنید.")
    else:
        # اگر درخواست GET بود، یک فرم خالی می‌سازیم
        form = LoginForm()

    next_url = request.POST.get('next') or request.GET.get('next')
    # فرم را حتماً به کانتکست پاس می‌دهیم تا در HTML رندر شود
    context = {
        'form': form,
        'next_url': next_url,
    }
    return render(request, 'accounts/login.html', context)


class UserLogoutView(View):
    """
    ویو حرفه‌ای برای خروج کاربر.
    """

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "با موفقیت از حساب کاربری خود خارج شدید.", "success")
        return redirect('core:home')


def verify_otp_view(request):
    """
    ویوی بررسی کد تایید پیامکی و تکمیل فرآیند ورود دو مرحله‌ای
    """
    user_id = request.session.get('auth_user_id')
    saved_otp = str(request.session.get('otp_code'))
    masked_phone = request.session.get('masked_phone')

    if not user_id or not saved_otp:
        messages.warning(request, "نشست شما منقضی شده یا نامعتبر است. لطفاً ابتدا لاگین کنید.")
        return redirect('accounts:login')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code')

        if entered_otp == saved_otp:
            try:
                user = User.objects.get(id=user_id)

                # تایید شماره موبایل در دیتابیس
                if not getattr(user, 'is_verified', True):
                    user.is_verified = True
                    user.save()

                # 🔥 لاگین کاربر در سیستم 🔥
                login(request, user)

                # پاکسازی اطلاعات موقت احراز هویت از سشن
                request.session.pop('auth_user_id', None)
                request.session.pop('otp_code', None)
                request.session.pop('masked_phone', None)

                messages.success(request, "خوش آمدید! ورود با موفقیت انجام شد.")

                # ==========================================
                # 💥 جادوی انتقال مسیر (next) با امنیت کامل 💥
                # ==========================================
                # ۱. استخراج next_url از سشن
                next_url = request.session.pop('next_url', None)

                # ۲. ریدایرکت امن با بررسی دامین مجاز
                if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                else:
                    return redirect('core:home')
                # ==========================================

            except User.DoesNotExist:
                messages.error(request, "کاربر مورد نظر یافت نشد.")
                return redirect('accounts:login')
        else:
            messages.error(request, "کد تایید وارد شده اشتباه است. لطفاً دوباره بررسی کنید.")

    context = {
        'masked_phone': masked_phone
    }
    return render(request, 'accounts/verify.html', context)


@require_POST
def resend_otp_view(request):
    """
    ویوی AJAX برای ارسال مجدد کد تایید
    """
    user_id = request.session.get('auth_user_id')

    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'نشست شما منقضی شده است. لطفا دوباره لاگین کنید.'},
                            status=400)

    try:
        user = User.objects.get(id=user_id)

        # تولید کد ۵ رقمی جدید
        new_otp = str(random.randint(10000, 99999))
        request.session['otp_code'] = new_otp

        send_otp_sms(user.phone, new_otp)

        print(f"--- [RESEND] New OTP for user {user.phone} is: {new_otp} ---")

        return JsonResponse({'status': 'success', 'message': 'کد تایید جدید با موفقیت پیامک شد.'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'کاربر یافت نشد.'}, status=404)


@login_required(login_url='accounts:login')
def profile_dashboard_view(request):
    plans = PricingPlan.objects.prefetch_related('features').all()

    context = {
        'has_license': False,
        'plans': plans,
    }

    return render(request, 'accounts/dashboard/profile.html', context)


@login_required
def checkout_view(request, plan_id):
    # فرض می‌کنیم شماره تلفن در مدل یوزر شما ذخیره شده است
    # اگر شماره تلفن وجود داشته باشد، آن را به تمپلیت می‌فرستیم
    context = {
        'plan_id': plan_id,
        'user_phone': getattr(request.user, 'phone_number', '')  # جایگزین با فیلد دقیق مدل خودت
    }
    return render(request, 'accounts/dashboard/checkout.html', context)
