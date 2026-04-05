"""
╔══════════════════════════════════════════════════════╗
║   Sistema de Registro de Asistencia Estudiantil      ║
║   EESPP Gregoria Santos - Icuani                     ║
║   Versión 2.0 - Con importación desde Excel          ║
╚══════════════════════════════════════════════════════╝
"""

import json
import os
import sys
from datetime import datetime

# Intentar importar openpyxl (para leer Excel)
try:
    import openpyxl
    EXCEL_DISPONIBLE = True
except ImportError:
    EXCEL_DISPONIBLE = False


# ══════════════════════════════════════════════════════
# COLORES Y ESTILOS (ANSI)
# ══════════════════════════════════════════════════════

class Color:
    RESET      = "\033[0m"
    NEGRITA    = "\033[1m"
    AZUL       = "\033[94m"
    AZUL_OSCURO= "\033[34m"
    VERDE      = "\033[92m"
    AMARILLO   = "\033[93m"
    ROJO       = "\033[91m"
    GRIS       = "\033[90m"
    CIAN       = "\033[96m"
    MAGENTA    = "\033[95m"
    FONDO_AZUL = "\033[44m"
    FONDO_VERDE= "\033[42m"
    BLANCO     = "\033[97m"

def c(texto, *colores):
    """Aplica uno o más colores a un texto."""
    estilo = "".join(colores)
    return f"{estilo}{texto}{Color.RESET}"

def limpiar():
    """Limpia la pantalla."""
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """Pausa hasta que el usuario presione Enter."""
    input(c("\n  Presiona Enter para continuar...", Color.GRIS))


# ══════════════════════════════════════════════════════
# COMPONENTES VISUALES
# ══════════════════════════════════════════════════════

ANCHO = 58

def linea(caracter="═", color=Color.AZUL):
    print(c(f"  {''.join([caracter]*ANCHO)}", color))

def linea_delgada(color=Color.GRIS):
    print(c(f"  {'─'*ANCHO}", color))

def encabezado():
    limpiar()
    linea("═", Color.AZUL)
    print(c(f"  {'SISTEMA DE ASISTENCIA ESTUDIANTIL':^{ANCHO}}", Color.AZUL, Color.NEGRITA))
    print(c(f"  {'EESPP Gregoria Santos · Icuani':^{ANCHO}}", Color.CIAN))
    linea("═", Color.AZUL)
    print()

def titulo_seccion(texto, icono="📋"):
    print()
    linea("─", Color.AZUL)
    print(c(f"  {icono}  {texto}", Color.AZUL, Color.NEGRITA))
    linea("─", Color.AZUL)
    print()

def ok(msg):    print(c(f"\n  ✅  {msg}", Color.VERDE, Color.NEGRITA))
def error(msg): print(c(f"\n  ❌  {msg}", Color.ROJO))
def aviso(msg): print(c(f"\n  ⚠️   {msg}", Color.AMARILLO))
def info(msg):  print(c(f"  ℹ️   {msg}", Color.CIAN))

def opcion_menu(num, icono, texto):
    print(c(f"  [{num}]", Color.AMARILLO, Color.NEGRITA) + f"  {icono}  {texto}")

def pedir(prompt):
    return input(c(f"\n  → {prompt}: ", Color.CIAN)).strip()


# ══════════════════════════════════════════════════════
# ARCHIVOS DE DATOS
# ══════════════════════════════════════════════════════

ARCHIVO_DATOS       = "datos_asistencia.json"
ARCHIVO_ESTUDIANTES = "estudiantes.json"

def cargar_json(archivo):
    try:
        if not os.path.exists(archivo):
            return []
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        aviso(f"El archivo '{archivo}' está dañado. Se iniciará vacío.")
        return []
    except Exception as e:
        error(f"Error al cargar '{archivo}': {e}")
        return []

def guardar_json(archivo, datos):
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except PermissionError:
        error("No tienes permiso para escribir en este archivo.")
        return False
    except Exception as e:
        error(f"Error al guardar: {e}")
        return False


# ══════════════════════════════════════════════════════
# MÓDULO: GESTIÓN DE ESTUDIANTES
# ══════════════════════════════════════════════════════

def mostrar_lista_estudiantes(estudiantes, titulo="LISTA DE ESTUDIANTES"):
    """Muestra la lista con formato de tabla."""
    print(c(f"\n  {'N°':<5}{'Nombre completo':<45}", Color.NEGRITA, Color.AZUL))
    linea_delgada()
    for i, est in enumerate(estudiantes, 1):
        num = c(f"  {i:<5}", Color.AMARILLO)
        print(f"{num}{est['nombre']}")
    linea_delgada()
    print(c(f"  Total: {len(estudiantes)} estudiante(s)", Color.GRIS))

def listar_estudiantes():
    estudiantes = cargar_json(ARCHIVO_ESTUDIANTES)
    if not estudiantes:
        aviso("No hay estudiantes registrados aún.")
    else:
        mostrar_lista_estudiantes(estudiantes)
    return estudiantes

def agregar_estudiante():
    titulo_seccion("AGREGAR ESTUDIANTE", "➕")
    while True:
        nombre = pedir("Nombre completo (o 0 para cancelar)")
        if nombre == "0":
            info("Operación cancelada.")
            return
        if not nombre:
            error("El nombre no puede estar vacío.")
            continue
        if len(nombre) < 3:
            error("El nombre es demasiado corto.")
            continue
        if not all(c_.isalpha() or c_.isspace() for c_ in nombre):
            error("El nombre solo debe contener letras y espacios.")
            continue
        break

    estudiantes = cargar_json(ARCHIVO_ESTUDIANTES)
    if nombre.lower() in [e["nombre"].lower() for e in estudiantes]:
        aviso(f"'{nombre.title()}' ya está registrado.")
        return

    estudiantes.append({"nombre": nombre.title()})
    if guardar_json(ARCHIVO_ESTUDIANTES, estudiantes):
        ok(f"'{nombre.title()}' agregado correctamente.")

def eliminar_estudiante():
    titulo_seccion("ELIMINAR ESTUDIANTE", "🗑️")
    estudiantes = listar_estudiantes()
    if not estudiantes:
        return

    while True:
        try:
            op = pedir("Número del estudiante a eliminar (o 0 para cancelar)")
            if op == "0":
                info("Operación cancelada.")
                return
            n = int(op)
            if 1 <= n <= len(estudiantes):
                break
            error(f"Elige un número entre 1 y {len(estudiantes)}.")
        except ValueError:
            error("Ingresa un número válido.")

    nombre = estudiantes[n - 1]["nombre"]
    conf = pedir(f"¿Eliminar a '{nombre}'? (s/n)").lower()
    if conf == "s":
        estudiantes.pop(n - 1)
        guardar_json(ARCHIVO_ESTUDIANTES, estudiantes)
        ok(f"'{nombre}' eliminado.")
    else:
        info("Operación cancelada.")


# ══════════════════════════════════════════════════════
# MÓDULO: IMPORTAR DESDE EXCEL
# ══════════════════════════════════════════════════════

def importar_desde_excel():
    titulo_seccion("IMPORTAR ESTUDIANTES DESDE EXCEL", "📊")

    if not EXCEL_DISPONIBLE:
        error("La librería 'openpyxl' no está instalada.")
        info("Ejecuta en la terminal:  pip install openpyxl")
        pausar()
        return

    print(c("  INSTRUCCIONES:", Color.NEGRITA, Color.AMARILLO))
    print(c("  ─────────────────────────────────────────────────", Color.GRIS))
    print("  1. Abre tu Excel y copia la columna de nombres")
    print("  2. Pégala aquí (uno por línea)")
    print("  3. Cuando termines, escribe  FIN  y presiona Enter")
    print(c("  ─────────────────────────────────────────────────\n", Color.GRIS))

    nombres_pegados = []
    print(c("  Pega los nombres aquí:", Color.CIAN))
    while True:
        try:
            linea_entrada = input("  ")
        except EOFError:
            break
        if linea_entrada.strip().upper() == "FIN":
            break
        if linea_entrada.strip():
            nombres_pegados.append(linea_entrada.strip())

    if not nombres_pegados:
        aviso("No se ingresó ningún nombre.")
        pausar()
        return

    # Limpiar y validar nombres
    estudiantes_actuales = cargar_json(ARCHIVO_ESTUDIANTES)
    existentes = {e["nombre"].lower() for e in estudiantes_actuales}

    agregados   = []
    duplicados  = []
    invalidos   = []

    for nombre_raw in nombres_pegados:
        # Limpiar espacios extra y tabs (frecuente al pegar de Excel)
        nombre = " ".join(nombre_raw.split()).title()

        if len(nombre) < 3:
            invalidos.append(nombre_raw)
            continue
        if not all(ch.isalpha() or ch.isspace() for ch in nombre):
            invalidos.append(nombre_raw)
            continue
        if nombre.lower() in existentes:
            duplicados.append(nombre)
            continue

        estudiantes_actuales.append({"nombre": nombre})
        existentes.add(nombre.lower())
        agregados.append(nombre)

    # Guardar
    if agregados:
        guardar_json(ARCHIVO_ESTUDIANTES, estudiantes_actuales)

    # Resumen
    print()
    linea("─", Color.AZUL)
    print(c(f"  📊  RESUMEN DE IMPORTACIÓN", Color.NEGRITA, Color.AZUL))
    linea("─", Color.AZUL)
    print(c(f"  ✅  Agregados:   {len(agregados)}", Color.VERDE, Color.NEGRITA))
    print(c(f"  ⚠️   Duplicados:  {len(duplicados)}", Color.AMARILLO))
    print(c(f"  ❌  Inválidos:   {len(invalidos)}", Color.ROJO))

    if agregados:
        print(c("\n  Estudiantes agregados:", Color.VERDE))
        for n in agregados:
            print(c(f"    · {n}", Color.VERDE))
    if duplicados:
        print(c("\n  Ya existían (no se duplicaron):", Color.AMARILLO))
        for n in duplicados:
            print(c(f"    · {n}", Color.AMARILLO))
    if invalidos:
        print(c("\n  No se pudieron procesar:", Color.ROJO))
        for n in invalidos:
            print(c(f"    · {n}", Color.ROJO))
    linea("─", Color.AZUL)
    pausar()


# ══════════════════════════════════════════════════════
# MÓDULO: REGISTRO DE ASISTENCIA
# ══════════════════════════════════════════════════════

ESTADOS = {"1": "Presente", "2": "Tardanza", "3": "Falta"}
ICONOS  = {"Presente": c("✅ Presente", Color.VERDE),
           "Tardanza": c("⏰ Tardanza", Color.AMARILLO),
           "Falta":    c("❌ Falta",    Color.ROJO)}

def registrar_asistencia():
    titulo_seccion("REGISTRO DE ASISTENCIA", "📝")
    estudiantes = cargar_json(ARCHIVO_ESTUDIANTES)
    if not estudiantes:
        aviso("Primero debes agregar estudiantes.")
        pausar()
        return

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    asistencias = cargar_json(ARCHIVO_DATOS)

    registros_hoy = [r for r in asistencias if r["fecha"] == fecha_hoy]
    if registros_hoy:
        aviso(f"Ya se registró asistencia para hoy ({fecha_hoy}).")
        conf = pedir("¿Registrar nuevamente? Borrará el registro anterior (s/n)").lower()
        if conf != "s":
            info("Operación cancelada.")
            pausar()
            return
        asistencias = [r for r in asistencias if r["fecha"] != fecha_hoy]

    print(c(f"  📅  Fecha: {fecha_hoy}", Color.CIAN, Color.NEGRITA))
    print(c(f"\n  {'Tecla':<8}{'Estado'}", Color.NEGRITA))
    print(c(f"  {'1':<8}Presente", Color.VERDE))
    print(c(f"  {'2':<8}Tardanza", Color.AMARILLO))
    print(c(f"  {'3':<8}Falta",    Color.ROJO))
    linea_delgada()

    nuevos = []
    total = len(estudiantes)
    for i, est in enumerate(estudiantes, 1):
        while True:
            try:
                progreso = c(f"[{i}/{total}]", Color.GRIS)
                nombre_c = c(est['nombre'], Color.NEGRITA)
                estado_input = input(f"  {progreso} {nombre_c}: ").strip()
                if estado_input not in ESTADOS:
                    print(c("        Ingresa 1, 2 o 3.", Color.ROJO), end="\r")
                    continue
                break
            except KeyboardInterrupt:
                print()
                aviso("Registro interrumpido.")
                pausar()
                return

        nuevos.append({"fecha": fecha_hoy, "nombre": est["nombre"], "estado": ESTADOS[estado_input]})
        # Mostrar confirmación en la misma línea
        icono = {"1": "✅", "2": "⏰", "3": "❌"}[estado_input]
        print(c(f"        → {icono} {ESTADOS[estado_input]}", Color.GRIS))

    asistencias.extend(nuevos)
    if guardar_json(ARCHIVO_DATOS, asistencias):
        ok(f"Asistencia del {fecha_hoy} guardada correctamente.")
    pausar()


# ══════════════════════════════════════════════════════
# MÓDULO: REPORTES
# ══════════════════════════════════════════════════════

def barra_porcentaje(valor, total, ancho=20):
    """Genera una barra visual de porcentaje."""
    if total == 0:
        return ""
    lleno = int((valor / total) * ancho)
    barra = "█" * lleno + "░" * (ancho - lleno)
    pct   = round((valor / total) * 100, 1)
    return f"{barra} {pct}%"

def ver_asistencia_por_fecha():
    titulo_seccion("ASISTENCIA POR FECHA", "📅")
    asistencias = cargar_json(ARCHIVO_DATOS)
    if not asistencias:
        aviso("No hay registros de asistencia aún.")
        pausar()
        return

    fechas = sorted(set(r["fecha"] for r in asistencias), reverse=True)
    print(c(f"  {'N°':<5}{'Fecha'}", Color.NEGRITA, Color.AZUL))
    linea_delgada()
    for i, fecha in enumerate(fechas, 1):
        print(f"  {c(str(i)+'.',Color.AMARILLO):<14}{fecha}")
    linea_delgada()

    while True:
        try:
            op = pedir("Número de fecha (o 0 para cancelar)")
            if op == "0":
                return
            n = int(op)
            if 1 <= n <= len(fechas):
                break
            error(f"Elige entre 1 y {len(fechas)}.")
        except ValueError:
            error("Ingresa un número válido.")

    fecha_elegida = fechas[n - 1]
    registros = [r for r in asistencias if r["fecha"] == fecha_elegida]

    print()
    linea("═", Color.AZUL)
    print(c(f"  {'ASISTENCIA DEL '+fecha_elegida:^{ANCHO}}", Color.NEGRITA, Color.AZUL))
    linea("═", Color.AZUL)
    print(c(f"\n  {'N°':<5}{'Nombre':<35}{'Estado'}", Color.NEGRITA))
    linea_delgada()

    pres = tard = falt = 0
    for i, r in enumerate(registros, 1):
        estado = r["estado"]
        if estado == "Presente":  icono = c("✅ Presente", Color.VERDE);   pres += 1
        elif estado == "Tardanza": icono = c("⏰ Tardanza", Color.AMARILLO); tard += 1
        else:                      icono = c("❌ Falta",    Color.ROJO);     falt += 1
        num = c(f"  {i}.", Color.AMARILLO)
        print(f"{num:<14}{r['nombre']:<35}{icono}")

    total = len(registros)
    linea_delgada()
    print(c(f"\n  RESUMEN:", Color.NEGRITA, Color.AZUL))
    print(f"  {c('✅ Presentes:', Color.VERDE)}  {pres:<4} {c(barra_porcentaje(pres,total), Color.VERDE)}")
    print(f"  {c('⏰ Tardanzas:', Color.AMARILLO)} {tard:<4} {c(barra_porcentaje(tard,total), Color.AMARILLO)}")
    print(f"  {c('❌ Faltas:   ', Color.ROJO)}   {falt:<4} {c(barra_porcentaje(falt,total), Color.ROJO)}")
    print(c(f"\n  Total de estudiantes: {total}", Color.GRIS))
    linea("═", Color.AZUL)
    pausar()

def reporte_por_estudiante():
    titulo_seccion("HISTORIAL POR ESTUDIANTE", "📊")
    estudiantes = listar_estudiantes()
    if not estudiantes:
        pausar()
        return

    while True:
        try:
            op = pedir("Número del estudiante (o 0 para cancelar)")
            if op == "0":
                return
            n = int(op)
            if 1 <= n <= len(estudiantes):
                break
            error(f"Elige entre 1 y {len(estudiantes)}.")
        except ValueError:
            error("Ingresa un número válido.")

    nombre = estudiantes[n - 1]["nombre"]
    asistencias = cargar_json(ARCHIVO_DATOS)
    historial = sorted([r for r in asistencias if r["nombre"] == nombre], key=lambda x: x["fecha"])

    if not historial:
        aviso(f"No hay registros de asistencia para '{nombre}'.")
        pausar()
        return

    print()
    linea("═", Color.AZUL)
    print(c(f"  {nombre.upper():^{ANCHO}}", Color.NEGRITA, Color.AZUL))
    linea("═", Color.AZUL)
    print(c(f"\n  {'Fecha':<15}{'Estado'}", Color.NEGRITA))
    linea_delgada()

    pres = tard = falt = 0
    for r in historial:
        if r["estado"] == "Presente":  icono = c("✅ Presente", Color.VERDE);   pres += 1
        elif r["estado"] == "Tardanza": icono = c("⏰ Tardanza", Color.AMARILLO); tard += 1
        else:                           icono = c("❌ Falta",    Color.ROJO);     falt += 1
        print(f"  {r['fecha']:<15}{icono}")

    total = len(historial)
    linea_delgada()
    print(c(f"\n  ESTADÍSTICAS:", Color.NEGRITA, Color.AZUL))
    print(f"  {c('✅ Presentes:', Color.VERDE)}  {pres:<4} {c(barra_porcentaje(pres,total), Color.VERDE)}")
    print(f"  {c('⏰ Tardanzas:', Color.AMARILLO)} {tard:<4} {c(barra_porcentaje(tard,total), Color.AMARILLO)}")
    print(f"  {c('❌ Faltas:   ', Color.ROJO)}   {falt:<4} {c(barra_porcentaje(falt,total), Color.ROJO)}")
    print(c(f"\n  Total de clases registradas: {total}", Color.GRIS))
    linea("═", Color.AZUL)
    pausar()


# ══════════════════════════════════════════════════════
# MENÚS
# ══════════════════════════════════════════════════════

def menu_estudiantes():
    while True:
        encabezado()
        titulo_seccion("GESTIÓN DE ESTUDIANTES", "👥")
        opcion_menu("1", "📋", "Ver lista de estudiantes")
        opcion_menu("2", "➕", "Agregar estudiante manualmente")
        opcion_menu("3", "📊", "Importar estudiantes desde Excel (copia y pega)")
        opcion_menu("4", "🗑️ ", "Eliminar estudiante")
        opcion_menu("0", "🔙", "Volver al menú principal")
        linea_delgada()

        op = pedir("Elige una opción")
        if op == "1":
            encabezado()
            titulo_seccion("LISTA DE ESTUDIANTES", "📋")
            listar_estudiantes()
            pausar()
        elif op == "2":
            encabezado()
            agregar_estudiante()
            pausar()
        elif op == "3":
            encabezado()
            importar_desde_excel()
        elif op == "4":
            encabezado()
            eliminar_estudiante()
            pausar()
        elif op == "0":
            break
        else:
            error("Opción inválida.")
            pausar()

def menu_principal():
    while True:
        encabezado()

        # Mostrar estado rápido
        ests = cargar_json(ARCHIVO_ESTUDIANTES)
        asis = cargar_json(ARCHIVO_DATOS)
        hoy  = datetime.now().strftime("%Y-%m-%d")
        reg_hoy = any(r["fecha"] == hoy for r in asis)
        estado_hoy = c("✅ Registrada", Color.VERDE) if reg_hoy else c("⏳ Pendiente", Color.AMARILLO)

        print(c(f"  📅 Hoy: {hoy}   |   👥 Estudiantes: {len(ests)}   |   Asistencia hoy: ", Color.GRIS) + estado_hoy)
        print()
        linea_delgada()
        opcion_menu("1", "📝", "Registrar asistencia de hoy")
        opcion_menu("2", "👥", "Gestionar estudiantes")
        opcion_menu("3", "📅", "Ver asistencia por fecha")
        opcion_menu("4", "📊", "Ver historial por estudiante")
        opcion_menu("0", "🚪", "Salir")
        linea_delgada()

        op = pedir("Elige una opción")
        if op == "1":
            encabezado()
            registrar_asistencia()
        elif op == "2":
            menu_estudiantes()
        elif op == "3":
            encabezado()
            ver_asistencia_por_fecha()
        elif op == "4":
            encabezado()
            reporte_por_estudiante()
        elif op == "0":
            limpiar()
            print(c("\n  👋  ¡Hasta luego!\n", Color.AZUL, Color.NEGRITA))
            sys.exit(0)
        else:
            error("Opción inválida. Elige entre 0 y 4.")
            pausar()


# ══════════════════════════════════════════════════════
# INICIO
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    menu_principal()
