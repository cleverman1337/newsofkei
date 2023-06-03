# Generated by Django 4.1.7 on 2023-04-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsline', '0004_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='imgurl',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ссылка на изображение'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='anons',
            field=models.CharField(max_length=250, verbose_name='анонс'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='title',
            field=models.CharField(max_length=140, verbose_name='имя статьи'),
        ),
    ]
