from django.db import models
from django.utils.html import mark_safe
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model


class Banner(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="عنوان اصلی"
    )
    highlight_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="متن هایلایت (برجسته)"
    )
    subtitle = models.TextField(
        max_length=500,
        verbose_name="متن توضیحات (زیرنویس)"
    )

    # لینک‌های دانلود اپلیکیشن
    app_store_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="لینک اپ استور"
    )
    google_play_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="لینک گوگل پلی"
    )

    # --- فیلدهای جدید: تصاویر دکمه‌های دانلود ---
    apple_store_image = models.ImageField(
        upload_to='banners/store_buttons/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp', 'svg'])],
        blank=True,
        null=True,
        verbose_name="تصویر دکمه اپ استور"
    )
    google_play_image = models.ImageField(
        upload_to='banners/store_buttons/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp', 'svg'])],
        blank=True,
        null=True,
        verbose_name="تصویر دکمه گوگل پلی"
    )

    # تصاویر موکاپ گوشی‌ها
    iphone_image = models.ImageField(
        upload_to='banners/iphone/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])],
        verbose_name="تصویر داخل آیفون"
    )
    android_image = models.ImageField(
        upload_to='banners/android/',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])],
        verbose_name="تصویر داخل اندروید"
    )

    # تنظیمات مدیریتی
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال باشد؟",
        help_text="اگر فعال باشد در صفحه اصلی نمایش داده می‌شود."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "بنر صفحه اصلی"
        verbose_name_plural = "بنرهای صفحه اصلی"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {'(فعال)' if self.is_active else '(غیرفعال)'}"

    # متدهای پیش‌نمایش تصاویر موکاپ
    def iphone_image_preview(self):
        if self.iphone_image:
            return mark_safe(
                f'<img src="{self.iphone_image.url}" width="80" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />')
        return "بدون تصویر"

    iphone_image_preview.short_description = 'پیش‌نمایش آیفون'

    def android_image_preview(self):
        if self.android_image:
            return mark_safe(
                f'<img src="{self.android_image.url}" width="80" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />')
        return "بدون تصویر"

    android_image_preview.short_description = 'پیش‌نمایش اندروید'

    # --- متدهای جدید: پیش‌نمایش دکمه‌های دانلود ---
    def apple_store_preview(self):
        if self.apple_store_image:
            return mark_safe(f'<img src="{self.apple_store_image.url}" height="40" style="border-radius: 4px;" />')
        return "بدون تصویر"

    apple_store_preview.short_description = 'نمایش دکمه اپل'

    def google_play_preview(self):
        if self.google_play_image:
            return mark_safe(f'<img src="{self.google_play_image.url}" height="40" style="border-radius: 4px;" />')
        return "بدون تصویر"

    google_play_preview.short_description = 'نمایش دکمه گوگل'


class PricingPlan(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام پلن (مثل: اقتصادی)")
    description = models.TextField(verbose_name="توضیحات پلن")
    icon_svg = models.TextField(verbose_name="کد SVG آیکون", help_text="کد تگ <svg> را کامل اینجا کپی کنید.")

    # ادمین امکانات را زیر هم تایپ می‌کند
    features = models.TextField(verbose_name="امکانات پلن",
                                help_text="هر ویژگی را در یک خط بنویسید (با Enter جدا کنید).")

    is_featured = models.BooleanField(default=False, verbose_name="آیا پیشنهاد ویژه است؟")
    badge_text = models.CharField(max_length=50, blank=True, null=True, default="پیشنهاد ویژه",
                                  verbose_name="متن نشان ویژه")

    button_text = models.CharField(max_length=50, verbose_name="متن دکمه (مثل: شروع اقتصادی)")
    button_url = models.CharField(max_length=255, default="#", verbose_name="لینک دکمه")

    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "پلن قیمت‌گذاری"
        verbose_name_plural = "پلن‌های قیمت‌گذاری"
        ordering = ['order']

    def __str__(self):
        return self.name

    # این تابع شاهکار ماست! متن‌ها رو خط به خط جدا میکنه تا تو تمپلیت حلقه بزنیم روشون
    def get_features_list(self):
        return [feature.strip() for feature in self.features.split('\n') if feature.strip()]


class AppVideoSection(models.Model):
    customers_video = models.FileField(upload_to='videos/home/', blank=True, null=True,
                                       verbose_name="ویدیو تجربه مشتریان")
    founder_video = models.FileField(upload_to='videos/home/', blank=True, null=True,
                                     verbose_name="ویدیو سخنی از سازنده")
    about_video = models.FileField(upload_to='videos/home/', blank=True, null=True, verbose_name="ویدیو درباره اپ آترا")
    tutorial_video = models.FileField(upload_to='videos/home/', blank=True, null=True,
                                      verbose_name="ویدیو آموزش اپلیکیشن")
    is_active = models.BooleanField(default=True, verbose_name="نمایش در سایت")

    class Meta:
        verbose_name = "ویدیوهای صفحه اصلی"
        verbose_name_plural = "ویدیوهای صفحه اصلی"

    def __str__(self):
        return "تنظیمات ویدیوهای سایت"


class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام شرکت")
    logo = models.ImageField(upload_to='partners/logos/', verbose_name="لوگوی شرکت")
    is_active = models.BooleanField(default=True, verbose_name="نمایش در سایت")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "همکار"
        verbose_name_plural = "همکاران ما"
        ordering = ['order', '-id']  # مرتب‌سازی بر اساس ترتیب، سپس جدیدترین‌ها

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")

    class Meta:
        verbose_name = "عضو خبرنامه"
        verbose_name_plural = "اعضای خبرنامه"

    def __str__(self):
        return self.email


User = get_user_model()


class Ticket(models.Model):
    DEPARTMENT_CHOICES = (
        ('tech', 'پشتیبانی فنی'),
        ('sales', 'فروش و مشاوره'),
        ('finance', 'امور مالی و حسابداری'),
        ('other', 'سایر موارد'),
    )

    STATUS_CHOICES = (
        ('open', 'باز'),
        ('pending', 'در حال بررسی'),
        ('closed', 'بسته شده'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کاربر")
    name = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='tech', verbose_name="دپارتمان")
    subject = models.CharField(max_length=255, verbose_name="موضوع تیکت")
    message = models.TextField(verbose_name="متن پیام")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"


class PlanSingle(models.Model):
    slug = models.SlugField(max_length=50, unique=True, verbose_name="شناسه انگلیسی پلن (Slug)")
    title = models.CharField(max_length=255, verbose_name="عنوان پلن")
    subtitle = models.TextField(verbose_name="توضیحات زیر عنوان", blank=True, null=True)

    # تغییر مهم اینجا اعمال شد: null=True و blank=True اضافه شد
    price = models.PositiveIntegerField(
        verbose_name="قیمت (تومان)",
        null=True,
        blank=True,
        help_text="برای قیمت «توافقی» این فیلد را کاملاً خالی بگذارید."
    )

    period = models.CharField(max_length=50, default="سالانه", verbose_name="دوره پرداخت")

    badge_text = models.CharField(max_length=100, blank=True, null=True,
                                  verbose_name="متن بج (مثل: پرطرفدارترین انتخاب)")
    theme_color = models.CharField(max_length=20, default="#059669", help_text="کد رنگ هگز، مثلا #DC8214",
                                   verbose_name="رنگ تم پلن")

    is_active = models.BooleanField(default=True, verbose_name="فعال است؟")

    class Meta:
        verbose_name = "پلن پایه‌ای"
        verbose_name_plural = "پلن‌های پایه‌ای"
        # دقت کن: مقادیر خالی (Null) در مرتب‌سازی ممکنه اول یا آخر بیان.
        # معمولا در دیتابیس‌ها مقادیر Null اول قرار می‌گیرند.
        ordering = ['price']

    @property
    def persian_price(self):
        """
        این متد قیمت را خوانده، چک می‌کند که آیا سفارشی است یا خیر،
        سپس در صورت نیاز به عدد، سه رقم سه رقم جدا کرده و فارسی می‌کند.
        """
        # جادوی اصلی اینجاست: اگر تو ادمین قیمت رو وارد نکنی، میگه توافقی!
        if self.price is None:
            return "توافقی / تماس بگیرید"

        # یه آپشن جذاب دیگه: اگه عدد صفر وارد کردی بگه رایگان! (اختیاری)
        if self.price == 0:
            return "رایگان"

        # مرحله ۱: تبدیل به رشته و جدا کردن سه رقم سه رقم با کاما
        formatted_price = f"{self.price:,}"

        # مرحله ۲: دیکشنری تبدیل کاراکترهای اعداد انگلیسی به فارسی
        translation_table = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

        # اعمال تبدیل و برگرداندن خروجی نهایی
        return formatted_price.translate(translation_table)