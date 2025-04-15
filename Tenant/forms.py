from django import forms
from .models import Tenant, HomeOwner, FamilyMember, PreviousResidence, User

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ['user', 'status', 'police_status', 'police_remark']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
            'serving_certificate': forms.FileInput(attrs={'accept': 'image/*, .pdf', 'class': 'form-control'}),
            'retired_certificate': forms.FileInput(attrs={'accept': 'image/*, .pdf', 'class': 'form-control'}),
            'sikkim_certificate_file': forms.FileInput(attrs={'accept': 'image/*, .pdf', 'class': 'form-control'}),
            'signature_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'signature': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tenant_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'tehsil': forms.TextInput(attrs={'class': 'form-control'}),
            'post_office': forms.TextInput(attrs={'class': 'form-control'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'police_station': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'owner_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.Select(attrs={'class': 'form-control'}),
            'other_profession': forms.TextInput(attrs={'class': 'form-control'}),
            'serving_employee': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'retired_employee': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'sikkim_certificate': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'previous_police_station': forms.TextInput(attrs={'class': 'form-control'}),
        }

class HomeOwnerForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = HomeOwner
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhar_card': forms.FileInput(attrs={'accept': 'image/*, .pdf', 'class': 'form-control'}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'sikkim_certificate': forms.FileInput(attrs={'accept': 'image/*, .pdf', 'class': 'form-control'}),
            'residential_certificate': forms.FileInput(attrs={'accept': 'image/*, .pdf', 'class': 'form-control'}),
            'land_parcha': forms.FileInput(attrs={'accept': 'image/*, .pdf', 'class': 'form-control'}),
        }

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        exclude = ['tenant']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PreviousResidenceForm(forms.ModelForm):
    class Meta:
        model = PreviousResidence
        exclude = ['tenant']
        widgets = {
            'from_place': forms.TextInput(attrs={'class': 'form-control'}),
            'to_place': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

class OTPVerificationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
