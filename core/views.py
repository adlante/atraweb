import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import (
    HeroSection,
    PillarCard,
    BentoProductionSection,
    OfflineFirstSection,
    ShowcaseProject,
    AIModelShowcase,
    FAQItem
)
from .forms import NewsletterForm, TicketForm
import datetime
from .models import SecurityTrapLog


# ------------------ Home & Core Views ------------------

def home(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    pillars = PillarCard.objects.filter(is_active=True).order_by('order')
    bento = BentoProductionSection.objects.filter(is_active=True).first()
    offline_section = OfflineFirstSection.objects.filter(is_active=True).first()
    showcase_projects = ShowcaseProject.objects.filter(is_active=True).order_by('order')[:6]
    ai_models = AIModelShowcase.objects.filter(is_active=True).order_by('order')
    faqs = FAQItem.objects.filter(is_active=True).order_by('order')

    context = {
        "hero": hero,
        "pillars": pillars,
        "bento": bento,
        "offline_section": offline_section,
        "showcase_projects": showcase_projects,
        "ai_models": ai_models,
        "faqs": faqs,
    }
    return render(request, "core/home.html", context)


def portfolio_view(request):
    """نمایش کارنامه مهندسی و ۵۰+ پروژه تخصصی آترا (شامل پروژه پرچمدار شیمکس)"""
    context = {}
    return render(request, "core/portfolio.html", context)


def submit_ticket_view(request):
    initial_data = {}

    # پر کردن نام در صورت لاگین بودن
    if request.user.is_authenticated:
        first_name = getattr(request.user, 'first_name', '') or ''
        last_name = getattr(request.user, 'last_name', '') or ''
        full_name = f"{first_name} {last_name}".strip()
        if full_name:
            initial_data['name'] = full_name

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            if request.user.is_authenticated:
                ticket.user = request.user
            ticket.save()
            messages.success(request, "درخواست پروژه شما با موفقیت ثبت شد و به زودی توسط مهندسین آترا بررسی می‌شود.")
            return redirect('core:submit_ticket')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = TicketForm(initial=initial_data)

    return render(request, 'core/ticket.html', {'form': form})


def subscribe_newsletter(request):
    """ثبت‌نام در خبرنامه تخصصی مهندسی و هوش مصنوعی"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            form = NewsletterForm(data)

            if form.is_valid():
                form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'عضویت شما در خبرنامه تخصصی با موفقیت ثبت شد!'
                })
            else:
                error_message = list(form.errors.values())[0][0]
                return JsonResponse({
                    'status': 'error',
                    'message': error_message
                })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'داده‌های ارسالی نامعتبر است.'})
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'خطایی در سیستم رخ داد. لطفاً دوباره تلاش کنید.'})

    return JsonResponse({'status': 'error', 'message': 'فقط درخواست‌های POST مجاز هستند.'})


# ------------------ Backend & API Services Views ------------------

def backend_modular_view(request):
    """رندر صفحه معماری ماژولار Django & DRF"""
    return render(request, 'core/backend/modular_django.html', {})


def backend_postgresql_view(request):
    """رندر صفحه طراحی دیتابیس و PostgreSQL"""
    return render(request, 'core/backend/postgresql_database.html', {})


def backend_otp_view(request):
    """رندر صفحه احراز هویت پیامکی OTP و JWT"""
    return render(request, 'core/backend/otp_authentication.html', {})


def backend_celery_redis_view(request):
    """رندر صفحه مدیریت صف‌های سنگین Celery/Redis"""
    return render(request, 'core/backend/backend_celery_redis.html', {})


# ------------------ Flutter Services Views ------------------

def flutter_crossplatform_view(request):
    """رندر صفحه کراس‌پلتفرم iOS و Android با فلاتر"""
    return render(request, 'core/flluter/flutter_crossplatform.html', {})


def flutter_offline_first_view(request):
    """رندر صفحه معماری آفلاین‌محور در فلاتر (Offline-First)"""
    return render(request, 'core/flluter/flutter_offline_first.html', {})


def flutter_ai_streaming_view(request):
    """رندر صفحه استریم پاسخ‌های هوش مصنوعی (SSE & WebSockets)"""
    return render(request, 'core/flluter/flutter_ai_streaming.html', {})


def flutter_memory_optimization_view(request):
    """رندر صفحه بهینه‌سازی مصرف حافظه و رندرینگ ۶۰ فریم"""
    return render(request, 'core/flluter/flutter_memory_optimization.html', {})


# ------------------ AI & LLM Services Views ------------------

def ai_rag_system_view(request):
    """رندر صفحه پایگاه دانش سازمانی RAG"""
    return render(request, 'core/ai/ai_rag_system.html', {})


def ai_vector_databases_view(request):
    """رندر صفحه پایگاه‌های برداری Vector DBs (Qdrant & pgvector)"""
    return render(request, 'core/ai/ai_vector_databases.html', {})


def ai_finetuning_lora_view(request):
    """رندر صفحه فاین‌تیونینگ مدل‌های زبانی با متد LoRA"""
    return render(request, 'core/ai/ai_finetuning_lora.html', {})


def ai_generative_studio_view(request):
    """رندر صفحه استودیوهای تولید تصویر Generative AI"""
    return render(request, 'core/ai/ai_generative_studio.html')


# ------------------ Development Plans Views ------------------

def plan_backend_api_view(request):
    """رندر صفحه پلن توسعه اختصاصی بک‌اند و API"""
    return render(request, 'core/plans/plan_backend_api.html', {})


def plan_rag_service_view(request):
    """رندر صفحه پلن پیاده‌سازی پایگاه دانش RAG سازمانی"""
    return render(request, 'core/plans/plan_rag_service.html', {})


def plan_fullstack_ai_view(request):
    """رندر صفحه پلن توسعه محصول کامل (End-to-End Product)"""
    return render(request, 'core/plans/plan_fullstack_ai.html', {})


def plan_finetune_consulting_view(request):
    """رندر صفحه پلن سفارشی‌سازی و مشاوره Fine-Tuning"""
    return render(request, 'core/plans/plan_finetune_consulting.html', {})


# ------------------ DevOps & Deployment Services Views ------------------

def devops_linux_ubuntu_view(request):
    """رندر صفحه پیکربندی و امن‌سازی سرورهای لینوکس اوبونتو"""
    return render(request, 'core/solutions/devops_linux_ubuntu.html', {})


def devops_nginx_ssl_view(request):
    """رندر صفحه کانفیگ وب‌سرور Nginx و گواهی امنیتی SSL"""
    return render(request, 'core/solutions/devops_nginx_ssl.html', {})


def devops_docker_container_view(request):
    """رندر صفحه کانتینرسازی و استقرار با Docker"""
    return render(request, 'core/solutions/devops_docker_container.html', {})


def devops_store_publishing_view(request):
    """رندر صفحه انتشار در مارکت‌ها و استورها (گوگل‌پلی، کافه‌بازار، اپ‌استور)"""
    return render(request, 'core/solutions/devops_store_publishing.html', {})


# ------------------ Legal & Information Views ------------------

def terms_view(request):
    """رندر صفحه قوانین و مقررات همکاری مهندسی"""
    return render(request, 'core/terms.html', {})


def privacy_view(request):
    """رندر صفحه حفظ محرمانگی داده‌ها و قرارداد NDA"""
    return render(request, 'core/privacy.html', {})


def help_center_view(request):
    """رندر صفحه مرکز راهنمایی و پشتیبانی"""
    return render(request, 'core/help_center.html', {})


def blog_view(request):
    """رندر صفحه وبلاگ و مقالات تخصصی استودیو آترا"""
    return render(request, 'core/blog.html', {})


def fake_admin_trap(request):
    """تله امنیتی: استخراج دقیق آی‌پی و ثبت آن در دیتابیس"""
    ip = (
            request.META.get('HTTP_CF_CONNECTING_IP') or
            request.META.get('HTTP_X_REAL_IP') or
            request.META.get('HTTP_X_FORWARDED_FOR') or
            request.META.get('REMOTE_ADDR')
    )
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    ip = ip or '127.0.0.1'
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Agent')
    remote_port = request.META.get('REMOTE_PORT', '443')
    host = request.get_host()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

    # ذخیره در دیتابیس
    try:
        SecurityTrapLog.objects.create(
            ip_address=ip,
            user_agent=user_agent,
            path_attempted=request.path
        )
    except Exception:
        pass

    context = {
        'client_ip': ip,
        'user_agent': user_agent,
        'remote_port': remote_port,
        'host': host,
        'timestamp': current_time,
    }
    return render(request, 'core/fake_admin.html', context, status=403)
