import time
import datetime
import pandas as pd
import psycopg2
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

def test_selenium_server_available():
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry

    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    session.get("http://selenium_service:4444/wd/hub")

def chegou_ao_fim():
    global driver
    # Obtém a posição vertical atual do navegador
    posicao_atual = driver.execute_script("return window.scrollY;")

    # Obtém a altura total da página
    altura_total = driver.execute_script("return document.body.scrollHeight;")

    # Se a posição atual for igual ou maior que a altura total, chegamos ao fim da página
    return posicao_atual + 1000 > altura_total 

def save_date(last_date):
    with open('last_extraction_date.txt', 'w') as file:
        file.write(last_date)

def get_last_date():
    with open('last_extraction_date.txt', 'r') as file:
        data = file.readline().split('/')
        return datetime.datetime(int(data[2]), int(data[1]), int(data[0]))

    return datetime.datetime.now().strftime("%d/%m/%Y")


test_selenium_server_available()

options = Options()

driver = webdriver.Remote(
    command_executor="http://selenium_service:4444/wd/hub",
    options=options
)

url = 'https://www.olx.com.br/imoveis/venda/casas/estado-ce/fortaleza-e-regiao/fortaleza'

driver.maximize_window()

max_pag = 100
count = 1
dif_date = 1
first_date = ''
date_last = get_last_date()
casas = []

print(f'INICIADO NOVO SCRAPING NA DATA:{datetime.datetime.now().strftime("%d/%m/%Y-%H:%M")}')
while(count <= max_pag and url != None and dif_date >= 0):
    driver.get(url)
    time.sleep(5)
    url = None

    try:
        xpath_button = '/html/body/div[1]/div[1]/main/div[1]/div[2]/main/div[3]/div[1]/div[2]/button[2]'
        button = driver.find_element(By.XPATH, xpath_button)

        button.click()
    except:
        pass
    
    while(not chegou_ao_fim()):
        print('ENTRAMOS NO LOOP')
        webdriver.ActionChains(driver).scroll_by_amount(0, 700).perform()

        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        just_elements = soup.find_all('section')

        elements = soup.find_all('section', attrs={
            'data-ds-component': True,
            'data-ds-component': 'DS-AdCard'
        })

        print(f'\n\nA QUANTIDADE DE ELEMENTOS ENCONTRADOS NESSA PAGINA FORAM {len(just_elements)}')
        print(f'QUANTIDADE DE ELEMENTOS COM COMPONENTES ENCONTRADOS NESSA PAGINA FORAM {len(elements)}')
        # print(f'CLASSES DO ELEMENTO ENCONTRADO {just_elements[0].attrs}')
        for e in elements:
            for class_parent in [parent.get('class', []) for parent in e.parents if parent.name == 'div']:
                if('sc-1b37e288-2' in class_parent):     
                    #PRECO, IPTU, CONDOMINIO========================= sc-e04933d-2 fhgICW
                    div_preco = e.find('div', attrs={
                        'class':lambda x: x == 'olx-ad-card__details-price--vertical' or x == 'olx-ad-card__details-price--horizontal'
                        })

                    preco =  None
                    iptu = None
                    condominio = None

                    if div_preco.find('h3') != None:
                        preco = ''.join([c for c in div_preco.find('h3').get_text() if c.isdigit()])

                    p_elements = div_preco.find_all('p')

                    for p in p_elements:
                        text = p.get_text()

                        if 'IPTU' in text:
                            iptu = ''.join([c for c in text if c.isdigit()])
                        
                        if 'Cond' in text:
                            condominio = ''.join([c for c in text if c.isdigit()])


                    #METRO_Q, QUARTO, BANHEIRO, GARAGEM========================= olx-ad-card__details-ads olx-ad-card__details-ads--vertical     
                    div_elementos = e.find('div', attrs={
                    'class':lambda x: x == 'olx-ad-card__details-ads olx-ad-card__details-ads--vertical' or x == 'olx-ad-card__details-ads olx-ad-card__details-ads--horizontal'
                    })

                    metro_quadrado = None
                    quarto = None
                    banheiro = None
                    garagem =  None
                    descricao = None

                    span_elements = div_elementos.find_all('span')

                    for span in span_elements:
                        text = span.get_text()

                        if 'metro' in span['aria-label']:
                            metro_quadrado = ''.join([c for c in text if c.isdigit()])[:-1]
                        
                        if 'quarto' in span['aria-label']:
                            quarto = ''.join([c for c in text if c.isdigit()])
                        
                        if 'banheiro' in span['aria-label']:
                            banheiro = ''.join([c for c in text if c.isdigit()])
                        
                        if 'garagem' in span['aria-label']:
                            garagem = ''.join([c for c in text if c.isdigit()])
                    
                    a_descricao = div_elementos.find('a')

                    if a_descricao != None:
                        descricao = a_descricao.get_text()

                    #REGIAO, DATA_POSTAGEM, PROFISSIONAL========================= 
                    div_regiao = e.find('div', attrs={
                    'class':lambda x: x == 'olx-ad-card__bottom'
                    })

                    regiao = None
                    data = None
                    vendedor = 'Direto com o dono'

                    p_elements = div_regiao.find_all('p')

                    for p in p_elements:
                        text = p.get_text()
                        
                        if 'Profissional' in text:
                            vendedor = text
                        
                        if 'Fortaleza' in text:
                            regiao = text      
                        
                        if 'date' in ' '.join(p['class']):
                            data = text.split(',')
                            
                            if data[0].lower() == 'hoje':
                                data[0] = datetime.datetime.now().strftime("%d/%m/%Y")
                            elif data[0].lower() == 'ontem':
                                data[0] = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d/%m/%Y")
                            else:
                                new_data = data[0]

                                map = {
                                    "jan": "january",
                                    "fev": "february",
                                    "mar": "march",
                                    "abr": "april",
                                    "mai": "may",
                                    "jun": "june",
                                    "jul": "july",
                                    "ago": "august",
                                    "set": "september",
                                    "out": "october",
                                    "nov": "november",
                                    "dez": "december"
                                }

                                for name, value in map.items():
                                    new_data = new_data.replace(name, value)
                                
                                if('29 de february' in new_data):
                                    new_data = new_data['data'].replace('29', '28')
                                
                                new_data = pd.to_datetime(new_data, format='%d de %B')
                                new_data = new_data.replace(year=datetime.datetime.now().year)

                                data[0] = new_data.strftime("%d/%m/%Y")

                            data = data[0]

                            data_split = data.split('/') 

                            date_now = datetime.datetime(int(data_split[2]), int(data_split[1]), int(data_split[0]))
                            
                            
                            if first_date == '':
                                first_date = data

                            dif_date = (date_now - date_last).days 
                            # print('dif_date: ', dif_date)

                    casa = {
                        'preco': float(preco) if preco != None else None,
                        'iptu': float(iptu) if iptu != None else None,
                        'condominio': float(condominio) if condominio != None else None,
                        'metro_quadrado': float(metro_quadrado) if metro_quadrado != None else None,
                        'quarto': int(quarto) if quarto != None else None,
                        'banheiro': int(banheiro) if banheiro != None else None,
                        'garagem': int(garagem) if garagem != None else None,
                        'regiao': regiao,
                        'data': data,
                        'vendedor': vendedor,
                        'descricao': descricao
                    }

                    if casa not in casas:
                        casas.append(casa)
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        prox = soup.find_all('a')

        for a in prox:
            if a.get_text() == 'Próxima página':
                url = a.get('href') 
        
        print(f'FORAM CONSULADAS {len(casas)} CASAS ATÉ O MOMENTO.')
        print(f'PROXIMO URL A SER CONSULTADO:\n   {url}')
    
    count += 1

new_df = pd.DataFrame(casas)

#ADICIONANDO DADOS NO BANCO
coon =  psycopg2.connect(host='postgres', dbname='houses_db', user='postgres', password='postgres', port=5432)
cur = coon.cursor()

cur.execute("""
    SELECT * FROM House;
""")
print(len(cur.fetchall()))

insert = """
INSERT INTO House(preco, iptu, condominio, metro_quadrado, quarto, banheiro, garagem, regiao, data, vendedor, descricao) VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
#preco;iptu;condominio;metro_quadrado;quarto;banheiro;garagem;regiao;vendedor
for index, row in  new_df.iterrows():
    cur.execute(insert, row)

cur.execute("""
    SELECT * FROM House;
""")
print(len(cur.fetchall()))

cur.execute("""
DELETE FROM House
WHERE id IN (
    SELECT id
    FROM (
        SELECT id, ROW_NUMBER() OVER(PARTITION BY preco, metro_quadrado, quarto, banheiro, garagem, regiao, vendedor ORDER BY id) AS linha
        FROM House
    ) subconsulta
    WHERE linha > 1
);            
""")

cur.execute("""
    SELECT * FROM House;
""")
print(len(cur.fetchall()))

#SALVANDO NO ARQUIVO CSV
save_date(first_date)
print('========================= ANALISE FINAL ===========================')
old_df = pd.read_csv('casas.csv', sep=';')
print(f'QUANTIDADE INICIAL DE CASAS: {old_df.shape}')

final_df = pd.concat([new_df, old_df], axis='index')

consider_columns = list(final_df.columns)
consider_columns.remove('iptu')
consider_columns.remove('descricao')
consider_columns.remove('data')
consider_columns.remove('condominio')

final_df = final_df.drop_duplicates(consider_columns, keep='last')
print(f'QUANTIDADE FINAL DE CASAS: {final_df.shape}')

final_df.to_csv('casas.csv', sep=';', index=False)

driver.close()
