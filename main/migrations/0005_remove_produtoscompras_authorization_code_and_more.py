# Generated by Django 5.0.6 on 2024-12-12 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_compras_remove_carritoitem_carrito_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produtoscompras',
            name='authorization_code',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='buy_order',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='cod_respuesta',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='cuota_monto',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='cuotas',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='date_time',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='nro_tarjeta',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='session_id',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='tipo_pago',
        ),
        migrations.RemoveField(
            model_name='produtoscompras',
            name='token_ws',
        ),
    ]
