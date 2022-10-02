import datetime
import json
import os
import time

import pandas as pd
import requests

from whatsapp import WhatsApp


def make_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None


def main():
    HORA_ATUAL = datetime.datetime.now()
    HORA_ATUAL = str(HORA_ATUAL.strftime("%d/%m/%Y %Hh%M"))
    
    # Presidente - Brasil Consolidado
    URL = 'https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r.json'

    # Senador SP
    # URL = 'https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp-c0005-e000546-r.json'

    # Governador SP
    # URL = 'https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp-c0003-e000546-r.json'

    # Deputado Federal SP
    # URL = 'https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp-c0006-e000546-r.json'

    # Deputado Estadual SP
    # URL = 'https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp-c0007-e000546-r.json'

    response = make_request(URL)

    json_data = json.loads(response)
    canditados = []
    partidos = []
    votos = []
    porcentagem = []

    seções_finalizadas = str(json_data['pst']).replace(',', '.') + '%'

    for infos in json_data['cand']:
        if str(infos['nm']).startswith('FELIPE'):
            canditados.append('FELIPE D\'AVILA')
            votos.append(infos['vap'])
            partidos.append(infos['cc'])
            porcentagem.append(infos['pvap'])  

        else:
            canditados.append(infos['nm'])
            votos.append(infos['vap'])
            partidos.append(infos['cc'])
            porcentagem.append(infos['pvap'])

    # df_eleicao = pd.DataFrame(list(zip(canditados, partidos, votos, porcentagem)), columns = ['Candidato', 'Partido', 'Votos', 'Porcentagem'])
    df_eleicao = pd.DataFrame(list(zip(canditados, votos, porcentagem)), columns = ['Candidato', 'Votos', 'Porcentagem'])
    df_eleicao['Votos'] = df_eleicao['Votos'].astype(int)
    df_eleicao['Porcentagem'] = df_eleicao['Porcentagem'].apply(lambda x: x.replace(',', '.'))
    df_eleicao['Porcentagem'] = df_eleicao['Porcentagem'].astype(float)
    df_eleicao = df_eleicao.sort_values('Porcentagem', ascending=False)
    print(df_eleicao.head(10))

    total = df_eleicao['Votos'].sum()
    print(f'\nTotal de votos: {total}')
    print(f'Seções finalizadas: {seções_finalizadas}')
    
    # Mandar no WhatsApp
    mensagem = HORA_ATUAL + '\n\n'
    for index, row in df_eleicao.iterrows():
        mensagem_aux = f'{row["Candidato"]} - {row["Porcentagem"]}%\n'
        mensagem += mensagem_aux

    mensagem += f'\nSeções finalizadas: {seções_finalizadas}'

    messenger = WhatsApp()
    messenger.find_by_username('Eu mesmo')
    time.sleep(5)
    messenger.send_message(mensagem)
    time.sleep(5)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
