# Generated by Django 5.0.6 on 2024-06-26 11:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_alter_news_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="news",
            options={"verbose_name": "News", "verbose_name_plural": "News"},
        ),
    ]
