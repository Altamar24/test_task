# Generated by Django 5.1.2 on 2024-10-09 10:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('breed', models.CharField(choices=[('Абиссинская', 'Абиссинская'), ('Австралийский мист', 'Австралийский мист'), ('Азиатская (табби)', 'Азиатская (табби)'), ('Американский бобтейл длинношёрстный', 'Американский бобтейл длинношёрстный'), ('Американский бобтейл короткошёрстный', 'Американский бобтейл короткошёрстный'), ('Американская жесткошёрстная', 'Американская жесткошёрстная'), ('Американский кёрл длинношёрстный', 'Американский кёрл длинношёрстный'), ('Американский кёрл короткошёрстный', 'Американский кёрл короткошёрстный'), ('Американская короткошёрстная', 'Американская короткошёрстная'), ('Анатолийская', 'Анатолийская'), ('Аравийский мау', 'Аравийский мау'), ('Балинезийская (Балинез, балийская)', 'Балинезийская (Балинез, балийская)'), ('Бенгальская', 'Бенгальская'), ('Бомбейская', 'Бомбейская'), ('Бразильская короткошёрстная', 'Бразильская короткошёрстная'), ('Британская длинношёрстная', 'Британская длинношёрстная'), ('Британская короткошёрстная', 'Британская короткошёрстная'), ('Бурма (Бурманская)', 'Бурма (Бурманская)'), ('Бурмилла длинношёрстный', 'Бурмилла длинношёрстный'), ('Бурмилла короткошёрстный', 'Бурмилла короткошёрстный'), ('Гавана', 'Гавана'), ('Гималайская кошка', 'Гималайская кошка'), ('Девон рекс', 'Девон рекс'), ('Домашняя', 'Домашняя'), ('Донской сфинкс', 'Донской сфинкс'), ('Кельтская (Европейская короткошёрстная)', 'Кельтская (Европейская короткошёрстная)'), ('Египетская мау', 'Египетская мау'), ('Йорк', 'Йорк'), ('Калифорнийская сияющая', 'Калифорнийская сияющая'), ('Канаани', 'Канаани'), ('Карельский бобтейл длинношёрстный', 'Карельский бобтейл длинношёрстный'), ('Карельский бобтейл короткошёрстный', 'Карельский бобтейл короткошёрстный'), ('Кимрик', 'Кимрик'), ('Корат', 'Корат'), ('Корниш рекс', 'Корниш рекс'), ('Курильский бобтейл длинношёрстный', 'Курильский бобтейл длинношёрстный'), ('Курильский бобтейл короткошёрстный', 'Курильский бобтейл короткошёрстный'), ('Лаперм длинношёрстный', 'Лаперм длинношёрстный'), ('Лаперм короткошёрстный', 'Лаперм короткошёрстный'), ('Манчкин длинношёрстная', 'Манчкин длинношёрстная'), ('Манчкин короткошёрстная', 'Манчкин короткошёрстная'), ('Мейн-кун', 'Мейн-кун'), ('Меконгский бобтейл', 'Меконгский бобтейл'), ('Минскин', 'Минскин'), ('Мэнкс (Мэнская кошка)', 'Мэнкс (Мэнская кошка)'), ('Наполеон', 'Наполеон'), ('Немецкий рекс', 'Немецкий рекс'), ('Нибелунг', 'Нибелунг'), ('Норвежская лесная', 'Норвежская лесная'), ('Орегон-рекс', 'Орегон-рекс'), ('Ориентальная длинношёрстная', 'Ориентальная длинношёрстная'), ('Ориентальная короткошёрстная', 'Ориентальная короткошёрстная'), ('Охос азулес', 'Охос азулес'), ('Охос азулес длинношёрстный', 'Охос азулес длинношёрстный'), ('Оцикет', 'Оцикет'), ('Персидская (Колорпойнт)', 'Персидская (Колорпойнт)'), ('Колорпойнт', 'Колорпойнт'), ('Петерболд', 'Петерболд'), ('Пиксибоб длинношёрстный', 'Пиксибоб длинношёрстный'), ('Пиксибоб короткошёрстный', 'Пиксибоб короткошёрстный'), ('Рагамаффин', 'Рагамаффин'), ('Русская голубая', 'Русская голубая'), ('Рэгдолл', 'Рэгдолл'), ('Саванна', 'Саванна'), ('Священная бирманская', 'Священная бирманская'), ('Сейшельская длинношёрстная', 'Сейшельская длинношёрстная'), ('Сейшельская короткошёрстная', 'Сейшельская короткошёрстная'), ('Селкирк рекс длинношёрстный', 'Селкирк рекс длинношёрстный'), ('Селкирк рекс короткошёрстный', 'Селкирк рекс короткошёрстный'), ('Серенгети', 'Серенгети'), ('Сиамская', 'Сиамская'), ('Сибирская', 'Сибирская'), ('Экспериментальная порода', 'Экспериментальная порода'), ('Невская маскарадная', 'Невская маскарадная'), ('Сингапурская', 'Сингапурская'), ('Скоттиш фолд', 'Скоттиш фолд'), ('Скоттиш страйт', 'Скоттиш страйт'), ('Сноу-Шу', 'Сноу-Шу'), ('Сококе', 'Сококе'), ('Сомали', 'Сомали'), ('Сфинкс (канадский)', 'Сфинкс (канадский)'), ('Тайская', 'Тайская'), ('Шантильи-тиффани', 'Шантильи-тиффани'), ('Тойгер', 'Тойгер'), ('Тонкинская', 'Тонкинская'), ('Турецкая ангора', 'Турецкая ангора'), ('Турецкий ван', 'Турецкий ван'), ('Украинский левкой', 'Украинский левкой'), ('Уральский рекс длинношёрстный', 'Уральский рекс длинношёрстный'), ('Уральский рекс короткошёрстный', 'Уральский рекс короткошёрстный'), ('Форин Вайт', 'Форин Вайт'), ('Хайленд фолд', 'Хайленд фолд'), ('Цейлонская', 'Цейлонская'), ('Хауси', 'Хауси'), ('Шартрез', 'Шартрез'), ('Эгейская кошка', 'Эгейская кошка'), ('Экзотическая', 'Экзотическая'), ('Яванез (Яванская кошка)', 'Яванез (Яванская кошка)'), ('Японский бобтейл длинношёрстный', 'Японский бобтейл длинношёрстный'), ('Японский бобтейл короткошёрстный', 'Японский бобтейл короткошёрстный')], default='Абиссинская', max_length=40)),
                ('age', models.PositiveBigIntegerField(blank=True, null=True)),
                ('hairiness', models.CharField(choices=[('Безволосая', 'Безволосая'), ('Волосатая', 'Волосатая'), ('Гладкошёрстная', 'Гладкошёрстная'), ('Длинношёрстная', 'Длинношёрстная'), ('Короткошёрстная', 'Короткошёрстная'), ('Полудлинношёрстная', 'Полудлинношёрстная')], default='Безволосая', max_length=20)),
                ('breeder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Кот',
                'verbose_name_plural': 'Коты',
            },
        ),
    ]
