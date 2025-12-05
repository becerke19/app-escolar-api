# Generated migration to fix materias_json data format
import ast
import json
from django.db import migrations


def fix_materias_json(apps, schema_editor):
    """Convierte datos viejos de materias_json (strings de Python) a JSON válido"""
    Maestros = apps.get_model('app_escolar_api', 'Maestros')
    
    for maestro in Maestros.objects.all():
        if maestro.materias_json and isinstance(maestro.materias_json, str):
            try:
                # Intenta parsear como representación de Python (comillas simples)
                parsed = ast.literal_eval(maestro.materias_json)
                if isinstance(parsed, list):
                    # Convierte a JSON válido
                    maestro.materias_json = json.dumps(parsed)
                    maestro.save()
            except (ValueError, SyntaxError):
                # Si no puede parsear, lo deja como array vacío
                maestro.materias_json = []
                maestro.save()


def reverse_fix(apps, schema_editor):
    """Función inversa (no hace nada en este caso)"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app_escolar_api', '0008_alter_maestros_materias_json'),
    ]

    operations = [
        migrations.RunPython(fix_materias_json, reverse_fix),
    ]
