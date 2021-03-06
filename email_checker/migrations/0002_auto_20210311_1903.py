# Generated by Django 3.1.7 on 2021-03-11 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_checker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvfile',
            name='csv_file',
            field=models.FileField(upload_to=''),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('write_date', models.DateTimeField(auto_now=True, null=True)),
                ('email', models.TextField(max_length=256)),
                ('valid', models.BooleanField(blank=True, null=True)),
                ('accessible', models.BooleanField(blank=True, null=True)),
                ('catchall', models.BooleanField(blank=True, null=True)),
                ('csv_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='email_checker.csvfile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
