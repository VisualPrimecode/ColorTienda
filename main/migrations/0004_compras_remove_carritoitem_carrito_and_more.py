# Generated by Django 5.0.6 on 2024-12-11 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_carrito_carritoitem_envio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('id_tbk', models.IntegerField(default=0)),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=15)),
                ('telefono', models.CharField(max_length=12)),
                ('correo', models.EmailField(max_length=100)),
                ('costo_envio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('direccion', models.CharField(max_length=300)),
                ('neto', models.IntegerField(default=0)),
                ('iva', models.IntegerField(default=0)),
                ('total', models.IntegerField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='carritoitem',
            name='carrito',
        ),
        migrations.RemoveField(
            model_name='carritoitem',
            name='producto',
        ),
        migrations.CreateModel(
            name='produtosCompras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('oferta', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('precio_final', models.IntegerField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('session_id', models.CharField(max_length=100)),
                ('token_ws', models.CharField(max_length=200)),
                ('cod_respuesta', models.CharField(blank=True, max_length=10, null=True)),
                ('buy_order', models.CharField(max_length=100)),
                ('authorization_code', models.CharField(max_length=20)),
                ('tipo_pago', models.CharField(max_length=10)),
                ('cuotas', models.IntegerField(blank=True, null=True)),
                ('cuota_monto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('nro_tarjeta', models.CharField(max_length=4)),
                ('id_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.compras')),
                ('id_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.DeleteModel(
            name='Envio',
        ),
        migrations.DeleteModel(
            name='Carrito',
        ),
        migrations.DeleteModel(
            name='CarritoItem',
        ),
    ]
