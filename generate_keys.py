from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_key_pair():
    # تولید کلید خصوصی RSA-2048
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # استخراج کلید عمومی از کلید خصوصی
    public_key = private_key.public_key()

    # ذخیره کلید خصوصی در فایل (فقط برای سرور جنگو)
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # ذخیره کلید عمومی در فایل (برای استخراج و استفاده در اسکریپت XOR)
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("✅ جفت‌کلید با موفقیت تولید شد!")
    print("فایل‌های private_key.pem و public_key.pem در همین مسیر ایجاد شدند.")


if __name__ == "__main__":
    generate_rsa_key_pair()
