from rest_framework import serializers
from .models import product

class ProductSerializer(serializers.ModelSerializer):


 class Meta:                                   # أي موديل نستخدم
                                               #أي الحقول نعرضها
    model = product
    fields = '__all__'                         #fields = ['name', 'price']
    

