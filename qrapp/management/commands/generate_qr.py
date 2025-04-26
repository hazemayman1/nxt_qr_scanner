from django.core.management.base import BaseCommand
import qrcode
from qrapp.models import Attendee
from urllib.parse import urlencode

class Command(BaseCommand):
    help = 'Generate a QR code for a frontend link with user ID'

    def handle(self, *args, **options):
        attendees = Attendee.objects.filter(is_vip = True).exclude(ptr_id__in = [1001, 987,654])

        for emp in attendees:
            link = f"https://qr-scanner-frontend-psi.vercel.app/scan?user_id={emp.ptr_id}"
            qr = qrcode.QRCode(
                version=1,  # controls size of the QR Code
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # L, M, Q, H
                box_size=10,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)

            img = qr.make_image(fill="black", back_color="white")
            img.save("qrapp/qrcodes_vip/"+emp.name.replace(" ", "") + ".png")
