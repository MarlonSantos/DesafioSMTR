import requests
import time

API_URL = 'https://api.dados.rio/v2/adm_cor_comando/procedimento_operacional_padrao_orgaos_responsaveis/'
# adm_cor_comando/ocorrencias_orgaos_responsaveis/

# {'ocorrencias_orgaos_responsaveis': 'https://api.dados.rio/v2/adm_cor_comando/ocorrencias_orgaos_responsaveis/', 
# 'procedimento_operacional_padrao_orgaos_responsaveis': 'https://api.dados.rio/v2/adm_cor_comando/procedimento_operacional_padrao_orgaos_responsaveis/', 
# 'ocorrencias': 'https://api.dados.rio/v2/adm_cor_comando/ocorrencias/', 
# 'ocorrencias_abertas': 'https://api.dados.rio/v2/adm_cor_comando/ocorrencias_abertas/', 
# 'pops': 'https://api.dados.rio/v2/adm_cor_comando/pops/'
 
def check_for_new_data(evento_id):
    API_URL = f'https://api.dados.rio/v2/adm_cor_comando/ocorrencias_orgaos_responsaveis/?eventoId={evento_id}'
    # API_URL = 'https://api.dados.rio/v2/adm_cor_comando/ocorrencias/?eventoId={evento_id}&orgaoResponsavelId={orgao_responsavel_id}'

    # API_URL ='https://api.dados.rio/v2/adm_cor_comando/ocorrencias_orgaos_responsaveis/?eventoId=98811'
    # API_URL = 'https://api.dados.rio/v2/adm_cor_comando/procedimento_operacional_padrao_orgaos_responsaveis/?popId=1'
    # API_URL = 'https://api.dados.rio/v2/adm_cor_comando/ocorrencias/?inicio=2023-07-02 00:00:00.0&fim=2023-07-04 23:59:59.0'

    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        # Process the data as per your requirements
        # ...
        # Example: Print the data
        print(data)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# if __name__ == '__main__':
#     while True:
#         check_for_new_data()
#         time.sleep(60)  # Wait for 60 seconds before making the next request
check_for_new_data(98867)

# {'tipo': 'PRIMARIO', 
# 'pop_id': 1, 
# 'bairro': 'Barra da Tijuca', 
# 'latitude': -23.0076006, 
# 'inicio': '2023-07-04 13:29:31.0', 
# 'titulo': 'AC 2 VPs', 
# 'fim': '2023-07-04 13:53:43.0', 
# 'prazo': 'CURTO', 
# 'descricao': 'Av. das Américas - Alt. BRT Guiomar de Novaes - Recreio - Sent. Santa Cruz', 
# 'informe_id': 98867, 
# 'gravidade': 'BAIXO', 
# 'id': 98866, 
# 'longitude': -43.4381311, 
# 'status': 'FECHADO'}