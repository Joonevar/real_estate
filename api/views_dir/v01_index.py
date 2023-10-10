from rest_framework.views import APIView, Response
from django.db.models import Q
from django.core.paginator import Paginator

import requests

from api.serializers import s01_property
from main.models_dir import m01_properties


class IndexApi(APIView):
    def post(self, request):
        
        action = request.data.get('action')
        if action == 'properties':
            return self.get_properties(request)


        return Response({
            "no data!"
        })


    # Get Properties as desired
    def get_properties(self, request):
        # Get serializer from request and check validation
        serializer = s01_property.PropertySearchSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': 'not_valid',
            })
        
        data            = serializer.validated_data
        returned_data   = {
            "category": "any",
        }

        keyword         = data.get('keyword')
        filter_dict     = data.get('filter_dict')
        category        = data.get('category')
        page            = data.get('page')
        
        
        properties      = m01_properties.Property.objects.order_by('id')
        properties_def  = m01_properties.Property.objects.order_by('upload_date')

        # Check for search request
        if keyword:
            properties  = properties.filter(
                Q(name__contains                    = keyword)  |
                Q(price__contains                   = keyword)  |
                Q(details__contains                 = keyword)  |
                Q(city__contains                    = keyword)  |
                Q(country__contains                 = keyword)
            )
        
        # Check for filteration request
        if filter_dict:
            if 'extra_features' in filter_dict:
                extra_features = filter_dict['extra_features']
                for i in extra_features:
                    properties = properties.filter(extra_features__contains = i)

                del filter_dict['extra_features']

            properties = properties.filter(**filter_dict)
        
        if category:
            if not category == 'any':
                properties = properties.filter(category = category)
                returned_data['category'] = category
        
            
        
        # Paginate Properties
        properties = Paginator(properties, 20)
        properties = properties.get_page(page)
        
        # Serialze Properties
        properties_serializer = s01_property.PropertySerializer(properties, many = True)
        
        returned_data["status"] = "ok"
        returned_data["data"] = properties_serializer.data
        returned_data["page"] = properties.number
        returned_data["total"] = properties.paginator.num_pages
        
        if len(properties) == 0:
            properties_def = Paginator(properties_def, 20)
            properties_def = properties_def.get_page(1)
            
            # Serialze Properties
            properties_def_serializer = s01_property.PropertySerializer(properties_def, many = True)
            returned_data["default"] = properties_def_serializer.data
        

        
        # Get Images 
        return Response(returned_data)
    
    








