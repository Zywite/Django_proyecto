# Sistema de Gestión de Albergue

Este proyecto es una aplicación web desarrollada en **Django** para la gestión integral de un albergue. Permite administrar habitaciones, reservas, inventario de recursos, clima y mensajes de contacto.

## 🚀 Características

-   **Gestión de Habitaciones**: Control de disponibilidad, tipos y precios.
-   **Reservas**: Sistema para registrar y gestionar estancias de clientes.
-   **Inventario**: Control de recursos (consumibles y reutilizables) y sus movimientos.
-   **Clima**: Registro de condiciones climáticas.
-   **Contacto**: Formulario para recibir mensajes y sugerencias de los usuarios.
-   **Diseño Moderno**: Interfaz limpia y responsiva con tema personalizado.

## 🛠️ Requisitos Previos

-   Python 3.8 o superior
-   PostgreSQL (recomendado) o SQLite (por defecto para desarrollo rápido)
-   Virtualenv (opcional pero recomendado)

## 📥 Instalación

1.  **Clonar el repositorio** (si aún no lo tienes):
    ```bash
    git clone https://github.com/Zywite/Django_proyecto
    cd albergue_project
    ```

2.  **Crear y activar un entorno virtual**:
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r ../requirements.txt
    ```

4.  **Configurar la Base de Datos**:
    -   Asegúrate de tener PostgreSQL corriendo y una base de datos llamada `albergue_db` creada (o ajusta `settings.py`).
    -   Aplica las migraciones:
        ```bash
        python manage.py migrate
        ```

5.  **Poblar la Base de Datos (Datos de Prueba)**:
    -   Para tener datos iniciales (usuarios, habitaciones, etc.), ejecuta:
        ```bash
        python populate_db.py
        ```

6.  **Crear un Superusuario (Admin)**:
    ```bash
    python manage.py createsuperuser
    ```

## ▶️ Ejecución

Para iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

Abre tu navegador en `http://127.0.0.1:8000/`.

## 🤝 Colaboración

### Estructura del Proyecto
-   `albergue_project/`: Configuración principal del proyecto.
-   `gestion/`: Aplicación principal con modelos, vistas y formularios.
-   `templates/`: Archivos HTML.
-   `static/`: Archivos CSS, JS e imágenes.

### Flujo de Trabajo
1.  Asegúrate de estar en la rama correcta.
2.  Haz tus cambios.
3.  Ejecuta las migraciones si modificaste modelos (`makemigrations` y `migrate`).
4.  Haz commit de tus cambios con mensajes claros en español.

---
Desarrollado con ❤️ usando Django.
