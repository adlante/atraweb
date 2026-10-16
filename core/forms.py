import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Newsletter, Ticket


class NewsletterForm(forms.ModelForm):
    """فرم عضویت در خبرنامه فنی آترا"""
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'newsletter-input',
                'placeholder': 'ایمیل کاری یا سازمانی خود را وارد کنید...',
                'autocomplete': 'email',
                'dir': 'ltr',
            }),
        }
        error_messages = {
            'email': {
                'required': 'وارد کردن ایمیل الزامی است.',
                'invalid': 'لطفاً یک آدرس ایمیل معتبر وارد کنید (مثال: dev@domain.com).',
                'unique': 'این آدرس ایمیل قبلاً در پایگاه خبرنامه ثبت شده است.'
            }
        }

    def clean_email(self):
        email = str(self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            raise ValidationError('وارد کردن ایمیل الزامی است.')

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValidationError('فرمت ایمیل نامعتبر است. لطفاً از کاراکترهای مجاز انگلیسی استفاده کنید.')
        return email


class TicketForm(forms.ModelForm):
    """فرم ثبت بریف پروژه و درخواست مشاوره فنی مهندسی"""
    class Meta:
        model = Ticket
        fields = ['name', 'phone', 'department', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control atra-ticket-input',
                'placeholder': 'نام و نام خانوادگی یا عنوان سازمان'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control atra-ticket-input',
                'placeholder': 'مثال: 09123456789',
                'dir': 'ltr'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select atra-ticket-select',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control atra-ticket-input',
                'placeholder': 'عنوان کلی پروژه یا درخواست مشاوره'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control atra-ticket-textarea',
                'rows': 5,
                'placeholder': 'شرح جزئیات فنی، اهداف، نیازمندی‌ها، امکانات و ددلاین پروژه...'
            }),
        }

    # 🛡️ اعتبارسنجی‌های ضد خطا (Safe Type Casting)

    def clean_name(self):
        name = str(self.cleaned_data.get('name') or '').strip()
        if not name:
            raise ValidationError("وارد کردن نام و نام خانوادگی الزامی است.")
        if len(name) < 3 or len(name) > 70:
            raise ValidationError("نام و نام خانوادگی باید بین ۳ تا ۷۰ کاراکتر باشد.")
        return name

    def clean_phone(self):
        phone = str(self.cleaned_data.get('phone') or '').strip()
        # تبدیل اعداد فارسی/عربی احتمالی به انگلیسی
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        arabic_digits = '٠١٢٣٤٥٦٧٨٩'
        for i in range(10):
            phone = phone.replace(persian_digits[i], str(i)).replace(arabic_digits[i], str(i))

        if not phone:
            raise ValidationError("وارد کردن شماره تماس الزامی است.")

        if not re.match(r'^09\d{9}$', phone):
            raise ValidationError("شماره تماس باید یک شماره موبایل معتبر ۱۱ رقمی ایران با پیش‌شماره 09 باشد.")
        return phone

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if not department:
            raise ValidationError("لطفاً حوزه فنی و دسته‌بندی پروژه را انتخاب کنید.")
        return department

    def clean_subject(self):
        subject = str(self.cleaned_data.get('subject') or '').strip()
        if not subject:
            raise ValidationError("وارد کردن عنوان کلی پروژه الزامی است.")
        if len(subject) < 3 or len(subject) > 120:
            raise ValidationError("عنوان پروژه باید بین ۳ تا ۱۲۰ کاراکتر باشد.")
        return subject

    def clean_message(self):
        message = str(self.cleaned_data.get('message') or '').strip()
        if not message:
            raise ValidationError("لطفاً شرح نیازمندی‌ها یا توضیحات فنی پروژه را وارد کنید.")
        if len(message) < 15:
            raise ValidationError("شرح پروژه باید حداقل شامل ۱۵ کاراکتر باشد تا امکان بررسی و ارائه پیشنهاد فنی فراهم شود.")
        if len(message) > 4000:
            raise ValidationError("متن پیام بیش از حد طولانی است (حداکثر ۴۰۰۰ کاراکتر).")
        return message



