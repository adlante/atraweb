from django.contrib import admin
from .models import HeroSection, PillarCard, BentoProductionSection, OfflineFirstSection, ShowcaseProject, \
    AIModelShowcase, FAQItem, Newsletter, Ticket, SecurityTrapLog


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title_p1', 'highlight_text', 'is_active', 'updated_at')
    fieldsets = (
        ('بخش معرفی و تیترها', {
            'fields': ('badge_text', 'title_p1', 'highlight_text', 'description')
        }),
        ('آمارهای سه‌گانه', {
            'fields': (
                ('stat_1_number', 'stat_1_label'),
                ('stat_2_number', 'stat_2_label'),
                ('stat_3_number', 'stat_3_label'),
            )
        }),
        ('کنسول هوش مصنوعی و پایپ‌لاین', {
            'fields': (
                'console_filename',
                'console_prompt_label',
                'console_prompt_text',
                ('vector_store_value', 'llm_model_value'),
            )
        }),
        ('وضعیت انتشار', {
            'fields': ('is_active',)
        }),
    )

    def has_add_permission(self, request):
        # اجازه ساخت بیشتر از ۱ رکورد داده نمی‌شود تا پنل مرتب بماند
        return not HeroSection.objects.exists()


@admin.register(PillarCard)
class PillarCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')


@admin.register(BentoProductionSection)
class BentoProductionSectionAdmin(admin.ModelAdmin):
    list_display = ('title_regular', 'title_gradient', 'is_active', 'updated_at')
    fieldsets = (
        ('هدر و تیتر اصلی', {
            'fields': ('badge_text', 'title_regular', 'title_gradient', 'subtitle')
        }),
        ('کارت ۱: معماری RAG', {
            'fields': ('rag_badge', 'rag_title', 'rag_desc', 'rag_image_url')
        }),
        ('کارت ۲: فاین‌تیونینگ و LoRA', {
            'fields': ('finetune_badge', 'finetune_title', 'finetune_desc', 'finetune_image_url')
        }),
        ('کارت ۳: کارت جامع Full-Stack & Flutter', {
            'fields': (
                'fullstack_badge', 'fullstack_title', 'fullstack_desc',
                'fullstack_image_url', 'fullstack_feature_1', 'fullstack_feature_2'
            )
        }),
        ('وضعیت انتشار', {
            'fields': ('is_active',)
        }),
    )

    def has_add_permission(self, request):
        return not BentoProductionSection.objects.exists()


@admin.register(OfflineFirstSection)
class OfflineFirstSectionAdmin(admin.ModelAdmin):
    list_display = ('title_regular', 'title_highlight', 'is_active', 'updated_at')
    fieldsets = (
        ('عناوین و متن توضیحات', {
            'fields': ('title_regular', 'title_highlight', 'description', 'footer_note')
        }),
        ('ویژگی‌های چهارگانه', {
            'fields': (
                ('feature_1_icon', 'feature_1_text'),
                ('feature_2_icon', 'feature_2_text'),
                ('feature_3_icon', 'feature_3_text'),
                ('feature_4_icon', 'feature_4_text'),
            )
        }),
        ('تصویر ماک‌آپ و وضعیت', {
            'fields': ('image_url', 'is_active')
        }),
    )

    def has_add_permission(self, request):
        return not OfflineFirstSection.objects.exists()


@admin.register(ShowcaseProject)
class ShowcaseProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'tech_stack', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'excerpt', 'tech_stack')


@admin.register(AIModelShowcase)
class AIModelShowcaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle_en', 'is_featured', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'is_featured')
    search_fields = ('title', 'subtitle_en', 'stack_tag', 'description')


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_highlight', 'order', 'is_active')
    list_editable = ('order', 'is_highlight', 'is_active')
    search_fields = ('question', 'answer')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_checked', 'created_at')
    list_filter = ('is_checked', 'created_at')
    search_fields = ('name', 'phone', 'message')
    list_editable = ('is_checked',)


@admin.register(SecurityTrapLog)
class SecurityTrapLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path_attempted', 'timestamp')
    readonly_fields = ('ip_address', 'user_agent', 'path_attempted', 'timestamp')
    search_fields = ('ip_address', 'user_agent')
    list_filter = ('timestamp',)

    # جلوگیری از ویرایش یا افزودن دستی رکورد توسط ادمین تا لاگ‌ها تمیز بمانند
    def has_add_permission(self, request):
        return False
