# Deployment en Render - App Escolar API

## Pasos para desplegar:

### 1. Preparar el repositorio
Los archivos necesarios ya están configurados:
- `build.sh` - Script de construcción
- `render.yaml` - Configuración de Render
- `runtime.txt` - Versión de Python
- `requirements.txt` - Dependencias actualizadas

### 2. Subir cambios a GitHub
```bash
cd app_escolar_api
git add .
git commit -m "Configurar deployment para Render"
git push origin master
```

### 3. Crear cuenta en Render
- Ve a https://render.com
- Regístrate con tu cuenta de GitHub

### 4. Crear nuevo Web Service
1. Click en "New +" → "Web Service"
2. Conecta tu repositorio de GitHub
3. Selecciona el repositorio `app-escolarr-webapp`
4. Configuración:
   - **Name**: app-escolar-api
   - **Root Directory**: app_escolar_api
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app_escolar_api.wsgi:application`

### 5. Crear base de datos PostgreSQL
1. En Render, click en "New +" → "PostgreSQL"
2. Configuración:
   - **Name**: app-escolar-db
   - **Database**: app_escolar_db
   - **User**: app_escolar_user
   - **Plan**: Free

### 6. Configurar variables de entorno
En el Web Service, ve a "Environment" y agrega:
- `DATABASE_URL`: (se auto-completa al conectar la BD)
- `SECRET_KEY`: (genera una clave segura)
- `DEBUG`: False
- `PYTHON_VERSION`: 3.11.0

### 7. Conectar la base de datos
En el Web Service:
1. Ve a "Environment"
2. En "Environment Variables", añade la conexión a la BD PostgreSQL creada

### 8. Deploy
- Render automáticamente desplegará tu aplicación
- El proceso tomará unos minutos

## Actualizar frontend con la URL del backend

Una vez desplegado, copia la URL de Render (ej: `https://app-escolar-api.onrender.com`) y actualízala en:
- `app-escolar-webapp/src/environments/environment.prod.ts`

## Notas importantes
- **Base de datos**: En producción usa PostgreSQL (incluido gratis en Render)
- **Desarrollo local**: Sigue usando MySQL con `my.cnf`
- **CORS**: Ya configurado para aceptar requests de Vercel
- La primera vez tardará más porque creará las tablas en PostgreSQL
