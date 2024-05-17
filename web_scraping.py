import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def chegou_ao_fim():
    global driver
    # Obtém a posição vertical atual do navegador
    posicao_atual = driver.execute_script("return window.scrollY;")

    # Obtém a altura total da página
    altura_total = driver.execute_script("return document.body.scrollHeight;")

    # Se a posição atual for igual ou maior que a altura total, chegamos ao fim da página
    return posicao_atual + 1000 > altura_total 

options = Options()
options.add_argument("--enable-chrome-browser-cloud-management")

ser = Service("C:\\Users\\Denis\\Documents\\GitHub\\Web_House_Prediction\\msedgedriver.exe")  # Here you specify the path of Edge WebDriver
driver = webdriver.Edge(service = ser, options=options)

url = 'https://www.olx.com.br/imoveis/venda/casas/estado-ce/fortaleza-e-regiao/fortaleza'

headers = {
    "Authority": "www.olx.com.br",
    "Method": "GET",
    "Path": "/imoveis/venda/casas/estado-ce/fortaleza-e-regiao/fortaleza",
    "Scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Cookie": "cf_clearance=vcD1G6FSgg5m6F79_ROLJGNoqD1BcGX1OgtvfHWmpwU-1704750771-0-2-c7772eaa.3544eea8.9076714a-0.2.1704750771; _ym_uid=1704750773948885872; _ym_d=1704750773; _hjSessionUser_736533=eyJpZCI6IjBhMDkzYjEwLTcwNWQtNTY5ZS1iNGNlLWY3ODYxNjc4ZWFhZSIsImNyZWF0ZWQiOjE3MDQ4OTI0NjgzMTIsImV4aXN0aW5nIjpmYWxzZX0=; r_id=2835adc5-d34a-4f4d-a657-458b377023b0; _cfuvid=UEm75TI31Iddy3LWF9qv0.sCxM5UWhH7sczlyF8CMEs-1715698764105-0.0.1.1-604800000; nl_id=678c3b49-1a04-4241-aee2-2d8a9bab7043; l_id=3a91d268-68e8-44fc-a3ef-bc0f72cb1f65; mf_b837e449-83ee-457f-9ef5-8f976953f2bc=||1715698764657||0||||0|0|64.88215; _gcl_au=1.1.324188290.1715698765; _cc_id=fa4465d330fb9ab4b42a6f0fbba9d786; panoramaId_expiry=1716303565667; panoramaId=1661e9b3957efaaa5b6bf3bcff3316d53938a074b73ff4f047ac7d5feb397f62; panoramaIdType=panoIndiv; _gid=GA1.3.595417293.1715698765; _tt_enable_cookie=1; _ttp=sUNWWNLlz0QDUiKtc6CfhG-XuL0; __spdt=e80cb68aa08941c5937911daee4144ea; _fbp=fb.2.1715698765307.576231043; _lr_geo_location_state=CE; _lr_geo_location=BR; pbjs_sharedId=16af6d1b-fe9a-429a-82dc-64153016b5b8; pbjs_sharedId_cst=zix7LPQsHA%3D%3D; olx-cookies-accept=1; _lr_sampling_rate=100; _lr_env_src_ats=true; idl_env_cst=zix7LPQsHA%3D%3D; cf_clearance=ARyll1jj1vHAc2fGKa1Q4Vsgw.XGkSw8uzVTgXaDVV8-1715698790-1.0.1.1-Bz3xTFr_Gu.rRRrwPSLkYvyPWJPv3oTmwAyYxhJstOXw4BpqNDJWE14cuWjA.e1Iehz3tBJ9xukgUOjCmpDIxA; nvg83482=14a3e8ec439574801a425b912d10|0_136; _pbjs_userid_consent_data=3524755945110770; _pubcid=40a68ccd-3662-45bd-a698-e9b388e0acd8; pbjs-unifiedid=%7B%22TDID%22%3A%22bdbf2c7b-9989-469b-bc3d-9e43c70bffd0%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-05-14T15%3A00%3A53%22%7D; newIsGrid=true; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22undefined%22%2C%22hash%22%3A%22wBiML0Lv0cEh18cEd5DU%22%7D; TestAB_Groups=sxp-std-bo_enabled.sxp-std-au_control.free-insertion-goods-parcela_enabled.ppc-myplan-redirect-lp_enabled.autofill-2_enabled.ds-header-navbar_enabled.onb-perfil_enabled.mes-chats-http-retrieves_enabled.contentmod-gallery-tip_final.payg-redirect-nc_enabled.new-report_enabled.pos-cars-fee-boost_d-first.cmod-security-central-my-ads_autos.free-edtion-goods-parcela_enabled.payg-discount-julius_ml-c-mab.trp-cvv-ck_enabled.fee-boost-goods-parcela_enabled.autospp-notshow-modal-hv-myads_enabled.new-profile-history-component_enabled.ngage-new-home-autos_enabled.poscarsswt_control.autospp-marketplace-header_enabled.cnt-rating_single.menu-pro_enabled.sqld-btl_control.payg-discount-re-julius_ml-clu-mab.sanityweb50_control.cmod-pro-ad-showphone-body_enabled.nc-sub_control.txppayxpan_enabled.frrnwgoods_enabled.ds-adcard-optimized_on.adv-homegr_after-thirdgallery.ai-stp-v2_olx.adv-cookieless-liveramp_enabled.additional-seller-info-profile_enabled.additional-seller-info-edit_enabled.adv-native_grid-list.prf-rating_control.report-api_enabled.mes-dtadog_control.rec-3f7688_enabled.txpWarInfo_enabled.delivery-address-management_a.adfacelift-goods-web_upgrade.mes-or-dot_enabled.wv2-report_control.ai-stp-v3_on.rec-ab91bd_sacred.rec-h34113_sacred.ck-filters_enabled.sxp-std-mo_enabled.reval-log_control.ck-verbolx_enabled.sxp-std-tr_enabled; s_id=24089cb9-c9be-4edd-9050-680a025808f12024-05-14T17:39:38.973Z; ___iat_ses=2E9DD10A23260BCF; _lr_env=eyJ0aW1lc3RhbXAiOjE3MTU3MDgzNzk4NTYsInZlcnNpb24iOiIxLjUuMCIsImVudmVsb3BlIjoiQW5hNlZKZFZKRGRVa3Q2NHVodjUxWFVNUzRwYUM5bWY3UElMdzZCbHM1TmdyX0tGbmpmT3FLa1hHZy1CNWFySFdkMGRHZlFtQ0JuaklPNExLT0JnNTNIdFc2UGJBcGxtSkR2bGtGQmwtb3FtVlI0SDh5S2lUdmFqdGN4MGlJVDd2S2lmZFRGaUNMNlhwQXV1bXJiQnNMUDJmS2xkUFZ4ZElaS2hSQnhWTGJMSmZGX0NCemNxNHE5cFktRkNiMHpxcUkwRnV0YkwifQ%3D%3D; _lr_pairId=eyJ0aW1lc3RhbXAiOjE3MTU3MDgzNzk4NTcsInZlcnNpb24iOiIxLjUuMCIsImVudmVsb3BlIjpbIkEyWWVKSlZRaTZvUVhqeTM0bHR3UUdqWHJGKzVZOUxKTkVKd05zMXFmckN2Il19; idl_env=Ana6VJdVJDdUkt64uhv51XUMS4paC9mf7PILw6Bls5Ngr_KFnjfOqKkXGg-B5arHWd0dGfQmCBnjIO4LKOBg53HtW6PbAplmJDvlkFBl-oqmVR4H8yKiTvajtcx0iIT7vKifdTFiCL6XpAuumrbBsLP2fKldPVxdIZKhRBxVLbLJfF_CBzcq4q9pY-FCb0zqqI0FutbL; idl_env_last=Tue%2C%2014%20May%202024%2017%3A39%3A44%20GMT; __gads=ID=1201ec5081d45d97:T=1715698765:RT=1715709743:S=ALNI_MbIPreuJZeUdzRl2rAwNBdu87CpHA; __gpi=UID=00000a26ba7978d0:T=1715698765:RT=1715709743:S=ALNI_Mbt1mRjHIVPq0NuqhGhi5B9u33hVg; __eoi=ID=aa7a7e87262c84e3:T=1715698765:RT=1715709743:S=AA-AfjZswejDwnWmBID1JLR8zz3R; __cf_bm=fdlGntbiXEgLGOOYMmcaqqsw9tMpdFer5RorGElw3JI-1715709818-1.0.1.1-DTfSFCtX4w7Mu7KOp2rhJUBJwHw2f8F8Q9O9D0U7BFt.WPzWfAgR.et8f7.k.nTmcXMLXqnWyRgcQnV79Wl62g; _ga=GA1.3.603674138.1715698764; ___iat_vis=2E9DD10A23260BCF.5597f7f48e07ee4e38ecedc59d2e73bb.1715709821676.06e7716d55239db9683020a11c452cca.ORJBIJARMA.11111111.1.0; _ga_50C013M2CC=GS1.1.1715707133.2.1.1715709823.54.0.0; cto_bundle=P_DSC19TZjBGeFJhdlpDMmlUZmhJMm4xb2plVGFLaGw4a0NZRGJVOTlMUFlXUklPbEhqRnlPM1pUSmklMkZCJTJGT2ZzN3pEY2tUNXVLcERGcllValBQYmhyMUcwQk9mT294MVRIQTZ4d0FPblVLUzlVbWNrRmJxZmk1WDRPd0NyNERsNDBPUVF6bEElMkI2MW85TVBnUEZBQSUyQjRPeU0yUSUzRCUzRA; cto_bidid=zUfaZF8zdE12cVNsa3l4NUpBcHFOdlJUMkR5RUFFZkpKTlV4bU0lMkZsQWdEemlTbUFYcFg5alkzb3pneGJEUmtCQXlGbDM3NmZySnAxUDlPMlVNJTJGN1k5UGR5bzNhZXdKRmFoWU9HbSUyRno0M09YMXY3cyUzRA; cto_dna_bundle=nOW9R180M0RITmhlJTJCZkMwOUJGQlhaMUN2c3l2dmFDSnE3eE95YSUyQmI1ZENOSGdDYTRXb0lIZSUyRmxlb01rdkJpcFl0c3dX; _dd_s=rum=0&expire=1715711083917",
    "If-None-Match": "\"bn8g9fnluvxjty\"",
    "Priority": "u=0, i",
    "Referer": "https://www.olx.com.br/imoveis/venda/casas/estado-ce/fortaleza-e-regiao",
    "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
}

driver.maximize_window()

max_pag = 50
count = 1
casas = []

while(count <= max_pag and url != None):
    driver.get(url)
    url = None

    try:
        xpath_button = '/html/body/div[1]/div[1]/main/div[1]/div[2]/main/div[3]/div[1]/div[2]/button[2]'
        button = driver.find_element(By.XPATH, xpath_button)

        button.click()
    except:
        pass

    while(not chegou_ao_fim()):
        webdriver.ActionChains(driver).scroll_by_amount(0, 700).perform()

        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # section = []
        elements = soup.find_all('section', attrs={
            'data-ds-component': True,
            'data-ds-component': 'DS-AdCard'
        })

        for e in elements:
            for class_parent in [parent.get('class', []) for parent in e.parents if parent.name == 'div']: 
                if('sc-a8d048d5-2' in class_parent):
                    #PRECO, IPTU, CONDOMINIO=========================
                    div_preco = e.find('div', attrs={
                        'class':lambda x: x =='olx-ad-card__details-price--vertical' or x == 'olx-ad-card__details-price--horizontal'
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
                        
                        if ' '.join(p['class']) == 'olx-text olx-text--caption olx-text--block olx-text--regular':
                            regiao = text
                        
                        if 'date' in ' '.join(p['class']):
                            data = text.split(',')
                            
                            if data[0].lower() == 'hoje':
                                data[0] = datetime.datetime.now().strftime("%d/%m/%y")
                            elif data[0].lower() == 'ontem':
                                data[0] = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d/%m/%y")
                            
                            data[1] = data[1].strip()
                            data = '-'.join(data)
                            

                    casa = {
                        'preco': preco,
                        'iptu': iptu,
                        'condominio': condominio,
                        'metro_quadrado': metro_quadrado,
                        'quarto': quarto,
                        'banheiro': banheiro,
                        'garagem': garagem,
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
    
    count += 1


df = pd.DataFrame(casas)

print(df)

df.to_csv('casas.csv', sep=';', index=False)

driver.close()

