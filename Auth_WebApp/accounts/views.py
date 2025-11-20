from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


from .utils import send_otp_email
from .models import PasswordResetOTP



import csv
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth import get_user_model

# PDF Imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


User = get_user_model()

class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        #Pass 'request=request' explicitly
        user = authenticate(request=request, username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number
            })
        
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class RequestPasswordResetOTPAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            send_otp_email(user) # Generates and sends OTP
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Security: Don't reveal if email exists or not, just say sent
            return Response({"message": "If an account exists, an OTP has been sent."}, status=status.HTTP_200_OK)

class ResetPasswordWithOTPAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_input = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not email or not otp_input or not new_password:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            
            # Find the OTP in DB
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp_code=otp_input).last()

            if otp_obj and otp_obj.is_valid():
                # Success! Change Password
                user.set_password(new_password)
                user.save()
                
                # Delete used OTP
                otp_obj.delete()
                
                return Response({"message": "Password changed successfully. You can now login."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
                
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class DownloadUserCSVAPI(APIView):
    permission_classes = [IsAdminUser] # Only Admins can download

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_users.csv"'

        writer = csv.writer(response)
        # Write Header
        writer.writerow(['ID', 'Username', 'Email', 'Phone Number', 'First Name', 'Last Name', 'Date Joined'])

        # Write Data (Using iterator for memory efficiency with 10k users)
        users = User.objects.all().iterator()
        
        for user in users:
            writer.writerow([
                user.id, 
                user.username, 
                user.email, 
                user.phone_number, 
                user.first_name, 
                user.last_name,
                user.date_joined.strftime("%Y-%m-%d %H:%M:%S")
            ])

        return response

class DownloadUserPDFAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="all_users.pdf"'

        # Create PDF Document (Landscape mode to fit columns)
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []
        
        # Title
        styles = getSampleStyleSheet()
        elements.append(Paragraph("User Registry Report", styles['Title']))

        # Table Header
        data = [['ID', 'Username', 'Email', 'Phone', 'Joined']]

        # Fetch Data (Limit to 500 for PDF to prevent timeout, or remove slice for all)
        # Rendering 10,000 rows in PDF is very heavy. CSV is better for that. 
        # Here we grab all, but be warned it might take a few seconds.
        users = User.objects.all().order_by('-date_joined') 

        for user in users:
            data.append([
                str(user.id),
                user.username[:15], # Truncate long text
                user.email[:25],
                user.phone_number or "N/A",
                user.date_joined.strftime("%Y-%m-%d")
            ])

        # Create Table
        table = Table(data, colWidths=[40, 120, 180, 100, 100])

        # Add Styling (Borders, Colors)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        elements.append(table)
        doc.build(elements)
        
        return response