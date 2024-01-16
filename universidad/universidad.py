from aux_resources.clear_console import Clear_console
from connectionDB.connectionDB import Connection
class Universidad:

    def __init__(self, user):
        self.username = user
        self.menu_main_universidad()
    
    
    def menu_main_universidad(self):
        print()
        print(f"Hola{self.username}. ¿Qué deseas hacer?: ")
        print("1. Ver tu programa")
        print("2. Inscribir un programa")
        print("0. Regresar al menu principal")
        option_main = input()

        while option_main != "1" and option_main != "2" and option_main != "3" and option_main != "4" and option_main != "5" and  option_main != "0":
            # Clear_console()
            print("Opcion no valida", option_main)
            option_main = input("Hola. Por favor, autenticate (1) o registrate (2): ")

        if option_main == "1":
            Clear_console()
            print("Ingresas a tu programa")
            self.mostrar_programa()
        elif option_main == "2":
            Clear_console()
            self.inscribir_programa()
        elif option_main == "0":
            Clear_console()

    def mostrar_programa(self):
        if Connection().get_user_square_program_campus(self.username) == None:
            print("No tienes programa")
            print("¿Deseas inscribir un programa?")
            option_program = input("Presione 1 para inscribir o cualquier otra tecla para continuar: ")
            if option_program == "1":
                self.inscribir_programa()
            else:
                return 0

        else:
            print("Informacion de tu programa: ")
            information_university_by_user = Connection().get_university_information_by_username(self.username)
            print(f"Programa: {Connection().get_program_by_id(information_university_by_user.program_id).Name}")
            print(f"Campus: {Connection().get_campus_by_id(information_university_by_user.campus_id).Name}")
            print(f"Plaza: {information_university_by_user.name}")
            input("Presione enter para continuar")

    def inscribir_programa(self):
        if Connection().get_user_square_program_campus(self.username) != None: print("Ya estas inscrito en un programa");input("Presione enter para continuar");return 0
        print("Inscribir programa")
        id_campus_and_programs_availables = self.programs_and_campus_available()
        print("Se tiene cupo disponible, en los siguientes programas")
        for i in id_campus_and_programs_availables[0]: print(f"{i} - {Connection().get_program_by_id(i).Name}")
        opt_program = int(input("Por favor elige un programa:"))
        while opt_program not in id_campus_and_programs_availables[0]:
            print("Opcion no valida")
            opt_program =input("Por favor elige un programa:")
        print("Se tiene cupo disponible, en los siguientes campus")
        for i in id_campus_and_programs_availables[1]: print(f"{i} - {Connection().get_campus_by_id(i).Name}")
        opt_campus = int(input("Por favor elige un campus:"))
        while opt_campus not in id_campus_and_programs_availables[1]:
            print("Opcion no valida")
            opt_campus =input("Por favor elige un campus:")
        print("Has elegido:")
        print(f"*Programa: {Connection().get_program_by_id(opt_program).Name}\n*Campus: {Connection().get_campus_by_id(opt_campus).Name}")
        opt = input("Presione 1 para confirmar o cualquier otra tecla para regresar")
        if opt == "1":
            x = Connection().get_square_program_campus_available_by_program_id_and_campus_id(opt_program, opt_campus)
            Connection().update_square_program_campus(x.id)
            Connection().create_user_program_campus(Connection().get_user_by_name(self.username).id, x.id)
            print(f"Campus: {Connection().get_campus_by_id(opt_campus).Name}inscrito")
            print(f"Programa: {Connection().get_program_by_id(opt_program).Name}inscrito")
            print(f"Plaza: {Connection().get_square_program_campus_by_id(Connection().get_user_square_program_campus_by_user_id(Connection().get_user_by_name(self.username).id).square_program_campus_id).name} ")
            print("Gracias por inscribirte, preciona cualquier tecla para continuar")
        else:
            return 0
        input()


    def programs_and_campus_available(self):
        id_campus_availables = []
        id_programs_availables = []
        result = []
        x = Connection().get_square_program_campus_available()
        for i in x:
            if i.campus_id not in id_campus_availables:
                id_campus_availables.append(i.campus_id)
            if i.program_id not in id_programs_availables:
                id_programs_availables.append(i.program_id)
        id_campus_availables = sorted(id_campus_availables)
        id_programs_availables = sorted(id_programs_availables)
        result = [id_programs_availables, id_campus_availables]
        return result
    

    
