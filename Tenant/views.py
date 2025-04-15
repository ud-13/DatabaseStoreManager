from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Tenant, FamilyMember, PreviousResidence, HomeOwner, User
from .forms import TenantForm, HomeOwnerForm, FamilyMemberForm, PreviousResidenceForm, OTPVerificationForm, UserLoginForm
import random
import re
import os
from datetime import datetime, timedelta
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

# Helper functions
def generate_otp():
    return str(random.randint(100000, 999999))

def is_police(user):
    return user.role == 'police'

def is_homeowner(user):
    return user.role == 'home_owner'

def is_tenant(user):
    return user.role == 'tenant'

# View functions
def login(request):
    if request.method == 'GET':
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
    return render(request, 'login.html')

def index(request):
    role = request.GET.get('role', 'tenant')
    context = {'role': role}
    return render(request, 'index.html', context)

@user_passes_test(is_police)
def SignUpPolice(request):
    return render(request, 'SignUpPolice.html')

def ApplicationStatus(request):
    if 'verified_email' in request.session:
        email = request.session['verified_email']
        try:
            user = User.objects.get(email=email)
            tenants = Tenant.objects.filter(user=user)
            return render(request, 'ApplicationStatus.html', {'tenants': tenants})
        except User.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, 'ApplicationStatus.html')

@user_passes_test(is_homeowner)
def HomeOwnerdashboard(request):
    try:
        homeowner = HomeOwner.objects.get(user=request.user)
        tenants = Tenant.objects.filter(owner_phone_number=homeowner.phone)
        return render(request, 'HomeOwnerdashboard.html', {'homeowner': homeowner, 'tenants': tenants})
    except HomeOwner.DoesNotExist:
        messages.error(request, "Home owner profile not found")
        return redirect('signup_homeowner')

@user_passes_test(is_police)
def Policedashboard(request):
    tenants = Tenant.objects.filter(status='approved', police_status='pending')
    return render(request, 'Policedashboard.html', {'tenants': tenants})

@user_passes_test(is_police)
def police_approve_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        tenant.police_status = 'approved'
        tenant.save()
        try:
            send_mail(
                'Tenant Verification Approved',
                f'Dear {tenant.first_name}, your verification has been successfully approved by the police.',
                settings.DEFAULT_FROM_EMAIL,
                [tenant.user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
        
        messages.success(request, f"Tenant {tenant.first_name} {tenant.last_name} approved successfully")
        return redirect('Policedashboard')
    return render(request, 'Policedashboard.html')

@user_passes_test(is_police)
def police_reject_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        remark = request.POST.get('remark')
        if not remark:
            messages.error(request, "Please provide a reason for rejection")
            return redirect('Policedashboard')
            
        tenant.police_status = 'rejected'
        tenant.police_remark = remark
        tenant.save()
        
        try:
            send_mail(
                'Tenant Verification Rejected',
                f'Dear {tenant.first_name}, your verification has been rejected by the police.\nReason: {remark}',
                settings.DEFAULT_FROM_EMAIL,
                [tenant.user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            
        messages.success(request, f"Tenant {tenant.first_name} {tenant.last_name} rejected")
        return redirect('Policedashboard')
    return render(request, 'Policedashboard.html')

@login_required
def check_verification(request):
    return JsonResponse({
        'verified': True,
        'email': request.user.email
    })

@csrf_exempt
def Registration(request):
    if request.method == 'GET':
        if not request.session.get('verified_email'):
            return redirect('login')
        
        tenant_form = TenantForm()
        family_form = FamilyMemberForm()
        residence_form = PreviousResidenceForm()
        
        return render(request, 'Registration.html', {
            'tenant_form': tenant_form,
            'family_form': family_form,
            'residence_form': residence_form
        })
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                verified_email = request.session.get('verified_email')
                if not verified_email:
                    return JsonResponse({
                        'success': False,
                        'error': "Please verify your email first. Check your inbox!",
                        'redirect_url': reverse('login')
                    }, status=403)

                # Get or create user
                try:
                    user = User.objects.get(email=verified_email)
                except User.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': "User not found. Please verify your email again.",
                        'redirect_url': reverse('login')
                    }, status=404)

                # Handle file uploads
                def handle_upload(file_field, upload_to):
                    if file_field in request.FILES:
                        file_obj = request.FILES[file_field]
                        fs = FileSystemStorage(location=f'media/{upload_to}')
                        filename = fs.save(file_obj.name, file_obj)
                        return f'{upload_to}/{filename}'
                    return None

                # Validate and prepare tenant data
                tenant_data = {
                    'user': user,
                    'first_name': request.POST.get('first_name', '').strip(),
                    'middle_name': request.POST.get('middle_name', '').strip() or None,
                    'last_name': request.POST.get('last_name', '').strip(),
                    'date_of_birth': request.POST.get('date_of_birth'),
                    'age': request.POST.get('age') or None,
                    'photo': handle_upload('photo', 'tenant_photos'),
                    'father_name': request.POST.get('father_name', '').strip(),
                    'permanent_address': request.POST.get('permanent_address', '').strip(),
                    'village': request.POST.get('village', '').strip(),
                    'tehsil': request.POST.get('tehsil', '').strip(),
                    'post_office': request.POST.get('post_office', '').strip(),
                    'pin_code': request.POST.get('pin_code', '').strip(),
                    'police_station': request.POST.get('police_station', '').strip(),
                    'district': request.POST.get('district', 'Gangtok'),  
                    'tenant_phone_number': request.POST.get('tenant_phone_number', '').strip(),
                    'owner_phone_number': request.POST.get('owner_phone_number', '').strip(),
                    'profession': request.POST.get('profession', 'Others'),
                    'other_profession': request.POST.get('other_profession', '').strip() or None,
                    'serving_employee': request.POST.get('serving_employee', 'No'),
                    'serving_certificate': handle_upload('serving_certificate', 'certificates'),
                    'retired_employee': request.POST.get('retired_employee', 'No'),
                    'retired_certificate': handle_upload('retired_certificate', 'certificates'),
                    'sikkim_certificate': request.POST.get('sikkim_certificate', 'No'),
                    'sikkim_certificate_file': handle_upload('sikkim_certificate_file', 'certificates'),
                    'previous_police_station': request.POST.get('previous_police_station', '').strip() or None,
                    'signature_date': request.POST.get('signature_date'),
                    'signature': handle_upload('signature', 'signatures'),
                    'status': 'pending',  
                    'police_status': 'pending',  
                }

                # Validate required fields
                required_fields = [
                    'first_name', 'last_name', 'date_of_birth', 'father_name',
                    'permanent_address', 'post_office', 'pin_code', 'police_station',
                    'tenant_phone_number', 'owner_phone_number', 'signature_date',
                    'photo', 'signature'
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field in ['photo', 'signature']:
                        if not tenant_data.get(field):
                            missing_fields.append(field)
                    elif not tenant_data.get(field):
                        missing_fields.append(field)
                
                if missing_fields:
                    return JsonResponse({
                        'success': False,
                        'error': f'Missing required fields: {", ".join(missing_fields)}'
                    }, status=400)

                # Handle age calculation if not provided
                if not tenant_data['age'] and tenant_data['date_of_birth']:
                    try:
                        dob = datetime.strptime(tenant_data['date_of_birth'], '%Y-%m-%d').date()
                        today = timezone.now().date()
                        tenant_data['age'] = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                    except (ValueError, TypeError) as e:
                        logger.error(f"Age calculation error: {str(e)}")

                # Create tenant
                tenant = Tenant.objects.create(**tenant_data)
                
                # Process family members
                i = 0
                while f'family_members[{i}][first_name]' in request.POST:
                    family_data = {
                        'tenant': tenant,
                        'first_name': request.POST.get(f'family_members[{i}][first_name]', '').strip(),
                        'middle_name': request.POST.get(f'family_members[{i}][middle_name]', '').strip() or None,
                        'last_name': request.POST.get(f'family_members[{i}][last_name]', '').strip(),
                        'date_of_birth': request.POST.get(f'family_members[{i}][dob]'),
                        'age': request.POST.get(f'family_members[{i}][age]') or None,
                        'relationship': request.POST.get(f'family_members[{i}][relationship]', '').strip(),
                        'profession': request.POST.get(f'family_members[{i}][profession]', '').strip(),
                    }
                    
                    # Calculate age if not provided
                    if not family_data['age'] and family_data['date_of_birth']:
                        try:
                            dob = datetime.strptime(family_data['date_of_birth'], '%Y-%m-%d').date()
                            today = timezone.now().date()
                            family_data['age'] = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                        except (ValueError, TypeError) as e:
                            logger.error(f"Family member age calculation error: {str(e)}")
                    
                    FamilyMember.objects.create(**family_data)
                    i += 1

                # Process previous residences
                j = 0
                while f'previous_residences[{j}][from_place]' in request.POST:
                    PreviousResidence.objects.create(
                        tenant=tenant,
                        from_place=request.POST.get(f'previous_residences[{j}][from_place]', '').strip(),
                        to_place=request.POST.get(f'previous_residences[{j}][to_place]', '').strip(),
                        address=request.POST.get(f'previous_residences[{j}][address]', '').strip()
                    )
                    j += 1

                # Clear session and show success
                if 'verified_email' in request.session:
                    del request.session['verified_email']

                return JsonResponse({
                    'success': True,
                    'message': 'Your tenant registration has been successful',
                    'redirect_url': reverse('ApplicationStatus')
                })

        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f"An error occurred: {str(e)}"
            }, status=500)

def signup_homeowner(request):
    if request.method == 'POST':
        form = HomeOwnerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    
                    # Create or get user
                    user, created = User.objects.get_or_create(
                        email=email,
                        defaults={
                            'role': 'home_owner',
                            'is_active': True
                        }
                    )
                    
                    if created:
                        user.set_password(password)
                        user.save()
                    
                    # Create home owner profile
                    homeowner = form.save(commit=False)
                    homeowner.user = user
                    homeowner.save()
                    
                    # Log in the user
                    auth_login(request, user)
                    
                    messages.success(request, 'Account created successfully!')
                    return redirect('HomeOwnerdashboard')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = HomeOwnerForm()
    return render(request, 'signup_homeowner.html', {'form': form})

@csrf_exempt
def send_otp(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    email = request.POST.get('email', '').strip()
    role = request.POST.get('role', 'tenant').strip()
    
    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)
    
    if not re.match(r'^[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
        return JsonResponse({'success': False, 'error': 'Invalid email format'}, status=400)
    
    try:
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'role': role,
                'is_active': True
            }
        )
        
        # Generate and save OTP
        otp = generate_otp()
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # Send OTP email
        send_mail(
            'Your OTP Code for Tenant Verification',
            f'Your verification code is: {otp}\n\nThis code will expire in 5 minutes.\n\nPlease do not share this code with anyone.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return JsonResponse({
            'success': True,
            'message': 'OTP has been sent to your email'
        })
    except Exception as e:
        logger.error(f"OTP sending error: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred while sending OTP. Please try again.'
        }, status=500)

@csrf_exempt
def verify_otp(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
    email = request.POST.get('email', '').strip().lower()
    otp = request.POST.get('otp', '').strip()
    role = request.POST.get('role', 'tenant').strip().lower()
    
    if not email or not otp:
        return JsonResponse({'success': False, 'error': 'Email and OTP are required'}, status=400)
    
    try:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
        
        # Update role if needed
        if user.role != role:
            user.role = role
            user.save()
        
        # Verify OTP
        if not user.otp or user.otp != otp:
            return JsonResponse({'success': False, 'error': 'Invalid OTP'}, status=400)
            
        # Check OTP expiration (5 minutes)
        if not user.otp_created_at or (timezone.now() - user.otp_created_at) > timedelta(minutes=5):
            return JsonResponse({
                'success': False, 
                'error': 'OTP has expired. Please request a new one.'
            }, status=400)
        
        # Mark OTP as verified by saving it in session
        request.session['verified_email'] = email
        
        # Clear OTP after successful verification
        user.otp = None
        user.save()
        
        # Determine redirect URL based on role
        if role == 'tenant':
            redirect_url = reverse('Registration')
        elif role == 'home_owner':
            redirect_url = reverse('signup_homeowner')
        elif role == 'police':
            redirect_url = reverse('Policedashboard')
        else:
            redirect_url = reverse('index')
        
        return JsonResponse({
            'success': True,
            'message': 'OTP verified successfully',
            'redirect_url': redirect_url
        })
        
    except Exception as e:
        logger.error(f"OTP verification error: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred while verifying OTP'
        }, status=500)
