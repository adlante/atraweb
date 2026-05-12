from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.views import View
from django.contrib.auth import logout, authenticate
from .forms import RegisterForm, LoginForm, CheckoutProfileForm, CustomPasswordChangeForm
from .utils import generate_otp_code, send_otp_sms
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.http import JsonResponse
import random
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import PricingPlan, Profile
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.db.models import Q

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


@login_required(login_url='accounts:login')
def checkout_view(request, plan_id):
    # قدم اول: پیدا کردن پلن انتخابی کاربر
    # چون plan_id از سمت جاوااسکریپت به صورت متن میاد (مثل 'advanced')
    # باید بر اساس فیلدی مثل slug یا name توی دیتابیس بگردیم، نه id.
    plan = get_object_or_404(PricingPlan, slug=plan_id)

    # قدم دوم: پیدا کردن یا ساختن پروفایل کاربر (ضدگلوله و دقیق)
    profile, created = Profile.objects.get_or_create(user=request.user)

    # قدم سوم: دریافت شماره تلفن کاربر (فرض بر این است که در مدل User ذخیره شده)
    user_phone = getattr(request.user, 'phone_number', '')

    # قدم چهارم: پردازش فرم تکمیل اطلاعات کاربر
    if request.method == 'POST':
        form = CheckoutProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات شما با موفقیت ثبت شد و پروفایل تکمیل گردید.')

            # بعد از ذخیره اطلاعات، کاربر را به درگاه پرداخت یا صفحه تایید هدایت کن
            return redirect('accounts:profile_dashboard')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')

    else:
        # اگر درخواست GET بود، فرم را با اطلاعات فعلی پروفایل پر می‌کنیم
        form = CheckoutProfileForm(instance=profile)

    # قدم پنجم: ارسال تمام دیتاهای مورد نیاز به سمت فرانت‌اند
    context = {
        'form': form,
        'plan': plan,
        'plan_id': plan_id,
        'user_phone': user_phone,
    }

    return render(request, 'accounts/dashboard/checkout.html', context)


class AjaxPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    این ویو برای تغییر رمز عبور از طریق AJAX طراحی شده.
    از فرم سفارشی CustomPasswordChangeForm برای اعتبارسنجی‌های پیشرفته استفاده می‌کنه.
    """
    # اتصال ویو به فرم سفارشی
    form_class = CustomPasswordChangeForm

    # این دو مورد برای حالت غیر-AJAX لازم هستند، اما ما آن‌ها را override می‌کنیم.
    template_name = 'accounts/partials/password_change_form.html'  # یک تمپلیت که فقط شامل فرم باشه
    success_url = reverse_lazy('accounts:dashboard')  # آدرس بازگشتی در صورت موفقیت (غیر-AJAX)

    def dispatch(self, request, *args, **kwargs):
        # این متد قبل از بقیه اجرا می‌شه. اطمینان حاصل می‌کنیم که فقط درخواست‌های AJAX پذیرفته بشن.
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # اگر درخواست AJAX نبود، می‌تونی یک خطای 400 برگردونی یا به یک صفحه دیگه هدایتش کنی
            return JsonResponse({'error': 'فقط درخواست‌های AJAX مجاز هستند.'}, status=400)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        وقتی فرم کاملاً معتبر باشه، این متد اجرا می‌شه.
        رمز عبور رو ذخیره می‌کنه و پاسخ موفقیت JSON برمی‌گردونه.
        """
        form.save()
        # این خط حیاتیه! برای اینکه کاربر بعد از تغییر رمز از حسابش خارج نشه.
        update_session_auth_hash(self.request, form.user)

        return JsonResponse({
            'success': True,
            'message': 'رمز عبور شما با موفقیت به‌روزرسانی شد.'
        })

    def form_invalid(self, form):
        """
        وقتی فرم دارای خطا باشه (رمز فعلی اشتباه، عدم تطابق رمزهای جدید و ...)،
        این متد اجرا می‌شه و خطاها رو در یک فرمت JSON تمیز برمی‌گردونه.
        """
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


def password_reset_request_view(request):
    """
    مرحله ۱: دریافت نام کاربری/ایمیل، تولید کد و ارسال پیامک
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        # نام فیلد در HTML که ساختی username_or_email بود
        identifier = request.POST.get('username_or_email', '').strip()

        if identifier:
            try:
                # کاربر رو با نام کاربری یا ایمیل پیدا می‌کنیم
                user = User.objects.get(Q(username=identifier) | Q(email=identifier))

                # تولید کد ۵ رقمی و استخراج شماره تلفن
                otp_code = generate_otp_code()
                user_phone = user.phone  # فرض بر این است که شماره در user.phone ذخیره شده

                # ارسال پیامک
                sms_sent = send_otp_sms(user_phone, otp_code)

                if sms_sent:
                    # ذخیره در سشن برای مراحل بعدی
                    request.session['reset_user_id'] = str(user.id)
                    request.session['reset_otp_code'] = str(otp_code)

                    messages.success(request, "کد تایید با موفقیت ارسال شد.")
                    return redirect('accounts:password_reset_verify')
                else:
                    messages.error(request, "ارسال پیامک با خطا مواجه شد. لطفاً دوباره تلاش کنید.")

            except User.DoesNotExist:
                # برای امنیت بیشتر، بهتره پیام کلی بدیم تا هکرها نتونن نام‌های کاربری رو حدس بزنن
                messages.error(request, "حساب کاربری با این مشخصات یافت نشد.")
        else:
            messages.error(request, "لطفاً نام کاربری یا ایمیل خود را وارد کنید.")

    return render(request, 'accounts/password_reset_request.html')


def password_reset_verify_view(request):
    """
    مرحله ۲: بررسی کد تایید وارد شده توسط کاربر
    """
    user_id = request.session.get('reset_user_id')
    saved_otp = request.session.get('reset_otp_code')

    # اگر دیتای سشن وجود نداشت، کاربر رو برمی‌گردونیم به مرحله اول
    if not user_id or not saved_otp:
        messages.warning(request, "نشست شما نامعتبر یا منقضی شده است. لطفاً دوباره تلاش کنید.")
        return redirect('accounts:password_reset_request')

    if request.method == 'POST':
        # نام فیلد در HTML شما code بود
        entered_otp = request.POST.get('code', '').strip()

        if entered_otp == saved_otp:
            # کد درسته! یک پرچم (flag) تو سشن می‌ذاریم که کاربر مجازه رمز رو عوض کنه
            request.session['reset_is_verified'] = True
            return redirect('accounts:password_reset_confirm')
        else:
            messages.error(request, "کد وارد شده اشتباه است.")

    return render(request, 'accounts/password_reset_verify.html')


def password_reset_confirm_view(request):
    """
    مرحله ۳: دریافت رمز عبور جدید، هش کردن و ذخیره در دیتابیس
    """
    user_id = request.session.get('reset_user_id')
    is_verified = request.session.get('reset_is_verified')

    # بررسی امنیتی: آیا کاربر مرحله تایید کد رو با موفقیت گذرونده؟
    if not user_id or not is_verified:
        messages.error(request, "دسترسی غیرمجاز! لطفاً مراحل فراموشی رمز را از ابتدا طی کنید.")
        return redirect('accounts:password_reset_request')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not new_password or not confirm_password:
            messages.error(request, "لطفاً هر دو فیلد رمز عبور را پر کنید.")
        elif new_password != confirm_password:
            messages.error(request, "رمز عبور جدید و تکرار آن با هم مطابقت ندارند.")
        elif len(new_password) < 8:
            messages.error(request, "رمز عبور باید حداقل ۸ کاراکتر باشد.")
        else:
            try:
                # پیدا کردن کاربر و تغییر رمز
                user = User.objects.get(id=user_id)
                user.set_password(new_password)  # این متد به صورت خودکار رمز رو هش (Hash) می‌کنه
                user.save()

                # پاکسازی سشن‌ها (بسیار مهم برای امنیت)
                request.session.pop('reset_user_id', None)
                request.session.pop('reset_otp_code', None)
                request.session.pop('reset_is_verified', None)

                messages.success(request, "رمز عبور شما با موفقیت تغییر کرد! حالا می‌توانید وارد شوید.")
                return redirect('accounts:login')

            except User.DoesNotExist:
                messages.error(request, "خطایی رخ داده است. کاربر یافت نشد.")
                return redirect('accounts:password_reset_request')

    return render(request, 'accounts/password_reset_confirm.html')