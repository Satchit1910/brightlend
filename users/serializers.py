from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # credit_score = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'email','annual_income','credit_score')
