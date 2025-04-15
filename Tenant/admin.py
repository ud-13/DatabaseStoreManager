from django.contrib import admin
from .models import User, Tenant, FamilyMember, PreviousResidence, HomeOwner

class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 1

class PreviousResidenceInline(admin.TabularInline):
    model = PreviousResidence
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('OTP', {'fields': ('otp', 'otp_created_at')}),
    )
    readonly_fields = ('date_joined',)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'tenant_phone_number', 'district', 'status', 'police_status', 'created_at')
    list_filter = ('district', 'profession', 'status', 'police_status', 'created_at')
    search_fields = ('first_name', 'last_name', 'tenant_phone_number', 'owner_phone_number')
    inlines = [FamilyMemberInline, PreviousResidenceInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'age', 'photo', 'father_name', 'tenant_phone_number')
        }),
        ('Address Information', {
            'fields': ('permanent_address', 'village', 'tehsil', 'post_office', 'pin_code', 'police_station', 'district', 'owner_phone_number')
        }),
        ('Professional Information', {
            'fields': ('profession', 'other_profession')
        }),
        ('Employment Status', {
            'fields': ('serving_employee', 'serving_certificate', 'retired_employee', 'retired_certificate')
        }),
        ('Sikkim Certificate', {
            'fields': ('sikkim_certificate', 'sikkim_certificate_file')
        }),
        ('Additional Information', {
            'fields': ('previous_police_station',)
        }),
        ('Signature', {
            'fields': ('signature_date', 'signature')
        }),
        ('Status', {
            'fields': ('status', 'police_status', 'police_remark')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'relationship', 'tenant')
    list_filter = ('relationship',)
    search_fields = ('first_name', 'last_name', 'tenant__first_name', 'tenant__last_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PreviousResidence)
class PreviousResidenceAdmin(admin.ModelAdmin):
    list_display = ('from_place', 'to_place', 'tenant')
    search_fields = ('from_place', 'to_place', 'tenant__first_name', 'tenant__last_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(HomeOwner)
class HomeOwnerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')
