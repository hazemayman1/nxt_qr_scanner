from django.core.management.base import BaseCommand
import qrcode
from qrapp.models import Attendee
from urllib.parse import urlencode

class Command(BaseCommand):
    help = 'Generate a QR code for a frontend link with user ID'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('--user_id', type=int, required=True, help='User ID to encode in QR code')
        # parser.add_argument('--base_url', type=str, default='https://your-frontend.com/attendee', help='Frontend base URL')

    def handle(self, *args, **options):
        attendees = Attendee.objects.all()

        for emp in attendees:
            link = "https://example.com/some-page/" + str(emp.ptr_id)
            qr = qrcode.QRCode(
                version=1,  # controls size of the QR Code
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # L, M, Q, H
                box_size=10,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)

            img = qr.make_image(fill="black", back_color="white")
            img.save("qrapp/qrcodes/"+emp.name.replace(" ", "") + ".png")
