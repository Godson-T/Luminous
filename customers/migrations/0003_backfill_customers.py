from django.db import migrations

def create_customers(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Customer = apps.get_model('customers', 'Customer')

    for user in User.objects.all():
        if not hasattr(user, 'customer_profile'):
            Customer.objects.create(
                user=user,
                name=user.username,
                address="",
                phone=""
            )

class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_customers),
    ]
