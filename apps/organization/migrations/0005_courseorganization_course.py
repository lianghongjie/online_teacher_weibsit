# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-01 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('organization', '0004_courseorganization_course_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorganization',
            name='course',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.Course', verbose_name='\u8bfe\u7a0b\u5916\u952e'),
            preserve_default=False,
        ),
    ]