# Generated by Django 3.1.1 on 2020-12-10 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('manufacture', models.CharField(max_length=255, verbose_name='Производитель')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
        ),
    ]
