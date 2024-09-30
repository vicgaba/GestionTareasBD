import sys
import os

from tareas import(
    GestionTareas,
    TareaSimple,
    TareaRecurrente
)
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("1. Agregar Tarea Simple")
    print("2. Agregar Tarea Recurrente")
    print("3. Mostrar Tareas")
    print("4. Eliminar Tarea")
    print("5. Modificar Estado de Tarea")
    print("6. Salir")
    print('======================================================')

def agregar_tarea_simple(gestion):
    id = input("Ingrese el ID de la tarea: ")
    titulo = input("Ingrese el título de la tarea: ")
    descripcion = input("Ingrese la descripción de la tarea: ")
    fecha_ingreso = input("Ingrese la fecha de ingreso (YYYY-MM-DD): ")
    fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ")
    estado = input("Ingese el estado, 1. Pendiente, 2. En Progreso, 3. Completada: ")
    tarea = TareaSimple(id, titulo, descripcion, fecha_ingreso, estado, fecha_vencimiento)

    gestion.agregar_tarea(tarea)
    input("Presione Enter para continuar...")

def agregar_tarea_recurrente(gestion):
    id = input("Ingrese el ID de la tarea: ")
    titulo = input("Ingrese el título de la tarea: ")
    descripcion = input("Ingrese la descripción de la tarea: ")
    fecha_ingreso = input("Ingrese la fecha de ingreso (YYYY-MM-DD): ")
    frecuencia = input("Ingrese la frecuencia de la tarea (diaria, semanal, mensual): ")
    estado = input("Ingese el estado, 1. Pendiente, 2. En Progreso, 3. Completada: ")
    tarea = TareaRecurrente(id, titulo, descripcion, fecha_ingreso, estado, frecuencia)

    gestion.agregar_tarea(tarea)
    input("Presione Enter para continuar...")

def eliminar_tarea(gestion):
    gestion.mostrar_tareas()
    id = input("Ingrese el ID de la tarea a eliminar: ")
    gestion.eliminar_tarea(id)
    gestion.mostrar_tareas()
    input("Presione Enter para continuar...")

def modificar_estado_tarea(gestion):
    gestion.mostrar_tareas()
    id = input("Ingrese el ID de la tarea a modificar: ")
    estado = input("Ingrese el nuevo estado: ")
    gestion.modificar_estado_tarea(id, estado)
    gestion.mostrar_tareas()
    input("Presione Enter para continuar...")
    
if __name__ == '__main__':
    archivo_tareas = 'tareas.json'
    gestion = GestionTareas(archivo_tareas)
    limpiar_pantalla()
    mostrar_menu()
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            agregar_tarea_simple(gestion)
        elif opcion == '2':
            agregar_tarea_recurrente(gestion)
        elif opcion == '3':
            gestion.mostrar_tareas()
            input("Presione Enter para continuar...")
        elif opcion == '4':
            eliminar_tarea(gestion)
        elif opcion == '5':
            modificar_estado_tarea(gestion)
        elif opcion == '6':
            sys.exit()