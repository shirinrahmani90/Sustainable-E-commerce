from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from .models import Product, Collection, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer,UpdateCartItemSerializer
from .filters import ProductFilter

class ProductPagination(PageNumberPagination):
    page_size=10


class ProductViewSet(ModelViewSet):
   queryset=Product.objects.all()
   serializer_class=ProductSerializer
   filter_backends=[DjangoFilterBackend, SearchFilter, OrderingFilter]
   filterset_class=ProductFilter
   pagination_class=ProductPagination
   search_fields=['title', 'description']
   ordering_fields=['unit_price', 'last_update']
        

   def get_serializer_context(self):
      return {'request':self.request}
   
class CollectionPagination(PageNumberPagination):
    page_size=10  
        
class CollectionViewSet(ModelViewSet):
      queryset=Collection.objects.annotate(products_count=Count('products')).all()
      serializer_class=CollectionSerializer
      pagination_class=CollectionPagination


class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
   
class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cart_id = str(instance.id)
        response_data = {'cart_id': cart_id, 'cart_data': serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)
      
class CartItemViewSet(ModelViewSet):
    http_method_names=['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
      
     

   
