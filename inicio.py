import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from enviar_email import send_email

# DataFrame to store the results
df = pd.DataFrame(columns=["numero", "url", "descripcion","monto"])

# Initialize the browser
driver = webdriver.Chrome()  # Ensure that the WebDriver is in your PATH

try:
    # Open the webpage
    driver.get('https://panamacompra.gob.pa/Inicio/#!/busquedaAvanzad')

    # Close the announcement if necessary
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close' and @title='cerrar']"))
        )
        close_button.click()
        time.sleep(1)  # Wait a moment after closing the announcement
    except Exception as e:
        print("No se encontró el botón de cerrar:", e)
    time.sleep(10)
    # Click on the "Búsqueda" button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@title='Búsqueda']"))
    )
    search_button.click()
    time.sleep(2)  # Wait a moment to observe the result

    # Click on the "Búsqueda Avanzada V2" link
    advanced_search_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#/busqueda-avanzada-v2') and contains(text(), 'Búsqueda Avanzada V2')]"))
    )
    advanced_search_link.click()
    time.sleep(2)  # Wait a moment for the new page to load

    # Interact with the description field, writing "sistemas"
    description_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='descripcion']"))
    )
    description_field.clear()
    description_field.send_keys("sistemas")  # Write "sistemas" in the description field
    
    # Interact with the date field, writing "01-09-2023"
    date_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "fd"))  # Use the ID of the date field
    )
    date_field.clear()
    date_field.send_keys("01-09-2023")  # Send the date in the format dd-mm-yyyy
    
    # Wait a moment to observe the result
    time.sleep(10)

    # Enable the search button if it's disabled
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/app-root/main/ng-component/div/div/form[2]/div[13]/button"))
    )
    if search_button.get_attribute('disabled'):
        driver.execute_script("arguments[0].removeAttribute('disabled')", search_button)

    # Press the "Buscar" button
    search_button.click()

    time.sleep(20)
    # Wait for the results to load
    #tabla= WebDriverWait(driver, 20).until(
        #EC.presence_of_element_located((By.XPATH, "//tbody/tr")))

    # Get all rows from the table
    tabla = driver.find_elements(By.XPATH, "//tbody/tr")
    filas_tabla = len(tabla)

    print(f"Total filas encontradas: {filas_tabla}")

    for i in range(1, filas_tabla):  # Iterate over all rows in the table
        try:
            time.sleep(20)
            # Obtain the number from the correct element
            numero_element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, f"//tbody/tr[{i}]/td[1]/a"))
            )
            numero = numero_element.text.strip()  # Get the number and clean whitespaces

            # Obtain the URL
            text_url = numero_element.get_attribute('href')

            # Obtain the description
            description = WebDriverWait(driver, 50).until(
                EC.visibility_of_element_located((By.XPATH, f"//tbody/tr[{i}]/td[3]"))
            ).text.strip()

            # Print the captured values
            print(f"Fila {i}: Número={numero}, URL={text_url}, Descripción={description}")

            # Add the data to the DataFrame using pd.concat
            new_row = pd.DataFrame({"numero": [numero], "url": [text_url], "descripcion": [description]})
            df = pd.concat([df, new_row], ignore_index=True)

                # Print the captured values
            print(f"Fila {i}: Número={numero}, URL={text_url}, Descripción={description}")

        except Exception as e:
            print(f"Error al capturar la fila {i}: {e}")
    
    # Save the DataFrame to an Excel file
    df.to_excel("reporte_busqueda.xlsx", index=False)
    print("El reporte ha sido guardado como 'reporte_busqueda.xlsx'.")

    # Call the send_email function
    recipients = [
        'Aprendiz.gestion@gruporeditos.com'
    ]
    subject = 'PRUEBA'
    body = 'si les llega chimba'
    
    send_email(recipients, subject, body, "reporte_busqueda.xlsx")  # Send the email

finally:
    # Close the browser
    driver.quit()

