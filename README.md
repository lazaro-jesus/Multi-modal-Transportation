# Multi-model Transportation

Descripción general del proyecto

## Pasos para correr el proyecto

### Configuración del entorno

**Crear variables de entorno:**

Copiar el contenido de `.env.example` a un nuevo archivo y nombrarlo `.env`.

```bash
cp .env.example .env
```

**Crear entorno virtual:**

```bash
python3 -m venv env
```

o en Windows:

```powershell
py -m venv env
```

**Activar entorno virtual:**

En Unix o MacOS:

```bash
source env/bin/activate
```

En Windows

```powershell
.\env\Scripts\activate
```

**Instalar dependencias:**

```bash
pip install -r requirements.txt
```

### Configuración de la base de datos

**Migrar base de datos:**

```bash
python manage.py makemigrations
python manage.py migrate
```

### Poblar la base de datos con datos de ejemplo

**Crear datos de ejemplo:**

```bash
python manage.py create_data
```

### Correr el proyecto

**Correr aplicación:**

```bash
python manage.py runserver
```
