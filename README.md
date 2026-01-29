# RoMA - Sistema de Gestión de Proyectos y Catálogo de Materiales

**RoMA** es una plataforma web integral desarrollada en **Django** diseñada para optimizar la gestión de portfolios de obras civiles/industriales y catálogos de productos premium (Porcelanatos y Prefabricados de Hormigón).

Este proyecto combina un **CMS (Sistema de Gestión de Contenidos)** personalizado con una interfaz pública moderna, permitiendo a la administración mantener actualizado su inventario y portfolio de obras con facilidad.

---

## 🚀 Características Principales

### 🏗️ Gestión de Portfolio de Proyectos
- **Categorización Inteligente**: Clasificación de proyectos en Ingeniería Civil, Industrial y Otros.
- **Galerías Multimedia**: Soporte para múltiples imágenes y videos (YouTube/Vimeo) por proyecto.
- **Fichas Técnicas**: Detalles de cliente, fechas de finalización y descripciones técnicas.

### 📦 Catálogo de Productos Avanzado
- **Módulo de Porcelanatos**:
  - Clasificación por tipología (Madera, Mármol, Cemento, etc.).
  - Ficha técnica detallada: Dimensiones, uso (Interior/Exterior), rectificado, precio y rendimiento por caja.
- **Módulo de Prefabricados de Hormigón**:
  - Catálogo específico para elementos de construcción pesada.

### 🛡️ Seguridad y Auditoría
- **Sistema de Auditoría (Audit Log)**: Registro automático de acciones críticas (Logins exitosos/fallidos, IP del usuario).
- **Protección contra Fuerza Bruta**: Implementación de `django-ratelimit` en el login para prevenir ataques automatizados.
- **Roles y Permisos**: Acceso restringido al panel de administración y áreas de edición.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3, Django 5.x
- **Base de Datos**: SQLite (Entorno Local) / PostgreSQL (Producción recomendado)
- **Seguridad**: `django-ratelimit`, Gestión de variables de entorno con `python-dotenv`.
- **Media**: Gestión eficiente de archivos estáticos y media con `Whitenoise`.
- **Frontend**: HTML5, CSS3, JavaScript (integrado con Templates de Django).

---

## 🔧 Instalación y Configuración Local

Sigue estos pasos para levantar el proyecto en tu entorno local:

1.  **Clonar el repositorio**
    ```bash
    git clone https://github.com/GerardodeMartini/RoMA.git
    cd roma
    ```

2.  **Crear entorno virtual**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno**
    Crea un archivo `.env` en la raíz del proyecto (basado en el ejemplo o solicitando las claves al administrador):
    ```env
    SECRET_KEY=tu_clave_secreta_aqui
    DEBUG=True
    ```

5.  **Migrar base de datos**
    ```bash
    python manage.py migrate
    ```

6.  **Crear superusuario** (para acceder al admin)
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecutar el servidor**
    ```bash
    python manage.py runserver
    ```

---

## 📂 Estructura del Proyecto

- `projects/`: Aplicación principal que contiene la lógica de negocio (Modelos, Vistas, Forms).
- `config/`: Configuraciones globales del proyecto Django (Settings, URLs principales).
- `templates/`: Plantillas HTML para el frontend.
- `static/` y `media/`: Archivos estáticos y contenido subido por usuarios.

---

## 👤 Autor

Desarrollado por **Gerardo**.
*Portfolio Version 1.0*
