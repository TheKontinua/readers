<<<<<<< HEAD
# Generated by Django 4.2.6 on 2023-11-30 20:13
=======
# Generated by Django 4.2.5 on 2023-11-30 06:11
>>>>>>> 875bd7f (models)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
<<<<<<< HEAD
            field=models.UUIDField(default='f8958313-1ae6-4f27-8dfc-957c77f542be', editable=False, primary_key=True, serialize=False, unique=True),
=======
            field=models.UUIDField(default='efea6342-58f3-4eae-bdf9-e08987ecafec', editable=False, primary_key=True, serialize=False, unique=True),
>>>>>>> 875bd7f (models)
        ),
    ]