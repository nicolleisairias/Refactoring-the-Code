from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.credentials import credentials
from AXA.AXA_Liv import AxaLivBot
from datetime import datetime
import time

class sheet_axa_liv:
    #primero se reciben los valores del json
    def __init__(self, key_path, spreadsheet_id):
        self.key_path = key_path
        self.spreadsheet_id = spreadsheet_id
        self.creds = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/spreadsheets'])
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = self.service.spreadsheets()

    #funcion para actualizar valor de la columna
    def actualizar_valor(self, fila, valor, columna):
        value_range_body = {
            'values': [
                [valor]
            ]
        }
        rango_celda = f'LIVIANOS!{columna}{fila}'
        update_result = self.sheet.values().update(spreadsheetId=self.spreadsheet_id, range=rango_celda, valueInputOption='RAW', body=value_range_body).execute()
        print(f'Valor actualizado en la celda {rango_celda}')

    def cotizar_bot(self):
     while True:
        print("Revisando la hoja de cálculo...")
        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id, range='LIVIANOS!AH:AH').execute()
        values = result.get('values', [])
        tamaño_bucle = len(values)

        if not values:
            print('No se encontraron datos en la columna AC.')
        bot1 = AxaLivBot
        fila_idx = 1
        #si el valor de la fila es 1 se inicia el login 
        if fila_idx == 1:
            contador_404 = 0
            driver_local = bot1.login()


        for fila in values:
            contador_no = 0
            if contador_404 == 2:
                bot1.cerrar_navegador(driver_local)
                driver_local = bot1.login()  # Realizar login inicial o después de 3 errores "404"
                contador_404 = 0

            if fila and fila[0] != '' and fila[0] != 'NO COTIZA':
                print(f'Ya se realizó el cálculo en la fila {fila_idx}. Se omite el proceso.')
                fila_idx += 1
                continue
            if fila and fila[0] == 'NO COTIZA':
                contador_no = 1
                
            result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id, range=f'LIVIANOS!A{fila_idx}:V{fila_idx}').execute()
            fila_values = result.get('values', [])

            if not fila_values:
                print(f'La fila {fila_idx} está vacía. Se detiene el proceso.')
                bot1.cerrar_navegador(driver_local)
                break
            else:
                #valores especificos de AXA para la cotizacion 
                numero_cc = fila_values[0][0]
                tipo_de_doc = fila_values[0][4]
                fecha_n = fila_values[0][5]
                genero = fila_values[0][6]
                validacion = fila_values[0][8]if len(fila_values[0]) > 8 and fila_values[0][8] != '' else None
                placa = fila_values[0][9]
                tipo_placa = fila_values[0][10]
                marca = fila_values[0][11]
                nit = fila_values[0][12] if len(fila_values[0]) > 12 and fila_values[0][12] != '' else None
                fasecolda = fila_values[0][15]
                modelo = fila_values[0][16]
                valor_c = fila_values[0][20] 
                ciudad = fila_values[0][18]
                cobertura = fila_values[0][21]
                fila_actualizar = fila_idx

                if validacion != "AXA COLPATRIA" :

                    bot = AxaLivBot(marca=marca, año=modelo, valor_c=valor_c, Documento=numero_cc, placa=placa, fecha_n=fecha_n,genero = genero,
                                tipo_doc=tipo_de_doc, color_ve="ALUMINIO METAL", tipo_ve=tipo_placa, zona_cir="BOGOTA",
                                cobertura=cobertura, fila=fila_actualizar, tamaño_t=tamaño_bucle, driver=driver_local, nit=nit,fasecolda = fasecolda)
                
                    texto_extraido,texto_extraido2 = bot.ejecutar()
                
                    if texto_extraido2 == "ERROR":
                        contador_404 += 1
                    else:
                        contador_404 = 0  # Reiniciar el contador si el resultado no es 404

                    if texto_extraido == "NO COTIZA" and contador_no == 1:
                        texto_extraido = "NO COTIZA 2"

                else:
                    texto_extraido = "VIGENTE"
                    texto_extraido2 = "0"         
                     

            self.actualizar_valor(fila_actualizar, texto_extraido, "AH")
            self.actualizar_valor(fila_actualizar, texto_extraido2, "AI")

            fila_idx += 1
        print("Esperando 5 minutos antes de revisar nuevamente...")
        time.sleep(300)  # Espera 5 minutos   

