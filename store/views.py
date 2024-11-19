from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .Pagination import DefaultPageNumberPagination
from .filter import ProductFilter
from .models import Product, Review, CartItem, Cart, Order
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer, CollectionSerializer, CreateProductSerializer, ReviewSerializer, \
    CartItemSerializer, CartSerializer, AddToCartSerializer, CartUpdateSerializer, OrderSerializer, \
    CreateOrderSerializer
from .models import Collection


# Create your views here.

# class ProductListAPIView(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
#
# class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
#
# class CollectionDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#
#
# class CollectionListView(ListCreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = PageNumberPagination


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = DefaultPageNumberPagination
    permission_classes = [IsAdminOrReadOnly]


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        elif self.request.method == 'PATCH':
            return CartUpdateSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderViewSet(ModelViewSet):
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderSerializer
        return CreateOrderSerializer

    def get_serializer_context(self):
        return {'cart_id': self.request.user.id}


@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        productsAll = Product.objects.all()
        serializer = ProductSerializer(productsAll, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product(request, pk):
    # try:
    #     productDetails = Product.objects.get(pk=pk)
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializer(productDetails)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # except Product.DoesNotExist:
    #     return Response({"message:" f"product with {pk} does not exist"})

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = CreateProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection(request, pk):
    selected_collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(selected_collection)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def collections(request):
    all_collections = Collection.objects.all()
    serializer = CollectionSerializer(all_collections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
