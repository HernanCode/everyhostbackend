# Generated by Django 3.2.12 on 2023-04-25 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0003_alter_docker_subdomain'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('software', models.CharField(max_length=100)),
                ('subdomain', models.CharField(max_length=100, unique=True)),
                ('dbadmin', models.CharField(max_length=100)),
                ('dbpassword', models.CharField(max_length=228)),
                ('replicas', models.CharField(max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Docker',
        ),
    ]
