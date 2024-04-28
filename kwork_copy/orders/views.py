from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from orders.permissions import IsOwnerOrReadOnly
from orders.serializers import OrderSerializer
from users.models import CustomerProfile
from .models import Order


class OrderViewSet(GenericViewSet):
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_orders(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_order(self, request, pk):
        order = self.get_object()
        serializer = OrderSerializer(order, partial=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_order(self, request, pk):
        order = self.get_object()
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_order(self, request, pk):
        order = self.get_object()
        order.delete()
        return Response('Order deleted successfully', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        user = request.user
        profile = CustomerProfile.objects.all().filter(user=user).first()
        serializer = OrderSerializer(data=request.data, context={'user': profile})
        if serializer.is_valid():
            serializer.save(customer=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
