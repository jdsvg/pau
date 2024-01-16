from auth.login import Login
from auth.register import Register
from auth.encrypt_decrypt import Encriptar_Datos
from aux_resources.clear_console import Clear_console
from connectionDB.connectionDB import Connection
from banking.banking import Banking
from universidad.universidad import Universidad
from send_elements.send_elements import Send_Elements



class Main:
    def __init__(self):
        self.user = None
        if(Connection().status):
            if Connection().validate_db_tables_status() == 1:self.menu_main_login()
            else: exit(0)
        else: exit(0)



    def menu_main_login(self):
        print("\nHola. Por favor, autenticate o registrese: ")
        print("1. Iniciar sesion")
        print("2. Registrarse")
        print("0. Salir")
        option_main = input()

        while option_main != "1" and option_main != "2" and option_main != "0":
            Clear_console(); print("Opcion no valida", option_main)
            option_main = input("Hola. Por favor, autenticate (1) o registrate (2): ")
        if option_main == "1":
            Clear_console(); self.user = Login().username
            Clear_console();print(f"----------------------\nBienvenido {self.user}\n----------------------")
            input("Presione enter para continuar")
            Clear_console(); self.menu_main()
        elif option_main == "2":
            Clear_console(); Register()
            Clear_console(); self.user = Login().username
            Clear_console(); self.menu_main()
        elif option_main == "0":
            Clear_console(); Connection().close_connection(); print("\nHasta la proxima")
            exit(0)
        else: print("Opcion no valida")


    def menu_main(self):
        state_manu_main = False
        while not state_manu_main:
            Clear_console(); print(f"Hola {self.user}. ¿Qué deseas hacer?: ")
            print("1. Ir a Baking")
            print("2. Ir a Universidad")
            print("3. Ir a Envio de elementos")
            print("0. Salir")
            option_main = input("")

            if option_main == "1":Clear_console(); Banking(self.user)
            elif option_main == "2":Clear_console(); Universidad(self.user)
            elif option_main == "3":Clear_console(); Send_Elements(self.user)
            elif option_main == "0":Clear_console();print("\nHasta la proxima");exit(0)
            else:
                print("Opcion no valida")
                input("Opcion no valida. Presione enter para continuar")

obj_main = Main()