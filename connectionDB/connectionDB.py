from decouple import config
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from .models.models import Base, User_Data, Banking, Failed_Attempts, Currency, Program, City, Campus, Square_Program_Campus, User_Square_Program_Campus, Shipping_item, Financial_Management, Financial_Category, Tip_Financial_Category
from aux_resources.clear_console import Clear_console
import random
import datetime
from sqlalchemy import func
from sqlalchemy import cast
from sqlalchemy import Numeric
from sqlalchemy import literal_column

class Connection:
    def __init__(self):
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.database = config('DB_NAME')
        self.host = config('DB_HOST')
        self.port = config('DB_PORT')
        self.connection_string, self.engine, self.connection, self.status = self.validate_existence_db()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


        
    def close_connection(self): self.connection.close()

    def validate_existence_db(self):
        db_config = {
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'host': self.host,  
            'port': self.port
        }
        try:
            # connection = psycopg2.connect(**db_config)
            connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            engine = create_engine(connection_string)
            connection = engine.connect()
            status=True
            return connection_string, engine, connection, status 
        except OperationalError as e:
            print("Error al conectar a PostgreSQL:", e)
            print("*****************************************")
            print("Recuerda parametrizar correctamente el archivo '.env'...")
            print("Y revisar que tu base de datos este correctamente configurada y activa...")
            print("*****************************************")
            connection_string =None; engine=None; connection=None; status =None
            return connection_string, engine, connection, status


    def validate_tables_status(self, engine):
        tables = inspect(engine).get_table_names()
        tables_required = ['user_data', 'banking', 'failed_attempts', 'currencies', 'program', 'city', 'campus', 'square_program_campus', 'user_square_program_campus', 'shipping_item', 'financial_management', 'financial_category', 'tip_financial_category']
        tables_2_create =  []
        extra_tables = []
        if tables: #If there are tables
            for item in tables:
                if item not in tables_required: extra_tables.append(item)
            for item in tables_required:
                if item not in tables: tables_2_create.append(item)
            if extra_tables: return False, extra_tables #There are extra tables
            elif tables_2_create: return True, tables_2_create #There are tables to create
            else: return True, None #There are no tables to create
        else: return False, None #There are no any tables

    def create_all_tables(self, tables='All'):
        Base.metadata.create_all(self.engine)
        # For setting tables
        if ('currencies' in tables) or (tables == 'All'): self.set_currencies()
        if ('program' in tables) or (tables == 'All'): self.set_programs()
        if 'city' in tables or (tables == 'All'): self.set_cities()
        if 'campus' in tables or (tables == 'All'): self.set_campuses()
        if 'square_program_campus' in tables or (tables == 'All'): self.set_square_program_campus()
        if 'financial_category' in tables or (tables == 'All'): self.set_financial_category()
        if 'tip_financial_category' in tables or (tables == 'All'): self.set_tip_financial_category()
        print("Tablas creadas con exito")

    def validate_db_tables_status(self):
        status_tables_status, tables = self.validate_tables_status(self.engine)
        if(status_tables_status and tables == None): return 1 #If all tables required exists, no need to create tables
        elif(status_tables_status == False and tables): #If there are extra tables, needs fix the issue
            print("Por la seguridad e integridad de los datos se debes revizar la base de datos")
            print("Por favor en tu base de datos elimina las tablas que no hagan parte del programa")
            print("Una vez solucionado el incidente intentalo de nuevo")    
            print("*****************************************")
            print(f"La base de datos tiene las siguientes tablas agenas: {tables}")
            print("*****************************************")
            exit(0)
        elif(status_tables_status and tables): 
            print("La base de datos no tiene la(s) siguiente(s) tabla(s) necesaria(s):")
            print('*****************************************')
            print(tables)
            print('*****************************************')
            print("Presiona 1 crear las tablas faltantes o 0 para cerrar el programa")
            option_main = input()
            while option_main != "0" and option_main != "1":
                Clear_console()
                print("Opcion no valida", option_main)
                option_main = input("Ingrese una opcion valida: ")
            if option_main == "0":exit(0)
            elif option_main == "1":
                self.create_all_tables(tables)

                return 1
            else: return 1
        elif(status_tables_status == False and tables == None):
            input("La base de datos no tiene las tablas requeridas. Presione enter para crearlas: ")
            self.create_all_tables()
            return 1



    # Setters for initial tables
    def set_currencies(self):
        currencies = ['USD', 'CLP', 'ARS', 'EUR', 'TRY', 'GBP']
        for i in currencies:
            if i == 'USD': self.session.add(Currency(currency=i, value=1))
            elif i == 'CLP': self.session.add(Currency(currency=i, value=911))
            elif i == 'ARS': self.session.add(Currency(currency=i, value=815.40))
            elif i == 'EUR': self.session.add(Currency(currency=i, value=0.91))
            elif i == 'TRY': self.session.add(Currency(currency=i, value=30.12))
            elif i == 'GBP': self.session.add(Currency(currency=i, value=0.78))
        self.session.commit()

    def set_cities(self):
        cities = ['Londres', 'Liverpool', 'Manchester']
        for i in cities:
            self.session.add(City(Name=i))
        self.session.commit()

    def set_programs(self):
        programs = ['Informatica', 'Medicina', 'Marketing', 'Artes']
        for i in programs:
            self.session.add(Program(Name=i))
        self.session.commit()


    def set_campuses(self):
        campuses = ['Campus_Londres', 'Campus_Liverpool', 'Campus_Manchester']
        self.session.add(Campus(Name=campuses[0], square_max = 1, program_max=4,city_id=1))
        self.session.add(Campus(Name=campuses[1], square_max = 3, program_max=4,city_id=2))
        self.session.add(Campus(Name=campuses[2], square_max = 1, program_max=4,city_id=3))
        self.session.commit()
    
    def set_square_program_campus(self):
        #For Informatica, Medica, Marketing and Artes programs in Campus_Londres
        self.session.add(Square_Program_Campus(name='Londres_A1', campus_id=1, program_id=1, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Londres_B1', campus_id=1, program_id=2, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Londres_C1', campus_id=1, program_id=3, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Londres_D1', campus_id=1, program_id=4, quota_max=5, quota_used=0))
        
        # For Informatica, Medica, Marketing and Artes programs in Campus_Manchester
        self.session.add(Square_Program_Campus(name='Manchester_A1', campus_id=2, program_id=1, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Manchester_A2', campus_id=2, program_id=1, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Manchester_A3', campus_id=2, program_id=1, quota_max=5, quota_used=0))

        self.session.add(Square_Program_Campus(name='Manchester_B1', campus_id=2, program_id=2, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Manchester_B2', campus_id=2, program_id=2, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Manchester_B3', campus_id=2, program_id=2, quota_max=5, quota_used=0))
        
        self.session.add(Square_Program_Campus(name='Manchester_C1', campus_id=2, program_id=3, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Manchester_C2', campus_id=2, program_id=3, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Manchester_C3', campus_id=2, program_id=3, quota_max=5, quota_used=0))

        self.session.add(Square_Program_Campus(name='Manchester_D1', campus_id=2, program_id=4, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Manchester_D2', campus_id=2, program_id=4, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Manchester_D3', campus_id=2, program_id=4, quota_max=5, quota_used=0))

        # For Informatica, Medica, Marketing and Artes programs in Campus_Liverpool
        self.session.add(Square_Program_Campus(name='Liverpool_A1', campus_id=3, program_id=1, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Liverpool_B2', campus_id=3, program_id=2, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Liverpool_C3', campus_id=3, program_id=3, quota_max=5, quota_used=0))
        self.session.add(Square_Program_Campus(name='Liverpool_D3', campus_id=3, program_id=4, quota_max=5, quota_used=0))

        self.session.commit()


    def set_financial_category(self):
        self.session.add(Financial_Category(category="Income"))
        self.session.add(Financial_Category(category="Medical Expenses"))
        self.session.add(Financial_Category(category="Home Expenses"))
        self.session.add(Financial_Category(category="Leisure Expenses"))
        self.session.add(Financial_Category(category="Education Expenses"))
        self.session.add(Financial_Category(category="See Savings"))
        self.session.commit()

    def set_tip_financial_category(self):
        self.session.add(Tip_Financial_Category(tip="Seguro de salud adecuado: Asegúrate de tener un seguro de salud que se ajuste a tus necesidades para evitar gastos médicos inesperados.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Fondo de emergencia médica: Crea un fondo de emergencia específico para gastos médicos imprevistos.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Revisión de facturas médicas: Examina cuidadosamente tus facturas médicas y asegúrate de que no haya errores o cargos injustos.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Consulta médica preventiva: Programa revisiones médicas regulares para detectar problemas de salud a tiempo y evitar costosos tratamientos.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Medicamentos genéricos: Opta por medicamentos genéricos en lugar de marcas comerciales para ahorrar en recetas.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Vida saludable: Mantén un estilo de vida saludable para reducir la probabilidad de enfermedades y, por lo tanto, de gastos médicos.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Seguro de gastos mayores: Considera la posibilidad de adquirir un seguro de gastos mayores para cubrir enfermedades graves.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Presupuesto para gastos médicos: Incluye un presupuesto específico para gastos médicos en tu plan financiero mensual.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Comparación de costos: Compara costos y opciones antes de someterte a procedimientos médicos o cirugías.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Descuentos en medicina preventiva: Aprovecha descuentos y programas de medicina preventiva que puedan ofrecer tu empleador o tu plan de seguro.", category_id=2))
        self.session.add(Tip_Financial_Category(tip="Presupuesto doméstico: Establece un presupuesto mensual para tus gastos del hogar y síguelo de cerca.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Reducir servicios: Considera la posibilidad de reducir servicios como cable, internet o teléfono si no los utilizas completamente.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Energía eficiente: Adopta prácticas de eficiencia energética para reducir las facturas de electricidad y gas.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Compras a granel: Compra productos a granel para ahorrar en alimentos y productos de uso diario.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Seguro de vivienda: Asegúrate de que tu seguro de vivienda sea adecuado y esté actualizado.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Mantenimiento preventivo: Realiza un mantenimiento regular en tu hogar para evitar costosos problemas a largo plazo.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Compartir gastos: Considera compartir ciertos gastos con compañeros de casa o familiares si es posible.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Seguro de inquilinos: Si eres inquilino, asegúrate de tener un seguro de inquilinos para proteger tus pertenencias.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Descuentos y ofertas: Busca descuentos y ofertas al comprar electrodomésticos, muebles u otros productos para el hogar.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Ahorrar agua y energía: Adopta hábitos que te permitan ahorrar agua y energía, lo que también reducirá tus facturas.", category_id=3))
        self.session.add(Tip_Financial_Category(tip="Planificación de entretenimiento: Establece un límite mensual para gastos en entretenimiento y planea actividades que estén dentro de ese presupuesto.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Descuentos y ofertas: Busca ofertas, descuentos y promociones al comprar boletos para eventos o atracciones.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Entretenimiento en casa: Explora opciones de entretenimiento en casa, como noches de películas, juegos de mesa o actividades al aire libre.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Presupuesto para viajes: Si disfrutas de los viajes, crea un presupuesto específico para ellos y ahorra con anticipación.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Tarjetas de lealtad: Aprovecha las tarjetas de lealtad y programas de recompensas para obtener descuentos en restaurantes y actividades.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Comparación de precios: Investiga y compara precios antes de realizar compras importantes, como equipos deportivos o electrónicos.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Vida activa: Encuentra actividades de ocio que sean físicamente activas y no requieran gastos excesivos.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Planificación de comidas: Come en casa con regularidad y planea tus comidas para evitar comer fuera constantemente.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Bibliotecas y recursos locales: Utiliza las bibliotecas y recursos locales gratuitos para obtener libros, películas y eventos culturales.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Control de suscripciones: Revise periódicamente sus suscripciones a servicios de streaming, revistas o clubes de membresía para asegurarse de que estén en línea con sus intereses y presupuesto.", category_id=4))
        self.session.add(Tip_Financial_Category(tip="Comparación de opciones educativas: Investiga y compara opciones educativas para encontrar programas que se ajusten a tu presupuesto y metas.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Becas y subvenciones: Investiga oportunidades de becas y subvenciones para reducir los costos educativos.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Planificación financiera educativa: Crea un plan financiero para tu educación que incluya presupuesto, ahorro y opciones de financiamiento.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Alternativas a la educación tradicional: Explora opciones educativas en línea o programas de educación continua que puedan ser más asequibles.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Trabajo a medio tiempo: Si es posible, considera trabajar a medio tiempo para ayudar a financiar tu educación.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Compras de libros y materiales usados: Busca libros de texto y materiales de estudio usados para reducir los costos.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Descuentos estudiantiles: Aprovecha los descuentos y beneficios que las instituciones educativas ofrecen a los estudiantes.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Gastos relacionados con la educación: Incluye gastos relacionados con la educación en tu presupuesto y ajústalos según sea necesario.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Asesoramiento financiero estudiantil: Consulta a un asesor financiero especializado en educación para obtener orientación sobre préstamos y financiamiento.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Enfoque en resultados: Mantén el enfoque en tus metas y objetivos profesionales al tomar decisiones educativas para evitar gastar en exceso en títulos que pueden no ser necesarios.", category_id=5))
        self.session.add(Tip_Financial_Category(tip="Establecer metas financieras: Define objetivos de ahorro a corto y largo plazo para mantenerte motivado.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Automatización de ahorros: Configura transferencias automáticas a una cuenta de ahorros en cada ciclo de pago.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Presupuesto de ahorro: Incluye un porcentaje fijo de tus ingresos en tu presupuesto mensual como ahorro.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Planificación financiera: Consulta a un asesor financiero para establecer una estrategia de inversión y ahorro adecuada.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Separar cuentas: Mantén tus cuentas de ahorro separadas de tus cuentas de gasto para evitar gastos accidentales.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Reducción de gastos: Identifica áreas donde puedas reducir gastos innecesarios y dirige esos ahorros hacia tu cuenta de ahorro.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Empleador de ahorro: Aprovecha programas de ahorro de empleador como 401(k) o planes de jubilación similares.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Diversificación de inversiones: Si inviertes, diversifica tus inversiones para reducir el riesgo.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Revisión periódica: Revisa tus metas de ahorro periódicamente y ajústalas según sea necesario.", category_id=6))
        self.session.add(Tip_Financial_Category(tip="Educación financiera: Continúa educándote sobre estrategias de ahorro e inversión para tomar decisiones financieras más informadas.", category_id=6))
        self.session.commit()




    # Getters and other methods for DB Tables's User_Data context
    def get_user_by_name(self, name):
        return self.session.query(User_Data).filter_by(username=name).first()
    
    def get_user_by_id(self, id):
        return self.session.query(User_Data).filter_by(id=id).first()
    
    def validate_user_data_existence(self, nombre, apellido, option="1"):
        try:
            if option == "1": resultado = self.session.query(User_Data).filter_by(nombre=nombre, apellido=apellido).first()
            else: resultado = self.session.query(User_Data).filter_by(username=nombre).first()
            return resultado
        except Exception as e:
            input(f"{e}")
            return None
        
    def create_user(self, nombre, apellido, edad, username, password):
        try:
            new_user_data = User_Data(nombre=nombre, apellido=apellido, edad=edad, username=username, password=password )
            self.session.add(new_user_data)
            self.session.commit()
            x = self.validate_user_data_existence(username, None, "2")
            new_banking = Banking(account_number=str(random.randint(1000000000, 9999999999)) ,balance=2000,user_id=x.id)
            self.session.add(new_banking)
            self.session.commit()
            new_attempts = Failed_Attempts(failed_attempts=0,time_first_failed=datetime.datetime.utcnow(), time_last_attempt=datetime.datetime.utcnow() ,user_id=x.id)
            self.session.add(new_attempts)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        return True
    
    def block_user(self, username):
        x = self.session.query(User_Data).filter_by(username=username).first()
        x.bloqueado = True
        self.session.commit()
        return True
    
    def unblock_user(self, username):
        try: 
            x = self.session.query(User_Data).filter_by(username=username).first()
            x.bloqueado = False
            self.session.commit()
            z = self.session.query(Failed_Attempts).filter_by(user_id=x.id).first()
            z.failed_attempts = 0
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()

        return True


    # Getters and other methods for DB Tables's Banking context
    def get_currency_by_name(self, name):
        return self.session.query(Currency).filter_by(currency=name).first()

    def get_all_currencies(self):
        return self.session.query(Currency).all()
    
    def get_user_banking(self, id):
        return self.session.query(Banking).filter_by(user_id=id).first()

    def add_balance(self, id, amount):
        self.session.query(Banking).filter_by(user_id=id).update({Banking.balance: Banking.balance + amount})
        self.session.commit()

    def withdraw_balance(self, id, amount):
        self.session.query(Banking).filter_by(user_id=id).update({Banking.balance: Banking.balance - amount})
        self.session.commit()

    def transfer_balance(self, account_from, account_to, amount):
        account_from = str(account_from)
        account_to = str(account_to)
        self.session.query(Banking).filter_by(account_number=account_from).update({Banking.balance: Banking.balance - amount})
        self.session.query(Banking).filter_by(account_number=account_to).update({Banking.balance: Banking.balance + amount})
        self.session.commit()



    # Getters and other methods for DB Tables's Square_Program_Campus context
    def get_square_program_campus_available(self):
        return self.session.query(Square_Program_Campus).filter(Square_Program_Campus.quota_used <= 4).all()

    def get_square_program_campus_available_by_program_id_and_campus_id(self, program_id, campus_id):
        return self.session.query(Square_Program_Campus).filter(Square_Program_Campus.program_id == program_id, Square_Program_Campus.campus_id == campus_id, Square_Program_Campus.quota_used <= 4).first()    

    def update_square_program_campus(self, id):
        self.session.query(Square_Program_Campus).filter_by(id=id).update({Square_Program_Campus.quota_used: Square_Program_Campus.quota_used + 1})
        self.session.commit()
        
    def get_square_program_campus_by_id(self, id):
        return self.session.query(Square_Program_Campus).filter_by(id=id).first()

    def get_university_information_by_username(self, username):
        return Connection().get_square_program_campus_by_id(Connection().get_user_square_program_campus_by_user_id(Connection().get_user_by_name(username).id).square_program_campus_id)


    # Getters and other methods for DB Tables's User_Square_Program_Campus context
    def get_user_square_program_campus(self, user):
        try:
            return self.session.query(User_Square_Program_Campus).filter_by(user_id=self.get_user_by_name(user).id).first()
        except: return None

    def get_user_square_program_campus_by_user_id(self, user_id):
        return self.session.query(User_Square_Program_Campus).filter_by(user_id=user_id).first()
    
    def create_user_program_campus(self, user_id, square_program_campus_id):
        new_user_square_program_campus = User_Square_Program_Campus(user_id=user_id, square_program_campus_id=square_program_campus_id)
        self.session.add(new_user_square_program_campus)
        self.session.commit()
    

    # Getters and other methods for DB Tables's Program context
    def get_program_by_id(self, id):
        return self.session.query(Program).filter_by(id=id).first()
    

    # Getters adn other methods for DB Tables's Campus context
    def get_campus_by_id(self, id):
        return self.session.query(Campus).filter_by(id=id).first()
    
    
    # Getters and other methods for DB Tables's Failed_Attempts context
    def validate_attemps(self, username):
        x = self.session.query(Failed_Attempts).filter_by(user_id=self.validate_user_data_existence(username, None, "2").id).first()
        return x

    def set_attempts(self, username, minutes):
        x = self.session.query(Failed_Attempts).filter_by(user_id=self.validate_user_data_existence(username, None, "2").id).first()
        x.failed_attempts += 1
        x.time_first_failed = datetime.datetime.utcnow()
        x.time_last_attempt = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
        self.session.commit()
        return True
    
    # Getters and other methods for DB Tables's Shipping_item context

    def create_shipping_item(self, serial, name_element, weight,user_issuer, user_receiver, amount):
        new_shipping_item = Shipping_item(serial=serial, name=name_element, weight=weight, user_issuer=user_issuer, user_receiver=user_receiver, amount=amount)
        self.session.add(new_shipping_item)
        self.session.commit()

    def get_shipping_item_by_serial(self, serial):
        try: return self.session.query(Shipping_item).filter_by(serial=serial).first()
        except: return None

    def get_all_shipping_items_by_user_issuer_id(self, user_id):
        return self.session.query(Shipping_item).filter_by(user_issuer=user_id).all()

    def get_all_shipping_items_by_user_receiver_id(self, user_id):
        return self.session.query(Shipping_item).filter_by(user_receiver=user_id).all()
    
    # Getters and other methods for DB Tables's Financial_Category context

    def get__all_financial_category(self):
        return self.session.query(Financial_Category).all()
    
    def get_category_by_id(self, id):
        return self.session.query(Financial_Category).filter_by(id=id).first()
    

    # Getters and other methods for DB Tables's Financial_Management context

    def get_all_financial_management(self):
        return self.session.query(Financial_Management).all()
    
    def get_all_financial_management_income_by_user_id(self, user):
        return self.session.query(Financial_Management).filter_by(category_id=1, user_id=self.get_user_by_name(user).id).all()

    def delete_all_financial_management_income_by_user_id(self, user):
        self.session.query(Financial_Management).filter_by(category_id=1, user_id=self.get_user_by_name(user).id).delete()
        self.session.commit()

    def add_financial_management(self, movement, category_id, user_id, status_movement=False):
        new_financial_management = Financial_Management(movement=movement, category_id=category_id, user_id=user_id, status_movement=status_movement)
        self.session.add(new_financial_management)
        self.session.commit()

    def get_all_financial_management_by_user_and_category(self, user, category):
        try:return self.session.query(Financial_Management).filter_by(category_id=category, user_id=self.get_user_by_name(user).id).all()
        except: return 0


    # Getters and other methods for DB Tables's Tip_Financial_Category context
    def get_tip_management_by_id_and_category_id(self, id, category_id):
        return self.session.query(Tip_Financial_Category).filter_by(id=id, category_id=category_id).first()
    
    def get_tip_management_by_category_id(self, category_id):
        return self.session.query(Tip_Financial_Category).filter_by(category_id=category_id).all()