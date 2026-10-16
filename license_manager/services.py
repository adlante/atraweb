import hvac
import base64
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_license_signature(license_data: dict) -> str:
    vault_url = getattr(settings, 'VAULT_URL', 'http://127.0.0.1:8200')
    vault_token = getattr(settings, 'VAULT_TOKEN', None)

    if not vault_token:
        raise ValueError("VAULT_TOKEN is missing in settings.")

    client = hvac.Client(url=vault_url, token=vault_token)

    payload_str = json.dumps(license_data, separators=(',', ':'))
    encoded_payload = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')

    try:
        response = client.secrets.transit.sign_data(
            name="atradev-license",  # نام کلیدی که در Vault ساخته‌اید
            hash_algorithm='sha2-256',
            input=encoded_payload
        )
        return response['data']['signature'].split(':')[-1]
    except Exception as e:
        logger.error(f"Vault signing error: {str(e)}")
        raise RuntimeError("Failed to sign data via Vault.")
