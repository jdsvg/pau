from aux_resources.clear_console import Clear_console
from connectionDB.connectionDB import Connection
import random

class Financial_management:
    def __init__(self, user):
        self.user = user
        self.menu_main_Financial_management()
    
    
    def menu_main_Financial_management(self):
        state_menu_main_Financial_management = False
        while not state_menu_main_Financial_management:
            Clear_console(); print()
            print(f"Hola{self.user}. ¿Qué deseas hacer?: ")
            print("1. Ver tu gestion financiera general")
            print("2. Registrar tus Ingresos totales")
            print("3. Registrar tus gastos")
            print("4. Gastos medicos")
            print("5. Gastos del hogar")
            print("6. Gastos de ocio")
            print("7. Gastos de educacion")
            print("8. Ver Ahorros")
            print("0. Regresar al menu principal")
            option_main = input()
            if option_main == "1": Clear_console(); self.view_financial_management()
            elif option_main == "2": Clear_console(); self.register_total_incomes()
            elif option_main == "3": Clear_console(); self.register_financial_management()
            elif option_main == "4": Clear_console(); input(f"Tus gastos en Medicina son de: ${self.sum_medical_expenses()[0]}\nPresiona cualquier tecla para continuar")
            elif option_main == "5": Clear_console(); input(f"Tus gastos en Hogar son de: ${self.sum_home_expenses()[0]}\nPresiona cualquier tecla para continuar")
            elif option_main == "6": Clear_console(); input(f"Tus gastos en Ocio son de: ${self.sum_leisure_expenses()[0]}\nPresiona cualquier tecla para continuar")
            elif option_main == "7": Clear_console(); input(f"Tus gastos en Educacion son de: ${self.sum_education_expenses()[0]}\nPresiona cualquier tecla para continuar")
            elif option_main == "8": Clear_console(); input(f"Tus Ahorros son de: $-{self.sum_see_savings()[0]}\nPresiona cualquier tecla para continuar")
    
            elif option_main == "0": Clear_console(); state_menu_main_Financial_management=True; return 1
            else:input("Opcion no valida, presione enter para continuar")
        



    def view_financial_management(self):
        total_expenses = float(self.sum_medical_expenses()[0] + self.sum_home_expenses()[0] + self.sum_leisure_expenses()[0] + self.sum_education_expenses()[0])
        if total_expenses <= 0:
            print("Estado general de tus movimientos")
            print(f"Total de gastos: ${total_expenses}")
            print(f"Total de ahorros: ${self.sum_see_savings()[0]}")
            print(f"Total de ingresos ${self.sum_incomes()[0]}")
            print(f"Ingresos vs Gastos totales: ${self.sum_incomes()[0] + total_expenses}")
            print(f"Gastos totales vs ahorros: ${total_expenses + self.sum_see_savings()[0]}\n\n")
            

            if (((total_expenses/self.sum_incomes()[0])*100)*-1) >= 50: #If the expenditure is greater than the income, it is recommended to save money.
                arr = []; append_movements = self.append_sum_total_by_category(); append_movements_x = append_movements[:-2].copy(); min_element = min(append_movements_x); arr.append(min_element)
                for i in range(0, len(append_movements_x)):
                    if append_movements[i][0] <= min_element[0] and append_movements[i][1] != min_element[1]:arr.append(append_movements_x[i])
                    else: continue
                print("Tu(s) categoria(s) de mas gasto es(son):")
                for i in arr:
                    print(f"- {Connection().get_category_by_id(i[1]).category}: {i[0]}")
                print("\nToma en cuentas la siguientes recomendaciones: ")
                for i in arr:
                    arr2 = []
                    for j in Connection().get_tip_management_by_category_id(i[1]): arr2.append(j.id)
                    print(f"-{Connection().get_tip_management_by_id_and_category_id(random.choice(arr2) , i[1]).tip}")

            else: print("Felicitaciones, estas con buena salud financiera")
            if ((self.sum_see_savings()[0]/self.sum_incomes()[0])*100) >= 50:# If the savings are greater than the income, it is recommended to invest money.
                print("\n\nSi bien es importate ahorrar, tambien lo es invertir bien tu dinero: ")
                for j in Connection().get_tip_management_by_category_id(5): arr2.append(j.id)
                print(f"{Connection().get_tip_management_by_id_and_category_id(random.choice(arr2) , 5).tip}")
            input("\n\nPresiona cualquier tecla para continuar")
        else: input("No tienes gastos registrados, presiona cualquier tecla para continuar")

    def register_total_incomes(self):
        state_register_total_incomes = False
        print("Registraras tus ingresos totales")
        print("Ten encuenta que tu ingresos totales no represetan tus ahorros")
        while not state_register_total_incomes:
            try: amount = float(input("Ingresa el monto: ")); state_register_total_incomes = True
            except: input("Por favor ingresa tu gastos en formato decimal, presione enter para intentar de nuevo"); Clear_console()
        result = Connection().get_all_financial_management_income_by_user_id(self.user)
        if result:
            opt = input("Tienes ingresos registrados, si continuas, estos seran reseteados por el nuevo ingreso\nIngresa cualquier cosa para continuar o '0' para cancelar")
            if opt == "0": return 1
            Connection().delete_all_financial_management_income_by_user_id(self.user)
        Connection().add_financial_management("+"+str(amount), 1, Connection().get_user_by_name(self.user).id, status_movement=True)
        input("Se registro tu nuevo ingreso, presione enter para continuar")



    def register_financial_management(self):
        msg_fail_input_category = "Por favor ingresa correctamente el numero de la categoria, presione enter para intentar de nuevo"
        categories = Connection().get__all_financial_category()
        id_categories = []
        status_register_financial_management = False
        print("Registraras tus movimientos por categoria")
        while not status_register_financial_management: #Get amount
            try: amount = float(input("Ingresa el monto: ")); status_register_financial_management = True
            except: input("Por favor ingresa tu gastos en formato decimal, presione enter para intentar de nuevo"); Clear_console()
        while status_register_financial_management: #Get category
            print("Categorias:")
            for i in categories: id_categories.append(i.id); print(f"{i.id}-{i.category}")
            try: 
                category_x = int(input("Ingresa el numero de la categoria: "))
                if category_x in id_categories: status_register_financial_management = False
                else: input(msg_fail_input_category); Clear_console()
            except: input(msg_fail_input_category); Clear_console()
        Clear_console()
        while not status_register_financial_management:
            print("Se registrara el siguiente movimiento: ")
            print(f"Valor del movimiento: ${amount}")
            print(f"Categoria: {categories[category_x-1].category}")
            opt = input("Deseas registrar este movimiento? (Si: 1/ No: 0): ")
            if opt == "1": status_register_financial_management = True
            elif opt == "0": status_register_financial_management = True; return 1
            else: input("Por favor ingresa una opcion valida (Si: 1 / No: 0), presione enter para intentar de nuevo"); Clear_console()
        if category_x == 2 or category_x == 3 or category_x == 4 or category_x == 5: Connection().add_financial_management("-"+str(amount), category_x, Connection().validate_user_data_existence(self.user, None, "2").id)
        elif category_x == 1 or category_x == 6: Connection().add_financial_management("+"+str(amount), category_x, Connection().validate_user_data_existence(self.user, None, "2").id, status_movement=True)
        input("Registro de movimiento exitoso. Presione enter para continuar")


    def sum_medical_expenses(self): return self.iterate_financial_management_by_user_to_get_sum_total_by_category(2)

    def sum_home_expenses(self): return self.iterate_financial_management_by_user_to_get_sum_total_by_category(3)

    def sum_leisure_expenses(self): return self.iterate_financial_management_by_user_to_get_sum_total_by_category(4)

    def sum_education_expenses(self): return self.iterate_financial_management_by_user_to_get_sum_total_by_category(5)

    def sum_see_savings(self): return self.iterate_financial_management_by_user_to_get_sum_total_by_category(6)

    def sum_incomes(self): return self.iterate_financial_management_by_user_to_get_sum_total_by_category(1)

    def iterate_financial_management_by_user_to_get_sum_total_by_category(self, category_id):
        total = 0
        result = Connection().get_all_financial_management_by_user_and_category(self.user, category_id)
        if result != 0:
            for i in result: total += float(i.movement)
            return [total, category_id]
        else: return 0

    def append_sum_total_by_category(self):
        result = []
        result.append(self.sum_medical_expenses())
        result.append(self.sum_home_expenses())
        result.append(self.sum_leisure_expenses())
        result.append(self.sum_education_expenses())
        result.append(self.sum_see_savings())
        result.append(self.sum_incomes())
        return result