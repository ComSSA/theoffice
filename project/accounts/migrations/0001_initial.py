# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-31 03:47
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeydistUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('curtin_id', models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Must be a valid curtin ID', regex='^[0-9]+[A-Z]?$')])),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('tidyclub_api_token', models.CharField(blank=True, editable=False, max_length=256)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['first_name'],
                'permissions': set([('change_user_passowrd', "Can change any user's password"), ('sync_permissions', 'Can sync permissions'), ('see_admin', 'User can see the admin page')]),
            },
            bases=(models.Model,),
        ),
    ]