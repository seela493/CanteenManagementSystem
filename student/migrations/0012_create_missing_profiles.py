from django.db import migrations

def create_profiles_for_existing_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('student', 'Profile')  # Use the correct app name for your Profile model

    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            # Generate a unique RFID for each profile
            rfid_value = f"RFID{user.id:05d}"  # Example: Generate a unique RFID using the user ID
            Profile.objects.create(user=user, rfid=rfid_value)

class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_profile'),  # This should reference your last migration file
    ]

    operations = [
        migrations.RunPython(create_profiles_for_existing_users),
    ]
