# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-27 09:27
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields

import exo_messages.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'created', model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name='created',
                    ),
                ),
                (
                    'modified', model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name='modified',
                    ),
                ),
                ('can_be_closed', models.BooleanField(default=False)),
                ('read_when_login', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(null=True)),
                ('description', models.TextField(blank=True)),
                (
                    'code', models.CharField(
                        choices=[
                            ('P', 'PENDING_VALIDATION_EMAIL'), (
                                'V',
                                'CONFIRMATION_VALIDATION_EMAIL',
                            ), ('W', 'PENDING_CHANGE_PASSWORD'),
                        ], max_length=1,
                    ),
                ),
                (
                    'level', models.IntegerField(choices=[
                        (10, 'debug'),
                        (20, 'info'), (25, 'success'), (30, 'warning'), (40, 'error'),
                    ]),
                ),
                ('variables', django.contrib.postgres.fields.jsonb.JSONField()),
                (
                    'user', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='messages', to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelManagers(
            name='message',
            managers=[
                ('objects', exo_messages.manager.MessageManager()),
            ],
        ),
    ]