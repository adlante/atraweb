from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AtraStaticSitemap(Sitemap):
    """نقشه سایت استاندارد و با اولویت‌بندی برای کراولر گوگل"""
    protocol = 'https'

    def items(self):
        # ساختار: (نام ویو در urls, اولویت سئو, دوره آپدیت)
        return [
            # صفحات اصلی و کلیدی
            ('core:home', 1.0, 'daily'),
            ('core:portfolio', 0.9, 'weekly'),
            ('core:blog', 0.9, 'daily'),
            ('core:submit_ticket', 0.8, 'weekly'),

            # راهکارهای هوش مصنوعی و RAG (هسته بازاریابی و رتبه ۱)
            ('core:ai_rag_system', 0.95, 'weekly'),
            ('core:ai_vector_databases', 0.9, 'weekly'),
            ('core:ai_finetuning_lora', 0.9, 'weekly'),
            ('core:ai_generative_studio', 0.9, 'weekly'),

            # راهکارهای بک‌اند و صف‌ها
            ('core:backend_modular', 0.85, 'weekly'),
            ('core:backend_postgresql', 0.85, 'weekly'),
            ('core:backend_otp', 0.85, 'weekly'),
            ('core:backend_celery_redis', 0.9, 'weekly'),

            # راهکارهای فلاتر
            ('core:flutter_crossplatform', 0.85, 'weekly'),
            ('core:flutter_offline_first', 0.9, 'weekly'),
            ('core:flutter_ai_streaming', 0.85, 'weekly'),
            ('core:flutter_memory_optimization', 0.85, 'weekly'),

            # پلن‌های تجاری
            ('core:plan_backend_api', 0.8, 'monthly'),
            ('core:plan_rag_service', 0.85, 'monthly'),
            ('core:plan_fullstack_ai', 0.85, 'monthly'),
            ('core:plan_finetune_consulting', 0.8, 'monthly'),

            # سرور و دواپس
            ('core:devops_linux_ubuntu', 0.8, 'monthly'),
            ('core:devops_nginx_ssl', 0.8, 'monthly'),
            ('core:devops_docker_container', 0.8, 'monthly'),
            ('core:devops_store_publishing', 0.8, 'monthly'),

            # صفحات حقوقی
            ('core:terms', 0.4, 'yearly'),
            ('core:privacy', 0.4, 'yearly'),
            ('core:help_center', 0.6, 'monthly'),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]