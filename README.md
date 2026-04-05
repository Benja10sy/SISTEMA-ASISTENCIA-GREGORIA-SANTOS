# 📋 Sistema de Registro de Asistencia Estudiantil
### EESPP Gregoria Santos - Sicuani

---

## 🚀 PASO A PASO PARA ABRIR Y USAR LA APP

### Paso 1 — Verificar que tienes Python instalado

1. Abre el **Terminal** (o "Símbolo del sistema" en Windows)
2. Escribe este comando y presiona Enter:
   ```
   python --version
   ```
3. Si aparece algo como `Python 3.x.x` ✅ estás listo
4. Si no tienes Python, descárgalo de: https://www.python.org/downloads/

---

### Paso 2 — Abrir el proyecto en Visual Studio Code

1. Abre **Visual Studio Code**
2. Ve a `Archivo` → `Abrir Carpeta`
3. Selecciona la carpeta **asistencia** (donde está el archivo `asistencia.py`)
4. La carpeta aparecerá en el panel izquierdo

---

### Paso 3 — Abrir la Terminal en VS Code

1. En VS Code, ve al menú: `Terminal` → `Nueva Terminal`
2. Aparecerá una terminal en la parte inferior de la pantalla

---

### Paso 4 — Ejecutar la aplicación

En la terminal escribe:
```
python asistencia.py
```
Presiona **Enter** y la aplicación iniciará.

---

## 📱 CÓMO USAR LA APLICACIÓN

### Primera vez que usas la app:

1. **Primero agrega estudiantes:**
   - Elige opción `2` (Gestionar estudiantes)
   - Luego opción `2` (Agregar estudiante)
   - Escribe el nombre de cada estudiante y presiona Enter
   - Repite para cada estudiante
   - Elige `0` para volver al menú principal

2. **Luego registra la asistencia:**
   - Elige opción `1` (Registrar asistencia de hoy)
   - Para cada estudiante ingresa:
     - `1` = Presente
     - `2` = Tardanza
     - `3` = Falta

### Para ver reportes:
- Opción `3`: Ver quién asistió en una fecha determinada
- Opción `4`: Ver el historial completo de un estudiante

---

## 📁 ARCHIVOS QUE CREA LA APP

La aplicación guarda los datos automáticamente en:
- `estudiantes.json` → Lista de estudiantes
- `datos_asistencia.json` → Todos los registros de asistencia

> ⚠️ No borres estos archivos o perderás los datos.

---

## ✅ FUNCIONALIDADES

| Funcionalidad | Descripción |
|---|---|
| Agregar estudiantes | Registra nuevos estudiantes con validación de nombre |
| Eliminar estudiantes | Elimina un estudiante con confirmación |
| Registrar asistencia | Marca Presente / Tardanza / Falta por cada estudiante |
| Ver por fecha | Muestra la asistencia de un día específico con resumen |
| Historial por estudiante | Muestra todas las asistencias de un alumno con porcentaje |

---

## 🛡️ MANEJO DE ERRORES (para el informe técnico)

La app maneja los siguientes errores:
- Archivo JSON dañado o inexistente
- Nombre de estudiante vacío o con caracteres inválidos
- Ingreso de opciones fuera de rango
- Intento de duplicar estudiantes
- Registro doble de asistencia en el mismo día

---

## 👥 CRÉDITOS

Desarrollado como Producto Académico N°1  
Curso: Desarrollo Ágil con IA Generativa  
Institución de prácticas: EESPP Gregoria Santos, Sicuani  
