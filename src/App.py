import requests
from prefect import flow, task  
import time  
from datetime import datetime

#--------------------------------- Extraction -------------------------------#
#>>> Extrai dados de ocorrências <<<#
@task (name="Obtenção de dados de ocorrências ", retries=12, retry_delay_seconds=5)
def occ_data(startdate, enddate):
    API_URL = f'https://api.dados.rio/v2/adm_cor_comando/ocorrencias/?inicio={startdate}&fim={enddate}'
    response = requests.get(API_URL)
    data = response.json()
    return data

#>>> Consulta órgãos responsáveis <<<#
@task (name="Obtenção de órgãos responsáveis ", retries=5, retry_delay_seconds=2)
def get_responsibles(occ,orgao):
    
    def resp_data(eventoId):
        API_URL = f'https://api.dados.rio/v2/adm_cor_comando/ocorrencias_orgaos_responsaveis/?eventoId={eventoId}'
        response = requests.get(API_URL)
        data = response.json()
        return data
    
    conc_data = []
    for entry in occ['eventos']:
        linha = []
        entry['observed_epoch'] = time.time()
        evento_id = entry.get('id')
        resp_orgs = resp_data(evento_id)
        if 'atividades' in resp_orgs:
            atividades = resp_orgs['atividades']
            for item in atividades:
                if item['orgao'] == orgao:
                    linha.append(item)
            if len(linha) > 0: 
                entry['orgaos_responsaveis_ativ']=linha
                conc_data.append(entry)
    return conc_data 
#------------------------------ Transformation ------------------------------#
@task (name="Filtrando dados ")
def filter_data(raw_data):
    format = { 'observed_epoch', 'titulo', 'status', 'orgaos_responsaveis_ativ'}
    for line in raw_data:
        filtered_row = { key:value for key,value in line.items() if key in format}
        timestamp = datetime.fromtimestamp(filtered_row['observed_epoch'])
        filtered_row['datetime'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        filtered_row['quantidade_ocorrencia'] = len(filtered_row['orgaos_responsaveis_ativ'])
        filtered_row.pop('orgaos_responsaveis_ativ')
        filtered_row.pop('quantidade_ocorrencia')
        print(filtered_row)
        print(type(filtered_row))
        return filtered_row

#----------------------------------- Load -----------------------------------#
@flow (log_prints=True) #>>> Pipeline <<<#
def pipeline(start,end,orgao):
    data = occ_data(start,end)
    concatened_data = get_responsibles(data, orgao)
    filtered_data = filter_data(concatened_data)
    # print(filtered_data)
    # print(type(filtered_data))


if __name__ == "__main__":
    pipeline('2023-07-04 15:55:00.0', '2023-07-04 23:59:59.0', 'CET-RIO')