# Generated by Django 3.2.3 on 2024-09-20 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_remove_recipe_if_favorited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.ingredient', verbose_name='Ингридиент'),
        ),
    ]
