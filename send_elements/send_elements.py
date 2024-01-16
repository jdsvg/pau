from aux_resources.clear_console import Clear_console
from connectionDB.connectionDB import Connection
import random
import string

class Send_Elements:
    def __init__(self, user):
        self.user = user
        self.menu_main_Send_Elements()

    def menu_main_Send_Elements(self):
        print("Shipping Items")
        status_menu_main_Send_Elements = False

        while not status_menu_main_Send_Elements:
            Clear_console();
            print("1. Enviar un elemento")
            print("2. Revisar elementos enviados")
            print("3. Ver elementos que te enviaron")
            print("4. Ver elementos pendientes por recibir")
            print("0. Volver al menu principal")
            option_main_Send_Elements = input("")

            if option_main_Send_Elements == "1":Clear_console();self.send_element()
            if option_main_Send_Elements == "2":Clear_console();self.sent_items()
            if option_main_Send_Elements == "3":Clear_console();self.received_items()
            if option_main_Send_Elements == "4":Clear_console();self.pending_items()
            elif option_main_Send_Elements == "0":
                status_menu_main_Send_Elements = True
            else:
                print("Opcion no valida")

    def send_element(self):
        status_send_element = False
        print("Enviaras elementos")
        name_element = input("indica e nombre de tu elemento: ")
        while not status_send_element: 
            try: weight = float(input("indica el peso de tu elemento\nRecuerda por cad Kg, se cobraran $2.0: ")); status_send_element = True
            except: Clear_console(); print("Debes de introducir un valor numerico")

        while status_send_element:
            username_receiver = input("Indica el username de la persona que recibira tu elemento: ")
            result_username_receiver = Connection().get_user_by_name(username_receiver)
            if result_username_receiver != None:
                if result_username_receiver.username == self.user:
                    Clear_console(); print("No te puedes enviar elementos a ti mismo")
                    opt = input("Presiona enter para intentarlo de nuevo o 0 cancelar el envio: ")
                    if opt == "0": status_send_element = False; return 1
                else: Clear_console(); status_send_element = False
            else:
                Clear_console(); print(f"El usuario {username_receiver} no existe")
                opt = input("Presiona enter para intentarlo de nuevo o 0 cancelar el envio: ")
                if opt == "0": status_send_element = False; return 1
        amount = weight * 2
        serial = self.generar_serial()
        while not status_send_element:
            print("Informacion de envio:")
            print(f"Elemento: {name_element}")
            print(f"Peso: {weight} -kg")
            print(f"Receptor: {result_username_receiver.nombre} {result_username_receiver.apellido} ({result_username_receiver.username})")
            print(f"Valor a pagar: ${amount}")
            opt = input("Presiona 1 para confirmar o 0 para cancelar")
            if opt == "1":
                Connection().create_shipping_item(serial, name_element, weight, Connection().get_user_by_name(self.user).id, Connection().get_user_by_name(username_receiver).id, amount)
                input("Elemento enviado, presiona enter para continuar")
                status_send_element = True
            elif opt == "0":
                print("Envio cancelado")
                status_send_element = True
                return 1
            else: input("Opcion no valida, presiona cualquier tecla para continuar")

    def sent_items(self):
        received_status_x = ''
        data = [['serial', 'Nombre', 'Peso', 'Receptor', 'Valor','Estado']]
        result = Connection().get_all_shipping_items_by_user_issuer_id(Connection().get_user_by_name(self.user).id)
        for i in result: 
            if i.received_status == 0: received_status_x = "No recibido"
            else: received_status_x = "Recibido"
            data.append([i.serial, i.name, i.weight, Connection().get_user_by_id(int(i.user_receiver)).username, i.amount, received_status_x])
        column_lengths = [max(len(str(item)) for item in column) for column in zip(*data)]
        for i, header in enumerate(data[0]):print(f"{header:{column_lengths[i]}}", end=" | ")
        print("\n" + "-" * (sum(column_lengths) + 3 * len(column_lengths)))
        for row in data[1:]:
            for i, item in enumerate(row): print(f"{item:{column_lengths[i]}}", end=" | ")
            print()
        input("\n\nPresiona cualquier tecla para continuar")


    def received_items(self):
        received_status_x = ''
        data = [['serial', 'Nombre', 'Peso', 'Issuer','Estado']]
        result = Connection().get_all_shipping_items_by_user_receiver_id(Connection().get_user_by_name(self.user).id)
        for i in result: 
            if i.received_status == 0: received_status_x = "No recibido"
            else: received_status_x = "Recibido"
            data.append([i.serial, i.name, i.weight, Connection().get_user_by_id(int(i.user_receiver)).username, received_status_x])
        column_lengths = [max(len(str(item)) for item in column) for column in zip(*data)]
        for i, header in enumerate(data[0]):print(f"{header:{column_lengths[i]}}", end=" | ")
        print("\n" + "-" * (sum(column_lengths) + 3 * len(column_lengths)))
        for row in data[1:]:
            for i, item in enumerate(row): print(f"{item:{column_lengths[i]}}", end=" | ")
            print()
        input("\n\nPresiona cualquier tecla para continuar")


    def pending_items(self):
        count = 0
        received_status_x = ''
        data = [['serial', 'Nombre', 'Peso', 'Issuer','Estado']]
        result = Connection().get_all_shipping_items_by_user_receiver_id(Connection().get_user_by_name(self.user).id)
        for i in result: 
            if i.received_status == 1: continue
            else: received_status_x = "No Recibido"; count += 1; data.append([i.serial, i.name, i.weight, Connection().get_user_by_id(int(i.user_receiver)).username, received_status_x])
        if count > 0:
            print(f"Elementos pendientes por recibir: {count}\n")
            column_lengths = [max(len(str(item)) for item in column) for column in zip(*data)]
            for i, header in enumerate(data[0]):print(f"{header:{column_lengths[i]}}", end=" | ")
            print("\n" + "-" * (sum(column_lengths) + 3 * len(column_lengths)))
            for row in data[1:]:
                for i, item in enumerate(row): print(f"{item:{column_lengths[i]}}", end=" | ")
                print()
        else: input("No hay elementos pendientes por recibir, presiona cualquier tecla para continuar")

    def generar_serial(self):
        caracteres = string.ascii_letters + string.digits  # Letras y números
        concact_caracteres = ''.join(random.choice(caracteres) for _ in range(7))
        serial_x = ''
        for i in concact_caracteres: 
            try: int(i); a = i
            except: a = i.upper()
            serial_x = serial_x+str(a)
        if Connection().get_shipping_item_by_serial(serial_x) == None: return serial_x
        else: serial_x = generar_serial()



