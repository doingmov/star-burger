from django.db import migrations


def fill_price(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for order_item in OrderItem.objects.select_related('product').iterator():
        order_item.price = order_item.product.price
        order_item.save(update_fields=['price'])


def revert_price(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_orderitem_price'),
    ]

    operations = [
        migrations.RunPython(fill_price, revert_price),
    ]
