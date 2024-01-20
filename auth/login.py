from aux_resources.clear_console import Clear_console
from connectionDB.connectionDB import Connection
from auth.encrypt_decrypt import Encriptar_Datos
from datetime import datetime, timedelta
class Login:
    def __init__(self):
        print("Ingresaste a Login")
        self.username =self.menu_login()

    def menu_login(self):
        status_login_state = False
        print("Por favor,ingresa tus credenciales")
        while not status_login_state:
            username = input("Username: ")
            password = input("Password: ")
            if self.validate_login(username, password): status_login_state = True
        Connection().close_connection()
        return username



    def validate_login(self, username, password):
        minutes_x = 15
        msg_wrong_credentials_logith = "Ingresaste mal tus credenciales"
        msg_wrong_credentials_logith_user = "El usuario no existe"
        msg_user_blocked = f"El usuario esta bloqueado, por {minutes_x}min."
        user_instance = Connection().validate_user_data_existence(username, None, "2")
        if user_instance != None: # If the user exists
            if user_instance.bloqueado == True: # If the user is blocked
                attempts_by_user = Connection().validate_attemps(username)
                if attempts_by_user.time_last_attempt < datetime.utcnow(): # If the user is blocked for more than 15 minutes
                    Connection().unblock_user(username)
                    input("Tu usuario estaba bloqueado, ahora puedes continuar con tu sesion, presione enter para continuar")
                    return 1
                else: # If the user is not blocked for more than 15 minutes
                    Clear_console(); print(f"\n{msg_user_blocked}\nHora de desbloqueo estimada: {attempts_by_user.time_last_attempt}. \nHora actual: {datetime.utcnow()}")
                    exit(0)
                
            else: # If the user is not blocked
                if Encriptar_Datos().decrypt_AES_GCM(user_instance.password, password) == True: # If the password is correct
                    Connection().unblock_user(username)
                    return True
                    
                else: # If the password is wrong
                    Clear_console(); print(msg_wrong_credentials_logith)
                    Connection().set_attempts(username, minutes_x) # Set the attempts and time to block/unblock the user
                    fail_attempts = Connection().validate_attemps(username).failed_attempts
                    print(f"Intentos fallidos: {fail_attempts}")

                    if fail_attempts > 3: # If the user has failed more than 3 times
                        Connection().block_user(username)
                        attempts_by_user = Connection().validate_attemps(username)
                        Clear_console(); print(f"\n{msg_user_blocked}\nDebe esperar el tiempo estimado ({minutes_x} min) e intentar de nuevo\nHora de desbloqueo estimada: {attempts_by_user.time_last_attempt}. \nHora actual: {datetime.utcnow()}")
                        exit(0)
                    else: return 0

        else: Clear_console(); print(msg_wrong_credentials_logith_user); exit(0)