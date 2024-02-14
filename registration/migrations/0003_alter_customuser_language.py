# Generated by Django 4.0.3 on 2024-02-14 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_alter_customuser_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('gl', 'Galician'), ('ca', 'Catalan'), ('eu', 'Basque')], max_length=33),
        ),
    ]
