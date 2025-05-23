# Generated by Django 5.2 on 2025-04-16 09:14

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('photo', models.ImageField(upload_to='tenant_photos/')),
                ('father_name', models.CharField(max_length=100)),
                ('tenant_phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid 10-digit phone number')])),
                ('permanent_address', models.TextField()),
                ('village', models.CharField(max_length=100)),
                ('tehsil', models.CharField(max_length=100)),
                ('post_office', models.CharField(max_length=100)),
                ('pin_code', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^\\d{6}$', 'Enter a valid 6-digit pin code')])),
                ('police_station', models.CharField(max_length=100)),
                ('district', models.CharField(choices=[('Gangtok', 'Gangtok'), ('Mangan', 'Mangan'), ('Pakyong', 'Pakyong'), ('Soreng', 'Soreng'), ('Namchi', 'Namchi'), ('Gyalshing', 'Gyalshing')], max_length=100)),
                ('owner_phone_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid 10-digit phone number')])),
                ('profession', models.CharField(choices=[('Government Servant', 'Government Servant'), ('Public Sector Undertaking Employee', 'Public Sector Undertaking Employee'), ('Retired Government Servant', 'Retired Government Servant'), ('Retired PSU Employee', 'Retired PSU Employee'), ('Businessman/Self-Employed', 'Businessman/Self-Employed'), ('Private Employee', 'Private Employee'), ('Others', 'Others')], max_length=50)),
                ('other_profession', models.CharField(blank=True, max_length=100, null=True)),
                ('serving_employee', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3)),
                ('serving_certificate', models.FileField(blank=True, null=True, upload_to='certificates/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('retired_employee', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3)),
                ('retired_certificate', models.FileField(blank=True, null=True, upload_to='certificates/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('sikkim_certificate', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3)),
                ('sikkim_certificate_file', models.FileField(blank=True, null=True, upload_to='certificates/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('previous_police_station', models.CharField(blank=True, max_length=100, null=True)),
                ('signature_date', models.DateField()),
                ('signature', models.ImageField(upload_to='signatures/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('police_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('police_remark', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Tenant',
                'verbose_name_plural': 'Tenants',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PreviousResidence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_place', models.CharField(max_length=100)),
                ('to_place', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previous_residences', to='Tenant.tenant')),
            ],
            options={
                'verbose_name': 'Previous Residence',
                'verbose_name_plural': 'Previous Residences',
                'ordering': ['tenant', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('relationship', models.CharField(max_length=100)),
                ('profession', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_members', to='Tenant.tenant')),
            ],
            options={
                'verbose_name': 'Family Member',
                'verbose_name_plural': 'Family Members',
                'ordering': ['tenant', 'relationship'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(choices=[('tenant', 'Tenant'), ('home_owner', 'Home Owner'), ('police', 'Police')], max_length=20)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_created_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.AddField(
            model_name='tenant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='HomeOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('photo', models.ImageField(upload_to='homeowner_photos/')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d{10,15}$', 'Enter a valid phone number')])),
                ('aadhar_card', models.FileField(upload_to='aadhar_cards/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('aadhar_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator('^\\d{12}$', 'Enter a valid 12-digit Aadhar number')])),
                ('sikkim_certificate', models.FileField(upload_to='sikkim_certificates/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('residential_certificate', models.FileField(upload_to='residential_certificates/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('land_parcha', models.FileField(upload_to='land_parchas/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='homeowner_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Home Owner',
                'verbose_name_plural': 'Home Owners',
                'ordering': ['-created_at'],
            },
        ),
    ]
