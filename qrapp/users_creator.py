
from qrapp.models import Attendee  # Example
import pandas as pd

df = pd.read_excel('Vips.xlsx')
for index, row in df.iterrows():
    id = row['ID']
    name = row['Full Name']
    company = row['Company']
    # better be bulk create but not needed here, one time operation on only 250 rows
    Attendee.objects.create(name = name, ptr_id = id, company = company, is_vip = True)
