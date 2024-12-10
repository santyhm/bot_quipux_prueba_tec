from bot import *

def main():
    global driver
    url_form = 'https://arenarpa.com/crazy-form'
    route_excel = 'ArenaRPAFormData.xlsx'

    driver = open_url(url_form)
    data_excel = read_excel(route_excel)

    btn_init = driver.find_element(By.XPATH, "/html/body/app-root/app-crazy-form/div/div[1]/div[2]/div[2]/a")
    btn_init.click()
    ids = ['nombres', 'apellidos', 'empresa', 'numero', 'email', 'pais', 'web']
    for arg in data_excel:
        filter_data = {field: arg[field.capitalize()] for field in ids}
        paste_form(driver, filter_data)

    # If you want to close after finishing the process
    # driver.quit()

if __name__ == "__main__":
    main()
