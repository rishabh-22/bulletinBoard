# Generated by Django 4.0.6 on 2022-07-31 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_alter_board_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
