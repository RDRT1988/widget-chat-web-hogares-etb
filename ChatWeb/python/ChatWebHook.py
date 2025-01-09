import os
import sys

def getPath():
	getSctiptPath = os.path.abspath(__file__)
	scriptPath = os.path.dirname(getSctiptPath)
	return scriptPath

# customPath = os.path.join(getPath(),'venv', 'lib', 'python3.8','site-packages')
customPath = os.path.join(getPath(),'venv', 'lib', 'python3.8' or 'python3.10','site-packages')
sys.path.insert(0, customPath)

import random
import string
import socketio
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from crypt import DeCrypt, Encrypt
import pymysql
import requests
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import threading
import time
import pytz                       
import re
import pyshorteners
from suds.client import Client
# from config import keysdb, api, url_web_chat, PATH_PROJECT, api_ivr
servidor_chat = os.getenv("CHATWEB_URL")
servidorBOT = os.getenv("BOTCHATWEBHOOK_URL")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [servidor_chat, servidorBOT]}})
app.config['MAX_CONTENT_LENGTH'] = 25000000 # 25MB
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mp3', '.pdf', '.doc', '.docx']

def random_id():
	# Generar cadena alfanumérica de 10 caracteres
	alphanumeric_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
	timestamp = int(time.time())
	random_string = f"{alphanumeric_string}-{timestamp}"
	return random_string

# ! ACA PODEMOS ENCRIPTAR LAS VARIABLES DE LA BASE DE DATOS
# print('IP',Encrypt('localhost'))
# print('USER',Encrypt('root'))
# print('PASS',Encrypt('MySQL24*07'))
# print('DB',Encrypt('dbp_widget_chat_web_etb'))


global account_sid
global auth_token
global botWhatsappNum
global RutaProyecto
global URL

def cargarConfiguracionInicial():
	print(os.getenv("DB_HOST"))

	#INICIO DB
	app.config['DB_HOST'] = os.getenv("DB_HOST")
	app.config['DB_USER'] = os.getenv("DB_USER")
	app.config['DB_PASSWORD'] = os.getenv("DB_PASSWORD")
	app.config['DB_NAME'] = os.getenv("DB_NAME")
	app.config['DB_PORT'] = os.getenv("DB_PORT")
	print("La base de datos es: ", app.config['DB_NAME'])
	
	#FIN DB

	#INICIO PROVEEDOR
	app.config['BUSSINESSID'] = os.getenv("BUSSINESSID")
	app.config['APIKEY'] = os.getenv("APIKEY")
	app.config['LINEA'] = os.getenv("LINEA")
	app.config['WEBHOOK_PATH'] = os.getenv("WEBHOOK_PATH")
	app.config['WEBHOOK_URL'] = os.getenv("WEBHOOK_URL")
	app.config['WEBHOOK_PORT'] = os.getenv("WEBHOOK_PORT")
	#FIN PROVEEDOR

	#INICIO ZONA HORARIA
	app.config['ZONA_HORARIA'] = os.getenv("ZONA_HORARIA")
	#FIN ZONA HORARIA

	#INICIO OTROS
	# app.config['RECIBIR_MULTIMEDIA'] = os.getenv("RECIBIR_MULTIMEDIA")
	# app.config['RECIBIR_AUDIO'] = os.getenv("RECIBIR_AUDIO")
	app.config['HILOS'] = os.getenv("HILOS")
	#FIN OTROS


#Función para establecer la conexión a la base de datos MySQL
def connection():

    # Se retorna una conexión a la base de datos con los parámetros especificados
    # host: dirección del servidor de base de datos
    # user: nombre de usuario de la base de datos
    # password: contraseña del usuario de la base de datos
    # db: nombre de la base de datos a conectarse
    # use_unicode: habilita el uso de caracteres unicode en la conexión
    # charset: conjunto de caracteres utilizado en la conexión
    # cursorclass: tipo de cursor que se utilizará en la conexión
    # print(app.config['DB_HOST'])
    # print(app.config['DB_USER'])
    # print(app.config['DB_PASSWORD'])
    # print(app.config['DB_NAME'])
    # print(app.config['DB_PORT'])

    connectionMySQL = pymysql.connect(
        host = app.config['DB_HOST'],
        user = app.config['DB_USER'],
        password = app.config['DB_PASSWORD'],
        db = app.config['DB_NAME'],
        port = int(app.config['DB_PORT']),
        use_unicode = True, 
        charset = 'utf8mb4', 
        cursorclass = pymysql.cursors.DictCursor
    )
    connectionMySQL.autocommit(True)

    return connectionMySQL

def lineProfiling(code):

		# Se inicializan las variables globales necesarias para la aplicación
	global account_sid
	global auth_token
	global botWhatsappNum
	global RutaProyecto
	global URL
	
	account_sid = "5A6D4C325A775A6A41775A3241775A334177563241515778417748325A774C6C5A6D566C4D515A30417752325A6D5A325A7A446D42474C6C5A6D5A325A7757784177526D42475A335A6D74325A774C6B5A6D786D5A775A6B5A6D4C325A775A30"
	auth_token = "416D4E304D775A3041514C3141475A344177703241777031414744335A6D706C416D526C4D7748355A6D4E315A6D5A6B417A483342475A6B414774304C47486D416D746D4247703241774C3041775A30416D70324C474D75417748315A774830416D70314151457641545A32417748354147786D4D4E3D3D"
	botWhatsappNum = "5A7A566D41475A335A6D5A6D5A475A6D5A6D446D5A6D5A6A5A6D4E6D5A515A6A5A6D4E3D"
	RutaProyecto = "5A7A4C6D5A4770304177566C4D774579417A4C3241514C31415452315A6D577A41515A304D77486D414A4C31416D4434415152314151486D415152315A51486A414A4C3041514431415444304D77497A414744304251457A415444305A47486D5A7A4C31416D4C314177563042514D7A417A4C324C774833417774325A47706D417752335A51706A41515A324D774D79417A483241477030417A5A3342443D3D"
	URL = "4177743341517030416D4E335A6D41755A7A4C6C4D774C6C417A4C3341514C6D416D56324D517033417774325A477030416D5A325A47706A416D4E324D774C32417752324247706C4177486C4D47706C416D4E325A474C33416D56324D777031416D4E325A6D4D7A416D5A6C4D474C6D417A4C324D4E3D3D"

	print('┌---------------------Info-----------------------')
	print('├ [ account_sid ]', account_sid)
	print('├ [ auth_token ]', auth_token)
	print('└------------------------------------------------')



# Inicializar el cliente de Socket.IO
sio = socketio.Client()

# Conectar al servidor de chat
sio.connect(os.getenv("CHATWEB_URL"))
#sio.connect(servidor_chat)
print('Conectado a servidor chat - socket', os.getenv("CHATWEB_URL"))

def buildMenu(nombreMenu):
	connectionMySQL = connection()
	connectionMySQL.autocommit(True)
	with connectionMySQL.cursor() as cursor:

		sql = f"SELECT PKBTREE_NCODIGO,BTREE_OPTION_NUM,BTREE_TEXTO FROM {app.config['DB_NAME']}.tbl_bot_tree WHERE BTREE_TIPO_MSG='{nombreMenu}'"
		cursor.execute(sql)
		menu = cursor.fetchall()

		if len(menu) > 0:
			contenido_menu = ''
			for b in menu:
				if(b["BTREE_OPTION_NUM"].isnumeric()):
					contenido_menu = contenido_menu + f"{b['BTREE_OPTION_NUM']}. {b['BTREE_TEXTO']}\n"
				else:
					contenido_menu = contenido_menu + f"{b['BTREE_TEXTO']}\n"

	connectionMySQL.close

	return contenido_menu

# def requestWebServiceIVR(data):
# 	SCRIPT_NAME = data['scriptName']
# 	POLIZA = data['poliza']

# 	payload  = { 'scriptName': SCRIPT_NAME, 'poliza': POLIZA }

# 	if SCRIPT_NAME == 'ws_ivr_crear_solicitud':
# 		payload['tpd_codigo'] = data['tpdCodigo'] # codigo causa del daño
# 		payload['tpq_codigo'] = data['tpqCodigo'] # codigo actividad
# 		payload['tel_ivr'] = data['telIvr'] # telefono ingresedo por el usuario en ivr

# 	tiempo_espera = api_ivr['time_out']
# 	try:
# 		resp = requests.post(f"{api_ivr['url']}/generalscriptservice/rest/generalScriptRest/execute", json=payload, auth=(api_ivr['username'], api_ivr['password']), timeout=tiempo_espera)

# 		if resp.status_code == 200:
# 			# This means something went wrong.
# 			data = resp.json()
# 			# Manejar los datos de respuesta según tus necesidades
# 			# print(data)
# 			return data
# 		else:
# 			print("Error request IVR:", resp.status_code)
# 			return False
		
# 	except requests.exceptions.Timeout:
# 		print(f"La solicitud ha superado el tiempo de espera de {tiempo_espera} segundos.") 
# 		return False
# 	except:
# 		print('Error request IVR')
# 		return False




# ! DEFINIR VARIABLES - ARBOL
estadoChat = 'Novedad'
navegacionArbolChat = 'MSG_FIN'
resultApiNit = '' 
numeroNIT = '-'
estadoNit = '-'
segmento = '-'
razonSocial = '-'
tipoDocumento = '-'
numeroDocumento = '-'
nombreContacto = '-'
numeroContacto = '-'
correoContacto = '-'
# Grupos
gruposDisponibles = '-'
opcionGrupoSeleccionado = '-'
idGrupoSeleccionado = '-'
nombreGrupoSeleccionado = '-'
motivoTramite = '-'
peticionAbierta = '-'
numeroCaso = '-'
adjuntoDocumento = '-'
rutaArchivoAdjunto = '-'
idTipoAgendamiento = '-'
tipoAgendamiento = '-'
# Subgrupos
subGruposDisponibles = '-'
opcionSubGrupoSeleccionado = '-'
idSubGrupoSeleccionado = '-'
nombreSubGrupoSeleccionado = '-'
# Agendas
agendasDisponibles = '-'
opcionAgendaSeleccionada = '-'
# Especialista
idEspecialistaSeleccionado = '-'
especialistaSeleccionado = '-'
fechaHoraSeleccionada = '-'
estadoGestion = "Cerrado"
descripcionChat = '-'

# ! ARBOL DE NAVEGACION
def arbol(lastrowid, whatsappNum, Body):
    print('info mensaje', lastrowid, whatsappNum, Body)
    print('-----------ARBOL----------')
    
    # * VARIABLES
    global estadoChat
    global navegacionArbolChat
    global resultApiNit
    global numeroNIT
    global estadoNit
    global segmento
    global razonSocial
    global tipoDocumento
    global numeroDocumento
    global nombreContacto
    global numeroContacto
    global correoContacto
    # Grupos
    global gruposDisponibles
    global opcionGrupoSeleccionado
    global idGrupoSeleccionado
    global nombreGrupoSeleccionado
    global motivoTramite
    global peticionAbierta
    global numeroCaso
    global adjuntoDocumento
    global rutaArchivoAdjunto
    global idTipoAgendamiento
    global tipoAgendamiento
    # Subgrupos
    global subGruposDisponibles
    global opcionSubGrupoSeleccionado
    global idSubGrupoSeleccionado
    global nombreSubGrupoSeleccionado
    # Agendas
    global agendasDisponibles
    global opcionAgendaSeleccionada
    # Especialista
    global idEspecialistaSeleccionado
    global especialistaSeleccionado
    global fechaHoraSeleccionada
    global estadoGestion
    global descripcionChat
    
    # * DEFINIR MENSAJES FIJOS
    arbolIncio = 'Hola, \n En el momento que desee volver, por favor escriba <strong>inicio</strong> o <strong>INICIO</strong> para regresar al menu principal🔄'
    arbolPaso1 = '📝 <strong>Para continuar por favor ingrese el número de documento.</strong>\n\n ⚠️ <i>Minimo 7 dígitos.</i>\n 🚫 <i>Sin espacios ni caracteres especiales.</i>\n 🔢 <i>Solo números.</i>'
    arbolValidarNit = '❌ El documento ingresedo es inválido. Asegúrese de que tenga minimo 7 dígitos.'
    arbolRedireccionarCliente = '⚠️ <strong>No hemos logrado validar la información registrada.</strong>\n\n🏠 Si su servicio es de <strong>segmento XXXXX</strong>, lo invitamos a comunicarse a la línea WhatsApp XXXXX o al XXXXX opción XXXXX, donde uno de nuestros asesores atenderá su solicitud.\n\n🏢 Si su servicio corresponde al <strong>segmento ETB XXXXX</strong>, lo invitamos a comunicarse a la línea WhatsApp XXXXX, o al XXXXX opción XXXXX, donde uno de nuestros asesores atenderá su solicitud.'
    arbolTratamientoDatos = (
        "🔔 Al continuar, <strong>autoriza el tratamiento de datos personales</strong> y <strong>acepta los términos y condiciones</strong> "
        "de nuestro canal de atención digital. 📄 Puede consultarlos en el siguiente enlace: "
        "https://goto.now/NqJAd\n"
        "⚠️ <i>Abra el enlace en una nueva pestaña (ctrl + click).</i>\n\n"
        "✍️ <i>Ahora, para continuar, por favor diligencie su información de contacto.</i>\n\n"
        "📢 Al continuar en este chat está aceptando nuestra política de datos personales y la grabación de su video atención."
    )
    arbolTipoDocumento = (
        "📄 <strong>Seleccione el tipo de documento:</strong>\n"
        "1. CC\n"
        "2. CE"
    )
    arbolNumeroDocumento = (
        "🔢 <strong>Número de Documento:</strong> \n"
        "Por favor, ingrese un número válido según el tipo de documento seleccionado:\n"
        "• <i>Para <strong>CC</strong> (Cédula de Ciudadanía): debe tener un mínimo de <strong>7 dígitos</strong>.</i>\n"
        "• <i>Para <strong>CE</strong> (Cédula de Extranjería): debe tener un mínimo de <strong>9 dígitos</strong>.</i>\n"
        "⚠️ <i>Sin espacios ni caracteres especiales, solo números.</i>"
    )
    arbolNombreCliente = (
        "📝 <strong>Nombres y Apellidos:</strong> \n"
        "⚠️ <i>Por favor, ingrese sus nombres y apellidos completos.</i>"
    )
    arbolNumeroContacto = (
        "📞 <strong>Teléfono de Contacto:</strong> \n"
        "• <i>Para Telefonos fijos, por favor, ingrese el indicativo + número, por ejemplo: <strong>6015067898</strong>.</i>\n"
        "• <i>Para Número de Celular, se compone de 10 dígitos, por ejemplo: <strong>3057800000</strong>.</i>\n"
        "⚠️ <i>Sin espacios, solo números y sin caracteres especiales.</i>"
    )
    arbolCorreoCorporativo = (
        "📧 <strong>Correo de Contacto:</strong> \n"
        "• <i>Por favor, ingrese su correo electrónico.</i>\n"
        "⚠️ <i>Recuerda que el correo electrónico debe ser válido.</i>"
    )
    # Esto en realidad son grupos
    arbolTipoSolicitud = (
        "📝 <strong>A continuación, seleccione el tipo de consulta o trámite que desea realizar:</strong> \n"
        "1. Videoatención para Soporte Técnico.\n"
        "2. Videoatención para Trámites Posventa."
    )
    arbolMotivoAgendamiento = (
        "📝 <strong>Por favor, proporcione una descripción detallada del motivo del agendamiento:</strong>\n"
        "⚠️ <i>Máximo 1000 caracteres.</i>"
    )
    arbolPeticionAbierta = (
        "📝 <strong>Actualmente, ¿cuenta con un caso abierto sobre esta petición?</strong> \n"
        "1. Sí\n"
        "2. No"
    )
    arbolNumeroCaso = (
        "📝 <strong>Por favor, ingrese el número de caso:</strong> \n"
        "⚠️ <i>Sin espacios ni caracteres especiales.</i>\n"
        "🔢 <i>Solo números.</i>"
    )
    arbolAdjuntarDocumento = (
        "📝 <strong>Adjuntar documento:</strong> \n"
        "• <i>No es obligatorio.</i>\n"
        "⚠️ <i>El documento debe ser un archivo .pdf .xls .jpg .png .doc únicamente y no debe superar los 5 MB.</i>\n\n"
        "1. No deseo adjuntar documento."
    )
    arbolAdjuntoNoValido = (
        "⚠️ <strong>El documento adjunto no es válido.</strong> \n"
        "⚠️ <i>El documento debe ser un archivo .pdf .xls .jpg .png .doc únicamente y no debe superar los 5 MB.</i>"
    )
    arbolConfirmarAdjunto = (
    "📝 <strong>Hemos recibido y guardado su documento adjunto con éxito.</strong>"
    )
    arbolOpcionesAgendamiento = (
        "📝 <strong>Seleccione la opción de agendamiento:</strong> \n"
        "1. ¿Permanecer en la cola para ser atendido?\n"
        "2. ¿Desea agendar un espacio para atención?"
    )    
    arbolOpcionAgendamiento = (
        "📝 <strong>Vamos a agendar un espacio para atención</strong>\n"
        "2. Si, deseo agendar un espacio programado para atención.\n\n"
        "⚠️ <i>Entre las 06:00 pm y 05:59 am solo se agendan espacios programados para atención.</i>"
    )
    arbolGruposAgendamiento = ''
    arbolAgendasDisponibles = ''
    arbolAgendaNoDisponible = (
        "⚠️ <strong>La agenda seleccionada no está disponible.</strong> \n"
        "⚠️ <i>Por favor, selecciona una nueva agenda disponible ya que la agenda seleccionada no está disponible.</i>"
    )
    arbolEspecialistasNoDisponibles = (
        f"⚠️ En este momento, todos nuestros Agentes Especializados / Agentes de Soporte están en videollamada.\n\n"
        f"Si desea esperar, permanezca en línea y le avisaremos en cuanto podamos atenderle.\n\n"
        f"También puede agendar su espacio de videoatención según disponibilidad aquí."
    )
    arbolConsultandoAgendaInmediata = (
        "⏳ <strong>Buscando un especialista disponible.</strong>\n"
        "🙏 <i>Agradecemos su paciencia mientras localizamos al profesional adecuado para atenderle. Por favor, manténgase a la espera unos instantes.</i>"
    )
    arbolNoEntiendo = (
        "❓ <strong>No entiendo su respuesta.</strong> \n"
        "Por favor, asegúrese de seguir las instrucciones y proporciona una respuesta válida.\n\n"
        "En el momento que desee volver, por favor escriba <strong>inicio</strong> o <strong>INICIO</strong> para regresar al menú principal 🔄."
    )
    arbolErrorAPI = (
        "⏳ <strong>Estamos experimentando una incidencia técnica.</strong>\n"
        "🙏 <i>Le pedimos que espere o nos visite nuevamente en breve mientras solucionamos el inconveniente. Agradecemos su comprensión.</i>"
    )
    arbolFin = '🌟 ¡Gracias por haber utilizado nuestro servicio! \n\n 😊 Esperamos haberle ayudado. \n\n <strong>¡Hasta pronto!</strong> 👋'
    
    connectionDB = connection()
    connectionDB.autocommit(True)
    try:
        with connectionDB.cursor() as cursor:
            # regexNivel = r'^L\d+$'

            sql = f"SELECT cht_id, cht_navegacion_arbol, cht_estado_gestion, cht_descripcion FROM {app.config['DB_NAME']}.tbl_chat WHERE cht_id = '{str(lastrowid)}' AND cht_id_chat_web = '{whatsappNum}' AND cht_tipo_estado = 'Activo' ORDER BY cht_id DESC LIMIT 1;"

            cursor.execute(sql)
            rows = cursor.fetchall()

            current_time = datetime.now().time()

            # todo: Horario de atencion
            office_start_time = datetime.strptime("00:00", "%H:%M").time()
            office_end_time = datetime.strptime("23:59", "%H:%M").time()

            if len(rows) > 0:
                resultNavegacionArbol = str(rows[0]['cht_navegacion_arbol'])
                # todo: Arbol - Inicio
                BoddyUpper = Body.upper()
                if BoddyUpper == 'INICIO' or BoddyUpper=='*INICIO*':
                    if (rows[0]["cht_estado_gestion"] == "Abierto" and rows[0]["cht_estado_gestion"] != "MSG_ENCUESTA"):
                        # Variables
                        navegacionArbolChat = 'MSG_VERIFICAR_NIT'
                        
                        sendMessage(whatsappNum, arbolPaso1, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, lastrowid))
                # todo: Arbol - Cerrar chat
                elif Body == 'CERRAR':
                    # Variables
                    navegacionArbolChat = 'MSG_FIN'
                    estadoGestion = "Cerrado"
                    descripcionChat = 'BOT - CERRADO'
                    
                    # Actualizar el chat
                    sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_estado_gestion = %s, , cht_enviado = now(), cht_descripcion = %s WHERE cht_id = %s;"
                    cursor.execute(sql, (navegacionArbolChat, estadoGestion, descripcionChat, lastrowid))

                # todo: Arbol - Saludo
                elif resultNavegacionArbol == 'MSG_SALUDO':
                    # Variables
                    navegacionArbolChat = 'MSG_VERIFICAR_NIT'
                    descripcionChat = arbolPaso1
                    
                    sendMessage(whatsappNum, arbolIncio, lastrowid)
                    sendMessage(whatsappNum, arbolPaso1, lastrowid)
                    
                    # Actualizar el chat
                    sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                    cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))

                # todo: Arbol - Verificar NIT
                elif resultNavegacionArbol == 'MSG_VERIFICAR_NIT' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    if Body.isnumeric() and (len(Body) >= 7):
                        # while True:  # Bucle que se ejecuta indefinidamente hasta que se obtenga una respuesta válida
                            # Validar que sea un número y tenga 9 dígitos
                            # Pasar valores a variables globales
                            numeroNIT = Body
                            estadoNit = 'Registrado'
                            segmento = 'Hogares'
                            razonSocial = 'Pepito Prueba'
                            
                            # Mensaje de confirmación
                            navegacionArbolChat = 'MSG_CONFIRMANDO_NIT'
                            mensajeConfirmacionNit = (
                                f"🔍 La información ingreseda corresponde al cliente \n"
                                f"<strong>{razonSocial}</strong> con documento <strong>{numeroNIT}</strong>. \n\n"
                                f"<strong>¿Es correcto?</strong> \n 1. Sí \n 2. No"
                            )
                            descripcionChat = mensajeConfirmacionNit

                            sendMessage(whatsappNum, mensajeConfirmacionNit, lastrowid)
                            sql = f"""
                                UPDATE {app.config['DB_NAME']}.tbl_chat 
                                SET cht_navegacion_arbol = %s, cht_numero_nit = %s, cht_descripcion = %s 
                                WHERE cht_id = %s;
                            """
                            cursor.execute(sql, (navegacionArbolChat, numeroNIT, descripcionChat, lastrowid))

                            # # ? Consumir API consultar NIT
                            # # Variables
                            # txt_Nit = Body                              
                            # estadoGestion = "Cerrado"
                            # navegacionArbolChat = 'MSG_FIN'
                            # descripcionChat = '⚠️ No hemos logrado validar la información registrada.'
                            
                            # # Preparar la URL y los headers
                            # url = os.getenv('URL_API_CONSULTAR_NIT')
                            # headers = {
                            #     "X-API-Key": f"{os.getenv('TOKEN_API_CONSULTAR_NIT')}",
                            #     "Content-Type": "application/json"
                            # }
                            
                            # # Cuerpo de la solicitud
                            # payload = {
                            #     "account": txt_Nit
                            # }

                            # # Intentar realizar la solicitud
                            # try:
                            #     responseApiNit = requests.post(url, json=payload, headers=headers, verify=False)
                            #     print('responseApiNit ===> ', responseApiNit)

                            #     # Respuesta 200 - Éxito o 400
                            #     if responseApiNit.status_code == 200 or responseApiNit.status_code == 400:
                            #         data = responseApiNit.json()
                            #         print('result Api Nit data ===> ', data)

                            #         if data and 'data' in data and data['data']['statusNit']:  
                            #             # NIT válido (Corresponde a E&CI)
                            #             numeroNIT = data['data']['nit']
                            #             estadoNit = 'Corresponde a E&CI'
                            #             segmento = data['data']['segment']
                            #             razonSocial = data['data']['name']

                            #             # Mensaje de confirmación
                            #             navegacionArbolChat = 'MSG_CONFIRMANDO_NIT'
                            #             mensajeConfirmacionNit = (
                            #                 f"🔍 La información ingreseda corresponde al cliente \n"
                            #                 f"<strong>{razonSocial}</strong> con NIT <strong>{numeroNIT}</strong>. \n\n"
                            #                 f"<strong>¿Es correcto?</strong> \n 1. Sí \n 2. No"
                            #             )
                            #             descripcionChat = mensajeConfirmacionNit

                            #             sendMessage(whatsappNum, mensajeConfirmacionNit, lastrowid)
                            #             sql = f"""
                            #                 UPDATE {app.config['DB_NAME']}.tbl_chat 
                            #                 SET cht_navegacion_arbol = %s, cht_numero_nit = %s, cht_descripcion = %s 
                            #                 WHERE cht_id = %s;
                            #             """
                            #             cursor.execute(sql, (navegacionArbolChat, numeroNIT, descripcionChat, lastrowid))
                                    
                            #         else:
                            #             # NIT NO corresponde a E&CI
                            #             estadoNit = 'No corresponde a E&CI'
                            #             sendMessage(whatsappNum, arbolRedireccionarCliente, lastrowid)
                            #             sendMessage(whatsappNum, arbolFin, lastrowid)
                                        
                            #             sql = f"""
                            #                 UPDATE {app.config['DB_NAME']}.tbl_chat 
                            #                 SET cht_numero_nit = %s, cht_estado_nit = %s, cht_descripcion = %s 
                            #                 WHERE cht_id = %s;
                            #             """
                            #             cursor.execute(sql, (navegacionArbolChat, numeroNIT, estadoNit, descripcionChat, lastrowid))

                            #             # Cerrar el chat
                            #             cerrarChat(cursor, lastrowid, estadoGestion, navegacionArbolChat, descripcionChat)
                                    
                            #         break  # Si la consulta fue exitosa, salimos del bucle

                            #     # Respuesta 500 - Error del servidor
                            #     elif responseApiNit.status_code == 500:
                            #         print("Error 500: Problema en el servidor de la API")                        
                            #         # Variables
                            #         navegacionArbolChat = 'MSG_VERIFICAR_NIT'
                            #         descripcionChat = arbolErrorAPI

                            #         sendMessage(whatsappNum, arbolErrorAPI, lastrowid)
                            #         sql = f"""
                            #             UPDATE {app.config['DB_NAME']}.tbl_chat 
                            #             SET cht_estado_chat = %s, cht_navegacion_arbol = %s, cht_numero_nit = %s, cht_estado_nit = %s, cht_descripcion = %s 
                            #             WHERE cht_id = %s;
                            #         """
                            #         cursor.execute(sql, (estadoChat, navegacionArbolChat, numeroNIT, estadoNit, descripcionChat, lastrowid))

                            #         # Esperamos 1.5 minutos antes de intentar nuevamente
                            #         time.sleep(90)
                                
                            #     # Otros códigos de estado
                            #     else:
                            #         print(f"Error inesperado: {responseApiNit.status_code}")                        
                            #         # Variables
                            #         navegacionArbolChat = 'MSG_VERIFICAR_NIT'
                            #         descripcionChat = arbolErrorAPI

                            #         sendMessage(whatsappNum, arbolErrorAPI, lastrowid)
                                    
                            #         sql = f"""
                            #             UPDATE {app.config['DB_NAME']}.tbl_chat 
                            #             SET cht_estado_chat = %s, cht_navegacion_arbol = %s, cht_numero_nit = %s, cht_descripcion = %s 
                            #             WHERE cht_id = %s;
                            #         """
                            #         cursor.execute(sql, (estadoChat, navegacionArbolChat, numeroNIT, descripcionChat, lastrowid))

                            #         # Esperamos 1.5 minutos antes de intentar nuevamente
                            #         time.sleep(90)
                            
                            # except requests.exceptions.RequestException as e:
                            #     # Manejo de errores en la solicitud
                            #     print(f"Error en la solicitud: {str(e)}")
                        
                            #     # Variables
                            #     navegacionArbolChat = 'MSG_VERIFICAR_NIT'
                            #     descripcionChat = arbolErrorAPI

                            #     sendMessage(whatsappNum, arbolErrorAPI, lastrowid)
                                
                            #     sql = f"""
                            #         UPDATE {app.config['DB_NAME']}.tbl_chat 
                            #         SET cht_estado_chat = %s, cht_navegacion_arbol = %s, cht_numero_nit = %s, cht_descripcion = %s 
                            #         WHERE cht_id = %s;
                            #     """
                            #     cursor.execute(sql, (estadoChat, navegacionArbolChat, numeroNIT, descripcionChat, lastrowid))

                            #     # Esperamos 1.5 minutos antes de intentar nuevamente
                            #     time.sleep(90)
                            
                    elif Body.isnumeric() and (len(Body) < 7):  # Si no tiene 7 dígitos
                        sendMessage(whatsappNum, arbolValidarNit, lastrowid)
                        sendMessage(whatsappNum, arbolPaso1, lastrowid)
                        
                        # Variables
                        navegacionArbolChat = 'MSG_VERIFICAR_NIT'
                        descripcionChat = arbolValidarNit
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat,  lastrowid))
                    
                    else:
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        # Variables
                        navegacionArbolChat = 'MSG_VERIFICAR_NIT'
                        descripcionChat = arbolNoEntiendo
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat,  lastrowid))

                # todo: Arbol - Confirmar NIT e información
                elif resultNavegacionArbol == 'MSG_CONFIRMANDO_NIT' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    if Body.isnumeric() and (int(Body) == 1):
                        # Si la respuesta es 1 o mejor dicho Si                       
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_TIPODOCUMENTO'
                        descripcionChat = arbolTipoDocumento
                        
                        # Enviar mensaje tratamiento de datos
                        sendMessage(whatsappNum, arbolTratamientoDatos, lastrowid)
                        
                        # Enviar mensaje solicitando tipo de documento
                        sendMessage(whatsappNum, arbolTipoDocumento, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_numero_nit = %s, cht_estado_nit = %s, cht_segmento = %s, cht_razon_social = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, numeroNIT, estadoNit, segmento, razonSocial, descripcionChat, lastrowid))
                        
                    elif Body.isnumeric() and (int(Body) == 2):
                        # Si la respuesta es 2 o mejor dicho No 
                        # Variables
                        navegacionArbolChat = 'MSG_VERIFICAR_NIT'
                        descripcionChat = 'Solicitando nuevamente el número de Nit'
                        
                        sendMessage(whatsappNum, arbolPaso1, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_numero_nit = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, numeroNIT, descripcionChat, lastrowid))
                        
                    else:
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        # Variables
                        navegacionArbolChat = 'MSG_CONFIRMANDO_NIT'
                        descripcionChat = arbolNoEntiendo
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, lastrowid))
                
                # todo: Arbol - Solicitar tipo de documento
                elif resultNavegacionArbol == 'MSG_SOLICITA_TIPODOCUMENTO' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    if Body.isnumeric() and (int(Body) == 1) or Body.isnumeric() and (int(Body) == 2):
                        # Si la respuesta es 1 o mejor dicho C.C o 2 o mejor dicho C.E                        
                        # Pasar valores a variables globales
                        if Body.isnumeric() and (int(Body) == 1):
                            tipoDocumento = 'CC'
                        elif Body.isnumeric() and (int(Body) == 2):
                            tipoDocumento = 'CE'
                            
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_NUMERODOCUMENTO'
                        descripcionChat = arbolNumeroDocumento
                        
                        # Enviar mensaje solicitando número de documento
                        sendMessage(whatsappNum, arbolNumeroDocumento, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_tipo_documento = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, tipoDocumento, descripcionChat, lastrowid))
                        
                    else:
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_TIPODOCUMENTO'
                        descripcionChat = arbolNoEntiendo
                        
                        # Enviar mensaje
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                                                
                        # Actualizar el chat
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                        
                # todo: Arbol - Solicitar número de documento
                elif resultNavegacionArbol == 'MSG_SOLICITA_NUMERODOCUMENTO' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    if Body.isnumeric() and (int(Body)) :
                        # Si se obtiene un número de documento
                        # Pasar valores a variables globales
                        numeroDocumento = Body
                        
                        # Validación de la longitud según el tipo de documento
                        if tipoDocumento == 'CC' and len(numeroDocumento) > 7:
                            # Si el tipo es CC y la longitud es mayor o igual a 7
                            navegacionArbolChat = 'MSG_SOLICITA_NOMBRECLIENTE'
                            descripcionChat = arbolNombreCliente
                            
                            # Enviar mensaje solicitando nombre del cliente
                            sendMessage(whatsappNum, arbolNombreCliente, lastrowid)
                            
                            # Actualizar el estado en la base de datos
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_numero_documento = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (navegacionArbolChat, numeroDocumento, descripcionChat, lastrowid))

                        elif tipoDocumento == 'CE' and len(numeroDocumento) > 9:
                            # Si el tipo es CE y la longitud es mayor o igual a 9
                            navegacionArbolChat = 'MSG_SOLICITA_NOMBRECLIENTE'
                            descripcionChat = arbolNombreCliente
                            
                            # Enviar mensaje solicitando nombre del cliente
                            sendMessage(whatsappNum, arbolNombreCliente, lastrowid)
                            
                            # Actualizar el estado en la base de datos
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_numero_documento = %s , cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (navegacionArbolChat, numeroDocumento, descripcionChat, lastrowid))

                        
                        else:
                            
                            # Variables
                            navegacionArbolChat = 'MSG_SOLICITA_NUMERODOCUMENTO'
                            descripcionChat = arbolNoEntiendo
                        
                            sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                            
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (navegacionArbolChat, descripcionChat,  lastrowid))
                        
                    else:
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_NUMERODOCUMENTO'
                        descripcionChat = arbolNoEntiendo
                    
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat,  lastrowid))
                        
                # todo: Arbol - Solicitar nombre del cliente
                elif resultNavegacionArbol == 'MSG_SOLICITA_NOMBRECLIENTE' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    # Verificar si el Body no es vacío y contiene al menos dos palabras
                    if Body.strip() and len(Body.split()) >= 2:
                        # Si se obtiene un nombre de cliente válido con al menos un nombre y un apellido
                        # Pasar valores a variables globales
                        nombreContacto = Body.title()
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_NUMEROCONTACTO'
                        descripcionChat = arbolNumeroContacto
                        
                        # Enviar mensaje solicitando número de contacto
                        sendMessage(whatsappNum, arbolNumeroContacto, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_nombres_apellidos = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, nombreContacto, descripcionChat, lastrowid))
                        
                    else:
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_NOMBRECLIENTE'
                        descripcionChat = arbolNoEntiendo
                        
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)  
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                             
                # todo: Arbol - Solicitar número de contacto
                elif resultNavegacionArbol == 'MSG_SOLICITA_NUMEROCONTACTO' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    print('Body ===> ', Body)
                    # Validar que Body es numérico y tiene al menos 10 dígitos
                    if Body.isnumeric() and len(Body) >= 10:
                        print('Body es numérico y tiene valor válido ===> ', Body)
                        # Pasar valores a variables globales
                        numeroContacto = Body
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_CORREOCLIENTE'
                        descripcionChat = arbolCorreoCorporativo
                        
                        # Enviar mensaje solicitando correo del cliente
                        sendMessage(whatsappNum, arbolCorreoCorporativo, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_numero_contacto = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, numeroContacto, descripcionChat, lastrowid))
                    else:
                        # Si no es válido (no numérico, no tiene 10 caracteres, etc.)
                        print('Body no es válido ===> ', Body)
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_NUMEROCONTACTO'
                        descripcionChat = arbolNoEntiendo
                        
                        # Enviar mensaje de error
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))

                # todo: Arbol - Solicitar correo del cliente
                elif resultNavegacionArbol == 'MSG_SOLICITA_CORREOCLIENTE' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    # Verificar si el Body es un correo electrónico válido
                    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', Body.strip()):
                        # Si se obtiene un correo electrónico válido
                        # Pasar valores a variables globales
                        correoContacto = Body
                        
                        # ? Consumir API video atencion etb / Grupos - Anna
                        # Variables
                        result = '' 
                        
                        # Preparar la URL y los headers
                        url = os.getenv('URL_API_SOUL_ETB')+'/v1/public/groups/with-campaigns/list'
                        print("url: ", url)
                        headers = {
                            "Content-Type": "application/json"
                        }
                        
                        while True:
                            # Enviar la solicitud GET a la API
                            try:
                                responseApiGrupos = requests.get(url, headers=headers)  # Realiza la solicitud GET

                                # Verificar si la respuesta es exitosa (status_code 200)
                                if responseApiGrupos.status_code == 200:
                                    data = responseApiGrupos.json()  # Obtener los datos de la respuesta
                                    result = data

                                    # Si la respuesta es válida, procesamos los datos
                                    print('result Api GRUPOS ===> ', result)

                                    # Verificar si la clave 'groups' está presente en la respuesta y contiene datos
                                    if 'groups' in result and isinstance(result['groups'], list) and len(result['groups']) > 0:
                                        # Almacenar los grupos disponibles
                                        gruposDisponibles = {
                                            indice + 1: grupo
                                            for indice, grupo in enumerate(result['groups'])  # Acceder a la lista en 'groups'
                                        }

                                        # Generar el mensaje con las opciones enumeradas
                                        listarGruposDisponibles = "\n".join([
                                            f"{indice}. {grupo['name']}"  # Mostrar el nombre del grupo
                                            for indice, grupo in gruposDisponibles.items()
                                        ])
                                        
                                        # Generar las opciones para mostrar al usuario
                                        mensajeGruposDisponibles = f"📝 <strong>Por favor, elija un grupo:</strong>\n{listarGruposDisponibles}"
                                        
                                        # Pasar valores a variables globales
                                        arbolGruposDisponibles = mensajeGruposDisponibles
                                        navegacionArbolChat = 'MSG_TIPO_SOLICITUD'
                                        descripcionChat = arbolGruposDisponibles
                                        
                                        # Enviar mensaje solicitando agendas disponibles
                                        sendMessage(whatsappNum, arbolGruposDisponibles, lastrowid)
                                        
                                        # Actualizar base de datos
                                        sql = f"""
                                            UPDATE {app.config['DB_NAME']}.tbl_chat 
                                            SET cht_navegacion_arbol = %s, 
                                                cht_correo_contacto = %s,
                                                cht_descripcion = %s 
                                            WHERE cht_id = %s;
                                        """
                                        cursor.execute(sql, (navegacionArbolChat, correoContacto, descripcionChat, lastrowid))
                                        break  # Salir del bucle si la respuesta es exitosa
                                    
                                    else:
                                        # Si la respuesta es 200, pero no encontramos groups en el json que nos entrega la api
                                        print(f"Error en respuesta de API. No se encuentran grupos!!!!")
                                        result = False

                                else:
                                    # Si la respuesta no es 200, mostramos el error y enviamos el mensaje de error
                                    print(f"Error en respuesta de API. Código de estado: {responseApiGrupos.status_code}")
                                    result = False

                            except requests.exceptions.RequestException as e:
                                # Si ocurre una excepción, también manejamos el error
                                print(f"Error en python/ChatWebHook.py → responseApiGrupos: {str(e)}")
                                result = False

                            print('result en grupos ==================> ',result)
                            # Lógica para manejar errores: Enviar mensaje al usuario
                            if result is False:
                                navegacionArbolChat = 'MSG_SOLICITA_CORREOCLIENTE'
                                descripcionChat = arbolErrorAPI
                                
                                # Enviar mensaje de error al usuario
                                sendMessage(whatsappNum, arbolErrorAPI, lastrowid)
                                
                                # Actualizar la base de datos con el estado de error
                                sql = f"""
                                    UPDATE {app.config['DB_NAME']}.tbl_chat 
                                    SET cht_estado_chat = %s, 
                                        cht_navegacion_arbol = %s, 
                                        cht_descripcion = %s 
                                    WHERE cht_id = %s;
                                """
                                cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))

                            # Esperar 1.5 minutos antes de volver a intentar
                            time.sleep(90)
                            
                    else:
                        # Si no es válido (no numérico, no tiene 10 caracteres, etc.)
                        print('Body no es válido ===> ', Body)
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_CORREOCLIENTE'
                        descripcionChat = arbolNoEntiendo
                        
                        # Enviar mensaje de error
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                
                # todo: Arbol - Solicitar tipo de solicitud
                elif resultNavegacionArbol == 'MSG_TIPO_SOLICITUD' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    # Validamos que el valor de body sea un numero
                    if Body.isnumeric() and (int(Body)):
                        opcionGrupoSeleccionado = int(Body)  # Convertimos el input a entero
    
                        # Buscamos el grupo seleccionado en el diccionario
                        grupo = gruposDisponibles.get(opcionGrupoSeleccionado, None)
                        
                        if grupo:
                            # Variables                        
                            # Pasar valores a variables globales
                            idGrupoSeleccionado = grupo['id']
                            nombreGrupoSeleccionado = grupo['name']
                            navegacionArbolChat = 'MSG_SOLICITA_MOTIVOAGENDAMIENTO'
                            descripcionChat = arbolMotivoAgendamiento
                            
                            # Enviar mensaje solicitando motivo de agendamiento
                            sendMessage(whatsappNum, arbolMotivoAgendamiento, lastrowid)
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_id_grupo = %s, cht_nombre_grupo = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (navegacionArbolChat, idGrupoSeleccionado , nombreGrupoSeleccionado, descripcionChat, lastrowid))
 
                        else:
                            # Variables
                            navegacionArbolChat = 'MSG_TIPO_SOLICITUD'
                            descripcionChat = arbolNoEntiendo
                            
                            sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                            
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))
                            
                    else:
                        
                        # Variables
                        navegacionArbolChat = 'MSG_TIPO_SOLICITUD'
                        descripcionChat = arbolNoEntiendo
                        
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                        
                # todo: Arbol - Solicitar motivo de agendamiento
                elif resultNavegacionArbol == 'MSG_SOLICITA_MOTIVOAGENDAMIENTO' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    # Limpiar el Body y validar longitud
                    cleaned_body = Body.strip()
                    
                    if cleaned_body and len(cleaned_body) <= 1000:
                        # Si se obtiene un motivo de agendamiento válido
                        # Convertir la primera letra a mayúscula y el resto a minúsculas
                        formatted_body = cleaned_body.capitalize()
                        # Pasar valores a variables globales
                        motivoTramite = formatted_body                        
                        
                        # Variables
                        navegacionArbolChat = 'MSG_CONFIRMAR_PETICIONABIERTA'
                        descripcionChat = arbolPeticionAbierta
                        
                        # Enviar mensaje solicitando confirmar si tiene caso abierto
                        sendMessage(whatsappNum, arbolPeticionAbierta, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_motivo_tramite = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, motivoTramite, descripcionChat, lastrowid))
                        
                    else:
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_MOTIVOAGENDAMIENTO'
                        descripcionChat = arbolNoEntiendo
                        
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                        
                # todo: Arbol - Confirmar si tiene peticion abierta
                elif resultNavegacionArbol == 'MSG_CONFIRMAR_PETICIONABIERTA' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    if Body.isnumeric() and (int(Body) == 1):
                        # Si la respuesta es 1 o mejor dicho Si                        
                        # Pasar valores a variables globales
                        peticionAbierta = "Si"
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_NUMEROCASO'
                        descripcionChat = arbolNumeroCaso
                        
                        # Enviar mensaje solicitando número de caso
                        sendMessage(whatsappNum, arbolNumeroCaso, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_peticion_abierta = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, peticionAbierta, descripcionChat, lastrowid))
                    
                    elif Body.isnumeric() and (int(Body) == 2):
                        # Si la respuesta es 2 o mejor dicho No
                        # Pasar valores a variables globales
                        peticionAbierta = "No"
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_ADJUNTARDOCUMENTO'
                        descripcionChat = arbolAdjuntarDocumento
                        
                        # Enviar mensaje solicitando adjuntar documento
                        sendMessage(whatsappNum, arbolAdjuntarDocumento, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_peticion_abierta = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, peticionAbierta, descripcionChat, lastrowid))
                        
                        
                    else:
                        # Variables
                        navegacionArbolChat = 'MSG_CONFIRMAR_PETICIONABIERTA'
                        descripcionChat = arbolNoEntiendo
                        
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                        
                # todo: Arbol - Solicitar numero de caso
                elif resultNavegacionArbol == 'MSG_SOLICITA_NUMEROCASO' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    if Body.isnumeric() and (int(Body)):
                        # Si se obtiene un número de caso
                        # Pasar valores a variables globales
                        numeroCaso = Body
                        
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_ADJUNTARDOCUMENTO'
                        descripcionChat = arbolAdjuntarDocumento
                        
                        # Enviar mensaje solicitando adjuntar documento
                        sendMessage(whatsappNum, arbolAdjuntarDocumento, lastrowid)
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_numero_caso = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, numeroCaso, descripcionChat, lastrowid))
                        
                    else:
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_NUMEROCASO'
                        descripcionChat = arbolNoEntiendo
                        
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
            
                # todo: Arbol - Solicitar adjuntar documento
                elif resultNavegacionArbol == 'MSG_SOLICITA_ADJUNTARDOCUMENTO' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    # Verificar la hora actual
                    current_time = datetime.now().time()
                    office_start_time = datetime.strptime("06:00", "%H:%M").time()
                    office_end_time = datetime.strptime("18:00", "%H:%M").time()
                        
                    if Body.isnumeric() and (int(Body) == 1):
                        # Es decir no adjunto documento
                        # Pasar valores a variables globales
                        adjuntoDocumento = "No"

                        if office_start_time <= current_time <= office_end_time:
                            # ? Si estamos dentro de las 06:00 y 18:00
                            # Variables
                            navegacionArbolChat = 'MSG_SOLICITA_OPCIONESAGENDAMIENTO'
                            descripcionChat = arbolOpcionesAgendamiento
                            
                            # Enviar mensaje solicitando opciones de agendamiento
                            sendMessage(whatsappNum, arbolOpcionesAgendamiento, lastrowid)
                            
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_adjuntos = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (navegacionArbolChat, adjuntoDocumento, descripcionChat, lastrowid))
                        else:
                            # ? Si estamos fuera de las 06:00 y 18:00
                            # Variables
                            navegacionArbolChat = 'MSG_SOLICITA_OPCIONAGENDAMIENTO'
                            descripcionChat = arbolOpcionAgendamiento
                            
                            # Enviar mensaje solicitando opción de agendamiento
                            sendMessage(whatsappNum, arbolOpcionAgendamiento, lastrowid)
                            
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_adjuntos = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (navegacionArbolChat, adjuntoDocumento, descripcionChat, lastrowid))
                        
                    elif 'file' in request.files:
                        # Validar el archivo adjunto
                        file = request.files['file']
                        extFile = str(file.filename).split(".")[-1]
                        if extFile in ['pdf', 'xls', 'jpg', 'png', 'doc'] and file.content_length <= 5 * 1024 * 1024:  # 5 MB
                            # Obtenemos la url del archivo
                            # Pasar valores a variables globales
                            adjuntoDocumento = "Si"
                            rutaArchivoAdjunto = Body
                            
                            # Enviar mensaje informando que se adjunto el documento
                            sendMessage(whatsappNum, arbolConfirmarAdjunto, lastrowid)
                            
                            if office_start_time <= current_time <= office_end_time:
                                # ? Si estamos dentro de las 06:00 y 18:00
                                # Variables
                                navegacionArbolChat = 'MSG_SOLICITA_OPCIONESAGENDAMIENTO'
                                descripcionChat = arbolOpcionesAgendamiento
                                
                                # Enviar mensaje solicitando opciones de agendamiento
                                sendMessage(whatsappNum, arbolOpcionesAgendamiento, lastrowid)
                                
                                sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_adjuntos = %s, cht_ruta_archivo_adjunto = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                cursor.execute(sql, (navegacionArbolChat, adjuntoDocumento, rutaArchivoAdjunto, descripcionChat, lastrowid))
                            else:
                                # ? Si estamos fuera de las 06:00 y 18:00
                                # Variables
                                navegacionArbolChat = 'MSG_SOLICITA_OPCIONAGENDAMIENTO'
                                descripcionChat = arbolOpcionAgendamiento
                                
                                # Enviar mensaje solicitando opción de agendamiento
                                sendMessage(whatsappNum, arbolOpcionAgendamiento, lastrowid)
                                
                                sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                            
                        else:
                            # Variables
                            navegacionArbolChat = 'MSG_SOLICITA_ADJUNTARDOCUMENTO'
                            descripcionChat = arbolAdjuntoNoValido
                            
                            sendMessage(whatsappNum, arbolAdjuntoNoValido, lastrowid)
                            
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                    else:
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_ADJUNTARDOCUMENTO'
                        descripcionChat = arbolNoEntiendo
                        
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                        
                # todo: Arbol - Solicitar opciones de agendamiento
                elif resultNavegacionArbol == 'MSG_SOLICITA_OPCIONESAGENDAMIENTO' or resultNavegacionArbol == 'MSG_SOLICITA_OPCIONAGENDAMIENTO' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    
                        # ? Consumir API video atencion etb / Subgrupos - Anna
                        # Variables
                        result = '' 
                                          
                        # Preparar la URL y los headers
                        url = os.getenv('URL_API_SOUL_ETB')+'/v1/public/groups/'+str(idGrupoSeleccionado)+'/groups'
                        print("url: ", url)
                        headers = {
                            "Content-Type": "application/json"
                        }
                        
                        while True:
                            # Enviar la solicitud GET a la API
                            try:
                                responseApiSubGrupos = requests.get(url, headers=headers)  # Realiza la solicitud GET

                                # Verificar si la respuesta es exitosa (status_code 200)
                                if responseApiSubGrupos.status_code == 200:
                                    data = responseApiSubGrupos.json()  # Obtener los datos de la respuesta
                                    result = data

                                    # Si la respuesta es válida, procesamos los datos
                                    print('result Api SUBGRUPOS ===> ', result)

                                    # Verificar si la clave 'groups' está presente en la respuesta y contiene datos
                                    if 'groups' in result and isinstance(result['groups'], list) and len(result['groups']) > 0:
                                        # Almacenar los grupos disponibles
                                        subGruposDisponibles = {
                                            indice + 1: grupo
                                            for indice, grupo in enumerate(result['groups'])  # Acceder a la lista en 'groups'
                                        }
                                        print('subGruposDisponibles ====> ',subGruposDisponibles)

                                        # Generar el mensaje con las opciones enumeradas
                                        listarSubGruposDisponibles = "\n".join([
                                            f"{indice}. {grupo['name']}"  # Mostrar el nombre del grupo
                                            for indice, grupo in subGruposDisponibles.items()
                                        ])
                                        
                                        # Generar las opciones para mostrar al usuario
                                        mensajeSubGruposDisponibles = f"📝 <strong>Por favor, elija un subgrupo:</strong>\n{listarSubGruposDisponibles}"
                                        
                                        # Pasar valores a variables globales
                                        arbolSubGruposDisponibles = mensajeSubGruposDisponibles
                                        navegacionArbolChat = 'MSG_TIPO_SOLICITUD'
                                        descripcionChat = arbolSubGruposDisponibles
                            
                                        # ? Escenario tipo agendamiento inmediato
                                        if Body.isnumeric() and (int(Body) == 1):
                                            # Si la respuesta es 1 o mejor dicho Agendamiento inmediato
                                            # Pasar valores a variables globales
                                            idTipoAgendamiento = '1'
                                            tipoAgendamiento = 'Inmediato'
                                            
                                            # Variables
                                            navegacionArbolChat = 'MSG_SOLICITA_SUBGRUPOAGENDAMIENTO'
                                            descripcionChat = arbolSubGruposDisponibles
                                            
                                            # Enviar mensaje solicitando subgrupo de agendamiento
                                            sendMessage(whatsappNum, arbolSubGruposDisponibles, lastrowid)
                                            
                                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_id_tipo_agendamiento = %s, cht_tipo_agendamiento = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                            cursor.execute(sql, (navegacionArbolChat, idTipoAgendamiento, tipoAgendamiento, descripcionChat, lastrowid))
                                            
                                        # ? Escenario tipo agendamiento programado
                                        elif Body.isnumeric() and (int(Body) == 2):
                                            # Si la respuesta es 2 o mejor dicho Agendamiento programado
                                            # Pasar valores a variables globales
                                            idTipoAgendamiento = '2'
                                            tipoAgendamiento = 'Programado'
                                            
                                            # Variables
                                            navegacionArbolChat = 'MSG_SOLICITA_SUBGRUPOAGENDAMIENTO'
                                            descripcionChat = arbolSubGruposDisponibles
                                            
                                            # Enviar mensaje solicitando subgrupo de agendamiento
                                            sendMessage(whatsappNum, arbolSubGruposDisponibles, lastrowid)
                                            
                                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_id_tipo_agendamiento = %s, cht_tipo_agendamiento = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                            cursor.execute(sql, (navegacionArbolChat, idTipoAgendamiento, tipoAgendamiento, descripcionChat, lastrowid))
                                            
                                        else:
                                            # Variables
                                            navegacionArbolChat = 'MSG_SOLICITA_OPCIONESAGENDAMIENTO'
                                            descripcionChat = arbolNoEntiendo
                                            
                                            sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                                            
                                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                            cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                        
                                        
                                        break  # Salir del bucle si la respuesta es exitosa
                                
                                    else:
                                        # Si la respuesta es 200, pero no encontramos groups en el json que nos entrega la api
                                        print(f"Error en respuesta de API. No se obtuvieron subgrupos!!!")
                                        result = False
                                        

                                else:
                                    # Si la respuesta no es 200, mostramos el error y enviamos el mensaje de error
                                    print(f"Error en respuesta de API. Código de estado: {responseApiSubGrupos.status_code}")
                                    result = False

                            except requests.exceptions.RequestException as e:
                                # Si ocurre una excepción, también manejamos el error
                                print(f"Error en python/ChatWebHook.py → responseApiSubGrupos: {str(e)}")
                                result = False

                            print('Result en subgrupos ==========> ',result)
                            # Lógica para manejar errores: Enviar mensaje al usuario
                            if result is False:
                                navegacionArbolChat = 'MSG_SOLICITA_OPCIONESAGENDAMIENTO'
                                descripcionChat = arbolErrorAPI
                                
                                # Enviar mensaje de error al usuario
                                sendMessage(whatsappNum, arbolErrorAPI, lastrowid)
                                
                                # Actualizar la base de datos con el estado de error
                                sql = f"""
                                    UPDATE {app.config['DB_NAME']}.tbl_chat 
                                    SET cht_estado_chat = %s, 
                                        cht_navegacion_arbol = %s, 
                                        cht_descripcion = %s 
                                    WHERE cht_id = %s;
                                """
                                cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))

                            # Esperar 1.5 minutos antes de volver a intentar
                            time.sleep(90)
                    
                # todo: Arbol - Solicitar subgrupo de agendamiento
                elif resultNavegacionArbol == 'MSG_SOLICITA_SUBGRUPOAGENDAMIENTO' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    # Validamos que el valor de body sea un numero
                    if Body.isnumeric() and (int(Body)):
                        opcionSubGrupoSeleccionado = int(Body)  # Convertimos el input a entero
                        print('opcionSubGrupoSeleccionado ====> ',opcionSubGrupoSeleccionado)
                        # Buscamos el subgrupo seleccionado en el diccionario
                        subGrupo = subGruposDisponibles.get(opcionSubGrupoSeleccionado, None)
                        print('subGrupo ===========> ',subGrupo)
                        if subGrupo:
                            # Variables                        
                            # Pasar valores a variables globales
                            idSubGrupoSeleccionado = subGrupo['id']
                            nombreSubGrupoSeleccionado = subGrupo['name']
                            result = ''
                                
                            # ? Consumir API video atencion etb / Agendas Disponibles - Ana
                            
                            # Preparar la URL y los headers
                            url = os.getenv('URL_API_VIDEOATENCION_ETB')+'/chatBot/availableSchedules/'+str(idSubGrupoSeleccionado)
                            print("url: ", url)
                            headers = {
                                "Content-Type": "application/json"
                            }
                            
                            while True:
                                # Enviar la solicitud GET a la API
                                try:
                                    responseApiAvailableSchedules = requests.get(url, headers=headers)  # Realiza la solicitud GET

                                    # Verificar si la respuesta es exitosa (status_code 200)
                                    if responseApiAvailableSchedules.status_code == 200:
                                        data = responseApiAvailableSchedules.json()  # Obtener los datos de la respuesta
                                        result = data
                                        
                                        # Verificar si hay agendas disponibles
                                        if isinstance(result, list) and len(result) > 0:

                                            # Si la respuesta es válida, procesamos los datos
                                            print('result Api AGENDAS DISPONIBLES ===> ', result)

                                            # Almacenar las agendas disponibles
                                            agendasDisponibles = {
                                                indice + 1: agenda
                                                for indice, agenda in enumerate(result)  # result es la respuesta de la API
                                            }

                                            # Generar el mensaje con las opciones enumeradas
                                            listarAgendasDisponibles = "\n".join([
                                                f"{indice}. {agenda['advisor_name']} - {agenda['scheduled_date']}"
                                                for indice, agenda in agendasDisponibles.items()
                                            ])
                                            # Generar las opciones para mostrar al usuario
                                            mensajeAgendasDisponibles = f"📝 <strong>Por favor, elija una agenda:</strong>\n{listarAgendasDisponibles}"

                                            # Pasar valores a variables globales
                                            arbolAgendasDisponibles = mensajeAgendasDisponibles

                                            # Lógica para tipo de agendamiento
                                            if tipoAgendamiento == 'Inmediato':
                                                navegacionArbolChat = 'MSG_SOLICITA_AGENDAMIENTOINMEDIATO'
                                                descripcionChat = arbolAgendasDisponibles

                                                print('============Vamos por agendamiento inmediato============')
                                                # Obtener y asignar el primer registro de agendas disponibles
                                                if agendasDisponibles:  # Verificar si la lista no está vacía
                                                    primer_agenda = agendasDisponibles[1]
                                                    print('Esta es la primer agenda --- Inmediata ====> ',primer_agenda)
                                                    idEspecialistaSeleccionado = primer_agenda['advisor_id']
                                                    especialistaSeleccionado = primer_agenda['advisor_name']
                                                    fechaHoraSeleccionada = primer_agenda['scheduled_date']

                                                    # ? Consumir API video atencion etb / Tomar la agenda seleccionada - Anna
                                
                                                    # Preparar la URL y los headers
                                                    url = os.getenv('URL_API_VIDEOATENCION_ETB')+'/Room/saveRoomChatBot'
                                                    print("url: ", url)
                                                    headers = {
                                                        "Content-Type": "application/json"
                                                    }
                                                    
                                                    # Obtener fecha y hora actual
                                                    fechaHoraSeleccionada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                    print('Fecha y hora actual para el post ===> ',fechaHoraSeleccionada)
                                                    
                                                    # Datos a enviar
                                                    data = {
                                                        'client_identification': numeroDocumento,
                                                        'client_phone': numeroContacto,
                                                        'client_email': correoContacto,
                                                        'type_id': idTipoAgendamiento,
                                                        'scheduled_date': fechaHoraSeleccionada,
                                                        'id_group': idGrupoSeleccionado,
                                                        'id_skill': idSubGrupoSeleccionado,
                                                        'id_file': lastrowid
                                                    }
                                                    print("Data =========>" ,data)
                                                    
                                                    # Intentar la solicitud indefinidamente hasta obtener una respuesta 200 o 409
                                                    success = False  # Variable para saber si la solicitud fue exitosa

                                                    while not success:
                                                        try:
                                                            responseApiSaveRoom = requests.post(url, headers=headers, json=data)
                                                            
                                                            print('Result responseApiSaveRoom ====> ',responseApiSaveRoom)
                                                            
                                                            # ? Cuando se crea una video llamada
                                                            if responseApiSaveRoom.status_code == 200:
                                                                print('Agendar, tenemos respuesta 200')
                                                                # Si la solicitud es exitosa (status 200)
                                                                # Variables
                                                                data = responseApiSaveRoom.json()
                                                                resultNuevoAgendamiento = data.get('original', {})
                                                                print('Que tenemos de respuesta 200 Agendada ===> ',resultNuevoAgendamiento)
                                                                linkSala = resultNuevoAgendamiento.get('link', '')
                                                                print('linkSala ===> ',linkSala)
                                                                estadoGestion = "Cerrado"
                                                                navegacionArbolChat = 'MSG_FIN'

                                                                # Crear el mensaje para WhatsApp con la información recibida
                                                                arbolAgendamientoExitoso = (
                                                                    f"✅ <strong>¡Agendamiento Inmediato generado con éxito!</strong>\n\n"
                                                                    f"📝 <strong>Trámite:</strong> {nombreGrupoSeleccionado}\n"
                                                                    f"🔢 <strong>NIT:</strong> {numeroNIT}\n"
                                                                    f"🏢 <strong>Razón social:</strong> {razonSocial}\n"
                                                                    f"👤 <strong>Nombres y Apellidos:</strong> {nombreContacto}\n"
                                                                    f"🆔 <strong>Documento:</strong> {numeroDocumento}\n"
                                                                    f"📞 <strong>Contacto:</strong> {numeroContacto}\n"
                                                                    f"📧 <strong>Correo:</strong> {correoContacto}\n\n"
                                                                    f"📅 <strong>Detalles del agendamiento:</strong>\n"
                                                                    f"🕒 <strong>Fecha y Hora:</strong> {fechaHoraSeleccionada}\n"
                                                                    f"👨‍⚕️ <strong>Especialista:</strong> {especialistaSeleccionado}\n"
                                                                    f"🔗 <strong>Enlace a la sala:</strong> {linkSala if linkSala else 'No hemos podido proporcinar el link del agendamiento.'}\n\n"
                                                                    f"📌 <i>Recuerde copiar el enlace y/o abrirlo en una nueva pestaña (Ctrl + click).</i>"
                                                                )
                                                                descripcionChat = arbolAgendamientoExitoso
                                                                
                                                                print('Mensaje arbolAgendamientoExitoso ====> ',arbolAgendamientoExitoso)

                                                                # Enviar mensaje informando que el agendamiento fue exitoso
                                                                sendMessage(whatsappNum, arbolAgendamientoExitoso, lastrowid)
                                                                sendMessage(whatsappNum, arbolFin, lastrowid)

                                                                # Actualizar estado de la sala en la base de datos
                                                                sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_id_subgrupo = %s, cht_nombre_subgrupo = %s, cht_id_especialista = %s, cht_nombre_especialista = %s, cht_fecha_hora_agendamiento = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                                                cursor.execute(sql, (navegacionArbolChat, idSubGrupoSeleccionado, nombreSubGrupoSeleccionado, idEspecialistaSeleccionado, especialistaSeleccionado, fechaHoraSeleccionada, descripcionChat, lastrowid))

                                                                # Llamar a la función cerrar chat
                                                                cerrarChat(cursor, lastrowid, estadoGestion, navegacionArbolChat, descripcionChat)

                                                                success = True  # Marcar como exitoso y salir del bucle
                                                            
                                                            # ? Cuando no hay asesores disponibles - manejar error 400
                                                            elif responseApiSaveRoom.status_code == 400:
                                                                print('Agendar, tenemos respuesta 400')
                                                                # Si la respuesta es 400, significa que no hay asesores disponibles
                                                                # Variables
                                                                # Extraer los datos de la respuesta de la API
                                                                data = responseApiSaveRoom.json()
                                                                resultEnColamiento = data.get('error', {})
                                                                print('Que tenemos de respuesta 400 Agendada ===> ',resultEnColamiento)
                                                                # message = resultEnColamiento.get('message', 'No hay asesores disponibles por el momento.')                                            
                                                                navegacionArbolChat = 'MSG_SINESPECIALISTAS'                                            
                                                                # Personalizar el mensaje de error para el 400
                                                                descripcionChat = arbolEspecialistasNoDisponibles
                                                                
                                                                # Enviar mensaje al usuario
                                                                sendMessage(whatsappNum, arbolEspecialistasNoDisponibles, lastrowid)

                                                                # Actualizar estado en la base de datos
                                                                sql = f"""
                                                                    UPDATE {app.config['DB_NAME']}.tbl_chat 
                                                                    SET cht_navegacion_arbol = %s, 
                                                                        cht_descripcion = %s 
                                                                    WHERE cht_id = %s;
                                                                """
                                                                cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))

                                                                # Esperar 1.5 minutos antes de intentar nuevamente
                                                                time.sleep(90) 

                                                            # ? Cuando se cuenta con una video llamada agendada - se confirma agendamiento
                                                            elif responseApiSaveRoom.status_code == 409:
                                                                print('Agendar, tenemos respuesta 409')
                                                                # Si la respuesta es 409, significa que ya hay una sala asignada o un error similar
                                                                # Variables
                                                                data = responseApiSaveRoom.json()
                                                                # Validar y extraer los datos necesarios del error 409
                                                                resultConfirmarAgendamiento = data.get('error', {})
                                                                print('Que tenemos de respuesta 409 Agendada ===> ',resultConfirmarAgendamiento)
                                                                message = resultConfirmarAgendamiento.get('message', 'Error desconocido.')
                                                                sala = resultConfirmarAgendamiento.get('sala', '')
                                                                estadoGestion = "Cerrado"
                                                                navegacionArbolChat = 'MSG_FIN'
                                                                descripcionChat = message
                                                                
                                                                # Personalizar el mensaje de error para el 409
                                                                arbolConfirmarSala = (
                                                                    f"⚠️ <strong>Confirmar Sala previa asignada</strong>\n"
                                                                    f"🛑 {message}\n"
                                                                    f"🔗 {sala if sala else 'No se proporcionó enlace para la sala.'}\n\n"
                                                                    f"📌 <i>Copie el enlace y/o abra en una nueva pestaña (Ctrl + click).</i>"
                                                                )

                                                                # Enviar mensaje de error y confirmar la sala
                                                                sendMessage(whatsappNum, arbolConfirmarSala, lastrowid)
                                                                sendMessage(whatsappNum, arbolFin, lastrowid)

                                                                # Actualizar estado de la sala en la base de datos
                                                                sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_id_subgrupo = %s, cht_nombre_subgrupo = %s, cht_id_especialista = %s, cht_nombre_especialista = %s, cht_fecha_hora_agendamiento = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                                                cursor.execute(sql, (navegacionArbolChat, idSubGrupoSeleccionado, nombreSubGrupoSeleccionado, idEspecialistaSeleccionado, especialistaSeleccionado, fechaHoraSeleccionada, descripcionChat, lastrowid))

                                                                # Llamar a la función cerrar chat
                                                                cerrarChat(cursor, lastrowid, estadoGestion, navegacionArbolChat, descripcionChat)

                                                                # Salir del bucle
                                                                success = True


                                                            else:
                                                                print('Agendar, tenemos respuesta else... error o algo no esta mapeado...!!!!!!!!!!!')
                                                                # ? Si no obtenemos alguna de las respuestas anteriores entramos en bucle cada 1.5 minutos
                                                                # En caso de otro código de estado, simplemente espera 1.5 minutos y vuelve a intentar
                                                                print(f"Error inesperado: {responseApiSaveRoom.status_code}")
                                                                # Variables
                                                                navegacionArbolChat = 'MSG_ERRORAPI' 
                                                                descripcionChat = arbolErrorAPI
                                                                
                                                                # Enviar mensaje al usuario
                                                                sendMessage(whatsappNum, arbolErrorAPI, lastrowid)

                                                                # Actualizar estado en la base de datos
                                                                sql = f"""
                                                                    UPDATE {app.config['DB_NAME']}.tbl_chat 
                                                                    SET cht_estado_chat = %s, 
                                                                        cht_navegacion_arbol = %s, 
                                                                        cht_descripcion = %s 
                                                                    WHERE cht_id = %s;
                                                                """
                                                                cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))

                                                                # Esperar 1.5 minutos antes de intentar nuevamente
                                                                time.sleep(90)

                                                        except requests.exceptions.RequestException as e:
                                                            # ? Si no obtenemos alguna de las respuestas anteriores entramos en bucle cada 1.5 minutos
                                                            print(f"Error en la solicitud: {str(e)}")# Variables
                                                            navegacionArbolChat = 'MSG_ERRORAPI'    
                                                            descripcionChat = arbolErrorAPI
                                                            
                                                            # Enviar mensaje al usuario
                                                            sendMessage(whatsappNum, arbolErrorAPI, lastrowid)

                                                            # Actualizar estado en la base de datos
                                                            sql = f"""
                                                                UPDATE {app.config['DB_NAME']}.tbl_chat 
                                                                SET cht_estado_chat = %s, 
                                                                    cht_navegacion_arbol = %s, 
                                                                    cht_descripcion = %s 
                                                                WHERE cht_id = %s;
                                                            """
                                                            cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))

                                                            # Esperar 1.5 minutos antes de intentar nuevamente
                                                            time.sleep(90)


                                            elif tipoAgendamiento == 'Programado':
                                                navegacionArbolChat = 'MSG_SOLICITA_AGENDASDISPONIBLES'
                                                descripcionChat = arbolAgendasDisponibles
                                                
                                                # Enviar mensaje solicitando agendas disponibles
                                                sendMessage(whatsappNum, arbolAgendasDisponibles, lastrowid)
                                                
                                                # Actualizar base de datos
                                                sql = f"""
                                                    UPDATE {app.config['DB_NAME']}.tbl_chat 
                                                    SET cht_navegacion_arbol = %s, 
                                                        cht_id_subgrupo = %s, 
                                                        cht_nombre_subgrupo = %s, 
                                                        cht_descripcion = %s 
                                                    WHERE cht_id = %s;
                                                """
                                                cursor.execute(sql, (navegacionArbolChat, idSubGrupoSeleccionado, nombreSubGrupoSeleccionado, descripcionChat, lastrowid))

                                            break  # Salir del bucle si la respuesta es exitosa

                                        else:
                                                                                        
                                            # Si la respuesta es 200, pero no encontramos groups en el json que nos entrega la api
                                            print(f"Error en respuesta de API. No se obtuvieron agendas!!!")
                                            result = False
                                            
                                    else:
                                        # Si la respuesta no es 200, mostramos el error y enviamos el mensaje de error
                                        print(f"Error en respuesta de API. Código de estado: {responseApiAvailableSchedules.status_code}")
                                        result = False

                                except requests.exceptions.RequestException as e:
                                    # Si ocurre una excepción, también manejamos el error
                                    print(f"Error en python/ChatWebHook.py → responseApiAvailableSchedules: {str(e)}")
                                    result = False

                                # Lógica para manejar errores: Enviar mensaje al usuario
                                if result is False:
                                    navegacionArbolChat = 'MSG_SOLICITA_GRUPOAGENDAMIENTO'
                                    descripcionChat = arbolErrorAPI
                                    
                                    # Enviar mensaje de error al usuario
                                    sendMessage(whatsappNum, arbolErrorAPI, lastrowid)
                                    
                                    # Actualizar la base de datos con el estado de error
                                    sql = f"""
                                        UPDATE {app.config['DB_NAME']}.tbl_chat 
                                        SET cht_estado_chat = %s, 
                                            cht_navegacion_arbol = %s, 
                                            cht_descripcion = %s 
                                        WHERE cht_id = %s;
                                    """
                                    cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))

                                # Esperar 1.5 minutos antes de volver a intentar
                                time.sleep(90)  
                        
                        else:
                            # Variables
                            navegacionArbolChat = 'MSG_SOLICITA_GRUPOAGENDAMIENTO'
                            descripcionChat = arbolNoEntiendo
                            
                            sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                            
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))
                    else:
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_GRUPOAGENDAMIENTO'
                        descripcionChat = arbolNoEntiendo
                        
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))
                       
                # todo: Arbol - Solicitar opcion agendas disponibles - tomar agendamiento
                elif resultNavegacionArbol == 'MSG_SOLICITA_AGENDASDISPONIBLES' or resultNavegacionArbol == 'MSG_ALERTA_INACTIVIDAD':
                    # Validamos que el valor de body sea un numero
                    if Body.isnumeric() and (int(Body)):
                        opcionAgendaSeleccionada = int(Body)  # Convertimos el input a entero
    
                        # Buscamos la agenda seleccionada en el diccionario
                        agenda = agendasDisponibles.get(opcionAgendaSeleccionada, None)
                        
                        if agenda:
                            # Variables                        
                            # Pasar valores a variables globales
                            idEspecialistaSeleccionado = agenda['advisor_id']
                            especialistaSeleccionado = agenda['advisor_name']
                            fechaHoraSeleccionada = agenda['scheduled_date']
                            result = ''
                            
                            print("idEspecialistaSeleccionado: ", idEspecialistaSeleccionado)
                            print("especialistaSeleccionado: ", especialistaSeleccionado)
                            print("fechaHoraSeleccionada: ", fechaHoraSeleccionada)
                                
                            # ? Consumir API video atencion etb / Validar disponibilidad de la agenda - Anna
                            
                            # Preparar la URL y los headers
                            url = os.getenv('URL_API_VIDEOATENCION_ETB')+'/chatBot/validateAvailability/'+str(idEspecialistaSeleccionado)+'/'+str(fechaHoraSeleccionada)
                            print("url: ", url)
                            headers = {
                                "Content-Type": "application/json"
                            }

                            # Enviar la solicitud GET a la API
                            try:
                                responseApiValidateAvailability = requests.get(url, headers=headers)  # Realiza la solicitud GET
                                if responseApiValidateAvailability.status_code == 200:
                                    data = responseApiValidateAvailability.json()  # Obtener los datos de la respuesta
                                    result = data
                                else:
                                    result = False
                            except requests.exceptions.RequestException as e:
                                print(f"Error en python/ChatWebHook.py → responseApiValidateAvailability: {str(e)}")
                                result = False
                            
                            # ? Validar respuesta de la API
                            print('result Api AGENDAS DISPONIBLES ===> ', result)
                            
                            # Tomar la agenda seleccionada
                            if result:
                                
                                # ? Consumir API video atencion etb / Tomar la agenda seleccionada - Anna
                                
                                # Preparar la URL y los headers
                                url = os.getenv('URL_API_VIDEOATENCION_ETB')+'/Room/saveRoomChatBot'
                                print("url: ", url)
                                headers = {
                                    "Content-Type": "application/json"
                                }
                                # Datos a enviar
                                data = {
                                    'client_identification': numeroDocumento,
                                    'client_phone': numeroContacto,
                                    'client_email': correoContacto,
                                    'type_id': idTipoAgendamiento,
                                    'scheduled_date': fechaHoraSeleccionada,
                                    'id_group': idGrupoSeleccionado,
                                    'id_skill': idSubGrupoSeleccionado,
                                    'adviser_id': idEspecialistaSeleccionado,
                                    'id_file': lastrowid
                                }
                                print("Data =========>" ,data)
                                
                                # Intentar la solicitud indefinidamente hasta obtener una respuesta 200 o 409
                                success = False  # Variable para saber si la solicitud fue exitosa

                                while not success:
                                    try:
                                        responseApiSaveRoom = requests.post(url, headers=headers, json=data)
                                        
                                        print('Result responseApiSaveRoom ====> ',responseApiSaveRoom)
                                        
                                        # ? Cuando se crea una video llamada
                                        if responseApiSaveRoom.status_code == 200:
                                            print('Agendar, tenemos respuesta 200')
                                            # Si la solicitud es exitosa (status 200)
                                            # Variables
                                            data = responseApiSaveRoom.json()
                                            resultNuevoAgendamiento = data.get('original', {})
                                            print('Que tenemos de respuesta 200 Agendada ===> ',resultNuevoAgendamiento)
                                            linkSala = resultNuevoAgendamiento.get('link', '')
                                            print('linkSala ===> ',linkSala)
                                            estadoGestion = "Cerrado"
                                            navegacionArbolChat = 'MSG_FIN'

                                            # Crear el mensaje para WhatsApp con la información recibida
                                            arbolAgendamientoExitoso = (
                                                f"✅ <strong>¡Agendamiento programado con éxito!</strong>\n\n"
                                                f"📝 <strong>Trámite:</strong> {nombreGrupoSeleccionado}\n"
                                                f"🔢 <strong>NIT:</strong> {numeroNIT}\n"
                                                f"🏢 <strong>Razón social:</strong> {razonSocial}\n"
                                                f"👤 <strong>Nombres y Apellidos:</strong> {nombreContacto}\n"
                                                f"🆔 <strong>Documento:</strong> {numeroDocumento}\n"
                                                f"📞 <strong>Contacto:</strong> {numeroContacto}\n"
                                                f"📧 <strong>Correo:</strong> {correoContacto}\n\n"
                                                f"📅 <strong>Detalles del agendamiento:</strong>\n"
                                                f"🕒 <strong>Fecha y Hora:</strong> {fechaHoraSeleccionada}\n"
                                                f"👨‍⚕️ <strong>Especialista:</strong> {especialistaSeleccionado}\n"
                                                f"🔗 <strong>Enlace a la sala:</strong> {linkSala if linkSala else 'No hemos podido proporcinar el link del agendamiento.'}\n\n"
                                                f"📌 <i>Recuerde copiar el enlace y/o abrirlo en una nueva pestaña (Ctrl + click).</i>"
                                            )
                                            descripcionChat = arbolAgendamientoExitoso
                                            
                                            print('Mensaje arbolAgendamientoExitoso ====> ',arbolAgendamientoExitoso)

                                            # Enviar mensaje informando que el agendamiento fue exitoso
                                            sendMessage(whatsappNum, arbolAgendamientoExitoso, lastrowid)
                                            sendMessage(whatsappNum, arbolFin, lastrowid)

                                            # Actualizar estado de la sala en la base de datos
                                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_id_subgrupo = %s, cht_nombre_subgrupo = %s, cht_id_especialista = %s, cht_nombre_especialista = %s, cht_fecha_hora_agendamiento = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                            cursor.execute(sql, (navegacionArbolChat, idSubGrupoSeleccionado, nombreSubGrupoSeleccionado, idEspecialistaSeleccionado, especialistaSeleccionado, fechaHoraSeleccionada, descripcionChat, lastrowid))

                                            # Llamar a la función cerrar chat
                                            cerrarChat(cursor, lastrowid, estadoGestion, navegacionArbolChat, descripcionChat)

                                            success = True  # Marcar como exitoso y salir del bucle
                                        
                                        # ? Cuando no hay asesores disponibles - manejar error 400
                                        elif responseApiSaveRoom.status_code == 400:
                                            print('Agendar, tenemos respuesta 400')
                                            # Si la respuesta es 400, significa que no hay asesores disponibles
                                            # Variables
                                            # Extraer los datos de la respuesta de la API
                                            data = responseApiSaveRoom.json()
                                            resultEnColamiento = data.get('error', {})
                                            print('Que tenemos de respuesta 400 Agendada ===> ',resultEnColamiento)
                                            # message = resultEnColamiento.get('message', 'No hay asesores disponibles por el momento.')                                            
                                            navegacionArbolChat = 'MSG_SINESPECIALISTAS'                                            
                                            # Personalizar el mensaje de error para el 400
                                            descripcionChat = arbolEspecialistasNoDisponibles
                                            
                                            # Enviar mensaje al usuario
                                            sendMessage(whatsappNum, arbolEspecialistasNoDisponibles, lastrowid)

                                            # Actualizar estado en la base de datos
                                            sql = f"""
                                                UPDATE {app.config['DB_NAME']}.tbl_chat 
                                                SET cht_navegacion_arbol = %s, 
                                                    cht_descripcion = %s 
                                                WHERE cht_id = %s;
                                            """
                                            cursor.execute(sql, (navegacionArbolChat, descripcionChat, lastrowid))

                                            # Esperar 1.5 minutos antes de intentar nuevamente
                                            time.sleep(90) 

                                        # ? Cuando se cuenta con una video llamada agendada - se confirma agendamiento
                                        elif responseApiSaveRoom.status_code == 409:
                                            print('Agendar, tenemos respuesta 409')
                                            # Si la respuesta es 409, significa que ya hay una sala asignada o un error similar
                                            # Variables
                                            data = responseApiSaveRoom.json()
                                            # Validar y extraer los datos necesarios del error 409
                                            resultConfirmarAgendamiento = data.get('error', {})
                                            print('Que tenemos de respuesta 409 Agendada ===> ',resultConfirmarAgendamiento)
                                            message = resultConfirmarAgendamiento.get('message', 'Error desconocido.')
                                            sala = resultConfirmarAgendamiento.get('sala', '')
                                            estadoGestion = "Cerrado"
                                            navegacionArbolChat = 'MSG_FIN'
                                            descripcionChat = message
                                            
                                            # Personalizar el mensaje de error para el 409
                                            arbolConfirmarSala = (
                                                f"⚠️ <strong>Confirmar Sala previa asignada</strong>\n"
                                                f"🛑 {message}\n"
                                                f"🔗 {sala if sala else 'No se proporcionó enlace para la sala.'}\n\n"
                                                f"📌 <i>Copie el enlace y/o abra en una nueva pestaña (Ctrl + click).</i>"
                                            )

                                            # Enviar mensaje de error y confirmar la sala
                                            sendMessage(whatsappNum, arbolConfirmarSala, lastrowid)
                                            sendMessage(whatsappNum, arbolFin, lastrowid)

                                            # Actualizar estado de la sala en la base de datos
                                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_id_subgrupo = %s, cht_nombre_subgrupo = %s, cht_id_especialista = %s, cht_nombre_especialista = %s, cht_fecha_hora_agendamiento = %s, cht_descripcion = %s WHERE cht_id = %s;"
                                            cursor.execute(sql, (navegacionArbolChat, idSubGrupoSeleccionado, nombreSubGrupoSeleccionado, idEspecialistaSeleccionado, especialistaSeleccionado, fechaHoraSeleccionada, descripcionChat, lastrowid))

                                            # Llamar a la función cerrar chat
                                            cerrarChat(cursor, lastrowid, estadoGestion, navegacionArbolChat, descripcionChat)

                                            # Salir del bucle
                                            success = True


                                        else:
                                            print('Agendar, tenemos respuesta else... error o algo no esta mapeado...!!!!!!!!!!!')
                                            # ? Si no obtenemos alguna de las respuestas anteriores entramos en bucle cada 1.5 minutos
                                            # En caso de otro código de estado, simplemente espera 1.5 minutos y vuelve a intentar
                                            print(f"Error inesperado: {responseApiSaveRoom.status_code}")
                                            # Variables
                                            navegacionArbolChat = 'MSG_ERRORAPI' 
                                            descripcionChat = arbolErrorAPI
                                            
                                            # Enviar mensaje al usuario
                                            sendMessage(whatsappNum, arbolErrorAPI, lastrowid)

                                            # Actualizar estado en la base de datos
                                            sql = f"""
                                                UPDATE {app.config['DB_NAME']}.tbl_chat 
                                                SET cht_estado_chat = %s, 
                                                    cht_navegacion_arbol = %s, 
                                                    cht_descripcion = %s 
                                                WHERE cht_id = %s;
                                            """
                                            cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))

                                            # Esperar 1.5 minutos antes de intentar nuevamente
                                            time.sleep(90)

                                    except requests.exceptions.RequestException as e:
                                        # ? Si no obtenemos alguna de las respuestas anteriores entramos en bucle cada 1.5 minutos
                                        print(f"Error en la solicitud: {str(e)}")# Variables
                                        navegacionArbolChat = 'MSG_ERRORAPI'    
                                        descripcionChat = arbolErrorAPI
                                        
                                        # Enviar mensaje al usuario
                                        sendMessage(whatsappNum, arbolErrorAPI, lastrowid)

                                        # Actualizar estado en la base de datos
                                        sql = f"""
                                            UPDATE {app.config['DB_NAME']}.tbl_chat 
                                            SET cht_estado_chat = %s, 
                                                cht_navegacion_arbol = %s, 
                                                cht_descripcion = %s 
                                            WHERE cht_id = %s;
                                        """
                                        cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))

                                        # Esperar 1.5 minutos antes de intentar nuevamente
                                        time.sleep(90)
                                        
                            else:
                                
                                # ? La agenda ya no se encuentra disponible
                                # Variables
                                navegacionArbolChat = 'MSG_SOLICITA_AGENDASDISPONIBLES'
                                descripcionChat = arbolAgendaNoDisponible
                                
                                # Enviar mensaje solicitando agendas no disponibles
                                sendMessage(whatsappNum, arbolAgendaNoDisponible, lastrowid)
                                
                                # Actualizar base de datos
                                sql = f"""
                                    UPDATE {app.config['DB_NAME']}.tbl_chat 
                                    SET cht_navegacion_arbol = %s, 
                                        cht_id_grupo = %s, 
                                        cht_nombre_grupo = %s, 
                                        cht_descripcion = %s 
                                    WHERE cht_id = %s;
                                """
                                cursor.execute(sql, (navegacionArbolChat, idGrupoSeleccionado, nombreGrupoSeleccionado, descripcionChat, lastrowid))
                                        
                                # ? Consumir API video atencion etb / Agendas Disponibles - Anna
                                
                                # Preparar la URL y los headers
                                url = os.getenv('URL_API_VIDEOATENCION_ETB')+'/chatBot/availableSchedules/'+str(idGrupoSeleccionado)
                                print("url: ", url)
                                headers = {
                                    "Content-Type": "application/json"
                                }
                                
                                while True:
                                    # Enviar la solicitud GET a la API
                                    try:
                                        responseApiAvailableSchedules = requests.get(url, headers=headers)  # Realiza la solicitud GET

                                        # Verificar si la respuesta es exitosa (status_code 200)
                                        if responseApiAvailableSchedules.status_code == 200:
                                            data = responseApiAvailableSchedules.json()  # Obtener los datos de la respuesta
                                            result = data

                                            # Si la respuesta es válida, procesamos los datos
                                            print('result Api AGENDAS DISPONIBLES ===> ', result)

                                            # Almacenar las agendas disponibles
                                            agendasDisponibles = {
                                                indice + 1: agenda
                                                for indice, agenda in enumerate(result)  # result es la respuesta de la API
                                            }

                                            # Generar el mensaje con las opciones enumeradas
                                            listarAgendasDisponibles = "\n".join([
                                                f"{indice}. {agenda['advisor_name']} - {agenda['scheduled_date']}"
                                                for indice, agenda in agendasDisponibles.items()
                                            ])
                                            # Generar las opciones para mostrar al usuario
                                            mensajeAgendasDisponibles = f"📝 <strong>Por favor, elija una agenda:</strong>\n{listarAgendasDisponibles}"

                                            # Pasar valores a variables globales
                                            arbolAgendasDisponibles = mensajeAgendasDisponibles

                                            # Lógica para tipo de agendamiento
                                            if tipoAgendamiento == 'Inmediato':
                                                navegacionArbolChat = 'MSG_SOLICITA_AGENDASDISPONIBLES'
                                                descripcionChat = arbolAgendasDisponibles
                                                
                                                # Enviar mensaje solicitando agendas disponibles
                                                sendMessage(whatsappNum, arbolAgendasDisponibles, lastrowid)
                                                
                                                # Actualizar base de datos
                                                sql = f"""
                                                    UPDATE {app.config['DB_NAME']}.tbl_chat 
                                                    SET cht_navegacion_arbol = %s, 
                                                        cht_id_grupo = %s, 
                                                        cht_nombre_grupo = %s, 
                                                        cht_descripcion = %s 
                                                    WHERE cht_id = %s;
                                                """
                                                cursor.execute(sql, (navegacionArbolChat, idGrupoSeleccionado, nombreGrupoSeleccionado, descripcionChat, lastrowid))

                                            elif tipoAgendamiento == 'Programado':
                                                navegacionArbolChat = 'MSG_SOLICITA_AGENDASDISPONIBLES'
                                                descripcionChat = arbolAgendasDisponibles
                                                
                                                # Enviar mensaje solicitando agendas disponibles
                                                sendMessage(whatsappNum, arbolAgendasDisponibles, lastrowid)
                                                
                                                # Actualizar base de datos
                                                sql = f"""
                                                    UPDATE {app.config['DB_NAME']}.tbl_chat 
                                                    SET cht_navegacion_arbol = %s, 
                                                        cht_id_grupo = %s, 
                                                        cht_nombre_grupo = %s, 
                                                        cht_descripcion = %s 
                                                    WHERE cht_id = %s;
                                                """
                                                cursor.execute(sql, (navegacionArbolChat, idGrupoSeleccionado, nombreGrupoSeleccionado, descripcionChat, lastrowid))

                                            break  # Salir del bucle si la respuesta es exitosa

                                        else:
                                            # Si la respuesta no es 200, mostramos el error y enviamos el mensaje de error
                                            print(f"Error en respuesta de API. Código de estado: {responseApiAvailableSchedules.status_code}")
                                            result = False

                                    except requests.exceptions.RequestException as e:
                                        # Si ocurre una excepción, también manejamos el error
                                        print(f"Error en python/ChatWebHook.py → responseApiAvailableSchedules: {str(e)}")
                                        result = False

                                    # Lógica para manejar errores: Enviar mensaje al usuario
                                    if result is False:
                                        navegacionArbolChat = 'MSG_SOLICITA_SUBGRUPOAGENDAMIENTO'
                                        descripcionChat = arbolErrorAPI
                                        
                                        # Enviar mensaje de error al usuario
                                        sendMessage(whatsappNum, arbolErrorAPI, lastrowid)
                                        
                                        # Actualizar la base de datos con el estado de error
                                        sql = f"""
                                            UPDATE {app.config['DB_NAME']}.tbl_chat 
                                            SET cht_estado_chat = %s, 
                                                cht_navegacion_arbol = %s, 
                                                cht_descripcion = %s 
                                            WHERE cht_id = %s;
                                        """
                                        cursor.execute(sql, (estadoChat, navegacionArbolChat, descripcionChat, lastrowid))

                                    # Esperar 1.5 minutos antes de volver a intentar
                                    time.sleep(90)  
                                
                        else:
                            # Variables
                            navegacionArbolChat = 'MSG_SOLICITA_SUBGRUPOAGENDAMIENTO'
                            descripcionChat = arbolNoEntiendo
                            
                            sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                            
                            sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                            cursor.execute(sql, (navegacionArbolChat, lastrowid))
                    else:
                        # Variables
                        navegacionArbolChat = 'MSG_SOLICITA_SUBGRUPOAGENDAMIENTO'
                        descripcionChat = arbolNoEntiendo
                        
                        sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                        
                        sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                        cursor.execute(sql, (navegacionArbolChat, lastrowid))                  
                     
                else:
                    # todo: Enviamos mensaje no entiendo ya que no esta considerado en el arbol de atencion
                    
                    # Variables
                    navegacionArbolChat = 'MSG_SALUDO'
                    descripcionChat = arbolNoEntiendo
                    
                    sendMessage(whatsappNum, arbolNoEntiendo, lastrowid)
                    
                    sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = %s, cht_descripcion = %s WHERE cht_id = %s;"
                    cursor.execute(sql, (navegacionArbolChat, lastrowid))
                    
  
    except Exception as e:
        app.logger.info(f"ERROR: {e}")
    
    finally:
        connectionDB.close


# ! MAnnaGE TREE
# Administrar el arbol de atencion y asignacion de chats.
def mAnnageTree(idChat, mensaje):
    # Mensaje que se enviará al usuario si aún está en la cola de atención
    waitingMessage = 'No hay asesores disponibles para atender su solicitud '

    # Fecha y hora actual
    print("mAnnageTree idChat es : ", idChat)
    print("mAnnageTree mensaje es : ", mensaje)
    formatoHora = pytz.timezone(app.config['ZONA_HORARIA'])
    current_date = datetime.now(formatoHora).strftime("%Y-%m-%d %H:%M:%S")
    # current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lastrowid = 0
    # Inicializamos la variable comprobar como False
    comprobar = False
    # Establecemos la conexión a la base de datos
    connectionDB = connection()
    # Habilitamos la opción de autocommit para que los cambios se guarden automáticamente
    connectionDB.autocommit(True)
	# Creamos un cursor para ejecutar consultas en la base de datos
    with connectionDB.cursor() as cursor:
        # Consultamos el último registro de la tabla tbl_chat para el usuario especificado en idChat
        sql = f"SELECT cht_id, cht_navegacion_arbol, cht_estado_gestion, cht_descripcion FROM {app.config['DB_NAME']}.tbl_chat WHERE cht_id_chat_web = %s AND cht_tipo_estado = %s ORDER BY cht_id DESC LIMIT 1;"
        #app.logger.info(sql)
        cursor.execute(sql, (idChat, 'Activo'))
        rows = cursor.fetchall()
		# Si no hay ningún registro para el usuario, insertamos un nuevo registro en la tabla
        print("rows para la tabla tbl_chat: ", rows)
        if len(rows) == 0:

            sql = f"INSERT INTO  {app.config['DB_NAME']}.tbl_chat (cht_id_chat_web, cht_tipo_gestion, cht_estado_chat, cht_navegacion_arbol, cht_estado_gestion, cht_descripcion, cht_tipo_estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            # sql = f"INSERT INTO  {app.config['DB_NAME']}.tbl_chat (cht_id_chat_web, GES_CTIPO, cht_navegacion_arbol, GES_TIPO_CAnnaL, GES_CHORA_INICIO_GESTION, cht_tipo_estado) VALUES ('Abierto', '{str(idChat)}', 'inbound', 'MSG_SALUDO', 'WEB', '{str(current_date)}', 'Activo')"
            #app.logger.info(sql)
            cursor.execute(sql, (idChat, 'Inbound', 'Recibido', 'MSG_SALUDO', 'Abierto', mensaje, 'Activo'))
            lastrowid = cursor.lastrowid
            comprobar = True
			
        else:
            # todo: Si tenemos un chat abierto
            if rows[0]["cht_estado_gestion"] == "Abierto":
                    #sendMessage(idChat['sender']['id'], waitingMessage, lastrowid)
                    sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_descripcion = %s WHERE cht_id = %s;"
                    cursor.execute(sql, ('Enviado', mensaje, lastrowid))
                    
                    # Variables
                    lastrowid = rows[0]["cht_id"]
                    comprobar = True
            
            else:
                # todo: Si no tenemos un chat abierto. creamos el registro
                sql = f"INSERT INTO  {app.config['DB_NAME']}.tbl_chat (cht_id_chat_web, cht_tipo_gestion, cht_estado_chat, cht_navegacion_arbol, cht_estado_gestion, cht_descripcion, cht_tipo_estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                
                cursor.execute(sql, (idChat, 'Inbound', 'Recibido', 'MSG_SALUDO', 'Abierto', mensaje, 'Activo'))
                lastrowid = cursor.lastrowid
                comprobar = True
                
            # # Si hay un registro para el usuario, verificamos el valor del campo cht_navegacion_arbol
            # #Administrar arbol de atencion
            # if rows[0]["cht_navegacion_arbol"] == "MSG_FIN":
            #     # Si el valor es "MSG_FIN", verificamos el valor del campo cht_estado_gestion
            #     if rows[0]["cht_estado_gestion"] == "Abierto":
            #         # Si el valor es "Abierto", enviamos un mensaje al usuario y guardamos el ID del registro
            #         lastrowid = rows[0]["cht_id"]
            #         #comprobar = True
            #         #sendMessage(idChat['sender']['id'], waitingMessage, lastrowid)
            #         #sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_navegacion_arbol = 'MSG_PASO_ASESOR' WHERE (cht_id = '{str(lastrowid)}');"
            #         print("Probando cuando pasa por aca xd")
            #         print(lastrowid)
            #         print(rows[0]["cht_navegacion_arbol"])
            #         print(comprobar)
            #         cursor.execute(sql)
            #         return
            #     elif rows[0]["cht_estado_gestion"] == "Cerrado":
            #         # Si el valor es "Cerrado", insertamos un nuevo registro en la tabla y establecemos la variable comprobar como True

            #         sql = f"INSERT INTO  {app.config['DB_NAME']}.tbl_chat (cht_id_chat_web, cht_tipo_gestion, cht_estado_chat, cht_navegacion_arbol, cht_estado_gestion, cht_descripcion, cht_tipo_estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    
            #         # sql = f"INSERT INTO {app.config['DB_NAME']}.tbl_chat (cht_estado_gestion, cht_id_chat_web, cht_navegacion_arbol, GES_CHORA_INICIO_GESTION, cht_tipo_estado,GES_TIPO_CAnnaL) VALUES ('Abierto', '{str(idChat)}', 'MSG_SALUDO', '{str(current_date)}', 'Activo','WEB');"
            #         #app.logger.info(sql)
            #         cursor.execute(sql, (idChat, 'Inbound', 'Recibido', 'MSG_SALUDO', 'Abierto', 'Hemos recibido y abierto este chat.', 'Activo'))
            #         lastrowid = cursor.lastrowid
            #         comprobar = True
            #     elif rows[0]["cht_estado_gestion"] == "ATTENDING":
            #         # Si el valor es "ATTENDING", guardamos el ID del registro
            #         lastrowid = rows[0]["cht_id"]
            #         sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET GES_NAFK = 0 WHERE (cht_id = '{str(lastrowid)}');"
            #         cursor.execute(sql)
            #     elif rows[0]["cht_estado_gestion"] == "TRANSFERRED":
            #         # Si el valor es "TRANSFERRED", guardamos el ID del registro
            #         lastrowid = rows[0]["cht_id"]
            #         sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET GES_NAFK = 0 WHERE (cht_id = '{str(lastrowid)}');"
            #         cursor.execute(sql)

            #     else:
            #         # Si el valor del campo cht_navegacion_arbol es diferente de "MSG_FIN", establecemos la variable comprobar como True y guardamos el ID del registro
            #         comprobar = True
            #         lastrowid = rows[0]["cht_id"]

            # #Insertar la hora del mensaje recibido en la tabla de GESTION
            # sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s WHERE cht_id = %s;"
            # cursor.execute(sql, ('Recibido', lastrowid))

    connectionDB.close


    # Devolvemos las variables lastrowid y comprobar
    return lastrowid, comprobar

@app.before_request
def middleware():
	print("IP: ", request.remote_addr, "URL SOLICITADA: ", request.base_url)
	pass

@app.route('/static/videos/<filename>')
def get_video(filename):
    return send_from_directory('static/videos', filename)

# ! RUTA PARA RECIBIR MENSAJES
# Manejar el evento 'mensaje' cuando se recibe un mensaje de usuario externo al agente
@app.route('/inMessage', methods=['POST'])
# ! FUNCION PARA RECIBIR MENSAJES
def mensaje():
    ip = request.remote_addr
    sqlInsert = None
    mensaje = ''
    newNameFile = None
    extFile = None

    #  * no vienen archivos
    if 'file' not in request.files:
        data = request.json['texto']
        data = str(data).split(";;_;")
  
        print("Mensaje recibido", request.json['texto'])
 
        mensaje = data[0]
        mensaje = mensaje.replace("'", "").replace('"', "").replace("`", "")
        remitenteId = data[1]
        lastrowid, comprobar = mAnnageTree(remitenteId, mensaje)
        print(f"Mensaje recibido: {mensaje} - Remitente: {remitenteId}")
        
        # Asegúrate de que sqlInsert tenga un valor válido
        if mensaje:  # Verifica que el mensaje no esté vacío
            sqlInsert = f"INSERT INTO {app.config['DB_NAME']}.tbl_mensaje (MES_ACCOUNT_SID, FK_GES_CODIGO, MES_BODY, MES_FROM, MES_TO, MES_CHANNEL, MES_SMS_STATUS) VALUES ('WEB', '{str(lastrowid)}', '{mensaje}', '{str(remitenteId)}', '{botWhatsappNum}', 'RECEIVED', 'received')"
        else:
            print("El mensaje está vacío, no se puede insertar en la base de datos.")

        # * vienen archivos
    if 'file' in request.files:
        remitenteId = request.form.get('clientId')
        lastrowid, comprobar = mAnnageTree(remitenteId, mensaje)
        messageId = random_id()
        # * se guarda archivo en servidor, que envia usuario externo
        file = request.files['file']
        extFile = str(file.filename).split(".")[-1]

        # Reemplazar espacios en el nombre del archivo por guiones bajos
        original_filename = file.filename.replace(" ", "_")

        # Validar tipo de archivo y tamaño
        if extFile in ['pdf', 'xls', 'jpg', 'png', 'doc'] and file.content_length <= 5 * 1024 * 1024:  # 5 MB
            # Obtener la fecha y hora actual en el formato deseado
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
            newNameFile = f"{lastrowid}_{timestamp}_{original_filename}"  # Cambiar el nombre del archivo

            # Guardar el archivo en la carpeta 'docs' una carpeta atrás
            rutaCarpeta = os.getenv("RUTA_CARPETA_DOCS")+"/"
            print('rutaCarpeta Docs ====> ',rutaCarpeta)
            
            file.save(os.path.join(rutaCarpeta + newNameFile))

            # Generar la URL del archivo guardado
            nombreArchivoAdjunto = f"/{newNameFile}"  # Ajusta esta URL según tu configuración de rutas

            print("nombreArchivoAdjunto: ", nombreArchivoAdjunto)
            # Enviar la url del archivo como mensaje
            mensaje = nombreArchivoAdjunto

            # Aquí puedes usar nombreArchivoAdjunto para actualizar la base de datos o enviarlo en un mensaje
            sqlInsert = f"INSERT INTO {app.config['DB_NAME']}.tbl_mensaje (MES_ACCOUNT_SID, FK_GES_CODIGO, MES_BODY, MES_FROM, MES_TO, MES_CHANNEL, MES_MEDIA_TYPE, MES_MEDIA_URL, MES_MESSAGE_ID, MES_SMS_STATUS) VALUES ('WEB', '{str(lastrowid)}', '', '{str(remitenteId)}', '{botWhatsappNum}', 'RECEIVED', '{extFile}', '{nombreArchivoAdjunto}', '{messageId}', 'received')"
        else:
            print("El archivo no es válido o excede el tamaño permitido.")
   
    # Asegúrate de que sqlInsert tenga un valor válido antes de ejecutarlo
    if sqlInsert is not None:
        connectionMySQL = connection()
        connectionMySQL.autocommit(True)
        with connectionMySQL.cursor() as cursor:
            # insert de mensaje
            cursor.execute(sqlInsert)

            # registro de quien hace la ultima interacción
            sqlUpdate = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_recibido = NOW() WHERE cht_id = %s"
            cursor.execute(sqlUpdate, ('Recibido', lastrowid))

        connectionMySQL.close

        if comprobar == True:
            arbol(lastrowid, remitenteId, mensaje)

    # return { 'filename': nombreArchivoAdjunto, 'extFile' : extFile, 'mensaje': mensaje }
    return { 'mensaje': mensaje }

#validar el chat si está cerrado, oculta el input
@app.route('/validarChat', methods=['POST'])
def validaCaso():
	remitenteId = request.json['clientId']


	# Fecha y hora actual
	current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	connectionMySQL = connection()
	# Habilitamos la opción de autocommit para que los cambios se guarden automáticamente
	connectionMySQL.autocommit(True)
	# Creamos un cursor para ejecutar consultas en la base de datos
	with connectionMySQL.cursor() as cursor:
		# Consultamos el último registro de la tabla tbl_chat para el usuario especificado en idChat
		sql = f"SELECT cht_estado_gestion FROM {app.config['DB_NAME']}.tbl_chat WHERE cht_id_chat_web = '{remitenteId}' AND cht_tipo_estado = 'Activo' ORDER BY cht_id DESC LIMIT 1;"
		# print(sql)
		cursor.execute(sql)
		row = cursor.fetchone()


		# Si no hay ningún registro para el usuario, insertamos un nuevo registro en la tabla
		if row and row['cht_estado_gestion'] == "Cerrado":
			# El caso está cerrado
			validar = "Cerrado"

		else:
			# El caso no está cerrado o no se encontró
			validar = "Abierto"


	return validar

#Procesa la informacion del formulario
@app.route('/sendForm', methods=['POST'])
def procesarFormulario():
    remitenteId = request.json['clientId']
    nombre = request.json['nombre']
    pais = request.json['pais']
    ciudad = request.json['ciudad']
    documento = request.json['documento']
    telefono = request.json['telefono']
    correo = request.json['correo']
    indicativo = request.json['indicativo']

    print(remitenteId, nombre, pais, ciudad, documento, telefono, correo, indicativo)
    # Fecha y hora actual
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connectionMySQL = connection()
    # Habilitamos la opción de autocommit para que los cambios se guarden automáticamente
    connectionMySQL.autocommit(True)
    # Creamos un cursor para ejecutar consultas en la base de datos
    with connectionMySQL.cursor() as cursor:
        # Consultamos el último registro de la tabla tbl_chat para el usuario especificado en idChat
        sql = f"SELECT cht_id, cht_estado_gestion, cht_navegacion_arbol FROM {app.config['DB_NAME']}.tbl_chat WHERE cht_id_chat_web = '{remitenteId}' AND cht_tipo_estado = 'Activo' ORDER BY cht_id DESC LIMIT 1;"
        # print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Si no hay ningún registro para el usuario, insertamos un nuevo registro en la tabla
        if len(rows) == 0:
            sql = f"INSERT INTO {app.config['DB_NAME']}.tbl_chat (cht_estado_gestion, cht_id_chat_web, cht_navegacion_arbol, GES_CHORA_INICIO_GESTION, cht_tipo_estado, GES_CTIPO, GES_TIPO_CAnnaL, GES_FORM_NOMBRE, GES_FORM_PAIS, GES_FORM_CIUDAD, GES_FORM_DOCUMENTO, GES_FORM_TELEFONO, GES_FORM_CORREO, GES_INDICATIVO) VALUES ('Abierto', '{remitenteId}', 'MSG_SALUDO', '{str(current_date)}', 'Activo', 'inbound', 'WEB', '{nombre}', '{pais}', '{ciudad}', '{documento}', '{telefono}', '{correo}', '{indicativo}')"
            # print(sql)
            cursor.execute(sql)
            lastrowid = cursor.lastrowid

            # * registro de quien hace la ultima interacción
            # pero en esta caso no hubo interacción entonces que?
            sqlUpdate = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET GES_ULT_INTERACCION = 'SIN_INTERACCION' WHERE cht_id = '{str(lastrowid)}'"
            cursor.execute(sqlUpdate)

        return "True"

# Enviar un mensaje al servidor de chat desde Python (al usuario externo) - Está función solo la usa el bot
def sendMessage(remitenteId, mensaje, lastrowid, isFile=False, fileName=None, extFile=None, interaccion=True):
    if isFile:
        # Si se envía un archivo, por ejemplo un video
        messageId = f"{fileName}.{extFile}"
        sio.emit('server_py:mensaje', {'remitenteId': remitenteId, 'isFile': isFile, 'fileData': {'extFile': extFile, 'filename': messageId}})
        mediaType = extFile
        mediaUrl = messageId
        numMedia = '1'
    else:
        # Si es un mensaje de texto
        msg = str(mensaje + ":" + remitenteId)
        sio.emit('server_py:mensaje', {'remitenteId': remitenteId, 'isFile': False, 'mensaje': mensaje})
        mediaType = ''
        mediaUrl = ''
        numMedia = '0'

    # Inserta el mensaje en la base de datos
    connectionMySQL = connection()
    connectionMySQL.autocommit(True)
    with connectionMySQL.cursor() as cursor:
        sql = f"INSERT INTO {app.config['DB_NAME']}.tbl_mensaje (FK_GES_CODIGO, MES_ACCOUNT_SID, MES_API_VERSION, MES_BODY, MES_FROM, MES_TO, MES_CHANNEL, MES_MESSAGE_ID, MES_NUM_MEDIA, MES_DATE_SENT__MESSAGE, MES_DATE_CREATED_MESSAGE, MES_DATE_UPDATED_MESSAGE, MES_MEDIA_TYPE, MES_MEDIA_URL, MES_USER) VALUES ('{lastrowid}', 'WEB', '', '{str(mensaje)}', '', '{str(remitenteId)}', 'SEND', '{messageId if isFile else ''}', '{numMedia}', '', '', '', '{mediaType}', '{mediaUrl}', 'BOT')"
        cursor.execute(sql)

        sqlUpdate01 = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_enviado = NOW() WHERE cht_id = %s;"
        cursor.execute(sqlUpdate01, ('Enviado', lastrowid))

        if interaccion:
            sqlUpdate = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_enviado = NOW() WHERE cht_id = %s;"
            cursor.execute(sqlUpdate, ('Enviado', lastrowid))

    connectionMySQL.close()

# * esta ruta la usa el agente para enviar mensajes al usuario (Chat-Web)
@app.route("/SendMessage", methods=["POST"])
def sendMessageWeb():
	gestionId = request.json['gestionId']
	remitenteId = request.json['remitenteId']
	mensaje = request.json['mensaje']
	isFile = request.json['isFile']
	fileName = request.json['fileName']
	extFile = request.json['extFile']
	idAgent = request.json['idAgent']
	sqlInsert = None
	# * agente envia solo texto
	if isFile == False:
		print('-- Agente envia texto:', mensaje)
		print("Se aplicaron los cambios")
		print('--agent id:', idAgent)
		sqlInsert = f"INSERT INTO {app.config['DB_NAME']}.tbl_mensaje (FK_GES_CODIGO, MES_ACCOUNT_SID, MES_BODY, MES_FROM, MES_TO, MES_CHANNEL, MES_NUM_MEDIA, MES_USER, MES_SMS_STATUS) VALUES ('{gestionId}', 'WEB', '{str(mensaje)}', '{botWhatsappNum}', '{str(remitenteId)}', 'SEND', '{str('0')}', '{str(idAgent)}','read')"
		sio.emit('server_py:mensaje', {'remitenteId': remitenteId, 'isFile': isFile, 'mensaje': mensaje})

	# * agente envia solo file
	if isFile == True:
		print('-- Agente envia archivo', f"${fileName}.{extFile}")
		messageId = f"{fileName}.{extFile}"
		sqlInsert = f"INSERT INTO {app.config['DB_NAME']}.tbl_mensaje (FK_GES_CODIGO, MES_ACCOUNT_SID, MES_BODY, MES_FROM, MES_TO, MES_CHANNEL, MES_MEDIA_TYPE, MES_MEDIA_URL, MES_MESSAGE_ID, MES_NUM_MEDIA, MES_USER, MES_SMS_STATUS) VALUES ('{gestionId}', 'WEB', '{str(mensaje)}', '{botWhatsappNum}', '{str(remitenteId)}', 'SEND', '{extFile}', '{messageId}', '{fileName}', '{str('0')}', '{str(idAgent)}','read')"
		sio.emit('server_py:mensaje', {'remitenteId': remitenteId, 'isFile': isFile, 'fileData': {'extFile': extFile, 'filename': f"{fileName}.{extFile}"}})
		
	connectionMySQL = connection()
	connectionMySQL.autocommit(True)

	with connectionMySQL.cursor() as cursor:
		# Ejecuta sql
		cursor.execute(sqlInsert)

		sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_enviado = NOW() WHERE cht_id = %s;"
		cursor.execute(sql, ('Enviado', gestionId))

		sql = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_enviado = NOW() WHERE cht_id = %s;"
		cursor.execute(sql, ('Enviado', gestionId))

		sqlUpdate = f"UPDATE {app.config['DB_NAME']}.tbl_chat SET cht_estado_chat = %s, cht_enviado = NOW() WHERE cht_id = %s;"
		cursor.execute(sqlUpdate, ('AGENTE', gestionId))

	connectionMySQL.close

	return "True"

# ! MONITOREA CHATS INACTIVOS, ENVIA ALERTAS O CIERRA CHATS SEGUN EL TIEMPO DE INACTIVIDAD
def vigilaChats():
    # * VARIABLES
    metaMinutosAlerta = 5
    metaMinutosCierre = 10
    alertaMensajeInactividad_template = (
        "⏳ Apreciado cliente, hemos notado que lleva {tiempo} minutos sin actividad en el chat. "
        "🤔 ¿Necesita ayuda con su videoagendamiento en Meetings ETB? "
        "💬 Estamos aquí para asistirle. "
        "👉 Por favor, responda a su última interacción para continuar. 😊"
    )
    cierreMensajeInactividad = (
        "🚫 Su sesión de videoagendamiento en Meetings ETB ha finalizado debido a un periodo prolongado de inactividad. "
        "⏳ Si necesita asistencia para completar su agendamiento, no dude en contactarnos nuevamente. "
        "📞 ¡Estamos aquí para ayudarle! 😊"
    )
    navegacionArbolChat = '-'

    # * BUCLE INFINITO
    while True:
        try:
            connectionMySQL = connection()
            connectionMySQL.autocommit(True)

            with connectionMySQL.cursor(pymysql.cursors.DictCursor) as cursor:
                # Consulta registros con inactividad
                sqlChatsInactivos = f"""
                    SELECT 
                        cht_id, 
                        cht_recibido, 
                        cht_id_chat_web,
                        TIMESTAMPDIFF(SECOND, cht_recibido, NOW()) AS segundos_inactividad
                    FROM {app.config['DB_NAME']}.tbl_chat
                    WHERE cht_estado_chat = %s
                    AND cht_estado_gestion IN (%s)
                    HAVING segundos_inactividad >= %s;
                """
                cursor.execute(sqlChatsInactivos, ('Enviado', 'Abierto', metaMinutosAlerta * 60))
                registros = cursor.fetchall()

                print(f"Registros encontrados para verificar inactividad: {len(registros)}")

                for registro in registros:
                    segundos_inactividad = registro['segundos_inactividad']
                    minutos_inactividad = segundos_inactividad // 60
                    segundos_restantes = segundos_inactividad % 60
                    tiempo_formateado = f"{minutos_inactividad:02}:{segundos_restantes:02}"  # Formato MM:SS
                    id_gestion_inactiva = registro['cht_id']
                    whatsappNum = registro['cht_id_chat_web']

                    if metaMinutosAlerta * 60 <= segundos_inactividad < metaMinutosCierre * 60:
                        # variables
                        navegacionArbolChat = 'MSG_ALERTA_INACTIVIDAD'
                        alertaMensajeInactividad = alertaMensajeInactividad_template.format(tiempo=tiempo_formateado)
                        
                        # Actualizar chat y enviar alerta
                        actualizarChat(cursor, id_gestion_inactiva, navegacionArbolChat, alertaMensajeInactividad)
                        sendMessage(whatsappNum, alertaMensajeInactividad, id_gestion_inactiva)
                    elif segundos_inactividad >= metaMinutosCierre * 60:
                        # variables
                        navegacionArbolChat = 'MSG_FIN'
                        estadoGestion = "Cerrado"
                        
                        # Cerrar chat y notificar
                        cerrarChat(cursor, id_gestion_inactiva, estadoGestion, navegacionArbolChat, cierreMensajeInactividad)
                        sendMessage(whatsappNum, cierreMensajeInactividad, id_gestion_inactiva)

                print("Verificación de inactividad completada.")

        except pymysql.Error as e:
            print(f"Error en fn vigilaChats - Error de MySQL: {e}")
        except Exception as e:
            print(f"Error en fn vigilaChats\n{e}")
        finally:
            if connectionMySQL:
                connectionMySQL.close()

        # Pausa de 1.5 minutos antes de la siguiente ejecución
        time.sleep(90)

# ! FUNCION PARA ACTUALIZAR CHAT
def actualizarChat(cursor, idChat, navegacionArbolChat, descripcionChat):    
    sqlUpdateChat = f"""
    UPDATE {app.config['DB_NAME']}.tbl_chat 
    SET cht_navegacion_arbol = %s,
        cht_descripcion = %s
    WHERE cht_id = %s
    """
    cursor.execute(sqlUpdateChat, (navegacionArbolChat, descripcionChat, idChat))


# ! FUNCION PARA CERRAR CHAT
def cerrarChat(cursor, idChat, estadoGestion, navegacionArbolChat, descripcionChat):
    sqlCerrarChat = f"""
    UPDATE {app.config['DB_NAME']}.tbl_chat 
    SET cht_estado_gestion = %s, 
        cht_navegacion_arbol = %s,
        cht_descripcion = %s
    WHERE cht_id = %s
    """
    cursor.execute(sqlCerrarChat, (estadoGestion, navegacionArbolChat, descripcionChat, idChat))

lineProfiling(1)

if __name__ == '__main__':
    # * VARIABLES
    appBotHost = 'localhost'
    appBotPort = os.getenv('BOTCHATWEBHOOK_PORT')
    # app.run(host='127.0.0.1', port=api['port_bot'])
    cargarConfiguracionInicial()
    chatsInactivos = threading.Thread(target=vigilaChats)
    chatsInactivos.start()

    print("En linea en Host: ", appBotHost, " y puerto: ", appBotPort)
    app.run(host=appBotHost, port=appBotPort)
	  




# Mantener la conexión activa hasta que el cliente decida salir
while True:
	pass

# Desconectar del servidor de chat al salir
sio.disconnect()