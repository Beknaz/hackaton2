# Generated by Django 4.1 on 2022-08-22 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_alter_category_my_doctors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='my_doctors',
            field=models.ManyToManyField(blank=True, null=True, related_name='categorys', to='doctor.doctor'),
        ),
    ]
