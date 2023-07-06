import requests
from prefect import flow, task, get_run_logger  
import json
import time  
from datetime import datetime as dt
import datetime
import typer
from rich import print
from rich.prompt import Prompt
from rich.style import Style
from rich.progress import (BarColumn,Progress,SpinnerColumn,TaskProgressColumn,TimeElapsedColumn,)
import pandas as pd
from os.path import exists
import os
import schedule

#--------------------------------- Extraction -------------------------------#
#>>> Extrai dados de ocorrências <<<#
@task (name="Obtenção de dados de ocorrências ", retries=12, retry_delay_seconds=5, log_prints=True)
def occ_data(startdate, enddate):
    API_URL = f'https://api.dados.rio/v2/adm_cor_comando/ocorrencias/?inicio={startdate}&fim={enddate}'
    response = requests.get(API_URL)
    print(response.status_code)
    data = response.json()
    return data

#>>> Consulta órgãos responsáveis <<<#
@task (name="Obtenção de órgãos responsáveis ", retries=5, retry_delay_seconds=2, log_prints=True)
def get_responsibles(occ,orgao):
    
    def resp_data(eventoId):
        API_URL = f'https://api.dados.rio/v2/adm_cor_comando/ocorrencias_orgaos_responsaveis/?eventoId={eventoId}'
        response = requests.get(API_URL)
        print(response.status_code)
        data = response.json()
        return data
  
    conc_data = []
    if 'eventos' in occ:
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
@task (name="Filtro de dados ", log_prints=True)
def filter_data(raw_data):
    format = { 'id','observed_epoch', 'titulo', 'status', 'orgaos_responsaveis_ativ'}
    fil_data = []
    for line in raw_data:
        filtered_row = { key:value for key,value in line.items() if key in format}
        timestamp = dt.fromtimestamp(filtered_row['observed_epoch'])
        filtered_row['datetime'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        filtered_row['quantidade_ocorrencia'] = len(filtered_row['orgaos_responsaveis_ativ'])
        filtered_row.pop('orgaos_responsaveis_ativ')
        filtered_row.pop('observed_epoch')
        fil_data.append(filtered_row)
    return fil_data

#----------------------------------- Load -----------------------------------#
@task (name="Carregamento de dados ", log_prints=True)
def load_data(processed_data, filename, path):
    file = os.path.join(path, filename + '.csv')
    dfNew = pd.json_normalize(processed_data)
    if exists(file):
        dfLegacy  = pd.read_csv(file)
        # dfLegacy.loc[dfLegacy['id']==dfNew['id'],'status'] = dfNew['status']
        df_diff = pd.concat([dfLegacy, dfNew],ignore_index=True).drop_duplicates() 
        df_diff.to_csv(file, index=False, header=True)       
    else:
        dfNew.to_csv(file, index=False, header=True )
    
#--------------------------------- Pipeline ---------------------------------#
@flow (log_prints=True)
def pipeline(start,end,orgao):
    t = datetime.datetime.now()
    print(f"[grey74]{t.strftime('%H:%M:%S.%f')[:-3]}[/grey74] | [deep_sky_blue2]INFO[/deep_sky_blue2]    |[bold {prt}] Iniciando nova consulta, por favor aguarde.")
    nodata = False
    data = occ_data(start,end)
    if 'eventos' in data:
        if len(data['eventos']) == 0:
            nodata = True
        else:    
            concatened_data = get_responsibles(data, orgao)
            filtered_data = filter_data(concatened_data)
            load_data(filtered_data, name, path)
            print(f"[grey74]{t.strftime('%H:%M:%S.%f')[:-3]}[/grey74] | [deep_sky_blue2]INFO[/deep_sky_blue2]    |[bold {prt}] Consulta realizada.")
    else:
        nodata = True   

    if nodata == True: 
        t = datetime.datetime.now()
        print(f"[grey74]{t.strftime('%H:%M:%S.%f')[:-3]}[/grey74] | [deep_sky_blue2]INFO[/deep_sky_blue2]    |[bold {prt}] Não há eventos para o período selecionado.")


#------------------------------------ CLI -----------------------------------#
clr = 'blue'
prt = 'green'
path = os.getcwd()
name = "OcorrenciasCETRIO"
periodo = 20 #minutes

def configurar():
    global path, name, periodo
    name = Prompt.ask(f"[{prt}]Nome para o arquivo CSV")
    if name == "": name = "OcorrenciasCETRIO"
    print(f"nome: {name}.csv")
    path_try = Prompt.ask(f"[{prt}]Caminho o arquivo CSV")
    if path_try == "": 
        path = os.getcwd()
    else:
        if os.path.exists(path_try) == False:
            print(f"[red]Caminho não encontrado, verifique se o caminho está correto e tente configurar novamente.[/red]") 
        else:
            path = path_try
    print(f"caminho: {path}".replace("\\","/"))        
    per_try = Prompt.ask(f"[{prt}]Periodicidade [min]")
    if per_try.isnumeric():
        periodo = int(per_try)
    else:
        print(f"[red]Valor não numérico, verifique e tente configurar novamente.[/red]") 
    print(f"período:{periodo}")
    print(f"")
    print(f"[{prt}]Configurado.")
    print(f"")

def ajuda():
    print("")
    print("[bold {clr}]Ajuda:")
    print("_______________________________________________________________")
    print("")
    print("'Iniciar pipeline': começará o ciclo contínuo de coleta de dados, com a periodicidade configurada.")
    print("'Configurar': permite confugrar parâmetros de funcionamento do pipeline.")
    print("'Sair': encerra o programa.")
    print("_______________________________________________________________")
    print("")
    print("Periodicidade configurada [min]:")
    print(periodo)
    print("")
    print("Caminho configurado:")
    p = path.replace("\\","/")
    print(f"{p}/{name}.csv")  

    print("")
#----------------------------------- Main -----------------------------------#
def main():
    print(f"[bold {clr}]🚧 🚗🚐🚙🚌           Secretaria Municipal de Transportes - SMTR          🚓🚕🚛🛻[/bold {clr}]")
    print(f"[bold {clr}]🚧 🚗🚐🚙🚌                       Pipeline CET-RIO                        🚓🚕🚛🛻[/bold {clr}]")
    print("")
    while True:
        print(f"Pressionar 'enter': Iniciar pipeline | 'x' :sair | 'c': configurações | 'a': ajuda")
        cmd = Prompt.ask(f"[{prt}]>")

        match cmd:
            case "a":
                ajuda()
                continue
            case "x":
                break
            case "exit":
                break
            case "c":
                configurar()
            case "":
                # pipeline('2023-07-07 06:55:00.0', '2023-07-07 08:59:59.0', 'CET-RIO')
                # pipeline('2023-07-04 15:55:00.0', '2023-07-04 23:59:59.0', 'CET-RIO')
                # pipeline('2023-07-04 15:55:00.0', '2023-07-04 16:00:59.0', 'CET-RIO')
                pipeline('2023-07-05 06:55:00.0', '2023-07-05 7:59:59.0', 'CET-RIO')


                schedule.every(periodo).minutes.do(lambda: pipeline('2023-07-05 06:55:00.0', '2023-07-05 7:59:59.0', 'CET-RIO'))
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            case "enter": 
                pipeline('2023-07-07 06:55:00.0', '2023-07-07 08:59:59.0', 'CET-RIO') 
                schedule.every(periodo).minutes.do(lambda: pipeline('2023-07-05 06:55:00.0', '2023-07-05 7:59:59.0', 'CET-RIO'))
                while True:
                    schedule.run_pending()
                    time.sleep(1)            

            case _:
                print("")
                print("Comando desconhecido, digite 'help' para ver a lista de completa de comandos.")
                print("'exit' para sair.")
                print("")
                continue

if __name__ == "__main__":
    typer.run(main)
    