from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # View to obtain the access and refresh token
    TokenRefreshView,     # View to refresh the access token using the refresh token
)

urlpatterns = [
    path('scan/<int:user_id>/', views.HandleScanView.as_view(), name='scan_handler'),
    path('submit/', views.HandleSubmitView.as_view(), name='submit_handler'),
        # Endpoint to get the JWT token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Endpoint to refresh the JWT token (use refresh token)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]