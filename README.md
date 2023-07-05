# Desafio: Reporte de Ações de Mitigação de Ocorrências da Cidade 


## Introdução

Repositório para resolução do desafio da seleção para o cargo de engenheiro de dados da Secretaria Municipal de Transportes.

## Configurações do Usuário, Utilização & Informações Relevantes

Os parâmetros default de configuração são:
* Periodicidade: 20 minutos
* Pasta de criação do CSV: mesma pasta do App.py
* Nome do aqruivo CSV: OcorrenciasCETRIO.csv

Eles podem ser reconfigurados dentro do programa (opção "c").
Ao reconfigurar, caso deixe o prompt em branco, será utilizado o parâmetro default.


Rodar o arquivo App.py com o interpretador Python.

obs.: requirements.txt com dependências presente na pasta raíz.


Ao fazer uma nova consulta, o programa atualiza os status e a data de consulta das entradas antigas no CSV, caso haja mudança de status.

O intervalo de tempo (periodicidade) é contada a partir da conclusão da última iteração.

## Operação:

O programa consulta o endpoint https://api.dados.rio/v2/adm_cor_comando/ocorrencias/ para coletar as ocorrências.
Com esses dados, é feita a consulta linha a linha no endpoint https://api.dados.rio/v2/adm_cor_comando/ocorrencias_orgaos_responsaveis/ para a complementação das informações (dados de órgãos responsáveis).
Com todas os dados coletados é feito o cálculo de quantidade de ocorrências por dado coletado. Depois é feita a consulta no arquivo CSV (caso não seja a primeira rodada) pegando os dados legados e comparando-os via 'id' com os dados novos.
Caso para um mesmo id haja mudança de status, o dado será atualizado no CSV, assim como sua data de consulta. os demais dados novos serão incluídos no CSV e será iniciada a espera do período para que a nova iteração aconteça. 


## Referências Rápidas:

### src:
* Pasta contendo o [`código fonte`](./src/App.py).
### docs:
* Pasta contendo o [`enunciado do desafio`](./docs/Desafio.txt) e o [`diagrama solicitado`](./docs/Diagrama.pptx).

###

Espero que gostem e obrigado pela oportunidade.
