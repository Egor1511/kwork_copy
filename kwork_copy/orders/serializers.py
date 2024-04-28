from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'title', 'description', 'price', 'customer',
                  'freelancer']
        read_only_fields = ['customer']

