import base64
import codecs
import os
import sys
import datetime
import csv

def Encrypt(O0OO00OOOOOOOO00O):
    if O0OO00OOOOOOOO00O.strip() == '' or O0OO00OOOOOOOO00O.strip() == None:
        return 'Error'
    O0OO00OOOOOOOO00O = str(O0OO00OOOOOOOO00O.strip())
    try:
        O0OO00OOOOOOOO00O = ''.join(hex(ord(O0O00O0O000OO000O))[2:] for O0O00O0O000OO000O in O0OO00OOOOOOOO00O)
    except:
        return 'Error'
    O0OO00OOOOOOOO00O = O0OO00OOOOOOOO00O.upper()
    try:
        O0OO00OOOOOOOO00O = base64.b64encode(O0OO00OOOOOOOO00O.encode(
            str(''.join([chr(int(''.join(c), 16)) for c in zip('7574662D38'[0::2], '7574662D38'[1::2])]))))
        O0OO00OOOOOOOO00O = str(O0OO00OOOOOOOO00O, str(
            ''.join([chr(int(''.join(c), 16)) for c in zip('7574662D38'[0::2], '7574662D38'[1::2])])))
        O0OO00OOOOOOOO00O = codecs.encode(O0OO00OOOOOOOO00O, str(
            ''.join([chr(int(''.join(c), 16)) for c in zip('726F745F3133'[0::2], '726F745F3133'[1::2])])))
    except:
        return 'Error'
    try:
        O0OO00OOOOOOOO00O = ''.join(
            hex(ord(OOO00000OOOO00OO0))[2:] for OOO00000OOOO00OO0 in O0OO00OOOOOOOO00O)  # line:21
    except:
        return 'Error'
    O0OO00OOOOOOOO00O = O0OO00OOOOOOOO00O.upper()
    O0OO00OOOOOOOO00O = str(O0OO00OOOOOOOO00O.strip())
    return O0OO00OOOOOOOO00O

def DeCrypt(OOOOOOOO000000OO0):
    if OOOOOOOO000000OO0.strip() == '' or OOOOOOOO000000OO0.strip() == None:
        return 'Error'
    OOOOOOOO000000OO0 = str(OOOOOOOO000000OO0.strip())
    try:
        OOOOOOOO000000OO0 = ''.join([chr(int(''.join(O0O000000O0O00O00), 16)) for O0O000000O0O00O00 in
                                     zip(OOOOOOOO000000OO0[0::2], OOOOOOOO000000OO0[1::2])])
    except:
        return 'Error'
    try:
        OOOOOOOO000000OO0 = codecs.decode(OOOOOOOO000000OO0, str(
            ''.join([chr(int(''.join(c), 16)) for c in zip('726F745F3133'[0::2], '726F745F3133'[1::2])])))
    except:
        return 'Error'
    try:
        OOOOOOOO000000OO0 = OOOOOOOO000000OO0.encode(
            str(''.join([chr(int(''.join(c), 16)) for c in zip('6173636969'[0::2], '6173636969'[1::2])])))
        OOOOOOOO000000OO0 = base64.b64decode(OOOOOOOO000000OO0)
        OOOOOOOO000000OO0 = OOOOOOOO000000OO0.decode(
            str(''.join([chr(int(''.join(c), 16)) for c in zip('6173636969'[0::2], '6173636969'[1::2])])))
    except:
        return 'Error'
    try:
        OOOOOOOO000000OO0 = ''.join([chr(int(''.join(OO0O0O0OOOO0O0000), 16)) for OO0O0O0OOOO0O0000 in
                                     zip(OOOOOOOO000000OO0[0::2], OOOOOOOO000000OO0[1::2])])
    except:
        return 'Error'
    OOOOOOOO000000OO0 = str(OOOOOOOO000000OO0.strip())
    return OOOOOOOO000000OO0


comprobarRuta = str(os.path.dirname(sys.argv[0]))
if comprobarRuta.strip() == None:
    EjecutablePrograma = str(os.path.basename(sys.executable))
    RutaEjecutablePrograma = str(os.path.dirname(sys.executable))
elif comprobarRuta.strip() == '':
    EjecutablePrograma = str(os.path.basename(sys.executable))
    RutaEjecutablePrograma = str(os.path.dirname(sys.executable))
else:
    EjecutablePrograma = str(os.path.basename(sys.argv[0]))
    RutaEjecutablePrograma = str(os.path.dirname(sys.argv[0]))


"""Control Errores"""
def WLog(Data):

    try:
        FechaActual = datetime.datetime.now().strftime("%d%m%y")
    except:
        FechaActual = datetime.now().strftime("%d%m%y")

    if not os.path.exists(str(os.path.join(RutaEjecutablePrograma, "Log"))):
        os.makedirs(str(os.path.join(RutaEjecutablePrograma, "Log")))

    Archivo = str(os.path.join(RutaEjecutablePrograma, "Log", FechaActual + ".csv"))
    File_Exist = os.path.isfile(Archivo)
    Comprobar = "FALSE"
    if File_Exist == True:
        #os.remove(Archivo)
        Comprobar = "OK"
    elif File_Exist == False:
        #os.mkdir(path)
        Comprobar = "OK"
    else:
        Comprobar = "FALSE"

    if Comprobar == "OK":
        try:
            Array = []
            myData = [str(Data)]
            Array.append(myData)
            myFile = open(Archivo, 'a+', newline='', encoding="utf-8")
            with myFile:
                writer = csv.writer(myFile, delimiter=";")
                writer.writerows(Array)
            myFile.close()
            return 1
        except Exception as e:
            ControlERROR(e)

def ControlERROR(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    try:
        FechaActual = datetime.datetime.now().strftime("%d/%m/%y  %H:%M")
    except:
        FechaActual = datetime.now().strftime("%d/%m/%y  %H:%M")
    WLog(str(FechaActual) + " - " + str(e) + " - " + str(exc_type) + " - " + str(fname) + " - Line: " + str(exc_tb.tb_lineno))
    print(str(e), exc_type, fname, exc_tb.tb_lineno)
