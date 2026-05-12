from django import template

register = template.Library()


@register.filter(name='persian_int')
def persian_int(value):
    """
    این فیلتر عدد را می‌گیرد، سه رقم سه رقم با کاما جدا می‌کند
    و در نهایت تمام اعداد انگلیسی را به فارسی تبدیل می‌کند.
    """
    if value is None or value == '':
        return value

    try:
        # تبدیل مقدار به عدد صحیح برای جلوگیری از خطا
        int_value = int(value)
        # جدا کردن سه رقم سه رقم با کاما
        formatted_number = f"{int_value:,}"

        # تبدیل اعداد انگلیسی به فارسی با استفاده از maketrans
        english_to_persian = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
        persian_formatted_number = formatted_number.translate(english_to_persian)

        return persian_formatted_number
    except (ValueError, TypeError):
        # اگر مقداری که پاس داده شده عدد نبود، همان مقدار اولیه را برگردان
        return value
