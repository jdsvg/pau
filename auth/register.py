from aux_resources.clear_console import Clear_console
from connectionDB.connectionDB import Connection
from auth.encrypt_decrypt import Encriptar_Datos
import random

class Register:
    def __init__(self):
        print("Ingresaste al Register")
        self.menu_register()

    def menu_register(self):
        state_name_valid = False
        state_user_data_valid = False

        while not state_user_data_valid:
            print("Por favor,ingresa los siguientes datos")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = input("Edad: ")
            x = Connection().validate_user_data_existence(nombre, apellido, "1")
            if x == None: state_user_data_valid = True
            else: Clear_console(); print(f"Parece que este cliente {nombre, apellido} ya existe, intentalo de nuevo")

        while not state_name_valid:
            username = self.generate_username(nombre, apellido)
            print(f"Guarda tu nombre de usuario: {username}")
            x = Connection().validate_user_data_existence(username, None, "2")
            if x == None: state_name_valid = True

        input("Presiosa cualquier tecla para continuar con el registro")
        print("Por favor, ingresa la contraseña\n*La contraseña debe ser mayor a 6 caracteres")
        password = input("Contraseña: ")
        self.validate_password(password)

        while not self.validate_password(password):
            print("*Recuerda que lacontraseña debe ser mayor a 6 caracteres")
            password = input("Ingresa una contraseña correcta: ")
            self.validate_password(password)
        
        password_2 = input("Confirmar contraseña: ")
        if password == password_2: Clear_console(); print("Credenciales parametrizadas correctamente")
        else: print("Las contraseñas no coinciden")
        password = Encriptar_Datos().encrypt_AES_GCM(bytes(password, 'utf-8'))
        Connection().create_user(nombre, apellido, edad, username, password)
        print("Informacion del registro exitoso: ")
        print(f"Nombre: {nombre}\nApellido: {apellido}\nUsername: {username}\nEdad: {edad}")
        input("Presiona cualquier tecla para ir al menu principal")


    def validate_password(self, password):
        if len(password) > 6: return True
        else: return False
        
    def generate_username(self, nombre, apellido):
        n =  [random.randint(1, 100) for _ in range(3)]
        username = nombre[0] + apellido[0] + str(n[0])+str(n[1])+str(n[2])
        return username

