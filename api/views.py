from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import serializers
from servicestarter.utils import CustomSchema
import coreapi
import re

ITEM_COUNT_PER_PAGE = 20
SCHEMA_FILED_EXCEPT = ['page', 'filter', 'id']
CHAIN_FILTER = [
  'startswith', 'endwith', 
  'lte', 'gte', 'gt', 'lt', 
  'contains', 'icontains', 
  'exact', 'iexact']

def getSerializer(modelClass):
  class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelClass
        fields = '__all__'
  return ApiSerializer

def applyPagination(queryset, serializer_class,  page):
  paginator = Paginator(queryset, ITEM_COUNT_PER_PAGE)
  try:
    items = paginator.page(page)
  except PageNotAnInteger:
    items = paginator.page(1)
  except EmptyPage:
    items = paginator.page(paginator.num_pages)
  serializers = serializer_class(items, many=True)
  res = {
    'total_page': paginator.num_pages,
    'items': serializers.data
  }
  res['total_page'] 
  return res

def applyOption(request, queryset):
  op = request.GET.get('filter')
  params = {}
  for key in request.GET:
    if key in SCHEMA_FILED_EXCEPT:
      continue
    if op in CHAIN_FILTER:
      params[key+'__'+op] = request.GET.get(key)
    else:
      params[key] = request.GET.get(key)

  return queryset.filter(**params)

def addAllFieldToSchema(model, schema):
  for field in model._meta.fields:
    name = field.__str__().split('.')[-1]
    if name in SCHEMA_FILED_EXCEPT:
      continue
    schema.append(coreapi.Field(name, location='query'))
  return schema

def getViewSet(modelClass):
  @permission_classes((IsAuthenticatedOrReadOnly,))
  @authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
  class ApiViewSet(viewsets.ModelViewSet):
    queryset = modelClass.objects.all().order_by('-id')
    serializer_class = getSerializer(modelClass)

    schema = CustomSchema({
      'list': addAllFieldToSchema(modelClass, [
        coreapi.Field('page', required=False, location='query', type='int',description='It is for pagination. If not set, no pagination'),
        coreapi.Field('filter', required=False, location='query', type='string',description='support : '+', '.join(CHAIN_FILTER)),
      ])
    })

    def list(self, request):
      page = request.GET.get('page')

      queryset = applyOption(request, self.queryset)

      if page:
        res = applyPagination(queryset, self.serializer_class, page)
      else:
        serializers = self.serializer_class(queryset, many=True)
        res = serializers.data

      return Response(res, status=status.HTTP_200_OK)

  return ApiViewSet
