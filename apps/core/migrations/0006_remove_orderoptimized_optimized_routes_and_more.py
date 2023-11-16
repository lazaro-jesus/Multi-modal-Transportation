# Generated by Django 4.2.7 on 2023-11-16 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_orderoptimized_optimized_routes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderoptimized",
            name="optimized_routes",
        ),
        migrations.AlterField(
            model_name="orderoptimized",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="optimized",
                to="core.order",
                verbose_name="Órden",
            ),
        ),
        migrations.DeleteModel(
            name="RouteResult",
        ),
        migrations.AddField(
            model_name="orderoptimized",
            name="optimized_routes",
            field=models.TextField(default=1, verbose_name="Rutas Optimizadas"),
            preserve_default=False,
        ),
    ]