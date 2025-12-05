from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    fecha_nacimiento = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', 'iso-8601'], required=False, allow_null=True)
    class Meta:
        model = Alumnos
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    profesor_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Materias
        fields = '__all__'
    
    def get_profesor_nombre(self, obj):
        return f"{obj.profesor.user.first_name} {obj.profesor.user.last_name}"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    fecha_nacimiento = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', 'iso-8601'], required=False, allow_null=True)
    class Meta:
        model = Maestros
        fields = '__all__'