import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, phone, username, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError("شماره موبایل الزامی است.")
        if not username:
            raise ValueError("نام کاربری الزامی است.")

        # منطق طلایی برای هندل کردن ایمیل خالی و جلوگیری از خطای UNIQUE
        if email and str(email).strip():
            # ایمیل رو تمیز، نرمال و به حروف کوچک تبدیل می‌کنیم تا بعداً تو لاگین مشکل Case-Sensitivity نداشته باشیم
            email = self.normalize_email(str(email).strip()).lower()
        else:
            # اگر ایمیل خالی، فقط اسپیس یا None بود، قطعاً به دیتابیس None می‌فرستیم
            email = None

        # پاس دادن مستقیم ایمیل به مدل
        user = self.model(phone=phone, username=username, email=email, **extra_fields)

        # مدیریت پسورد
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, email=None, password=None, **extra_fields):
        # تنظیم مقادیر پیش‌فرض برای سوپریوزر
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        # اعتبارسنجی امنیتی
        if extra_fields.get("is_staff") is not True:
            raise ValueError("سوپریوزر باید is_staff=True داشته باشد.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("سوپریوزر باید is_superuser=True داشته باشد.")

        # فراخوانی متد create_user با پاس دادن ایمیل
        return self.create_user(phone, username, email, password, **extra_fields)


class User(AbstractUser):
    # UUID برای امنیت بیشتر و غیرقابل حدس بودن آیدی کاربران
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # فیلدهای پیش‌فرض نام و نام‌خانوادگی را حذف می‌کنیم تا دیتابیس سبک‌تر شود
    first_name = None
    last_name = None

    # فیلد ایمیل به صورت کاملاً اختیاری با پشتیبانی از مقادیر NULL در دیتابیس
    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="ایمیل (اختیاری)"
    )

    # --- اعتبارسنجی یوزرنیم ---
    username_validator = RegexValidator(
        regex=r"^[a-zA-Z0-9]+$",
        message="نام کاربری فقط باید شامل حروف انگلیسی و اعداد باشد (بدون فاصله یا کاراکتر خاص)."
    )

    username = models.CharField(
        max_length=12,
        unique=True,
        validators=[username_validator],
        db_index=True,
        verbose_name="نام کاربری"
    )

    # --- اعتبارسنجی شماره موبایل ---
    phone_validator = RegexValidator(
        regex=r"^09\d{9}$",
        message="شماره موبایل معتبر نیست. باید 11 رقم باشد و با 09 شروع شود."
    )

    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_validator],
        db_index=True,
        verbose_name="شماره موبایل"
    )

    # وضعیت کاربر
    is_verified = models.BooleanField(default=False, help_text="آیا شماره موبایل تایید شده است")
    is_blocked = models.BooleanField(default=False)
    blocked_at = models.DateTimeField(null=True, blank=True)
    block_reason = models.TextField(blank=True, verbose_name="دلیل بلاک")
    created_at = models.DateTimeField(auto_now_add=True)

    # سیستم لاگین با شماره موبایل
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.username} - {self.phone}"

    def block(self, reason=""):
        """متدی برای مسدود کردن سریع کاربر به همراه دلیل مسدودی"""
        self.is_blocked = True
        self.blocked_at = timezone.now()
        self.block_reason = reason
        self.save(update_fields=["is_blocked", "blocked_at", "block_reason"])

    def unblock(self):
        """متدی برای رفع مسدودی کاربر"""
        self.is_blocked = False
        self.blocked_at = None
        self.block_reason = ""
        self.save(update_fields=["is_blocked", "blocked_at", "block_reason"])

    def save(self, *args, **kwargs):
        # بررسی می‌کنیم اگر ایمیل یک رشته خالی است (یا فقط شامل اسپیس است)
        if not self.email or str(self.email).strip() == "":
            self.email = None  # به صورت قطعی به NULL تبدیلش می‌کنیم
        else:
            # اگر ایمیل معتبر بود، فاصله‌های اضافه‌اش را می‌گیریم و کوچک می‌کنیم
            # تا در لاگین‌های بعدی مشکلات Case-Sensitivity نداشته باشیم
            self.email = str(self.email).strip().lower()

        # در نهایت متد save اصلی مدل را صدا می‌زنیم تا در دیتابیس ثبت شود
        super().save(*args, **kwargs)


# -----------------------------------------------------------------------------
# مدل پروفایل کاربر (User Profile Model)
# -----------------------------------------------------------------------------

class Profile(models.Model):
    # ارتباط یک به یک با مدل یوزر کاستوم شما
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="کاربر"
    )

    # --- فیلدهای اطلاعات شخصی ---
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="نام"
    )

    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="نام خانوادگی"
    )

    # ولیدیشن دقیق برای کد ملی ایران (۱۰ رقم دقیق)
    national_code_validator = RegexValidator(
        regex=r"^\d{10}$",
        message="کد ملی باید دقیقاً ۱۰ رقم و فقط شامل اعداد باشد."
    )
    national_code = models.CharField(
        max_length=10,
        validators=[national_code_validator],
        blank=True,
        null=True,
        unique=True,  # کد ملی نباید تکراری باشد
        verbose_name="کد ملی"
    )

    # --- فیلدهای اطلاعات تجاری/تماس ---
    company_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="نام شرکت/مجموعه (اختیاری)"
    )

    landline_phone_validator = RegexValidator(
        regex=r"^09\d{9}$",
        message="شماره تماس باید ۱۱ رقم باشد و حتماً با 09 شروع شود."
    )

    landline_phone = models.CharField(
        max_length=11,
        validators=[landline_phone_validator],
        blank=True,
        null=True,
        verbose_name="تلفن ثابت (اختیاری)"
    )

    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="آدرس پستی"
    )

    postal_code_validator = RegexValidator(
        regex=r"^\d{10}$",
        message="کد پستی باید دقیقاً ۱۰ رقم باشد."
    )
    postal_code = models.CharField(
        max_length=10,
        validators=[postal_code_validator],
        blank=True,
        null=True,
        verbose_name="کد پستی"
    )

    # --- فیلدهای سیستمی و کنترلی ---
    is_completed = models.BooleanField(
        default=False,
        help_text="آیا کاربر اطلاعات ضروری پروفایل را برای خرید تکمیل کرده است؟",
        verbose_name="وضعیت تکمیل پروفایل"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"

    def __str__(self):
        if self.first_name and self.last_name:
            return f"پروفایل {self.first_name} {self.last_name}"
        return f"پروفایل {self.user.username}"

    # ==========================================
    # جادوی اصلی اینجاست: بازنویسی متد save
    # ==========================================
    def save(self, *args, **kwargs):
        # 1. لیست فیلدهایی که برای تکمیل بودن پروفایل "اجباری" هستند
        required_fields = [
            self.first_name,
            self.last_name,
            self.national_code,
            self.postal_code,
            self.address
        ]

        # 2. یک پرچم (Flag) در نظر می‌گیریم و فرض می‌کنیم پروفایل کامله
        profile_is_full = True

        # 3. با دقت تک تک فیلدها رو بررسی می‌کنیم
        for field in required_fields:
            # اگر فیلد None بود، یا خالی بود، یا کاربر فقط چندتا Space زده بود:
            if not field or not str(field).strip():
                profile_is_full = False
                break  # به محض پیدا کردن اولین فیلد خالی، حلقه رو می‌شکنیم تا بهینه باشه

        # 4. فیلد is_completed رو با نتیجه بررسی بالا آپدیت می‌کنیم
        self.is_completed = profile_is_full

        # 5. در نهایت، متد save اصلی جنگو رو صدا می‌زنیم تا دیتا رو تو دیتابیس بنویسه
        super().save(*args, **kwargs)


# -----------------------------------------------------------------------------
# سیگنال‌ها (Signals)
# -----------------------------------------------------------------------------

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    این سیگنال فقط یک کار انجام می‌دهد:
    هر زمان که یک User جدید ساخته شد (created=True)،
    یک Profile برای آن ایجاد می‌کند. همین!
    """
    if created:
        Profile.objects.create(user=instance)


class PricingPlan(models.Model):
    title = models.CharField(max_length=100, verbose_name="نام پلن")

    # فیلد قیمت رو CharField گذاشتیم تا هم عدد مثل "1,499,000" بگیره هم متن مثل "توافقی"
    price = models.CharField(max_length=100, verbose_name="قیمت", help_text="مثال: 1,499,000 یا توافقی")
    price_suffix = models.CharField(max_length=100, verbose_name="پسوند قیمت",
                                    help_text="مثال: تومان / سال یا تماس بگیرید")

    button_text = models.CharField(max_length=50, default="انتخاب پلن", verbose_name="متن دکمه")

    # تنظیمات استایل کارت
    is_highlight = models.BooleanField(default=False, verbose_name="پیشنهاد ویژه (رنگ متفاوت)")
    is_custom = models.BooleanField(default=False, verbose_name="پلن سفارشی (استایل تیره)")

    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']
        verbose_name = "پلن قیمت‌گذاری"
        verbose_name_plural = "پلن‌های قیمت‌گذاری"

    def __str__(self):
        return self.title


class PlanFeature(models.Model):
    plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, related_name='features', verbose_name="پلن")
    title = models.CharField(max_length=150, verbose_name="عنوان ویژگی")

    # True = تیک سبز ، False = ضربدر خاکستری
    is_included = models.BooleanField(default=True, verbose_name="وضعیت (دارد=تیک / ندارد=ضربدر)")

    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']
        verbose_name = "امکانات پلن"
        verbose_name_plural = "امکانات پلن‌ها"

    def __str__(self):
        return f"{self.title} - {self.plan.title}"
