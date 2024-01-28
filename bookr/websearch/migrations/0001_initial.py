# Generated by Django 4.2.4 on 2024-01-28 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_search', models.CharField(max_length=150)),
                ('exa_result', models.JSONField(default=list)),
                ('wikipedia_result', models.JSONField(default=list)),
                ('duckduckgo_result', models.JSONField(default=list)),
            ],
        ),
    ]
