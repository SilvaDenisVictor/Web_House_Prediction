from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configurar as opções do Chrome
chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# Conectar ao Selenium Docker
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=chrome_options
)

url = 'https://www.olx.com.br/imoveis/venda/casas/estado-ce/fortaleza-e-regiao/fortaleza'

driver.get(url)
print(driver.title)
driver.quit()