from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('', views.login, name='login'),
path('accounts/login/', views.login, name='auth_login'),
    path('registration/', views.Registration, name='Registration'),
    path('application-status/', views.ApplicationStatus, name='ApplicationStatus'),
    path('signup-homeowner/', views.signup_homeowner, name='signup_homeowner'),
    path('signup-police/', views.SignUpPolice, name='SignUpPolice'),
    path('homeowner-dashboard/', views.HomeOwnerdashboard, name='HomeOwnerdashboard'),
    path('police-dashboard/', views.Policedashboard, name='Policedashboard'),
    path('police/approve/<int:tenant_id>/', views.police_approve_tenant, name='police_approve_tenant'),
    path('police/reject/<int:tenant_id>/', views.police_reject_tenant, name='police_reject_tenant'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('check-verification/', views.check_verification, name='check_verification'),
    path('payment/', views.payment_view, name='payment'),
    path('logout/', views.logout_view, name='logout'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
