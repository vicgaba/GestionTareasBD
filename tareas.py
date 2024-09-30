import datetime
import json

class Tarea:
    def __init__(self, id, titulo, descripcion, fecha_ingreso, estado):
        self.id = self.validar_id(id)
        self.titulo = self.validar_titulo(titulo)
        self.descripcion = descripcion
        self.fecha_ingreso = fecha_ingreso
        self.estado = self.validar_estado(estado)

    def __str__(self):
        return f"{self.descripcion} - Ingreso: {self.fecha_ingreso} - Vencimiento: {self.fecha_vencimiento} - Estado: {self.estado}"
    
    @property
    def id(self):
        return self.__id
    @property
    def titulo(self):
        return self.__titulo
    @property
    def descripcion(self):
        return self.__descripcion
    @property
    def fecha_ingreso(self):
        return self.__fecha_ingreso
    @property
    def estado(self):
        return self.__estado
    @fecha_ingreso.setter
    def fecha_ingreso(self, fecha_ingreso):
        self.__fecha_ingreso = fecha_ingreso

    @estado.setter
    def estado(self, estado):
        self.__estado = self.validar_estado(estado)
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
    @id.setter
    def id(self, id):
        self.__id = self.validar_id(id)

    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = self.validar_titulo(titulo)
        return self.__titulo
    
    def validar_titulo(self, titulo):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        return titulo
    
    def validar_id(self, id):
        #ToDo validar que el id no exista para los nuevos y si exista para update y delete
        if not isinstance(int(id), int) or int(id) <= 0:
            raise ValueError("El ID debe ser un número entero positivo.")
        return id
    
    def validar_estado(self, estado):
        if estado not in ["1", "2", "3"]:
            raise ValueError("Estado inválido. Debe ser 'pendiente', 'en progreso' o 'completada'.")
        return estado
    
    def to_dict(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "descripcion": self.__descripcion,
            "fecha_ingreso": self.__fecha_ingreso,
            "estado": self.__estado
        }

class TareaSimple(Tarea):
    def __init__(self, id, titulo, descripcion, fecha_ingreso, estado, fecha_vencimiento):
        super().__init__(id, titulo, descripcion, fecha_ingreso, estado)
        self.fecha_vencimiento = self.validar_fecha_vencimiento(fecha_vencimiento)

    @property
    def fecha_vencimiento(self):
        return self.__fecha_vencimiento
    @fecha_vencimiento.setter

    def fecha_vencimiento(self, fecha_vencimiento):
        self.__fecha_vencimiento = self.validar_fecha_vencimiento(fecha_vencimiento)
        return self.__fecha_vencimiento
    
    def validar_fecha_vencimiento(self, fecha_vencimiento):
        try:
            if fecha_vencimiento < datetime.datetime.now().strftime('%Y-%m-%d'):
                raise ValueError("La fecha de vencimiento no puede ser en el pasado.")
        except ValueError as e:
            raise ValueError(f"Fecha de vencimiento inválida: {e}")
        return fecha_vencimiento
    
    def to_dict(self):
        data = super().to_dict()
        data["fecha_vencimiento"] = self.fecha_vencimiento
        return data
    
    def __str__(self):
        return f"super().__str__() - Vencimiento: {self.fecha_vencimiento}" 

class TareaRecurrente(Tarea):
    def __init__(self, id, titulo, descripcion, fecha_ingreso, estado, frecuencia):
        super().__init__(id, titulo, descripcion, fecha_ingreso, estado)
        self.frecuencia = self.validar_frecuencia(frecuencia)
    
    @property
    def frecuencia(self):
        return self.__frecuencia
    
    @frecuencia.setter
    def frecuencia(self, frecuencia):
        self.__frecuencia = self.validar_frecuencia(frecuencia)
        return self.__frecuencia
    
    def validar_frecuencia(self, frecuencia):
        if frecuencia not in ["diaria", "semanal", "mensual"]:
            raise ValueError("Frecuencia inválida. Debe ser 'diaria', 'semanal' o 'mensual'.")
        return frecuencia
    
    def to_dict(self):
        data = super().to_dict()
        data["frecuencia"] = self.frecuencia
        return data
    
    def __str__(self):
        return f"super().__str__() - Frecuencia: {self.frecuencia}"
class GestionTareas:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return{}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        return datos
    def agregar_tarea(self, tarea):
        try:
            datos = self.leer_datos()
            id = tarea.id      
            if str(id) not in datos.keys(): #keys = clave, value = valor, item = todo el registro
                datos[id] = tarea.to_dict()
                self.guardar_datos(datos)
                print(f'Tarea con el ID {id} creado correctamente.')
            else:
                print(f'Tarea con id {id} ya existe')
        except Exception as error:
            print(f'Error inesperado al crear la tarea: {error}')    
    def guardar_datos(self, datos):
        with open(self.archivo, 'w') as file:
            json.dump(datos, file, indent=4)
    def mostrar_tareas(self):
        datos = self.leer_datos()
        if not datos:
            print("No hay tareas registradas.")
        else:
            for tarea in datos.values():
                if 'fecha_vencimiento' in tarea:
                    match tarea['estado']:
                        case '1':
                            estado = 'Pendiente'
                        case '2':
                            estado = 'En Progreso'
                        case '3':
                            estado = 'Completada'
                    
                    print(tarea['id'] + ' ' + tarea['titulo'] + ' ' + tarea['descripcion'] + ' ' + tarea['fecha_ingreso'] + ' ' + tarea['fecha_vencimiento'] + ' ' + estado)
                else:
                    print(tarea['id'] + ' ' + tarea['titulo'] + ' ' + tarea['descripcion'] + ' ' + tarea['fecha_ingreso'] + ' ' + tarea['frecuencia'] + ' ' + estado)
    
        print("-----------------------------------------------------------------------------")

    def eliminar_tarea(self, id):
        try:
            datos = self.leer_datos()
            if str(id) in datos.keys():
                datos.pop(str(id))
                self.guardar_datos(datos)
                print(f"Tarea con id '{id}' eliminada correctamente.")
            else:
                print(f"No se encontró la tarea con id: {id}.")
        except Exception as error:
            print(f"Error al eliminar la tarea: {error}")

    def modificar_estado_tarea(self, id, estado):
        datos = self.leer_datos()
        if str(id) in datos.keys():
            tarea = datos[str(id)]
            if estado:
                tarea['estado'] = estado
            self.guardar_datos(datos)
            print(f"Tarea con id '{id}' modificada correctamente.")
        else:
            print(f"No se encontró la tarea con id: {id}.")