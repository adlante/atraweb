from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import HardwareLicense
from .services import generate_license_signature


@api_view(['POST'])
@permission_classes([AllowAny])  # در صورت نیاز به احراز هویت IsAuthenticated قرار دهید
def generate_license_view(request):
    device_id = request.data.get('device_id')

    if not device_id:
        return Response({"error": "device_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    # استفاده از transaction.atomic برای جلوگیری از Race Condition
    with transaction.atomic():
        expiration_date = timezone.now() + timedelta(days=365)

        # ثبت یا بروزرسانی در دیتابیس
        license_obj, created = HardwareLicense.objects.select_for_update().update_or_create(
            device_id=device_id,
            defaults={'expiration_date': expiration_date, 'is_active': True}
        )

        license_data = {
            "device_id": license_obj.device_id,
            "expiration_date": license_obj.expiration_date.isoformat(),
            "features": ["premium", "all_access"]
        }

        try:
            signature = generate_license_signature(license_data)
        except Exception as e:
            return Response(
                {"error": "Vault Security Error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response({
        "status": "success",
        "license_data": license_data,
        "signature": signature
    }, status=status.HTTP_200_OK)
