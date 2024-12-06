from AXA.AXA_Liv_sheet import sheet_axa_liv # Importa la clase sheet_axa desde el archivo AXA_sheet.py, este inicia el sheet y el robot
# from previsora.Prev_sheet import sheet_previ#importa la clase sheet_previ deesde el archivo. para iniciar el robot 
# #from Seguros_del_estado.Estado_Sheet import sheet_estado
# from Mapfre.mafre_liv_sheet import sheet_mapfre_liv
#from Seguros_del_estado.Estado_Sheet_psl import sheet_estado_psl
#from Mundial.mundial_sheet import sheet_mundial
#from HDI.HDI_sheet import 
from Liberty.liberty_liv_sheet import sheet_liberty_liv
from Bolivar.bolivar_liv_sheet import sheet_bolivar_liv
import threading
import time
#url diego 1bx8kOOmEygwgQLMxLAKb12cmeY7pWnLdmdGTFM5uSzQ
#url oscar 1H7zsE3lzSMT1mu0Aw0_g2z3OM7tUzEj7Iu8Ps_hdlkQ
def ejecutar_bot(nombre_bot, bot_class):
    key_path = 'key.json'
    with open('credenciales/URL.txt', 'r') as file:
        spreadsheet_id = file.read().strip()
  
    for _ in range(2):  # Ejecutar el bot dos veces
        try:
            print(f"Iniciando {nombre_bot}")
            bot_instance = bot_class(key_path, spreadsheet_id)
            bot_instance.cotizar_bot()
            print(f"{nombre_bot} ha terminado, esperando para relanzar...")
        except Exception as e:
            print(f"Error en el proceso de {nombre_bot}:", e)
        time.sleep(300)  # Esperar 5 minutos antes de relanzar el bot
    print(f"{nombre_bot} ha completado sus dos ejecuciones.")

if __name__ == "__main__":
    bots = [
        #("estado", sheet_estado),
        #("estado_psl", sheet_estado_psl),
        #("prev", sheet_previ),
        # ("axa", sheet_axa_liv),
        # ("liberty", sheet_liberty_liv),
        ("Bolivar", sheet_bolivar_liv),
        #("mapfre", sheet_mapfre_liv),
        #("mundial", sheet_mundial),
        #("HDI",sheet_HDI)
    ]
    
    threads = []
    for nombre_bot, bot_class in bots:
        thread = threading.Thread(target=ejecutar_bot, args=(nombre_bot, bot_class))
        thread.start()
        threads.append(thread)
    
    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()
