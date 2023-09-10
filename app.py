from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep

# Extrair descrições de uma página com base no termo de pesquisa
def extrair_descricoes(termo_pesquisa):
    driver.get(f'https://www.classitudodiariodaregiao.com.br/empregos&s={termo_pesquisa}')
    sleep(3)

    # Localiza todos os elementos que contêm as descrições de vagas
    elementos = driver.find_elements(By.CLASS_NAME, 'descricao')

    # Cria uma lista para armazenar as descrições
    descricoes = []

    # Itere pelos elementos e extraia as descrições
    for elemento in elementos:
        texto = elemento.text
        descricoes.append(texto)

    # Cria um DataFrame com as descrições
    df = pd.DataFrame({'Descrição da Vaga': descricoes})

    # Exporta o DataFrame para o Excel
    df.to_excel(f'dados_vagas_{termo_pesquisa}.xlsx', index=False)

# Inicialize o driver do Chrome
driver = webdriver.Chrome()

# Termos de pesquisa
termos_pesquisa = ['estagiario', 'admin', 'vendedor']

# Extrair descrições para cada termo de pesquisa
for termo in termos_pesquisa:
    extrair_descricoes(termo)

# Feche o driver do Chrome quando terminar
driver.quit()
