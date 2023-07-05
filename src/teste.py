import pandas as pd
import json
# q =  [{"titulo": "Engui\u00e7o CM", "status": "FECHADO", "datetime": "2023-07-05 13:48:07", "quantidade_ocorrencia": 2}, {"titulo": "Obra na via ( CET RIO )", "status": "FECHADO", "datetime": "2023-07-05 13:48:08", "quantidade_ocorrencia": 2}, {"titulo": "AC 2 VPs", "status": "FECHADO", "datetime": 
# "2023-07-05 13:48:08", "quantidade_ocorrencia": 2}, {"titulo": "AC VP x MT", "status": "FECHADO", "datetime": "2023-07-05 13:48:09", "quantidade_ocorrencia": 2}, {"titulo": "AC 2 MTs", "status": "FECHADO", "datetime": "2023-07-05 13:48:09", "quantidade_ocorrencia": 2}, {"titulo": "AC ON x MT",     
# "status": "FECHADO", "datetime": "2023-07-05 13:48:10", "quantidade_ocorrencia": 1}, {"titulo": "Animal na via", "status": "FECHADO", "datetime": "2023-07-05 13:48:10", "quantidade_ocorrencia": 4}, {"titulo": "AC VP x MT", "status": "FECHADO", "datetime": "2023-07-05 13:48:11",
# "quantidade_ocorrencia": 2}, {"titulo": "AC VP x MT", "status": "FECHADO", "datetime": "2023-07-05 13:48:13", "quantidade_ocorrencia": 1}, {"titulo": "AC CM x TX", "status": "FECHADO", "datetime": "2023-07-05 13:48:13", "quantidade_ocorrencia": 2}, {"titulo": "Queda MT", "status": "FECHADO",       
# "datetime": "2023-07-05 13:48:14", "quantidade_ocorrencia": 2}, {"titulo": "AC VP x MT", "status": "FECHADO", "datetime": "2023-07-05 13:48:15", "quantidade_ocorrencia": 2}, {"titulo": "AC VP x MT", "status": "FECHADO", "datetime": "2023-07-05 13:48:15", "quantidade_ocorrencia": 2}, {"titulo": "AC 
# 2 VPs", "status": "FECHADO", "datetime": "2023-07-05 13:48:16", "quantidade_ocorrencia": 2}, {"titulo": "AC TX x 2 VPs", "status": "FECHADO", "datetime": "2023-07-05 13:48:16", "quantidade_ocorrencia": 2}, {"titulo": "AC ON x VP", "status": "FECHADO", "datetime": "2023-07-05 13:48:17",
# "quantidade_ocorrencia": 2}, {"titulo": "AC 3 VPs", "status": "FECHADO", "datetime": "2023-07-05 13:48:17", "quantidade_ocorrencia": 2}]
p =  [{"titulo": "Engui\u00e7o CM", "status": "FECHADO", "datetime": "2023-07-05 13:48:07", "quantidade_ocorrencia": 2}]#, {"titulo": "Obra na via ( CET RIO )", "status": "FECHADO", "datetime": "2023-07-05 13:48:08", "quantidade_ocorrencia": 2}, {"titulo": "AC 2 VPs", "status": "FECHADO", "datetime": 

df = pd.json_normalize(p)
print (df)