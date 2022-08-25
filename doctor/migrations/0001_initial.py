from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('adress', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='doctors')),
                ('description', models.TextField()),
                ('number', models.CharField(max_length=13)),
                ('categories', models.ManyToManyField(related_name='doctors', to='doctor.category')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='doctor.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='doctor.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='doctor.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrys_time', models.DateTimeField(auto_now_add=True)),
                ('time_slot', models.IntegerField(choices=[(0, '09:00 - 10:00'), (1, '10:00 - 11:00'), (2, '11:00 - 12:00'), (3, '12:00 - 13:00'), (4, '14:00 - 15:00'), (5, '15:00 - 16:00'), (6, '16:00 - 17:00'), (7, '17:00 - 18:00')])),
                ('date', models.DateField(help_text='YYYY-MM-DD')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entrys', to='doctor.doctor')),
                ('service_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entrys', to='doctor.servicelisting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entrys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='service_listing',
            field=models.ManyToManyField(blank=True, null=True, related_name='doctors', to='doctor.servicelisting'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='doctor.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='my_doctors',
            field=models.ManyToManyField(blank=True, null=True, related_name='categorys', to='doctor.doctor'),
        ),
    ]
