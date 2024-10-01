import datetime
import mysql.connector
from mysql.connector import Error
from decouple import config

class Tarea:
    def __init__(self, id, titulo, descripcion, fechaIngreso, estado):
        self.__id = self.validar_id(id)
        self.__titulo = self.validar_titulo(titulo)
        self.__descripcion = descripcion
        self.__fechaIngreso = fechaIngreso
        self.__estado = self.validar_estado(estado)

    def __str__(self):
        return f"{self.descripcion} - Ingreso: {self.fechaIngreso} - Estado: {self.estado}"
    
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
    def fechaIngreso(self):
        return self.__fechaIngreso
    @property
    def estado(self):
        return self.__estado
    @fechaIngreso.setter
    def fechaIngreso(self, fechaIngreso):
        self.__fechaIngreso = fechaIngreso

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
        if estado not in [1, 2, 3]:
            raise ValueError("Estado inválido. Debe ser 'pendiente', 'en progreso' o 'completada'.")
        return estado
    
    def to_dict(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "descripcion": self.__descripcion,
            "fechaIngreso": self.__fechaIngreso,
            "estado": self.__estado
        }

class TareaSimple(Tarea):
    def __init__(self, id, titulo, descripcion, fechaIngreso, estado, fechaVencimiento):
        super().__init__(id, titulo, descripcion, fechaIngreso, estado)
        self.__fechaVencimiento = self.validar_fecha_vencimiento(fechaVencimiento)

    @property
    def fechaVencimiento(self):
        return self.__fechaVencimiento
    @fechaVencimiento.setter
    def fechaVencimiento(self, fechaVencimiento):
        self.__fechaVencimiento = self.validar_fecha_vencimiento(fechaVencimiento)
        return self.__fechaVencimiento
    
    def validar_fecha_vencimiento(self, fechaVencimiento):
        try:
            if fechaVencimiento < datetime.datetime.now().strftime('%Y-%m-%d'):
                raise ValueError("La fecha de vencimiento no puede ser en el pasado.")
        except ValueError as e:
            raise ValueError(f"Fecha de vencimiento inválida: {e}")
        return fechaVencimiento
    
    def to_dict(self):
        data = super().to_dict()
        data["fechaVencimiento"] = self.__fechaVencimiento
        return data
    
    def __str__(self):
        return f"super().__str__() - Vencimiento: {self.__fechaVencimiento}" 

class TareaRecurrente(Tarea):
    def __init__(self, id, titulo, descripcion, fechaIngreso, estado, frecuencia):
        super().__init__(id, titulo, descripcion, fechaIngreso, estado)
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
    def __init__(self):
        self.host = config('DB_HOST')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.database = config('DB_NAME')
        self.port = config('DB_PORT')

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )

            if connection.is_connected():
                return connection
 
        except mysql.connector.Error as error:
            print(f"Error al conectar a la base de datos: {error}")
            return None
    
    def agregar_tarea(self, tarea):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #Verificar si el id de tarea ya existe
                    cursor.execute("SELECT id FROM tareas WHERE id = %s", (tarea.id,))
                    result = cursor.fetchone()
                    if result:
                        print(f"Ya existe una tarea con el ID {tarea.id}")
                        return
                    else:
                        #Insertar la tarea
                        cursor.execute("INSERT INTO tareas (id, titulo, descripcion, fechaIngreso, estado) VALUES (%s, %s, %s, %s, %s)", (tarea.id, tarea.titulo, tarea.descripcion, tarea.fechaIngreso, tarea.estado))
                        #Verificar que tipo de tarea es
                        if isinstance(tarea, TareaSimple):
                            cursor.execute("INSERT INTO tareaSimple (id, fechaVencimiento) VALUES (%s, %s)", (tarea.id, tarea.fechaVencimiento))
                        elif isinstance(tarea, TareaRecurrente):
                            cursor.execute("INSERT INTO tareaRecurrente (id, frecuencia) VALUES (%s, %s)", (tarea.id, tarea.frecuencia))
                        connection.commit()
                        print(f"Tarea con el ID {tarea.id} creada correctamente.")
        except Exception as error:
            print(f'Error inesperado al crear la tarea: {error}')    

    def mostrar_tarea(self, id):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM tareas WHERE id = %s", (id,))
                    tarea_data = cursor.fetchone()
                    
                    if tarea_data:
                        cursor.execute("SELECT fechaVencimiento FROM tareaSimple WHERE id = %s", (id,))
                        fechaVencimiento = cursor.fetchone()

                        if fechaVencimiento:
                            tarea_data['fechaVencimiento'] = fechaVencimiento['fechaVencimiento']
                            tarea = TareaSimple(**tarea_data)
                        
                        else:
                            cursor.execute("SELECT frecuencia FROM tareaRecurrente WHERE id = %s", (id,))
                            frecuencia = cursor.fetchone()

                            if frecuencia:
                                tarea_data['frecuencia'] = frecuencia['frecuencia']
                                tarea = TareaRecurrente(**tarea_data)
                            else:
                                tarea = Tarea(**tarea_data)
                    else:
                        tarea = None

        except Error as error:
            print(f'Error inesperado al mostrar la tarea: {error}')
        else:
            return tarea
        finally:
            if connection:
                connection.close()  

    def mostrar_todas_las_tareas(self):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM tareas")
                tareas = cursor.fetchall()
                if not tareas:
                    print("No hay tareas registradas.")
                else:
                    for tarea in tareas:
                        cursor.execute("SELECT * FROM tareaSimple WHERE id = %s", (tarea[0],))
                        tarea_simple = cursor.fetchone()
                        cursor.execute("SELECT * FROM tareaRecurrente WHERE id = %s", (tarea[0],))
                        tarea_recurrente = cursor.fetchone()
                        if tarea_simple:
                            print(f"Tarea Simple: {tarea_simple}")
                        elif tarea_recurrente:
                            print(f"Tarea Recurrente: {tarea_recurrente}")
                        else:
                            print(f"Tarea: {tarea}")
        except Exception as error:
            print(f'Error inesperado al mostrar las tareas: {error}')

    def eliminar_tarea(self, id):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #Verifico si existe la tarea
                    if not self.mostrar_tarea(id):
                        print(f"No existe una tarea con el ID {id}")
                        return
                    #Elimino la tarea dependiendo el tipo
                    if isinstance(self.mostrar_tarea(id), TareaSimple):
                        cursor.execute("DELETE FROM tareaSimple WHERE id = %s", (id, ))
                    elif isinstance(self.mostrar_tarea(id), TareaRecurrente):
                        cursor.execute("DELETE FROM tareaRecurrente WHERE id = %s", (id, ))
                    cursor.execute("DELETE FROM tareas WHERE id = %s", (id,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f"Tarea con el ID {id} eliminada correctamente.")
        except Error as error:
            print(f'Error inesperado al eliminar la tarea: {error}')
        finally:
            if connection:
                connection.close()

    def modificar_estado_tarea(self, id, estado):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    if not self.mostrar_tarea(id):
                        print(f"No existe una tarea con el ID {id}")
                        return
                    cursor.execute("UPDATE tareas SET estado = %s WHERE id = %s", (estado, id))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f"Tarea con el ID {id} modificada correctamente.")
                    else:
                        print(f"No se pudo modificar la tarea con el ID {id}")
        except Exception as error:
            print(f'Error inesperado al modificar la tarea: {error}')
        finally:
            if connection:
                connection.close()