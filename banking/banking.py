from aux_resources.clear_console import Clear_console
from connectionDB.connectionDB import Connection
from . import Financial_management
class Banking:

    def __init__(self, user):
        self.user = user
        self.menu_main_banking()
    
    
    def menu_main_banking(self):
        print()
        print(f"Hola{self.user}. ¿Qué deseas hacer?: ")
        print("1. Ver tu cuenta")
        print("2. Depositar a tu cuenta")
        print("3. Retirar de tu cuenta")
        print("4. Realizar transferencias")
        print("5. Conversor de divisas")
        print("6. Gestion financiera")
        print("0. Regresar al menu principal")
        option_main = input()

        while option_main != "1" and option_main != "2" and option_main != "3" and option_main != "4" and option_main != "5" and  option_main != "6" and option_main != "0":
            # Clear_console()
            print("Opcion no valida", option_main)
            option_main = input("Hola. Por favor, autenticate (1) o registrate (2): ")

        if option_main == "1": Clear_console(); self.mostrar_cuenta()
        elif option_main == "2": Clear_console(); self.depositar_cuenta()
        elif option_main == "3": Clear_console(); self.retirar_ecuenta()
        elif option_main == "4": Clear_console(); self.transferir_cuenta()
        elif option_main == "5": Clear_console(); self.convertir_divisas()    
        elif option_main == "6": Clear_console(); Financial_management.Financial_management(self.user)    
        elif option_main == "0": Clear_console(); return 1

    def mostrar_cuenta(self):
        user_bank_information = Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id)
        print("Esta es la informacion de tu cuenta")
        print(f"Titular de la cuenta: {Connection().validate_user_data_existence(self.user, None, '2').nombre} {Connection().validate_user_data_existence(self.user, None, '2').apellido}")
        print(f"Numero de cuenta: {user_bank_information.account_number}\nSaldo disponible: ${user_bank_information.balance}")
        input("Presione enter para continuar")
    
    def depositar_cuenta(self):
        print("Depositaras a tu cuenta\nRecuerda que los depositos se hacen en moneda local (USD)")
        amount = input("Por favor: indica el monto que deseas depositar: ")
        try:
            amount = float(amount)
            amunt_before = Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).balance
            Connection().add_balance(Connection().validate_user_data_existence(self.user, None, "2").id, amount)
            amunt_after = Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).balance
            print("Deposito exitoso")
            print(f"Tu saldo anterior era: ${amunt_before}\nTu saldo actual es: ${amunt_after}")
            input("Presione enter para continuar")
        except:
            print("Debes ingresar valores numericos")
            input("Presione enter para continuar")

    def retirar_ecuenta(self, amount = None):
        print("Retiraras de tu cuenta")
        print("Recuerda que los retiros se hacen en la moneda local (USD)")
        if amount == None:
            amount = input("Por favor: indica el monto que deseas retirar: ")
            print("Comision del 1%", float(float(amount)) * 0.01)
        elif float(amount) > 2000:
            print("No puedes retirar mas de $2000")
            input("Presione enter para continuar")
            return 0
        else: amount = amount
        try:
            amount = float(amount)
            commission = float(amount * 0.01)
            amunt_before = Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).balance
            if (Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).balance) - (amount + commission) < 0:
                print("Saldo insuficiente")
                input("Presione enter para continuar")
                return False
            else:
                Connection().withdraw_balance(Connection().validate_user_data_existence(self.user, None, "2").id, (amount + commission))
                amunt_after = Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).balance
                print(f"Retiro exitoso\nMonto retirado: ${amount}\nTu saldo anterior era: ${amunt_before}\nTu saldo actual es: ${amunt_after}\nComision de 1% {commission}\n")
                input("Presione enter para continuar")
        except Exception as e:
            print(e);print("Debes ingresar valores numericos")
            input("Presione enter para continuar")

    def transferir_cuenta(self, amount_transfer = None , cuenta_destino = None):
        print("Transferencias")
        input("Presione enter para continuar")
        if amount_transfer == None and cuenta_destino == None:
            amount_transfer = input("Por favor: indica el monto que deseas transferir: ")
            cuenta_destino = input("Por favor: indica la cuenta destino: ")
        try:
            amount_transfer = float(amount_transfer)
            cuenta_destino = int(cuenta_destino)
            amunt_before = Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).balance
            if (Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).balance) - amount_transfer < 0:
                print("Saldo insuficiente")
                input("Presione enter para continuar")
                return False
            else:
                Connection().transfer_balance(Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).account_number, cuenta_destino, amount_transfer)
                amunt_after = Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).balance
                print("Transferencia exitosa")
                print(f"Saldo transferido: {amount_transfer} $")
                print(f"Tu saldo anterior era: {amunt_before} $")
                print(f"Tu saldo actual es: {amunt_after} $")
                print(f"Cuenta origen: {Connection().get_user_banking(Connection().validate_user_data_existence(self.user, None, "2").id).account_number}")
                print(f"Cuenta destino: {cuenta_destino}")
                input("Presione enter para continuar")
        except Exception as e:
            print(e)
            input("Presione enter para continuar")


    def convertir_divisas(self):
        print("Conversor de monedas. Moneda local: USD")
        currencies_exist = Connection().get_all_currencies()
        list_currencies =  []
        for i in currencies_exist: list_currencies.append(i.currency)
        status_while_conversor = False
        while not status_while_conversor:
            Clear_console()
            print(f"Por favor: indica las moneda con las cuales quieres operar\n{'\n'.join(list_currencies)}\n")
            currency_item_from = input("Moneda inicial: ")
            currency_item_to = input("Moneda final: ")
            if currency_item_from in list_currencies and currency_item_to in list_currencies: status_while_conversor = True
            else:
                print("Opcion no valida")
                input("Presione enter para continuar")
                
        if status_while_conversor:
            amount = input("Por favor: indica el monto que deseas convertir: ")
            try:
                float(amount)
                Clear_console()
                converstion_resutl = self.conversor_moneda(amount, currency_item_from, currency_item_to)
                print(f"{amount} {currency_item_from} equivalen a {converstion_resutl} {list_currencies[list_currencies.index(currency_item_to)]}s")
                go_to_transfer = input(f"Si deseas retirar {converstion_resutl} {list_currencies[list_currencies.index(currency_item_to)]}s presiona 1, en caso contrario, para continuar, presiona cualquier tecla: ")
                if go_to_transfer == "1":
                    transfer_by_convertion = self.conversor_moneda(converstion_resutl, currency_item_to)
                    self.retirar_ecuenta(transfer_by_convertion)
                else: input("Presione enter para continuar")
            except:
                print("Debes ingresar valores numericos")
                input("Presione enter para continuar")
        else:
            print("Opcion no valida")
            input("Presione enter para continuar")


    def conversor_moneda(self, amount, currency_from, currency_to="USD"):
        operation = ((float(amount))/Connection().get_currency_by_name(currency_from).value)*Connection().get_currency_by_name(currency_to).value
        return operation
        