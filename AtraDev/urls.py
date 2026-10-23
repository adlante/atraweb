"""
URL configuration for AtraDev project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.http import HttpResponse

from core.views import fake_admin_trap
from core.sitemaps import AtraStaticSitemap

# دیکشنری نقشه‌های سایت برای موتورهای جستجو
sitemaps = {
    'static': AtraStaticSitemap,
}

urlpatterns = [
    # ------------------ سئو تکنیکال و ربات‌های گوگل / بینگ ------------------
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name='robots_file'),
    path('123229e81f9d4920afcf8a299f323e7a.txt', lambda r: HttpResponse('123229e81f9d4920afcf8a299f323e7a', content_type='text/plain'), name='indexnow_key'),

    # ------------------ امنیت و تله نفوذ ------------------
    path('admin/', fake_admin_trap, name='fake_admin'),

    # ------------------ پنل ادمین اصلی ------------------
    path('atra-studio-vault/', admin.site.urls),

    # ------------------ اپلیکیشن‌ها ------------------
    path('', include('core.urls', namespace='core')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)