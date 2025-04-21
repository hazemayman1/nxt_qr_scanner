from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from qrapp.models import Attendee
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import pandas as pd

import json



@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
class HandleScanView(APIView):
    def get(self,request, *args, **kwargs ):
        user_id = kwargs.get('user_id')
        user = Attendee.objects.filter(ptr_id = user_id)
        if not user:
            payload = {
                "msg" : "QRCode for this user doesn't exist",
                "name" : None,
                "entrance" : False,
                "coffee" : False,
            }
        else:
            user = user.last()
            payload = {
                    "msg" : "",
                    "usr_id" : user.ptr_id,
                    "name" : user.name,
                    "entrance" : user.has_entered,
                    "coffee" : user.got_coffee,
                    "vip" : user.is_vip,
                    "company": user.company
            }
        print(payload)
        return JsonResponse(payload, status = 200)
    
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
class HandleSubmitView(APIView):
    def post(self, request):

        body = json.loads(request.body.decode('utf-8'))  # Decode byte string to string
        
        # Access the specific field from the JSON body
        usr_ptr_id = body.get('id')  # Replace 'field_name' with your actual field
        step = body.get('step')  # Replace 'field_name' with your actual field
        user = Attendee.objects.filter(ptr_id = usr_ptr_id).last()
        if not user:
            return JsonResponse({"message": f"Unknown user, rescan QR code", "success": False})
        if step == 'entry':
            if user.has_entered:
                return JsonResponse({"message": f"{user.name} already scanned at the entrance", "success": False})
            else:
                user.has_entered = True
                user.save()
                return JsonResponse({"message": f"{user.name} entrance scanned succesfully", "success":True})
            
        if step == 'coffee':          
            if not user.has_entered:
                return JsonResponse({"message": f"{user.name}'s didn't scan at entrance", "success": False})
            if user.got_coffee:
                return JsonResponse({"message": f"{user.name}'s already claimed their free coffee", "success": False})
            else:
                user.got_coffee = True
                user.save()
                return JsonResponse({"message": f"{user.name}'s coffee claimed succesfully", "success": True})

        return JsonResponse({"message": f"Unknown request"})

class HandleResetView(APIView):
    def get(self,request, *args, **kwargs ):
        Attendee.objects.all().update(has_entered = False, got_coffee = False)
        return JsonResponse({"message": f"Success"})
    

class HandleExportView(APIView):
    def get(self, request, *args, **kwargs):
        # Get all attendees
        attendees = Attendee.objects.all().exclude(ptr_id__in = [1001, 987,654]).values('id', 'name', 'email', 'has_entered', 'got_coffee', 'is_vip')

        # Create DataFrame
        df = pd.DataFrame(attendees)

        # Create HTTP response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = f"attendees_data.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Write Excel to response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Attendees', index=False)

        return response