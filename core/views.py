from django.shortcuts import render, redirect, get_object_or_404
from .models import Banner, PricingPlan, AppVideoSection, Partner, PlanSingle
from django.http import JsonResponse
import json
from .forms import NewsletterForm, TicketForm
from django.contrib import messages


def home(request):
    # گرفتن آخرین بنری که در پنل ادمین فعال شده است
    banner = Banner.objects.filter(is_active=True).first()
    pricing_plans = PricingPlan.objects.order_by('order')
    videos = AppVideoSection.objects.filter(is_active=True).first()
    partners = Partner.objects.filter(is_active=True).order_by('order')
    context = {
        "banner": banner,
        "pricing_plans": pricing_plans,
        "videos": videos,
        "partners": partners,
    }
    return render(request, "core/home.html", context)


def subscribe_newsletter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            form = NewsletterForm(data)

            if form.is_valid():
                form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'عضویت شما با موفقیت ثبت شد!'
                })
            else:
                # گرفتن اولین ارور (مثلاً ارور فرمت نامعتبر یا تکراری بودن)
                error_message = list(form.errors.values())[0][0]
                return JsonResponse({
                    'status': 'error',
                    'message': error_message
                })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'داده‌های ارسالی نامعتبر است.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'خطایی در سیستم رخ داد. لطفاً دوباره تلاش کنید.'})

    return JsonResponse({'status': 'error', 'message': 'فقط درخواست‌های POST مجاز هستند.'})


def submit_ticket_view(request):
    initial_data = {}

    # بررسی لاگین بودن کاربر و پر کردن خودکار اطلاعات
    if request.user.is_authenticated:
        initial_data['phone'] = getattr(request.user, 'phone', '')  # فرض بر اینکه فیلد موبایل phone است

        # جلوگیری از چاپ None None
        first_name = getattr(request.user, 'first_name', '') or ''
        last_name = getattr(request.user, 'last_name', '') or ''
        full_name = f"{first_name} {last_name}".strip()

        if full_name:
            initial_data['name'] = full_name

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # اگر کاربر لاگین بود، تیکت رو به یوزرش وصل کن
            if request.user.is_authenticated:
                ticket.user = request.user
            ticket.save()
            messages.success(request, "تیکت شما با موفقیت ثبت شد و به زودی بررسی می‌شود.")
            return redirect('core:help_center')
        else:
            # نمایش خطاهای فرم به کاربر
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = TicketForm(initial=initial_data)

    return render(request, 'core/ticket.html', {'form': form})


def infrastructure_costs(request):
    context = {}
    return render(request, 'core/costs.html', context)


def about_us(request):
    context = {
    }
    return render(request, 'core/about_us.html', context)


def feature_offline_first(request):
    context = {}
    return render(request, 'core/features/offline_first.html', context)


def feature_decentralized(request):
    context = {}
    return render(request, 'core/features/decentralized.html', context)


def feature_smart_backup(request):
    context = {}
    return render(request, 'core/features/smart_backup.html', context)


def feature_stability(request):
    context = {}
    return render(request, 'core/features/stability.html', context)


def pricing_method(request):
    context = {}
    return render(request, 'core/pricing.html', context)


def plan_economic(request):
    plan = get_object_or_404(PlanSingle, slug='economic')

    context = {
        'plan': plan
    }
    return render(request, 'core/plans/economic.html', context)


def plan_advanced(request):
    """ رندر کردن صفحه اختصاصی پلن پیشرفته با دیتای داینامیک از دیتابیس """

    # 1. گرفتن دیتای پلن پیشرفته از دیتابیس با استفاده از اسلاگ دقیق
    plan = get_object_or_404(PlanSingle, slug='advanced')

    # 2. قرار دادن آبجکت پلن داخل کانتکست برای ارسال به فرانت‌اند
    context = {
        'plan': plan
    }

    # 3. رندر کردن صفحه به همراه دیتای کانتکست
    return render(request, 'core/plans/advanced.html', context)


def plan_professional(request):
    """ رندر کردن صفحه اختصاصی پلن حرفه‌ای با دیتای کاملا داینامیک """

    # اینجا پلن رو با اسلاگ دقیق دریافت می‌کنیم
    plan = get_object_or_404(PlanSingle, slug='professional')

    # ارسال پلن به عنوان کانتکست (context) به قالب HTML
    context = {
        'plan': plan
    }
    return render(request, 'core/plans/professional.html', context)


def plan_custom(request):
    plan = get_object_or_404(PlanSingle, slug='custom')

    # ارسال پلن به عنوان کانتکست (context) به قالب HTML
    context = {
        'plan': plan
    }
    return render(request, 'core/plans/custom.html', context)


def article_ai(request):
    """ رندر کردن صفحه مقاله هوش مصنوعی در حسابداری """
    context = {}
    return render(request, 'core/article/ai-article.html', context)


def article_reporting(request):
    """ رندر کردن صفحه مقاله گزارش‌گیری مالی """
    context = {}
    return render(request, 'core/article/reporting-article.html', context)


def article_debt_collection(request):
    """ رندر کردن صفحه مقاله وصول مطالبات """
    context = {}
    return render(request, 'core/article/debt-collection-article.html', context)


# ------------------ Solutions Views ------------------

def solution_smb(request):
    """ رندر کردن صفحه راهکار کسب‌وکارهای کوچک و متوسط """
    context = {}
    return render(request, 'core/solutions/smb.html', context)


def solution_ecommerce(request):
    """ رندر کردن صفحه راهکار فروشگاه‌های اینترنتی """
    context = {}
    return render(request, 'core/solutions/ecommerce.html', context)


def solution_b2b(request):
    """ رندر کردن صفحه راهکار شرکت‌های خدماتی و B2B """
    context = {}
    return render(request, 'core/solutions/b2b.html', context)


def solution_freelancer(request):
    """ رندر کردن صفحه راهکار مشاغل آزاد و فریلنسرها """
    context = {}
    return render(request, 'core/solutions/freelancer.html', context)


def terms_view(request):
    """
    ویوی مربوط به صفحه قوانین و مقررات (Terms and Conditions)
    """
    return render(request, 'core/terms.html')


def privacy_view(request):
    """
    ویوی مربوط به صفحه حریم خصوصی (Privacy Policy)
    """
    return render(request, 'core/privacy.html')


def blog_view(request):
    """نمایش صفحه وبلاگ و مقالات"""
    return render(request, 'core/blog.html')


def help_center_view(request):
    """نمایش صفحه مرکز راهنمایی و پشتیبانی"""
    return render(request, 'core/help_center.html')


def developers_view(request):
    """نمایش مستندات توسعه‌دهندگان و API"""
    return render(request, 'core/developers.html')





