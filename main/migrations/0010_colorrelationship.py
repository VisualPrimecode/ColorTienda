# Generated by Django 5.1.3 on 2024-12-31 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_color_relationships', to='main.color')),
                ('related_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_color_relationships', to='main.color')),
            ],
            options={
                'unique_together': {('base_color', 'related_color')},
            },
        ),
    ]