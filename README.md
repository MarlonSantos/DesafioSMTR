# Desafio: Reporte de Ações de Mitigação de Ocorrências da Cidade 


## Introdução

Repositório para resolução do desafio da seleção para o cargo de engenheiro de dados da Secretaria Municipal de Transportes.

## Informações Relevantes

1. A resolução das questões (itens 1 ao 3) está no arquivo: [`Resolução.md`](Resolução.md);
2. A análise dos dados encontra-se no arquivo: [`DataAnalisys.ipynb`](./Data_Analysis/DataAnalisys.ipynb);
3. Para o item 4, há o server [`DataSourceSim.py`](./App/DataSourceSim.py) e o client [`FraudDetector.py`](./App/FraudDetector.py); 
4. O cliente usa um banco MySQL localizado na Google CLoud. As análises de novos dados baseiam-se nos dados já recebidos, que são populados neste banco;
5. A análise utilizada para o modelo de Machine Learning encontra-se no arquivo: [`MachineLearning.ipynb`](./Data_Analysis/MachineLearning.ipynb);
6. Rule-based: foram utilizados todos as 3 checagens solicitadas no case; 
7. Score-based: foi utilizado o método "Random Forest" para a classificação; 
8. Foi desenvolvido um modelo híbrido de detecção, conforme permitido pelo case. O score serve de filtro para as transações que saem aptas do crivo do rule-based.


## Configurações do Usuário & Utilização

* O client inscreve-se em um canal via websockets enviando um json com parâmetro `"method": "subscribe"`, pode ser configurada duas formas de envios de dados: dados existentes no [`dataset`](./Data_Sources/transactional-sample.csv) ou dados fictícios gerados por um simulador implementado junto ao server. Para escolher o modo de envio de dados basta colocar a opção no parâmetro `"srctype"` (`"csv"` ou `"sim"`, respectivamente). Poderá ser escolhido o delay de envio, inicialmente em 0.8s, no parâmetro `"delay"`. Caso haja necessidade de usar dados de outro .csv, basta configurar  `"source"`. `'clearlegacy'` igual à "true", no modo csv, limpará o banco e começará a coleta da primeira linha do dataset, ao contrário continuará da última entrada. Já no modo simulador serão enviadas 100 transações fictícias;

 
* A tolerância para a aceitação do score-based pode ser configurada, foi usado o valor de 0.5 como padrão.


## Referências Rápidas:

### src:
* Pasta contendo o código fonte.

### App folder:
* DataSourceSim.py:  Server that takes data from .csv and build a websocket channel to stream data.
* FraudDetecor.py:  Connects to server, get almost real-time data and validate the transaction.

###

Espero que gostem e obrigado pela oportunidade.# DesafioSMRT
Minha solução para o desafio do processo de seleção para Engenheiro de Dados da SMTR  
