# Generated by Django 4.0.3 on 2024-01-30 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('es', 'Spanish'), ('gl', 'Galician'), ('ca', 'Catalan'), ('eu', 'Basque')], max_length=33, null=True),
        ),
    ]
