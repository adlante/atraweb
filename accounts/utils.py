import random
import requests
import logging
import traceback
from django.conf import settings

# تنظیم لاگر
logger = logging.getLogger(__name__)


def generate_otp_code() -> str:
    """
    تولید کد ۵ رقمی تصادفی برای احراز هویت
    """
    return str(random.randint(10000, 99999))


def send_otp_sms(mobile_number: str, otp_code: str) -> bool:
    """
    ارسال پیامک تایید با استفاده از سرویس Lookup کاوه‌نگار
    """
    try:
        # دریافت کلید API (در صورت عدم وجود، خطا ایجاد می‌کند تا متوجه شویم)
        api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
        if not api_key:
            logger.error("کلید KAVENEGAR_API_KEY در تنظیمات Django یافت نشد!")
            return False

        url = f"https://api.kavenegar.com/v1/{api_key}/verify/lookup.json"

        # پارامترها (حذف sender برای جلوگیری از تداخل در متد lookup، مگر اینکه پشتیبانی تایید کرده باشد)
        params = {
            'receptor': mobile_number,
            'template': 'otptemplate',
            'token': otp_code,
            'type': 'sms',
            # 'sender': '9981803677',  # 👈 فقط در صورتی آنکامنت کن که کاوه‌نگار این خط را برای lookup شما فعال کرده باشد
        }

        response = requests.post(url, data=params, timeout=10)

        # اگر پاسخ سرور 200 نباشد، جزئیات خطای خود کاوه‌نگار را لاگ می‌کنیم
        if response.status_code != 200:
            logger.error(f"خطا از سمت کاوه‌نگار: {response.status_code} - {response.text}")
            return False

        logger.info(f"✅ کد OTP ({otp_code}) با موفقیت به {mobile_number} ارسال شد.")
        return True

    except requests.exceptions.Timeout:
        logger.error(f"⏳ تایم‌اوت در اتصال به سرور کاوه‌نگار برای شماره {mobile_number}")
        return False

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ خطای شبکه در ارتباط با کاوه‌نگار: {e}")
        return False

    except Exception as e:
        logger.critical(f"🔥 خطای ناشناخته در سیستم پیامک: {e}\n{traceback.format_exc()}")
        return False
