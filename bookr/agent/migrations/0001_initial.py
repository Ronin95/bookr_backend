# Generated by Django 4.2.4 on 2024-01-29 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_messages', models.JSONField(default=list)),
                ('agent_messages', models.JSONField(default=list)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
