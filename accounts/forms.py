from django import forms
from django.contrib.auth import get_user_model
import re
from django.core.validators import RegexValidator, MinLengthValidator
from .models import Profile

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}),
        label="رمز عبور"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور'}),
        label="تکرار رمز عبور"
    )
    # فیلد ایمیل اختیاری با اعتبارسنجی داخلی خود جنگو
    email = forms.EmailField(
        required=False,
        empty_value=None,
        label="ایمیل ",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل (اختیاری)'})
    )

    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'password']

        # متد اضافه شده برای رفع خطای دیتابیس در هنگام خالی بودن ایمیل

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # ۱. حیاتی‌ترین بخش: تبدیل رشته خالی یا فقط فاصله به None
        if not email or str(email).strip() == "":
            return None

        # ۲. نرمال‌سازی ایمیل
        email = str(email).strip().lower()

        # ۳. اعتبارسنجی یکتا بودن ایمیل
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # اینجا بررسی می‌کنیم که ایمیل حتما وجود داشته باشه بعد تو دیتابیس بگردیم
        if email is not None and User.objects.filter(email=email).exists():
            raise forms.ValidationError("کاربری با این ایمیل از قبل وجود دارد.")

        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("نام کاربری الزامی است.")

        # 💡 حذف فاصله‌های ابتدا و انتها و تبدیل به حروف کوچک
        username = username.strip().lower()

        # کنترل طول رشته
        if len(username) < 3 or len(username) > 12:
            raise forms.ValidationError("نام کاربری باید بین ۳ تا ۱۲ کاراکتر باشد.")

        # کنترل نوع کاراکترها (فقط حروف و اعداد انگلیسی)
        if not re.match(r"^[a-z0-9]+$", username):  # چون حروف کوچک شد، A-Z رو برداشتم
            raise forms.ValidationError("نام کاربری فقط باید شامل حروف انگلیسی و اعداد باشد (بدون سیمبل یا زبان دیگر).")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلاً ثبت شده است.")

        return username

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            raise forms.ValidationError("شماره موبایل الزامی است.")
        if not phone.isdigit():
            raise forms.ValidationError("شماره موبایل باید فقط عدد باشد.")
        if len(phone) != 11:
            raise forms.ValidationError("شماره موبایل دقیقاً باید ۱۱ رقم باشد.")
        if not phone.startswith("09"):
            raise forms.ValidationError("شماره موبایل باید با ۰۹ شروع شود.")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("این شماره موبایل در سیستم وجود دارد.")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("رمز عبور الزامی است.")

        # محدودیت سخت‌گیرانه طول (جلوگیری از بافرهای بزرگ یا رمزهای خیلی کوتاه)
        if len(password) < 8 or len(password) > 14:
            raise forms.ValidationError("رمز عبور باید بین ۸ تا ۱۴ کاراکتر باشد.")

        # الزام به داشتن حداقل یک حرف بزرگ انگلیسی
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("رمز عبور باید شامل حداقل یک حرف بزرگ انگلیسی باشد.")

        # الزام به داشتن حداقل یک عدد
        if not re.search(r'\d', password):
            raise forms.ValidationError("رمز عبور باید شامل حداقل یک عدد باشد.")

        # الزام به داشتن حداقل یک کاراکتر خاص
        if not re.search(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|-]', password):
            raise forms.ValidationError("رمز عبور باید شامل حداقل یک کاراکتر خاص (مثل @, #, $ و...) باشد.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # بررسی تطابق پسوردها
        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "رمز عبور و تکرار آن با هم مطابقت ندارند.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # ست کردن امن پسورد
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            # ذخیره فیلدهای ManyToMany در صورت وجود
            if hasattr(self, 'save_m2m'):
                self.save_m2m()

        return user


class LoginForm(forms.Form):
    # دریافت نام کاربری با رعایت الگوی دقیق ثبت‌نام (حروف و اعداد انگلیسی)
    username = forms.CharField(
        label='نام کاربری',
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]+$",
                message="نام کاربری فقط باید شامل حروف انگلیسی و اعداد باشد."
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'نام کاربری خود را وارد کنید',
            'class': 'form-control',
            'id': 'username-input',
            'autocomplete': 'username'
        })
    )

    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور خود را وارد کنید',
            'class': 'form-control',
            'id': 'password-input',
            'autocomplete': 'current-password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # بررسی طول نام کاربری دقیقاً مثل فرم ثبت‌نام
        if len(username) < 3 or len(username) > 12:
            raise forms.ValidationError("نام کاربری باید بین ۳ تا ۱۲ کاراکتر باشد.")

        # نکته: بررسی وجود یوزر در دیتابیس را مستقیماً در view و با تابع authenticate انجام می‌دهیم
        # تا از حملات تشخیص نام کاربری (Username Enumeration) تا حدودی جلوگیری کنیم.
        return username


class CheckoutProfileForm(forms.ModelForm):
    # دقت کن: چون شهر و استان تو مدل Profile نبود، من اونا رو به عنوان فیلد موقت در فرم آوردم
    # تا تو View بتونی اونا رو به فیلد address بچسبونی یا جدا ذخیره کنی.
    province = forms.CharField(
        min_length=3, max_length=50,
        validators=[RegexValidator(r'^[\u0600-\u06FF\s]+$', message="استان باید فقط شامل حروف فارسی باشد.")],
        label="استان"
    )
    city = forms.CharField(
        min_length=3, max_length=50,
        validators=[RegexValidator(r'^[\u0600-\u06FF\s]+$', message="شهر باید فقط شامل حروف فارسی باشد.")],
        label="شهر"
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'national_code', 'address', 'postal_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اعمال طول و پترن برای نام
        self.fields['first_name'].validators.extend([
            MinLengthValidator(3, message="نام باید حداقل ۳ حرف باشد."),
            RegexValidator(r'^[\u0600-\u06FF\s]+$', message="نام باید فقط شامل حروف فارسی باشد.")
        ])

        # اعمال طول و پترن برای نام خانوادگی
        self.fields['last_name'].validators.extend([
            MinLengthValidator(3, message="نام خانوادگی باید حداقل ۳ حرف باشد."),
            RegexValidator(r'^[\u0600-\u06FF\s]+$', message="نام خانوادگی باید فقط شامل حروف فارسی باشد.")
        ])

        # آدرس (اگر خواستی فقط و فقط فارسی باشه بدون هیچ عدد یا پلاکی، رِجِکس زیر رو استفاده کن)
        self.fields['address'].validators.extend([
            MinLengthValidator(10, message="آدرس باید حداقل ۱۰ حرف باشد."),
            # اگر میخوای اعداد (مثل پلاک) مجاز باشن این رجکس: r'^[\u0600-\u06FF\s0-9۰-۹،.-]+$'
            RegexValidator(r'^[\u0600-\u06FF\s]+$', message="آدرس باید فقط شامل حروف فارسی باشد.")
        ])

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if not national_code.isdigit() or len(national_code) != 10:
            raise forms.ValidationError("کد ملی باید دقیقاً ۱۰ رقم عدد باشد.")
        return national_code

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code.isdigit() or len(postal_code) != 10:
            raise forms.ValidationError("کد پستی باید دقیقاً ۱۰ رقم عدد باشد.")
        return postal_code
