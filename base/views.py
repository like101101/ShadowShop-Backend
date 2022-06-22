from django.shortcuts import render
from django.http import JsonResponse
from sympy import product
from .products import products
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
# Create your views here.


@api_view(['GET'])
def get_routes(request):
    return Response('Hello')


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serialzer = ProductSerializer(products, many=True)
    return Response(serialzer.data)


@api_view(['GET'])
def get_product(request, pk):
    product = Product.objects.get(_id=pk)
    serialzer = ProductSerializer(product, many=False)
    return Response(serialzer.data)
