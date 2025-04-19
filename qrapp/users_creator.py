
from qrapp.models import Attendee  # Example
import pandas as pd
import qrcode

# df = pd.read_excel('EmployeesEmails.xlsx')

# for index, row in df.iterrows():
#     id = row['ID']
#     name = row['Full Name']
#     email = row['Company Email']
#     Attendee.objects.create(name = name, ptr_id = id, email = email)


attendees = Attendee.objects.all()

for emp in attendees:
    link = "https://example.com/some-page/" + emp.ptr_id
    qr = qrcode.QRCode(
        version=1,  # controls size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # L, M, Q, H
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save("qrcodes/"+emp.id+"_code.png")