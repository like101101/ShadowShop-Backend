from http.client import PAYMENT_REQUIRED
import imp
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from sympy import product
from yaml import serialize

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        if 'address2' in data['shippingAddress']:
            shipping = ShippingAddress.objects.create(
                order=order,
                address1=data['shippingAddress']['address1'],
                address2=data['shippingAddress']['address2'],
                city=data['shippingAddress']['city'],
                postalCode=data['shippingAddress']['postal'],
                states=data['shippingAddress']['states'],
            )
        else:
             shipping = ShippingAddress.objects.create(
                order=order,
                address1=data['shippingAddress']['address1'],
                address2='',
                city=data['shippingAddress']['city'],
                postalCode=data['shippingAddress']['postal'],
                states=data['shippingAddress']['states'],
            )


        for eachItem in orderItems:
            product = Product.objects.get(_id=eachItem['product'])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=eachItem['qty'],
                price=eachItem['price'],
                image=product.image.url,
            )
            product.countInStock -= int(item.qty)
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    serialzer = OrderSerializer(orders, many=True)
    return Response(serialzer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)