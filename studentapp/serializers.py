from rest_framework.serializers import ModelSerializer

from .models import *

class Loginserializer(ModelSerializer):
 class Meta:
    model=Registration_table
    fields=['user_name','phone_number',' password','confirm_password','user_type']
    