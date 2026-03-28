#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba.
Ejecutar: python poblar_db.py

O con argumentos:
    python poblar_db.py --clear              # Limpiar datos existentes
    python poblar_db.py --alumnos 5000      # Especificar numero de alumnos
    python poblar_db.py --help              # Ver todos los argumentos
"""

import os
import sys
import time
import random as rd
from random import random
import argparse

# Configurar Django ANTES de importar los modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "universidad.settings")

import django

django.setup()

# ============================================
# IMPORTAR MODELOS (despues de django.setup())
# ============================================
from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso
from universidad.Models.Catedratico.models import Catedratico
from universidad.Models.Nota.models import Nota
from universidad.Models.AsignacionCurso.models import AsignacionCurso
from universidad.Models.InscripcionAlumno.models import InscripcionAlumno

# ============================================
# VARIABLES GLOBALES (FACILES DE MODIFICAR)
# ============================================

# Cantidades por defecto (puedes cambiar estos numeros)
DEFAULT_CATEDRATICOS = 50
DEFAULT_CURSOS = 50
DEFAULT_ALUMNOS = 10000

# Rangos para generar datos
MIN_CURSOS_POR_ALUMNO = 3
MAX_CURSOS_POR_ALUMNO = 6
MIN_ASIGNACIONES_POR_CURSO = 1
MAX_ASIGNACIONES_POR_CURSO = 2

# ============================================
# DATOS DE EJEMPLO
# ============================================

# Vocales y consonantes para generar strings aleatorios
VOCALES = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
CONSONANTES = [
    'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'y', 'z',
    'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z'
]

# Nombres y apellidos predefinidos (para generar datos mas realistas)
NOMBRES = [
    'Juan', 'Maria', 'Carlos', 'Ana', 'Luis', 'Sofia', 'Pedro', 'Laura', 'Jorge', 'Isabel',
    'Miguel', 'Carmen', 'Alejandro', 'Patricia', 'Fernando', 'Elena', 'Roberto', 'Marta',
    'Ricardo', 'Andrea', 'Diego', 'Paula', 'Francisco', 'Silvia', 'David', 'Natalia',
    'Adrian', 'Gabriela', 'Oscar', 'Daniela', 'Raul', 'Veronica', 'Manuel', 'Cristina'
]

APELLIDOS = [
    'Perez', 'Garcia', 'Lopez', 'Martinez', 'Rodriguez', 'Gonzalez', 'Hernandez', 'Sanchez',
    'Ramirez', 'Torres', 'Flores', 'Vasquez', 'Castro', 'Morales', 'Ortega', 'Jimenez',
    'Ruiz', 'Reyes', 'Gutierrez', 'Mendoza', 'Cruz', 'Ortiz', 'Silva', 'Romero'
]

# Cursos base (codigo, nombre, creditos)
CURSOS_BASE = [
    ('MAT101', 'Matematicas Basicas', 3),
    ('MAT102', 'Calculo I', 4),
    ('MAT103', 'Calculo II', 4),
    ('FIS101', 'Fisica General', 3),
    ('FIS102', 'Fisica Moderna', 4),
    ('QUI101', 'Quimica General', 3),
    ('PRO101', 'Programacion I', 4),
    ('PRO102', 'Programacion II', 4),
    ('BD101', 'Bases de Datos', 3),
    ('RED101', 'Redes de Computadoras', 3),
    ('IA101', 'Inteligencia Artificial', 4),
    ('ING101', 'Ingles Tecnico', 2),
    ('CON101', 'Contabilidad General', 3),
    ('DER101', 'Introduccion al Derecho', 3),
]

# Especialidades para catedraticos
ESPECIALIDADES = [
    'Matematicas', 'Fisica', 'Quimica', 'Biologia', 'Historia', 'Literatura',
    'Programacion', 'Bases de Datos', 'Redes', 'Inteligencia Artificial',
    'Ingles', 'Contabilidad', 'Derecho', 'Medicina', 'Arquitectura'
]

# Estados para inscripciones
ESTADOS_INSCRIPCION = ['activo', 'retirado', 'aprobado', 'reprobado']

# Años disponibles
ANIOS_DISPONIBLES = [2022, 2023, 2024, 2025]

# Secciones disponibles
SECCIONES = ['A', 'B', 'C', 'D']


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def generar_string(longitud):
    """
    Genera una cadena aleatoria alternando vocales y consonantes.
    Util para generar nombres, apellidos, descripciones, etc.
    """
    if longitud <= 0:
        return ''

    resultado = ''
    for i in range(longitud):
        decision = rd.choice(('vocal', 'consonante'))

        if resultado and resultado[-1].lower() in VOCALES:
            decision = 'consonante'
        if resultado and resultado[-1].lower() in CONSONANTES:
            decision = 'vocal'

        if decision == 'vocal':
            caracter = rd.choice(VOCALES)
        else:
            caracter = rd.choice(CONSONANTES)

        resultado += caracter

    return resultado.capitalize()


def numero_aleatorio(minimo=1, maximo=10):
    """Genera un numero entero aleatorio entre minimo y maximo."""
    return int(random() * (maximo - minimo + 1) + minimo)


def generar_email(nombre, apellido, identificador, dominio='jp.edu.gt'):
    """Genera un email unico a partir del nombre, apellido y un identificador."""
    return f"{nombre.lower()}.{apellido.lower()}{identificador}@{dominio}"


def generar_telefono():
    """Genera un numero de telefono aleatorio."""
    return f"5555-{rd.randint(1000, 9999)}"


def generar_fecha_nacimiento():
    """Genera una fecha de nacimiento aleatoria (entre 18 y 35 años)."""
    import datetime
    hoy = datetime.date.today()
    edad = rd.randint(18, 35)
    fecha = hoy - datetime.timedelta(days=edad * 365 + rd.randint(0, 365))
    return fecha


# ============================================
# FUNCIONES DE POBLACION
# ============================================

def generar_catedraticos(cantidad):
    """Genera catedraticos con datos aleatorios."""
    print(f'\nGenerando {cantidad} catedraticos...')
    catedraticos = []

    for i in range(1, cantidad + 1):
        nombre = generar_string(numero_aleatorio(4, 8))
        apellido = generar_string(numero_aleatorio(4, 8))

        catedratico = Catedratico.objects.create(
            codigo=f'PROF{i:03d}',
            nombre=nombre,
            apellido=apellido,
            email=f"{nombre.lower()}.{apellido.lower()}{i}@jp.edu.gt",
            telefono=generar_telefono(),
            especialidad=rd.choice(ESPECIALIDADES),
            is_active=True
        )
        catedraticos.append(catedratico)

        if i % 10 == 0:
            print(f'   {i} catedraticos creados...')

    print(f'   Total: {len(catedraticos)} catedraticos')
    return catedraticos


def generar_cursos(cantidad):
    """Genera cursos a partir de los cursos base."""
    print(f'\nGenerando {cantidad} cursos...')
    cursos = []

    for i in range(1, cantidad + 1):
        base = CURSOS_BASE[i % len(CURSOS_BASE)]
        curso = Curso.objects.create(
            codigo=f'{base[0]}{i:03d}',
            nombre=f'{base[1]} {i}',
            creditos=base[2],
            descripcion=f'Curso de {base[1]} - Nivel {i}',
            is_active=True
        )
        cursos.append(curso)

        if i % 10 == 0:
            print(f'   {i} cursos creados...')

    print(f'   Total: {len(cursos)} cursos')
    return cursos


def generar_alumnos(cantidad):
    """Genera alumnos con datos realistas y emails unicos."""
    print(f'\nGenerando {cantidad} alumnos...')
    alumnos = []
    emails_creados = set()

    for i in range(1, cantidad + 1):
        nombre = rd.choice(NOMBRES)
        apellido = rd.choice(APELLIDOS)

        email = generar_email(nombre, apellido, i, 'estudiante.jp.edu.gt')

        while email in emails_creados:
            email = generar_email(nombre, apellido, f"{i}{rd.randint(1, 999)}", 'estudiante.jp.edu.gt')

        emails_creados.add(email)

        alumno = Alumno.objects.create(
            carnet=f'CARNET{i:06d}',
            first_name=nombre,
            last_name=apellido,
            email=email,
            phone=generar_telefono(),
            gender=rd.choice(['M', 'F']),
            birth_date=generar_fecha_nacimiento(),
            is_active=rd.choice([True, False])
        )
        alumnos.append(alumno)

        if i % 1000 == 0:
            print(f'   {i} alumnos creados...')

    print(f'   Total: {len(alumnos)} alumnos')
    return alumnos


def generar_asignaciones(cursos, catedraticos):
    """Asigna catedraticos a cursos (tabla asignacion_curso)."""
    print(f'\nGenerando asignaciones de cursos...')
    asignaciones = []

    # Conjunto para evitar duplicados en asignacion_curso
    combinaciones_usadas = set()

    for curso in cursos:
        num_asignaciones = numero_aleatorio(MIN_ASIGNACIONES_POR_CURSO, MAX_ASIGNACIONES_POR_CURSO)
        asignaciones_creadas = 0
        intentos = 0
        max_intentos = num_asignaciones * 3

        while asignaciones_creadas < num_asignaciones and intentos < max_intentos:
            catedratico = rd.choice(catedraticos)
            anio = rd.choice(ANIOS_DISPONIBLES)
            semestre = rd.choice([1, 2])
            seccion = rd.choice(SECCIONES)

            # Crear clave unica para evitar duplicados
            clave = f"{curso.id}-{anio}-{semestre}-{seccion}"

            if clave not in combinaciones_usadas:
                combinaciones_usadas.add(clave)
                asignacion = AsignacionCurso.objects.create(
                    curso=curso,
                    catedratico=catedratico,
                    anio=anio,
                    semestre=semestre,
                    seccion=seccion
                )
                asignaciones.append(asignacion)
                asignaciones_creadas += 1

            intentos += 1

    print(f'   Total: {len(asignaciones)} asignaciones')
    return asignaciones


def generar_inscripciones(alumnos, cursos, asignaciones):
    """Inscribe alumnos en cursos (tabla inscripcion_alumno)."""
    print(f'\nGenerando inscripciones de alumnos...')
    inscripciones = []

    # Conjunto para evitar duplicados en inscripcion_alumno
    combinaciones_usadas = set()

    for i, alumno in enumerate(alumnos):
        num_cursos = numero_aleatorio(MIN_CURSOS_POR_ALUMNO, MAX_CURSOS_POR_ALUMNO)
        cursos_disponibles = cursos.copy()
        rd.shuffle(cursos_disponibles)
        cursos_inscritos = cursos_disponibles[:min(num_cursos, len(cursos))]

        for curso in cursos_inscritos:
            # Buscar una asignacion existente para este curso
            asignaciones_curso = [a for a in asignaciones if a.curso_id == curso.id]
            if asignaciones_curso:
                asignacion = rd.choice(asignaciones_curso)

                clave = f"{alumno.id}-{curso.id}-{asignacion.anio}-{asignacion.semestre}"

                if clave not in combinaciones_usadas:
                    combinaciones_usadas.add(clave)
                    try:
                        inscripcion = InscripcionAlumno.objects.create(
                            alumno=alumno,
                            curso=curso,
                            anio=asignacion.anio,
                            semestre=asignacion.semestre,
                            estado=rd.choice(ESTADOS_INSCRIPCION)
                        )
                        inscripciones.append(inscripcion)
                    except Exception:
                        pass

        if (i + 1) % 1000 == 0:
            print(f'   {i + 1} alumnos procesados...')

    print(f'   Total: {len(inscripciones)} inscripciones')
    return inscripciones


def generar_notas(inscripciones):
    """Genera notas para las inscripciones."""
    print(f'\nGenerando notas...')
    notas = []

    for i, inscripcion in enumerate(inscripciones):
        nota1 = rd.randint(0, 15) if rd.random() > 0.1 else None
        nota2 = rd.randint(0, 15) if rd.random() > 0.1 else None
        nota3 = rd.randint(0, 35) if rd.random() > 0.1 else None
        examen_final = rd.randint(0, 35) if rd.random() > 0.1 else None

        try:
            nota = Nota.objects.create(
                alumno=inscripcion.alumno,
                curso=inscripcion.curso,
                nota1=nota1,
                nota2=nota2,
                nota3=nota3,
                examen_final=examen_final
            )
            notas.append(nota)
        except Exception:
            pass

        if (i + 1) % 2000 == 0:
            print(f'   {i + 1} notas procesadas...')

    print(f'   Total: {len(notas)} notas')
    return notas


def limpiar_datos():
    """Elimina todos los datos existentes en orden correcto."""
    print('\nLimpiando datos existentes...')
    Nota.objects.all().delete()
    InscripcionAlumno.objects.all().delete()
    AsignacionCurso.objects.all().delete()
    Curso.objects.all().delete()
    Catedratico.objects.all().delete()
    Alumno.objects.all().delete()
    print('   Datos limpiados correctamente')


def mostrar_resumen():
    """Muestra un resumen de los datos generados."""
    print('\n' + '=' * 60)
    print('RESUMEN FINAL')
    print('=' * 60)
    print(f'Catedraticos: {Catedratico.objects.count()}')
    print(f'Cursos: {Curso.objects.count()}')
    print(f'Alumnos: {Alumno.objects.count()}')
    print(f'Asignaciones: {AsignacionCurso.objects.count()}')
    print(f'Inscripciones: {InscripcionAlumno.objects.count()}')
    print(f'Notas: {Nota.objects.count()}')
    print('=' * 60)


# ============================================
# CONFIGURACION DE ARGUMENTOS
# ============================================

def parse_args():
    """Configura los argumentos de linea de comandos."""
    parser = argparse.ArgumentParser(
        description='Poblar la base de datos con datos de prueba',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
    python poblar_db.py                              # Poblar con valores por defecto
    python poblar_db.py --clear                      # Limpiar datos existentes y poblar
    python poblar_db.py --alumnos 5000               # Crear 5000 alumnos
    python poblar_db.py --catedraticos 100 --cursos 100  # Mas catedraticos y cursos
        """
    )

    parser.add_argument(
        '--clear',
        action='store_true',
        help='Limpiar datos existentes antes de poblar'
    )
    parser.add_argument(
        '--alumnos',
        type=int,
        default=DEFAULT_ALUMNOS,
        help=f'Numero de alumnos a crear (por defecto: {DEFAULT_ALUMNOS})'
    )
    parser.add_argument(
        '--catedraticos',
        type=int,
        default=DEFAULT_CATEDRATICOS,
        help=f'Numero de catedraticos a crear (por defecto: {DEFAULT_CATEDRATICOS})'
    )
    parser.add_argument(
        '--cursos',
        type=int,
        default=DEFAULT_CURSOS,
        help=f'Numero de cursos a crear (por defecto: {DEFAULT_CURSOS})'
    )

    return parser.parse_args()


# ============================================
# FUNCION PRINCIPAL
# ============================================

def main():
    """Funcion principal que ejecuta la poblacion."""

    args = parse_args()

    print('\n' + '=' * 60)
    print('INICIANDO POBLACION DE DATOS')
    print('=' * 60)

    inicio = time.strftime("%c")
    print(f'Fecha y hora de inicio: {inicio}')
    print(f'\nConfiguracion:')
    print(f'   - Alumnos: {args.alumnos}')
    print(f'   - Catedraticos: {args.catedraticos}')
    print(f'   - Cursos: {args.cursos}')
    print(f'   - Limpiar datos previos: {args.clear}')

    if args.clear:
        limpiar_datos()

    try:
        catedraticos = generar_catedraticos(args.catedraticos)
        cursos = generar_cursos(args.cursos)
        alumnos = generar_alumnos(args.alumnos)
        asignaciones = generar_asignaciones(cursos, catedraticos)
        inscripciones = generar_inscripciones(alumnos, cursos, asignaciones)
        notas = generar_notas(inscripciones)

        mostrar_resumen()

        fin = time.strftime("%c")
        print(f'Fecha y hora de finalizacion: {fin}')
        print('\nPOBLACION COMPLETADA EXITOSAMENTE')

    except Exception as e:
        print(f'\nERROR: {e}')
        print('   La poblacion se detuvo. Los datos creados hasta ahora permanecen.')
        sys.exit(1)


if __name__ == "__main__":
    main()