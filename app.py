from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import re

driver = webdriver.Chrome()

def extrair_descricoes_e_enviar_curriculo(termo_pesquisa):
    driver.get(f'https://www.classitudodiariodaregiao.com.br/empregos&s={termo_pesquisa}')
    sleep(3)

    elementos = driver.find_elements(By.CLASS_NAME, 'descricao')

    descricoes = []
    emails = []

    for elemento in elementos:
        texto = elemento.text
        descricoes.append(texto)

        matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', texto)

        if matches:
            emails.extend(matches)
        else:
            continue

    df = pd.DataFrame({'Descrição da Vaga': descricoes, 'E-mail': emails})
    df.to_excel(f'dados_vagas_{termo_pesquisa}.xlsx', index=False)


    enviar_curriculo_para_emails(emails)

def enviar_curriculo_para_emails(emails):
    remetente_email = 'no-reply@gmail.com'
    senha = 'aaah rá achou que eu ia deixar a senha né?'
    assunto = 'Currículo para a vaga'

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente_email
    mensagem['Subject'] = assunto

    corpo_mensagem = 'Segue curriculo para a vaga anunciada no diario web.'
    mensagem.attach(MIMEText(corpo_mensagem, 'plain'))

    curriculo_path = 'C:/Users/thiago.cardoso/Documents/Matheus.python/esseaqui.jpg'
    curriculo_anexo = MIMEApplication(open(curriculo_path, 'rb').read())
    curriculo_anexo.add_header('Content-Disposition', 'attachment', filename=os.path.basename(curriculo_path))
    mensagem.attach(curriculo_anexo)

    servidor_smtp = smtplib.SMTP('Servidor gato', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(remetente_email, senha)

    for destinatario_email in emails:
        mensagem['To'] = destinatario_email
        servidor_smtp.sendmail(remetente_email, destinatario_email, mensagem.as_string())

    servidor_smtp.quit()

termos_pesquisa = ['estagiario', 'programador', 'vendedor']

for termo in termos_pesquisa:
    extrair_descricoes_e_enviar_curriculo(termo)

driver.quit()
