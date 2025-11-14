# API CRUD de Ventas de Autos - FastAPI

## Descripción del Proyecto

Este proyecto implementa una API REST completa para la gestión de ventas de autos utilizando **FastAPI**, **SQLModel** y **PostgreSQL**. El sistema permite administrar un inventario de autos y registrar las ventas realizadas, implementando todas las operaciones CRUD y aplicando patrones de diseño profesionales.

## Características Implementadas

### Entidades Principales

#### Auto
- **marca**: Marca del vehículo (ej: Toyota, Ford, Chevrolet)
- **modelo**: Modelo específico (ej: Corolla, Focus, Cruze)  
- **año**: Año de fabricación (entre 1900 y año actual)
- **numero_chasis**: Número único de identificación del chasis (alfanumérico, único en el sistema)

#### Venta
- **nombre_comprador**: Nombre completo del comprador
- **precio**: Precio de venta del vehículo
- **auto_id**: Referencia al auto vendido (clave foránea)
- **fecha_venta**: Fecha y hora de la venta

### Funcionalidades

#### API de Autos (/autos)
- `POST /autos` - Crear nuevo auto
- `GET /autos` - Listar autos con paginación
- `GET /autos/{auto_id}` - Obtener auto por ID
- `PUT /autos/{auto_id}` - Actualizar auto
- `DELETE /autos/{auto_id}` - Eliminar auto
- `GET /autos/chasis/{numero_chasis}` - Buscar por número de chasis
- `GET /autos/{auto_id}/with-ventas` - Auto con sus ventas
- `GET /autos/search/` - Búsqueda por marca y modelo

#### API de Ventas (/ventas)
- `POST /ventas` - Crear nueva venta
- `GET /ventas` - Listar ventas con paginación
- `GET /ventas/{venta_id}` - Obtener venta por ID
- `PUT /ventas/{venta_id}` - Actualizar venta
- `DELETE /ventas/{venta_id}` - Eliminar venta
- `GET /ventas/auto/{auto_id}` - Ventas de un auto específico
- `GET /ventas/comprador/{nombre}` - Ventas por nombre de comprador
- `GET /ventas/{venta_id}/with-auto` - Venta con información del auto
- `GET /ventas/search/` - Búsqueda avanzada con filtros

#### APIs Existentes
- **Personas CRUD** (/personas) - Gestión de personas con relación a países
- **Países CRUD** (/paises) - Gestión de países
- **Objetos API** (/objects) - API de objetos en memoria

## Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido para APIs
- **SQLModel** - ORM moderno de SQLAlchemy con integración Pydantic
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos y serialización
- **Docker** - Contenedorización de PostgreSQL
- **Uvicorn** - Servidor ASGI para ejecutar FastAPI

## Instalación y Configuración

### Prerrequisitos

- Python 3.7 o superior
- pip (administrador de paquetes de Python)
- Docker (para PostgreSQL) o PostgreSQL instalado localmente

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd utn-tup-2025-fastapi
   ```

2. **Crear un entorno virtual**
   ```bash
   # Crear entorno virtual
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar PostgreSQL con Docker (Recomendado)**

   **Opción A: Con docker-compose**
   ```bash
   # Levantar el contenedor PostgreSQL
   docker-compose up -d postgres_utn
   
   # Ver logs del contenedor
   docker-compose logs postgres_utn
   
   # Parar el contenedor
   docker-compose down
   ```

   **Opción B: Con Docker directamente**
   ```bash
   # Construir la imagen
   docker build -f Dockerfile.postgres -t postgres-utn .
   
   # Ejecutar el contenedor
   docker run -d \
     --name postgres_utn_db \
     -e POSTGRES_DB=UTN \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -p 55432:5432 \
     -v postgres_utn_data:/var/lib/postgresql/data \
     postgres-utn
   ```

5. **Configurar variables de entorno**
   
   Crear un archivo `.env` basado en `env_example.txt`:
   ```bash
   # Copia el archivo de ejemplo
   cp env_example.txt .env
   
   # Edita .env con tus credenciales de PostgreSQL
   DATABASE_URL=postgresql://postgres:postgres@localhost:55432/UTN
   ```

### Conexión a la Base de Datos

- **Host**: localhost
- **Puerto**: 55432 (Docker) o 5432 (instalación local)
- **Base de datos**: UTN
- **Usuario**: postgres
- **Contraseña**: postgres
- **URL de conexión**: `postgresql://postgres:postgres@localhost:55432/UTN`

## Ejecutar la Aplicación

1. **Asegúrate de tener el entorno virtual activado**
   ```bash
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

2. **Iniciar el servidor de desarrollo**
   ```bash
   uvicorn main:app --reload
   ```

   O alternativamente:
   ```bash
   python -m uvicorn main:app --reload
   ```

3. **La aplicación estará disponible en:**
   - **API**: http://localhost:8000
   - **Documentación Interactiva**: http://localhost:8000/docs
   - **Documentación Alternativa**: http://localhost:8000/redoc

## Ejemplos de Uso de la API

### Crear un Auto:
```json
POST /autos
{
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "TOY2023COR123456"
}
```

### Crear una Venta:
```json
POST /ventas
{
    "nombre_comprador": "Juan Pérez",
    "precio": 25000.00,
    "auto_id": 1,
    "fecha_venta": "2024-03-15T10:30:00"
}
```

### Respuesta de Auto con Ventas:
```json
GET /autos/1/with-ventas
{
    "id": 1,
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "TOY2023COR123456",
    "ventas": [
        {
            "id": 1,
            "nombre_comprador": "Juan Pérez",
            "precio": 25000.00,
            "fecha_venta": "2024-03-15T10:30:00"
        }
    ]
}
```

## Estructura del Proyecto

```
proyecto/
├── main.py              # Aplicación FastAPI principal
├── database.py          # Configuración de base de datos
├── models.py            # Modelos SQLModel (Persona, Pais, Auto, Venta)
├── repository.py        # Patrón Repository para acceso a datos
├── personas.py          # Router de endpoints para personas
├── paises.py           # Router de endpoints para países
├── autos.py            # Router de endpoints para autos
├── ventas.py           # Router de endpoints para ventas
├── objects.py          # Router de endpoints para objetos (en memoria)
├── requirements.txt     # Dependencias Python
├── env_example.txt     # Ejemplo de variables de entorno
├── docker-compose.yml  # Configuración Docker Compose
├── Dockerfile.postgres # Dockerfile para PostgreSQL
└── README.md           # Este archivo
```

## Validaciones Implementadas

### Auto
- Año entre 1900 y año actual
- Número de chasis único y alfanumérico
- Marca y modelo requeridos

### Venta
- Precio mayor a 0
- Nombre del comprador no vacío
- Fecha no futura
- Auto debe existir antes de crear la venta

## Características Técnicas

### Patrón Repository
- Interfaces abstractas para cada entidad
- Implementaciones concretas con SQLModel
- Separación clara de responsabilidades

### Validaciones y Manejo de Errores
- Validación de integridad referencial
- Manejo apropiado de errores HTTP (400, 404, 422)
- Validaciones de datos con Pydantic

### Paginación
- Implementada en endpoints de listado
- Parámetros `skip` y `limit` con valores por defecto
- Validación de parámetros de paginación

### Funcionalidades de Búsqueda
- Búsqueda de autos por marca y modelo (parcial)
- Búsqueda de ventas por nombre de comprador
- Filtros por rango de fechas en ventas
- Filtros por rango de precios

## Documentación Interactiva

FastAPI genera automáticamente documentación interactiva de la API. Visita:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Estas interfaces te permiten:
- Ver todos los endpoints disponibles
- Ver esquemas de peticiones/respuestas
- Probar la API directamente desde el navegador
- Descargar la especificación OpenAPI

## Comandos Útiles

```bash
# Ejecutar aplicación en modo desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Verificar conexión a PostgreSQL
psql -h localhost -p 55432 -U postgres -d UTN

# Parar la aplicación
Ctrl + C

# Desactivar entorno virtual
deactivate
```

## Solución de Problemas Comunes

- **Error "uvicorn: command not found"**: Asegúrate de que el entorno virtual esté activado
- **Error de puerto ocupado**: Usa un puerto diferente con `--port 8080`
- **Error de conexión a PostgreSQL**: Verifica que Docker esté ejecutándose y el contenedor esté activo
- **Error de permisos**: En Linux/macOS, usa `python3` en lugar de `python`

## Notas Importantes

- **Seguridad**: Implementar validaciones robustas en todos los endpoints
- **Performance**: Usar paginación en listados grandes
- **Mantenibilidad**: Seguir principios SOLID en el diseño
- **Documentación**: FastAPI genera documentación automática, pero agregar comentarios en el código

## Licencia

Este es un proyecto de ejemplo con fines educativos para la Universidad Tecnológica Nacional.

---

**¡Proyecto completado exitosamente!** 🚗💻
