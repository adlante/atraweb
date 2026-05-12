from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, PricingPlan, PlanFeature


# ==========================================
# 1. تنظیمات Inline برای نمایش پروفایل داخل کاربر
# ==========================================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "اطلاعات پروفایل"
    fk_name = "user"
    readonly_fields = ('updated_at', 'is_completed')


# ==========================================
# 2. تنظیمات ادمین کاربر (متصل به Inline)
# ==========================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    inlines = (ProfileInline,)

    list_display = (
        "phone",
        "username",
        "email",
        "is_verified",
        "is_blocked",
        "is_staff",
        "profile_is_completed",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "is_blocked",
        "is_staff",
        "is_active",
        "created_at",
    )
    search_fields = ("phone", "username", "email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "last_login", "blocked_at")

    # ==========================================
    # 🎯 رفع ارور: بازنویسی fieldsets برای ویرایش کاربر
    # ==========================================

    fieldsets = (
        (None, {"fields": ("phone", "username", "password")}),
        ("اطلاعات ارتباطی (اختیاری)", {"fields": ("email",)}),
        ("وضعیت حساب و امنیت", {"fields": ("is_verified", "is_blocked", "block_reason", "blocked_at")}),
        ("دسترسی‌ها", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("تاریخ‌های مهم", {"fields": ("last_login", "created_at")}),
    )

    # ==========================================
    # 🎯 رفع ارور: بازنویسی add_fieldsets برای ساخت کاربر جدید
    # ==========================================
    # اینجا دقیقا همون چیزیه که گفتی: "ثبت اولیه بدون اطلاعات اضافی".
    # وقتی روی دکمه "افزودن کاربر" تو ادمین کلیک کنی، فقط این فیلدها رو میپرسه.
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "username", "password"),
        }),
    )

    # ==========================================
    # متد سفارشی برای نمایش وضعیت تکمیل پروفایل
    # ==========================================
    @admin.display(boolean=True, description='تکمیل پروفایل')
    def profile_is_completed(self, obj):
        try:
            return obj.profile.is_completed
        except Profile.DoesNotExist:
            return False


# ==========================================
# 3. تنظیمات ادمین مستقل برای پروفایل
# ==========================================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "national_code", "is_completed", "updated_at")
    list_filter = ("is_completed", "updated_at")
    search_fields = ("user__phone", "user__username", "first_name", "last_name", "national_code", "company_name")
    readonly_fields = ("is_completed", "updated_at")

    fieldsets = (
        ("کاربر متصل", {
            "fields": ("user", "is_completed")
        }),
        ("اطلاعات هویتی", {
            "fields": ("first_name", "last_name", "national_code")
        }),
        ("اطلاعات تماس و آدرس", {
            "fields": ("company_name", "landline_phone", "postal_code", "address")
        }),
        ("تاریخچه", {
            "fields": ("updated_at",)
        }),
    )


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1  # تعداد ردیف‌های خالی پیش‌فرض


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_highlight', 'is_custom', 'order']
    list_editable = ['order']  # برای تغییر سریع ترتیب نمایش
    inlines = [PlanFeatureInline]
