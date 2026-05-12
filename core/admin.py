from django.contrib import admin
from .models import Banner, PricingPlan, AppVideoSection, Partner, Newsletter, Ticket, PlanSingle


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست اصلی ادمین نمایش داده میشن
    list_display = (
        'title',
        'iphone_image_preview',
        'android_image_preview',
        'is_active',
        'updated_at'
    )

    # فیلترهای کناری پنل
    list_filter = ('is_active', 'created_at')

    # قابلیت جستجو
    search_fields = ('title', 'highlight_text', 'subtitle')

    # دسته‌بندی فیلدها در صفحه ویرایش/افزودن
    fieldsets = (
        ('محتوای متنی', {
            'fields': ('title', 'highlight_text', 'subtitle')
        }),
        ('دکمه‌ها و لینک‌های دانلود', {
            'fields': (
                ('app_store_url', 'apple_store_image', 'apple_store_preview'),
                ('google_play_url', 'google_play_image', 'google_play_preview')
            ),
            'classes': ('collapse',),  # این بخش به صورت کشویی درمیاد که شلوغ نشه
        }),
        ('تصاویر موکاپ', {
            'fields': (
                'iphone_image', 'iphone_image_preview',
                'android_image', 'android_image_preview'
            )
        }),
        ('تنظیمات', {
            'fields': ('is_active',)
        }),
    )

    # فقط خواندنی کردن پیش‌نمایش تصاویر در صفحه ویرایش
    readonly_fields = (
        'iphone_image_preview',
        'android_image_preview',
        'apple_store_preview',
        'google_play_preview'
    )

    # اکشن اختصاصی برای فعال/غیرفعال کردن سریع گروهی
    actions = ['make_active', 'make_inactive']

    @admin.action(description='فعال کردن بنرهای انتخاب شده')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='غیرفعال کردن بنرهای انتخاب شده')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    search_fields = ('name', 'description')


@admin.register(AppVideoSection)
class AppVideoSectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')
    list_editable = ('is_active',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'joined_at')
    search_fields = ('email',)
    list_filter = ('joined_at',)
    readonly_fields = ('joined_at',)
    ordering = ('-joined_at',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'department', 'status', 'created_at')
    list_filter = ('status', 'department', 'created_at')
    search_fields = ('subject', 'name', 'phone', 'message')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)

    # گروه‌بندی فیلدها در صفحه جزئیات
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'name', 'phone')
        }),
        ('جزئیات تیکت', {
            'fields': ('department', 'subject', 'message')
        }),
        ('وضعیت و زمان', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )


@admin.register(PlanSingle)
class PlanSingleAdmin(admin.ModelAdmin):
    # ستون‌هایی که تو لیست ادمین نمایش داده میشن
    list_display = ('title', 'slug', 'price', 'period', 'is_active')

    # امکان فیلتر کردن بر اساس وضعیت فعال بودن
    list_filter = ('is_active', 'period')

    # امکان جستجو در عنوان و شناسه
    search_fields = ('title', 'slug')

    # پر شدن خودکار slug از روی عنوان (اختیاری، ولی کار رو راحت می‌کنه)
    prepopulated_fields = {'slug': ('title',)}

    # دسته‌بندی فیلدها در صفحه ویرایش برای زیبایی بیشتر
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'subtitle', 'is_active')
        }),
        ('اطلاعات مالی', {
            'fields': ('price', 'period')
        }),
        ('ظاهر و استایل', {
            'fields': ('badge_text', 'theme_color')
        }),
    )