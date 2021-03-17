# Generated by Django 3.1.7 on 2021-03-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_checker', '0006_remove_email_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('write_date', models.DateTimeField(auto_now=True, null=True)),
                ('email', models.TextField(max_length=256)),
                ('valid', models.BooleanField(blank=True, default=False, null=True)),
                ('accessible', models.BooleanField(blank=True, default=False, null=True)),
                ('catchall', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
