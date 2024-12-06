from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
variable_login = 0
variable_bucle = 0

# funcion de hacer click, elementos xpath de momento
def hacer_clic_elemento_por_xpath(driver, xpath):
    # Esperar a que el elemento esté visible
    elemento = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    time.sleep(1)
    # Hacer clic en el elemento
    elemento.click()
    time.sleep(5)
#funcion para ingresar datos en un campo, se debe especificar se es un selector o xpath
def ingresar_datos(driver, CSS_SELECTOR,css_selector, datos):
    # Esperar a que el elemento esté visible
    elemento = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    time.sleep(1)
    # Limpiar el campo de texto
    elemento.clear()
    time.sleep(2)
    # Ingresar los datos en el campo
    elemento.send_keys(datos)
    time.sleep(5)
#funcion para uso de tecla abajo cantidad indefinida
def tecla_abajo(campo_entrada,repeticiones):
        for _ in range(repeticiones):
         campo_entrada.send_keys(Keys.ARROW_DOWN)
         time.sleep(1)
         
#recore las listas despegables con nomas de 3 campos
def capos_de_3(driver, ubi1,ubi2,variable_user,evaluar1,evaluar2):
        # Encontrar el campo de entrada
    campo = driver.find_element(By.CSS_SELECTOR, ubi1)
    time.sleep(3)
    # Hacer clic en el campo de entrada
    campo.click()
    time.sleep(3)
    

    # selecionar campo de entrada 
    campo2 = driver.find_element(By.CSS_SELECTOR, ubi2)
    if variable_user == evaluar1:
        repeticiones = 2
    elif variable_user == evaluar2:
        repeticiones = 3
    else:
        repeticiones = 1  

    tecla_abajo(campo2,repeticiones)
    time.sleep(3)
    campo2.send_keys(Keys.ENTER)
    time.sleep(1)

class AxaLivBot:
    def __init__(self, marca, año, valor_c, Documento, placa, fecha_n,genero, tipo_doc, color_ve, tipo_ve, zona_cir, cobertura,fila,tamaño_t, driver, nit,fasecolda):
        self.marca = marca
        self.año = año
        self.valor_c = valor_c
        self.Documento = Documento
        self.placa = placa
        self.fecha_n = fecha_n
        self.genero = genero
        self.tipo_doc = tipo_doc
        self.color_ve = color_ve
        self.tipo_ve = tipo_ve
        self.zona_cir = zona_cir
        self.cobertura = cobertura
        self.fila = fila
        self.tamaño_t =tamaño_t
        self.driver = driver
        self.nit = nit
        self.fasecolda = fasecolda

    def iniciar_navegador():
        # Configurar las opciones de Chrome
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Inicializar el navegador Chrome
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        return driver
    
    def login():
      driver = AxaLivBot.iniciar_navegador()
      try:
          #Usuario loguin axa
        driver.get("https://sucursalenlinea.axacolpatria.co/home")
        time.sleep(5)
        with open('credenciales/user_AXA/password_AXA.txt', 'r') as file:
         password = file.read().strip()

        with open('credenciales/user_AXA/USER_AXA.txt', 'r') as file:
         user = file.read().strip()

        #user
        ingresar_datos(driver, "CSS_SELECTOR","#_LoginPortlet_WAR_authenticationportlet_docNumber",user)
        ##_LoginPortlet_WAR_authenticationportlet_docNumber
        #password
        ingresar_datos(driver, "CSS_SELECTOR", "#_LoginPortlet_WAR_authenticationportlet_password",password)
  
        #Inicio login
        hacer_clic_elemento_por_xpath(driver,'//*[@id="_LoginPortlet_WAR_authenticationportlet_fm"]/div[3]/button')
        
        # Esperar a que el elemento de la lista desplegable esté presente
        lista_desplegable = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="_ProfileSelectorPortlet_WAR_authenticationportlet_profileSelection"]')))

        # Seleccionar la opción por su valor
        lista_desplegable = Select(lista_desplegable)
        lista_desplegable.select_by_value("ADM")

        #Inicio confimacion de datos
        hacer_clic_elemento_por_xpath(driver, '//*[@id="_ProfileSelectorPortlet_WAR_authenticationportlet_profileSelectorForm"]/div[4]/button[2]')
        driver.get("https://sucursalenlinea.axacolpatria.co/group/guest/herramientas/gestor-de-ventas/autos")
        time.sleep(7)

        return driver
      
      except Exception:
       print('Error Tiempo de login')
       time.sleep(30)
        #driver.close()

    def ejecutar(self): 
     driver = self.driver    
     #zona de execiones por marca 

     valor_c_sin_puntos = self.valor_c.replace('.', '').replace(",", "").replace("$", "")
     valor_c_entero = int(valor_c_sin_puntos)
     
     if self.marca in ["JAC", "FOTON", "JMC", "CHANGAN","HYUNDAI","DFSK/DFM/DFZL", "FIAT"] or int(valor_c_entero) > 300000001:
      texto_extraido = ("NO COTIZA marca o valor") 
      texto_extraido2 = ("0") 
      return texto_extraido,texto_extraido2
     else: 
    #zona de execiones por año y avaluo  
    #revicion modelo minimi. ¿98 cotiza 98?
      if self.año > "1997"  :

       try: 
         driver.get("https://pws.axacolpatria.co/PortalAsesor/QuoteVehicle/CreateQuoteVehicles")
         time.sleep(10)
         try: 
          elemento  = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="NoPlateModal"]/div/div/div[3]/button')))
          elemento.click()
          time.sleep(5)
         except:
          pass 
   
         #datos usuario
    
         #tipo de documento

         capos_de_3(driver, "#a_People_IdDocumentType","#input_People_IdDocumentType",self.tipo_doc,"CC","NIT")

        # Especial manejo para NIT
         if self.tipo_doc == "NIT":
            input_nit = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/form/div[2]/section/div/div[1]/div[2]/fieldset/div[1]/div[1]/div/div[3]/input')))
            input_nit.send_keys(self.nit)
            
            cc_tipo = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/form/div[2]/section/div/div[2]/div[2]/fieldset/div[1]/div[1]/div/div[1]/span')))
            cc_tipo.click()
            cc_sel = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH,'/html/body/ul[2]/li[2]')))
            cc_sel.click()

            input_CC = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/form/div[2]/section/div/div[2]/div[2]/fieldset/div[1]/div[1]/div/div[2]/input')))
            input_CC.send_keys(self.Documento)
            time.sleep(3)

            #datos_vehiculo
            ingresar_datos(driver,"CSS_SELECTOR","#CodFasecoldaInput",self.fasecolda)
            ingresar_datos(driver,"CSS_SELECTOR","#AnioFasecoldaInput",self.año)
            ingresar_datos(driver, "CSS_SELECTOR","#VehiculeData_Plaque",self.placa)

            #fecha_nacimiento
            # se comvierte la fecha del excel en la fecha adecuada para AXA
            fecha_original =self.fecha_n
            fecha_objeto = datetime.strptime(fecha_original, "%d/%m/%Y")
            fecha_formateada = fecha_objeto.strftime("%Y/%m/%d")
            fecha_nacim = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/form/div[2]/section/div/div[2]/div[2]/fieldset/div[2]/div/div/div[1]/input')))
            fecha_nacim.send_keys(fecha_formateada)
        # Ingresar número de documento CC
         elif self.tipo_doc == "CC":
            ingresar_datos(driver, "CSS_SELECTOR", "#People_DocumentNumber", self.Documento)
            time.sleep(3)

            #datos vehiculo
            hacer_clic_elemento_por_xpath (driver,'/html/body/div[2]/form/div[2]/section/div/div[3]/div[2]/div/div[2]/div[2]/div/label/div')
            ingresar_datos(driver,"CSS_SELECTOR","#CodFasecoldaInput",self.fasecolda)
            ingresar_datos(driver,"CSS_SELECTOR","#AnioFasecoldaInput",self.año)
            ingresar_datos(driver, "CSS_SELECTOR","#VehiculeData_Plaque",self.placa)

            #fecha_nacimiento
            # se comvierte la fecha del excel en la fecha adecuada para AXA
            fecha_original =self.fecha_n
            fecha_objeto = datetime.strptime(fecha_original, "%d/%m/%Y")
            fecha_formateada = fecha_objeto.strftime("%Y/%m/%d")
            ingresar_datos(driver, "CSS_SELECTOR","#People_BirthDate",fecha_formateada)

        # Genero del usuario
        
         if self.genero == "Mujer":
           hacer_clic_elemento_por_xpath(driver,'/html/body/div[2]/form/div[2]/section/div/div[1]/div[2]/fieldset/div[1]/div[2]/div/label[2]')

         time.sleep(25)

         #color_vehiculo
         capos_de_3(driver, "#a_VehiculeData_Color","#input_VehiculeData_Color",self.color_ve,"ACERO OSCURO","ALUMINIO METAL")

         #tipo de vehiculo
         if self.tipo_ve == "Público/taxi":
           capos_de_3(driver, "#a_VehiculeData_VehicleServiceType","#input_VehiculeData_VehicleServiceType",self.tipo_ve,"Particular","Público/taxi")
         else :    
          capos_de_3(driver, "#a_VehiculeData_VehicleServiceType","#input_VehiculeData_VehicleServiceType",self.tipo_ve,"Particular","Público")

         #zona de circulacio
    
         # Encontrar el campo de entrada
         campo_circule1 = driver.find_element(By.CSS_SELECTOR, '#a_VehiculeData_IdCIrculationZone')
   
         # Hacer clic en el campo de entrada
         campo_circule1.click()
         time.sleep(10)

         # selecionar tipo de zona
         campo_circule2 = driver.find_element(By.CSS_SELECTOR, '#input_VehiculeData_IdCIrculationZone')
         if self.tipo_ve == "Particular":
            if self.zona_cir == "MEDELLIN":
             repeticiones = 1
            elif self.zona_cir == "BARRANQUILLA":
               repeticiones = 4
            elif self.zona_cir == "BOGOTA":
             repeticiones = 5 
            elif self.zona_cir == "CARTAGENA":
             repeticiones = 6
            elif self.zona_cir == "CALI":
             repeticiones = 29
            else:
             repeticiones = 22 
         else: 
            if self.zona_cir == "MEDELLIN":
             repeticiones = 1
            elif self.zona_cir == "BOGOTA":
             repeticiones = 2
            elif self.zona_cir == "OTRAS":
             repeticiones = 3  
            elif self.zona_cir == "S/TANDER":
             repeticiones = 4
            elif self.zona_cir == "EJE CAFETERO":
             repeticiones = 5
            elif self.zona_cir == "CARTAGENA" or self.zona_cir == "BARRANQUILLA":
             repeticiones = 6
            else:
             repeticiones = 3 
             

         tecla_abajo(campo_circule2,repeticiones)
         time.sleep(3)
         campo_circule2.send_keys(Keys.ENTER)
         time.sleep(1)
    
        # cobertura 
         if self.tipo_ve == "Público" or self.tipo_ve == "Público/taxi":
            campo = driver.find_element(By.CSS_SELECTOR, "#a_VehiculeData_CoverIdTypeTaxi")
            time.sleep(3)
            # Hacer clic en el campo de entrada
            campo.click()
            time.sleep(3)
                

                # selecionar campo de entrada 
            campo2 = driver.find_element(By.CSS_SELECTOR, "#input_VehiculeData_CoverIdTypeTaxi")
            if self.tipo_ve == "Público":
                    repeticiones = 2
            elif self.tipo_ve == "Público/taxi":
                    repeticiones = 4
            else:
                    repeticiones = 2  

            tecla_abajo(campo2,repeticiones)
            time.sleep(3)
            campo2.send_keys(Keys.ENTER)
            time.sleep(1)
        
         if self.tipo_ve == "Público" or self.tipo_ve == "Público/taxi":
            hacer_clic_elemento_por_xpath(driver, '//*[@id="btnContinuar"]')
            time.sleep(23)
            elemento = driver.find_element(By.CSS_SELECTOR,"#DivVIP > div.col-xs-12.productAssistance > div > div > div > h3")
            texto_extraido = elemento.text
            print("Texto extraído:", texto_extraido)
            time.sleep(7)
            hacer_clic_elemento_por_xpath(driver,'//*[@id="BtnGuardarCot"]')
            time.sleep(7)
            hacer_clic_elemento_por_xpath(driver,'/html/body/div[2]/form/div[1]/div[2]/div/div/div[3]/button')
            time.sleep(5)
            hacer_clic_elemento_por_xpath(driver, '//*[@id="BtnContSinGuardar"]')
            time.sleep(7)
            hacer_clic_elemento_por_xpath(driver, '//*[@id="BtnCont"]')
            time.sleep(7)
            elemento2 = driver.find_element(By.CSS_SELECTOR,"#FormQuoteCarsProducts > div.container > div.col-md-12.col-sm-12.col-xs-12 > div > div:nth-child(2) > span > h5")
            texto_extraido2 = elemento2.text
            time.sleep(1)
            texto_extraido = texto_extraido.replace(",", ".")
            texto_extraido = texto_extraido.replace("$", " ")
            print('final')
            time.sleep(1)
            return texto_extraido, texto_extraido2


         else:   
            hacer_clic_elemento_por_xpath(driver, '//*[@id="btnContinuar"]')
            time.sleep(23)
            cot_plus = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/form/div[1]/div[1]/div/div[2]/div[1]/div/div[4]/div/div/div/label")))
            cot_plus.click()
            
            elemento = driver.find_element(By.XPATH,"/html/body/div[2]/form/div[1]/div[1]/div/div[2]/div[1]/div/div[4]/div/div/div/h3")
            texto_extraido = elemento.text

            print("Texto extraído:", texto_extraido)
            time.sleep(7)
            hacer_clic_elemento_por_xpath(driver,'//*[@id="BtnGuardarCot"]')
            time.sleep(7)
            hacer_clic_elemento_por_xpath(driver,'/html/body/div[2]/form/div[1]/div[2]/div/div/div[3]/button')
            time.sleep(5)
            hacer_clic_elemento_por_xpath(driver, '//*[@id="BtnContSinGuardar"]')
            time.sleep(7)
            hacer_clic_elemento_por_xpath(driver, '//*[@id="BtnCont"]')
            time.sleep(7)
            elemento2 = driver.find_element(By.XPATH,"/html/body/div[2]/form/div[2]/div[5]/div/div[1]/span/h5")
            texto_extraido2 = elemento2.text
            time.sleep(1)
            texto_extraido = texto_extraido.replace(",", ".")
            texto_extraido = texto_extraido.replace("$", " ")
            print('final')
            time.sleep(1)
            return texto_extraido, texto_extraido2
       
        
       except Exception:
        
        print('Error Tiempo')
        time.sleep(10)
        texto_extraido = ("NO COTIZA")
        texto_extraido2 = ("ERROR")
        return texto_extraido,texto_extraido2
      else :
        
       print('NO COTIZA')
       texto_extraido = ("NO COTIZA AÑO")
       texto_extraido2 = ("0") 
       return texto_extraido,texto_extraido2

    def cerrar_navegador(driver):
        try:
         driver.quit()
        except:
            pass  