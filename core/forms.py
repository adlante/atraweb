from django import forms
from .models import Newsletter, Ticket
import re
from django.core.exceptions import ValidationError


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        # اضافه کردن پیام‌های فارسی برای خطاهای پیش‌فرض جنگو
        error_messages = {
            'email': {
                'required': 'وارد کردن ایمیل الزامی است.',
                'invalid': 'لطفاً یک آدرس ایمیل معتبر وارد کنید (مثال: user@gmail.com).',
                'unique': 'این ایمیل قبلاً در خبرنامه ثبت شده است.'
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # اعتبارسنجی سخت‌گیرانه ما با Regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            # پرتاب خطای فارسی در صورتی که Regex پاس نشود
            raise forms.ValidationError('فرمت ایمیل نامعتبر است. لطفاً فقط از حروف و اعداد انگلیسی استفاده کنید.')

        return email


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'phone', 'department', 'subject', 'message']

        # 🎨 بخش ویجت‌ها: تزریق کلاس‌های CSS و Placeholder برای ظاهر زیبای فرم
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control atra-ticket-input',
                'placeholder': 'نام و نام خانوادگی خود را وارد کنید'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control atra-ticket-input',
                'placeholder': 'مثال: 09123456789'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select atra-ticket-select',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control atra-ticket-input',
                'placeholder': 'موضوع تیکت (کوتاه و گویا)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control atra-ticket-textarea',
                'rows': 5,
                'placeholder': 'پیام خود را با جزئیات بنویسید...'
            }),
        }

    # 🛡️ بخش اعتبارسنجی‌های دقیق (Validation)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        # فقط حروف انگلیسی، فارسی و فاصله. طول بین ۳ تا ۱۲ کاراکتر
        if not re.match(r'^[\u0600-\u06FFa-zA-Z\s]{3,12}$', name):
            raise ValidationError("نام باید بین ۳ تا ۱۲ حرف و فقط شامل حروف فارسی یا انگلیسی باشد.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # فقط ۱۱ رقم، شروع با 09
        if not re.match(r'^09\d{9}$', phone):
            raise ValidationError("شماره موبایل باید دقیقاً ۱۱ رقم باشد و با 09 شروع شود.")
        return phone

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if not department:
            raise ValidationError("لطفاً دپارتمان مربوطه را انتخاب کنید.")
        return department

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        # طول بین ۵ تا ۶۰ کاراکتر
        if len(subject) < 5 or len(subject) > 60:
            raise ValidationError("موضوع تیکت باید بین ۵ تا ۶۰ کاراکتر باشد.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        # فقط حروف فارسی، فاصله، نقطه و ویرگول. طول بین ۱۵ تا ۵۰۰ کاراکتر
        if not re.match(r'^[\u0600-\u06FF\s\.\,]{15,500}$', message):
            raise ValidationError("متن پیام باید بین ۱۵ تا ۵۰۰ کاراکتر باشد و فقط شامل حروف فارسی، نقطه و ویرگول باشد.")
        return message
