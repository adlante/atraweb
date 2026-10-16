from django.db import models


class HeroSection(models.Model):
    """مدیریت بخش هیرو صفحه اصلی (استودیو آترا)"""
    badge_text = models.CharField(
        max_length=150,
        default="اکوسیستم یکپارچه نرم‌افزار و هوش مصنوعی",
        verbose_name="متن نشانک (Badge)"
    )
    title_p1 = models.CharField(
        max_length=200,
        default="توسعه نرم‌افزارهای مقیاس‌پذیر",
        verbose_name="تیتر اصلی (بخش اول)"
    )
    highlight_text = models.CharField(
        max_length=200,
        default="Django ،Flutter و زیرساخت LLM/RAG",
        verbose_name="متن هایلایت زمردی"
    )
    description = models.TextField(
        default="طراحی بک‌اند پرسرعت و امن با Python و DRF، ساخت رابط‌های کاربری چندسکویی و پایدار در شرایط آفلاین با Flutter، و معماری اختصاصی خطوط بازیابی دانش (RAG)، تنظیم دقیق مدل‌ها (Fine-Tuning) و هوش مصنوعی چندوجهی.",
        verbose_name="شرح معرفی (Lead Text)"
    )

    # آمارهای کلیدی (Stats Band)
    stat_1_number = models.CharField(max_length=50, default="99.9%", verbose_name="عدد شاخص ۱")
    stat_1_label = models.CharField(max_length=100, default="پایداری دیتابیس و بک‌اند", verbose_name="عنوان شاخص ۱")

    stat_2_number = models.CharField(max_length=50, default="< 45ms", verbose_name="عدد شاخص ۲")
    stat_2_label = models.CharField(max_length=100, default="تاخیر استریم و همگام‌سازی", verbose_name="عنوان شاخص ۲")

    stat_3_number = models.CharField(max_length=50, default="Offline-1st", verbose_name="عدد شاخص ۳")
    stat_3_label = models.CharField(max_length=100, default="معماری بدون توقف کلاینت", verbose_name="عنوان شاخص ۳")

    # کنسول شبیه‌ساز مهندسی هوش مصنوعی (سمت چپ)
    console_filename = models.CharField(max_length=100, default="pipeline_orchestrator.py",
                                        verbose_name="نام فایل کنسول")
    console_prompt_label = models.CharField(max_length=100, default="RAG Knowledge Retrieval",
                                            verbose_name="برچسب پرامپت")
    console_prompt_text = models.TextField(
        default="«پایگاه داده اسناد سازمانی را جستجو کن و با مدل تنظیم‌شده پاسخ را به کلاینت فلاتر استریم کن.»",
        verbose_name="متن پرامپت مهندسی"
    )
    vector_store_value = models.CharField(max_length=100, default="Qdrant // 12.4k Chunks",
                                          verbose_name="مقدار دیتابیس برداری")
    llm_model_value = models.CharField(max_length=100, default="LoRA PEFT v2.1", verbose_name="نسخه مدل فاین‌تیون‌شده")

    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "تنظیمات هیرو صفحه اصلی"
        verbose_name_plural = "تنظیمات هیرو صفحه اصلی"

    def __str__(self):
        return f"هیرو صفحه اصلی (آخرین ویرایش: {self.updated_at.strftime('%Y-%m-%d %H:%M')})"


class PillarCard(models.Model):
    """کارت‌های ۴ ستون اصلی فناوری در صفحه اصلی"""
    title = models.CharField(max_length=150, verbose_name="عنوان کارت")
    description = models.TextField(
        help_text="می‌توانید از تگ‌های HTML مانند <span class='tech-tag'>...</span> استفاده کنید.",
        verbose_name="متن توضیحات"
    )
    svg_icon = models.TextField(
        blank=True,
        null=True,
        help_text="کد خام SVG آیکون را اینجا قرار دهید.",
        verbose_name="کد SVG آیکون"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")

    class Meta:
        verbose_name = "کارت ستون فناوری"
        verbose_name_plural = "کارت‌های ستون فناوری"
        ordering = ['order']

    def __str__(self):
        return self.title


class BentoProductionSection(models.Model):
    """مدیریت بخش بنتو گرید استقرار هوش مصنوعی در پروداکشن"""
    badge_text = models.CharField(
        max_length=150,
        default="پایپ‌لاین هوش مصنوعی در محیط پروداکشن",
        verbose_name="متن بج هدر"
    )
    title_regular = models.CharField(
        max_length=150,
        default="استقرار هوش مصنوعی؛",
        verbose_name="متن ساده عنوان"
    )
    title_gradient = models.CharField(
        max_length=150,
        default="از نظریه تا زیرساخت عملیاتی",
        verbose_name="متن گرادینت عنوان"
    )
    subtitle = models.TextField(
        default="حل چالش‌های کلیدی سیستم‌های هوش مصنوعی: کاهش هزینه توکن، کمینه‌سازی تاخیر (Latency)، حذف خطای توهم و حفظ امنیت داده‌های شرکتی",
        verbose_name="توضیح زیر عنوان"
    )

    # کارت ۱: RAG
    rag_badge = models.CharField(max_length=100, default="بازیابی هوشمند و پایگاه دانش", verbose_name="بج کارت RAG")
    rag_title = models.CharField(max_length=150, default="معماری داده‌محور RAG", verbose_name="عنوان کارت RAG")
    rag_desc = models.TextField(
        default="تبدیل اسناد، پایگاه‌های داده و مکاتبات سازمانی به بردارهای معنایی، ذخیره در پایگاه‌های برداری (<span class=\"tech-tag-accent\">ChromaDB / Qdrant / pgvector</span>) و پیاده‌سازی متدهای <span class=\"tech-tag-accent\">Hybrid Search</span> و <span class=\"tech-tag-accent\">Re-ranking</span> برای پاسخ‌دهی کاملاً منطبق بر اسناد سازمانی.",
        verbose_name="متن کارت RAG"
    )
    rag_image_url = models.URLField(
        max_length=500,
        default="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=700&q=80",
        verbose_name="آدرس تصویر پس‌زمینه RAG"
    )

    # کارت ۲: Fine-Tuning
    finetune_badge = models.CharField(max_length=100, default="بومی‌سازی و سفارشی‌سازی وزن‌ها",
                                      verbose_name="بج کارت فاین‌تیونینگ")
    finetune_title = models.CharField(max_length=150, default="Fine-Tuning با LoRA و QLoRA",
                                      verbose_name="عنوان کارت فاین‌تیونینگ")
    finetune_desc = models.TextField(
        default="بازآموزی مدل‌های زبانی متن‌باز (<span class=\"tech-tag-accent\">Llama, Mistral, Qwen</span>) جهت تطبیق لحن، یادگیری ساختارهای دستوری اختصاصی و کاهش مصرف منابع سرور با تکنیک‌های مدرن کوانتیزه‌سازی (<span class=\"tech-tag-accent\">4-bit / 8-bit Quantization</span>).",
        verbose_name="متن کارت فاین‌تیونینگ"
    )
    finetune_image_url = models.URLField(
        max_length=500,
        default="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=700&q=80",
        verbose_name="آدرس تصویر پس‌زمینه فاین‌تیونینگ"
    )

    # کارت ۳: کارت بزرگ سرتاسری (End-to-End)
    fullstack_badge = models.CharField(max_length=100, default="یکپارچه‌سازی سرتاسری (End-to-End)",
                                       verbose_name="بج کارت فول‌استک")
    fullstack_title = models.CharField(max_length=150, default="بک‌اند جنگو، استریم داده و رابط کاربری فلاتر",
                                       verbose_name="عنوان کارت فول‌استک")
    fullstack_desc = models.TextField(
        default="تبدیل خروجی مدل‌های هوش مصنوعی به محصولی پایدار و آماده پروداکشن؛ طراحی وب‌سرویس‌های ناهمگام با جنگو، پیاده‌سازی مکانیزم استریم آنی توکن‌ها (<span class=\"tech-tag-accent\">Token Streaming</span> با <span class=\"tech-tag-accent\">SSE</span> و <span class=\"tech-tag-accent\">WebSockets</span>) و ساخت کلاینت‌های نیتیو در فلاتر همراه با کنترل سهمیه مصرف، احراز هویت پیامکی و مدیریت بهینه حافظه.",
        verbose_name="متن کارت فول‌استک"
    )
    fullstack_image_url = models.URLField(
        max_length=500,
        default="https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=80",
        verbose_name="آدرس تصویر پس‌زمینه فول‌استک"
    )
    fullstack_feature_1 = models.CharField(
        max_length=255,
        default="سیستم‌های تولید تصویر، عکاسی مجازی و فیس‌استودیو (<span class=\"tech-tag-accent\">Generative Pipelines</span>)",
        verbose_name="آیتم چک‌لیست ۱"
    )
    fullstack_feature_2 = models.CharField(
        max_length=255,
        default="پیکربندی سرورهای لینوکس، <span class=\"tech-tag-accent\">Nginx, Gunicorn, Docker</span> و مدیریت امن کلیدهای API",
        verbose_name="آیتم چک‌لیست ۲"
    )

    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "بنتو گرید استقرار هوش مصنوعی"
        verbose_name_plural = "بنتو گرید استقرار هوش مصنوعی"

    def __str__(self):
        return f"بنتو گرید هوش مصنوعی (بروزرسانی: {self.updated_at.strftime('%Y-%m-%d')})"


class OfflineFirstSection(models.Model):
    """مدیریت بخش معماری Offline-First صفحه اصلی"""
    title_regular = models.CharField(
        max_length=150,
        default="معماری Offline-First،",
        verbose_name="بخش اول عنوان"
    )
    title_highlight = models.CharField(
        max_length=150,
        default="تداوم عملکرد بدون اینترنت",
        verbose_name="متن هایلایت عنوان"
    )
    description = models.TextField(
        default="یکی از بزرگ‌ترین چالش‌های اپلیکیشن‌ها در دنیای واقعی، ناپایداری شبکه است. راهکارهای نرم‌افزاری پیاده‌سازی‌شده با پایگاه داده‌های محلی (Local Cache/SQLite) تضمین می‌کنند که کاربر بدون کوچک‌ترین اختلال اسناد و داده‌ها را ثبت کند و سیستم به صورت هوشمند و بدون تعارض، در اولین اتصال دیتا را با سرور ابری همگام (Sync) کند.",
        verbose_name="متن توضیحات"
    )

    # ویژگی‌های چهارگانه
    feature_1_icon = models.CharField(max_length=20, default="⚡", verbose_name="آیکون ویژگی ۱")
    feature_1_text = models.CharField(max_length=100, default="کش و پایگاه داده محلی", verbose_name="عنوان ویژگی ۱")

    feature_2_icon = models.CharField(max_length=20, default="🔄", verbose_name="آیکون ویژگی ۲")
    feature_2_text = models.CharField(max_length=100, default="سینک دوطرفه بدون تعارض", verbose_name="عنوان ویژگی ۲")

    feature_3_icon = models.CharField(max_length=20, default="🛡️", verbose_name="آیکون ویژگی ۳")
    feature_3_text = models.CharField(max_length=100, default="رمزنگاری داده در لایه کلاینت",
                                      verbose_name="عنوان ویژگی ۳")

    feature_4_icon = models.CharField(max_length=20, default="🚀", verbose_name="آیکون ویژگی ۴")
    feature_4_text = models.CharField(max_length=100, default="صفر شدن خطای لودینگ شبکه", verbose_name="عنوان ویژگی ۴")

    footer_note = models.CharField(
        max_length=255,
        default="ترکیب قدرت پردازش ابری جنگو با استقلال کامل دستگاه کاربر در فلاتر.",
        verbose_name="یادداشت پایانی"
    )
    image_url = models.URLField(
        max_length=500,
        default="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=85",
        verbose_name="آدرس تصویر داشبورد"
    )

    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "تنظیمات بخش Offline-First"
        verbose_name_plural = "تنظیمات بخش Offline-First"

    def __str__(self):
        return f"بخش Offline-First (بروزرسانی: {self.updated_at.strftime('%Y-%m-%d')})"


class ShowcaseProject(models.Model):
    """مدیریت پروژه‌ها و محصولات نمایش‌داده‌شده در صفحه اصلی"""
    title = models.CharField(max_length=150, verbose_name="عنوان پروژه")
    badge = models.CharField(
        max_length=80,
        default="GenAI Workspace",
        verbose_name="نشانک دسته‌بندی (Badge)"
    )
    excerpt = models.TextField(verbose_name="خلاصه چالش و شرح فنی پروژه")
    tech_stack = models.CharField(
        max_length=200,
        default="Django Tasks + Flutter App + Image Models",
        verbose_name="فناوری‌ها و استک فنی"
    )
    image_url = models.URLField(
        max_length=500,
        default="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&q=80",
        verbose_name="آدرس تصویر پروژه"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")

    class Meta:
        verbose_name = "پروژه صفحه اصلی"
        verbose_name_plural = "پروژه‌های صفحه اصلی"
        ordering = ['order']

    def __str__(self):
        return self.title


class AIModelShowcase(models.Model):
    """مدل‌های هوش مصنوعی عملیاتی در صفحه اصلی"""
    title = models.CharField(max_length=150, verbose_name="عنوان فارسی کارت")
    subtitle_en = models.CharField(max_length=150, verbose_name="عنوان انگلیسی (زیرعنوان)")
    stack_tag = models.CharField(max_length=100, verbose_name="تگ بالای کارت (تکنولوژی‌ها)")
    description = models.TextField(verbose_name="متن توضیحات")
    chips = models.CharField(
        max_length=300,
        help_text="تگ‌های کوچک را با کاما جدا کنید. مثال: Hybrid Search, Fine-Tuning با LoRA",
        verbose_name="چیپ‌ها و برچسب‌های فنی"
    )
    action_text = models.CharField(max_length=100, default="سفارش راه‌اندازی", verbose_name="متن دکمه")
    is_featured = models.BooleanField(
        default=False,
        verbose_name="کارت ویژه (دارای افکت درخشان و ریبون)؟"
    )
    featured_ribbon_text = models.CharField(
        max_length=80,
        blank=True,
        default="پرتقاضاترین راهکار",
        verbose_name="متن ریبون ویژه"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")

    class Meta:
        verbose_name = "کارت ویترین هوش مصنوعی"
        verbose_name_plural = "کارت‌های ویترین هوش مصنوعی"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.subtitle_en})"

    def get_chips_list(self):
        """تبدیل رشته جدا شده با کاما به لیست"""
        if self.chips:
            return [chip.strip() for chip in self.chips.split(',') if chip.strip()]
        return []


class FAQItem(models.Model):
    """پرسش و پاسخ‌های فنی و معماری صفحه اصلی"""
    question = models.CharField(max_length=300, verbose_name="متن پرسش")
    answer = models.TextField(
        help_text="می‌توانید از تگ‌های <strong> یا لینک در متن پاسخ استفاده کنید.",
        verbose_name="متن پاسخ کامل"
    )
    is_highlight = models.BooleanField(
        default=False,
        verbose_name="هایلایت نئونی (استایل ویژه highlight-offline)؟"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")

    class Meta:
        verbose_name = "سوال متداول (FAQ)"
        verbose_name_plural = "سوالات متداول (FAQ)"
        ordering = ['order']

    def __str__(self):
        return self.question[:60]


from django.conf import settings


class Newsletter(models.Model):
    """مدل ذخیره ایمیل‌های عضویت در خبرنامه"""
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")

    class Meta:
        verbose_name = "عضو خبرنامه"
        verbose_name_plural = "اعضای خبرنامه"
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class Ticket(models.Model):
    """مدل ذخیره تیکت‌ها و بریف‌های پروژه‌ها"""
    DEPARTMENT_CHOICES = (
        ('general', 'مشاوره عمومی و همکاری'),
        ('backend', 'بک‌اند و معماری Django'),
        ('flutter', 'اپلیکیشن Flutter'),
        ('ai_rag', 'هوش مصنوعی و سیستم‌های RAG / LLM'),
        ('devops', 'سرور، لینوکس و استقرار'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="کاربر"
    )
    name = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='general',
        blank=True,
        null=True,
        verbose_name="دپارتمان / حوزه فنی"
    )
    subject = models.CharField(max_length=250, blank=True, null=True, verbose_name="موضوع")
    message = models.TextField(verbose_name="متن پیام / شرح پروژه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    is_checked = models.BooleanField(default=False, verbose_name="بررسی شده؟")

    class Meta:
        verbose_name = "تیکت / بریف پروژه"
        verbose_name_plural = "تیکت‌ها و بریف‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"


class SecurityTrapLog(models.Model):
    """ثبت لاگ متجاوزانی که وارد تله /admin/ شده‌اند"""
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آی‌پی")
    user_agent = models.TextField(blank=True, null=True, verbose_name="مشخصات دستگاه و مرورگر")
    path_attempted = models.CharField(max_length=255, default="/admin/", verbose_name="مسیر مورد نظر")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان وقوع نفوذ")

    class Meta:
        verbose_name = "لاگ تلاش نفوذ (Honeypot)"
        verbose_name_plural = "لاگ‌های تله امنیتی"
        ordering = ['-timestamp']

    def __str__(self):
        return f"نفوذ از آی‌پی {self.ip_address} در {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
