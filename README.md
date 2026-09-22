# Gestor Personal

Aplicación de escritorio (Windows) para gestionar tareas y notas, hecha en Python con PySide6 (Qt nativo) y SQLite. No es una página web: es una ventana de escritorio real.

## Funciones
- **Panel principal**: estadísticas (totales, pendientes, completadas, vencidas) y próximas tareas con fecha límite.
- **Tareas**: crear, editar, eliminar, marcar como completadas, categorías, prioridad (Alta/Media/Baja), fecha límite, búsqueda y filtros por categoría/estado.
- **Notas**: crear, editar, eliminar, fijar notas importantes, categorías, búsqueda.
- **Tema claro/oscuro** con botón de alternancia, se recuerda entre sesiones.
- **Datos persistentes** guardados localmente en `%USERPROFILE%\.gestor_personal\datos.db` (SQLite), no requiere internet ni servidor.

## Ejecutar desde el código fuente
```
pip install -r requirements.txt
python main.py
```

## Generar el ejecutable (.exe)
```
pyinstaller --noconsole --onefile --name "GestorPersonal" main.py
```
El ejecutable resultante queda en la carpeta `dist\GestorPersonal.exe`. Puedes copiarlo a cualquier parte y ejecutarlo con doble clic, sin necesidad de tener Python instalado.

## Estructura del proyecto
- `main.py` — punto de entrada
- `main_window.py` — ventana principal, navegación lateral y tema
- `database.py` — acceso a datos (SQLite)
- `view_dashboard.py`, `view_tasks.py`, `view_notes.py` — vistas de la interfaz
- `styles.py` — hojas de estilo (QSS) para tema claro/oscuro
