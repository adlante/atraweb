from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'تولید کلید عمومی مبهم‌سازی شده (XOR) برای اپلیکیشن فلاتر'

    def handle(self, *args, **kwargs):
        # کلید عمومی باید به صورت یک رشته چند خطی (Multi-line string) تعریف شود
        pem_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3iQhTgy5qgO+ITn2HP8+
cy2AuXgUS7n+iywufC710b6uVWjCqGKI39HyG1P1BuvRP6UsnTZj9mgd3lHct6wP
McZggcdFk2g15ra/9Yd2ZwenoPPOBKmxoLHqBhpCS+8toK4UYfqcJabdx6Dl68a5
+b+kJwSKsWQ8gYmHh7uouhzmB48vMA9dyKM5v3I8Ngc89Mi14jiZeQWN6HSIcPb6
+VX/4KlTdo/KWsdqJusMa7WdEnp08NMCmIhxvnsOVqtdf3A9lJ2k8DPVIwNEEdv5
RaM0aNiTZkQinfmTLSWMp7Mzwu+55/cXYKXgH2bv3EtEJ9B2Pequyc4myIp7LQfq
wwIDAQAB
-----END PUBLIC KEY-----"""

        xor_key = 0x4A

        # مبهم‌سازی با عملگر XOR
        obfuscated_bytes = [ord(char) ^ xor_key for char in pem_key]

        self.stdout.write(self.style.SUCCESS('کد زیر را در فایل license_validator.dart فلاتر قرار دهید:\n'))
        self.stdout.write(f"static final List<int> _obfuscatedPubKey = {obfuscated_bytes};")
