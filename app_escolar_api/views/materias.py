from django.db.models import *
from django.db import transaction
from app_escolar_api.serializers import MateriaSerializer
from app_escolar_api.models import Materias, Maestros
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class MateriasAll(generics.CreateAPIView):
    # Obtener la lista de todas las materias
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materias = Materias.objects.all().order_by("nrc")
        lista = MateriaSerializer(materias, many=True).data
        return Response(lista, 200)

class MateriasView(generics.CreateAPIView):
    # Obtener materia por ID
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        materia_data = MateriaSerializer(materia, many=False).data
        return Response(materia_data, 200)
    
    # Registrar nueva materia
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        
        # Validar que el NRC no esté duplicado
        nrc = request.data.get("nrc")
        if Materias.objects.filter(nrc=nrc).exists():
            return Response({"message": f"El NRC {nrc} ya está registrado"}, 400)
        
        # Validar que el profesor exista
        profesor_id = request.data.get("profesor_asignado_id")
        try:
            profesor = Maestros.objects.get(id=profesor_id)
        except Maestros.DoesNotExist:
            return Response({"message": "El profesor seleccionado no existe"}, 400)
        
        try:
            materia = Materias.objects.create(
                nrc=request.data["nrc"],
                nombre=request.data["nombre"],
                seccion=request.data["seccion"],
                dias_json=request.data["dias"],
                hora_inicio=request.data["hora_inicio"],
                hora_fin=request.data["hora_fin"],
                salon=request.data["salon"],
                programa_educativo=request.data["programa_educativo"],
                profesor=profesor,
                creditos=int(request.data["creditos"])
            )
            materia.save()
            return Response({
                "message": "Materia registrada exitosamente",
                "materia_id": materia.id,
                "materia": MateriaSerializer(materia).data
            }, 201)
        except Exception as e:
            return Response({"message": f"Error al registrar la materia: {str(e)}"}, 400)
    
    # Actualizar materia
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        materia = get_object_or_404(Materias, id=request.data["id"])
        
        # Validar NRC duplicado (excepto el mismo registro)
        nrc = request.data.get("nrc")
        if Materias.objects.filter(nrc=nrc).exclude(id=materia.id).exists():
            return Response({"message": f"El NRC {nrc} ya está registrado en otra materia"}, 400)
        
        # Validar que el profesor exista
        profesor_id = request.data.get("profesor_asignado_id")
        try:
            profesor = Maestros.objects.get(id=profesor_id)
        except Maestros.DoesNotExist:
            return Response({"message": "El profesor seleccionado no existe"}, 400)
        
        try:
            materia.nrc = request.data["nrc"]
            materia.nombre = request.data["nombre"]
            materia.seccion = request.data["seccion"]
            materia.dias_json = request.data["dias"]
            materia.hora_inicio = request.data["hora_inicio"]
            materia.hora_fin = request.data["hora_fin"]
            materia.salon = request.data["salon"]
            materia.programa_educativo = request.data["programa_educativo"]
            materia.profesor = profesor
            materia.creditos = int(request.data["creditos"])
            materia.save()
            
            return Response({
                "message": "Materia actualizada correctamente",
                "materia": MateriaSerializer(materia).data
            }, 200)
        except Exception as e:
            return Response({"message": f"Error al actualizar la materia: {str(e)}"}, 400)
    
    # Eliminar materia
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        try:
            materia.delete()
            return Response({"message": "Materia eliminada correctamente"}, 200)
        except Exception as e:
            return Response({"message": f"Error al eliminar la materia: {str(e)}"}, 400)
