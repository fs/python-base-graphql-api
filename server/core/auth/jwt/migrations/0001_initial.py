# Generated by Django 3.2.5 on 2021-07-28 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('jti', models.CharField(editable=False, max_length=255)),
                ('token', models.CharField(editable=False, max_length=255)),
                ('created_at', models.DateTimeField()),
                ('revoked_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Refresh token',
                'verbose_name_plural': 'Refresh tokens',
            },
        ),
        migrations.CreateModel(
            name='ResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(editable=False, max_length=255)),
                ('is_used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Reset token',
                'verbose_name_plural': 'Reset tokens',
            },
        ),
    ]