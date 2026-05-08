
# Crawler de Notícias dos Municípios Baianos

Script automatizado para monitoramento de notícias relacionadas a corrupção, fraudes, operações policiais e irregularidades em municípios da Bahia através do Google News e outras fontes. Desenvolvido para apoiar o trabalho de análise do Tribunal de Contas dos Municípios da Bahia (TCM-BA).

## Descrição

Este script realiza buscas automatizadas no Google News e outras fontes sobre diversos temas relacionados a irregularidades administrativas e operações policiais nos municípios da Bahia. Ele utiliza:

- Selenium para automação do navegador
- BeautifulSoup para extração dos dados
- Processamento de linguagem natural para identificação de municípios
- Pandas para manipulação e exportação dos dados


## Funcionalidades

- Busca automática por termos passados através de um arquivo ```.txt```
- Identificação inteligente de municípios citados nas notícias, com lógica aprimorada:
   - Pré-processamento dos textos para remoção de sufixos como "(BA)", "- BA", etc.
   - Detecção de contexto geográfico para evitar falsos positivos em nomes ambíguos (ex: "Glória", "Saúde", "Vitória")
   - Tratamento especial para municípios compostos (nomes com mais de uma palavra)
   - Utilização de modelo spaCy para extração inicial e múltiplos filtros contextuais
- Tratamento de palavras ambíguas para evitar falsos positivos
- Normalização e validação de datas de publicação
- Coleta de metadados completos (título, conteúdo, fonte, data, link, imagem)
- Eliminação automática de notícias duplicadas
- Exportação organizada em Excel

## Requisitos

- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome
- Pacotes Python listados em requirements.txt

Obs.: Para instalar o ChromeDriver, baixe a versão compatível com seu Chrome [aqui](https://developer.chrome.com/docs/chromedriver/get-started?hl=pt-br#setup) e adicione ao PATH do sistema ou coloque no diretório do script.

## Instalação

```
pip install -r requirements.txt
```

```
python -m spacy download pt_core_news_lg (ou pt_core_news_sm para um tamanho menor)
```

## Como usar


1. Certifique-se de que o ChromeDriver está configurado corretamente
2. Execute o script principal:

```
python .\src\main.py -t <caminho_para_arquivo_txt_com_termos_de_pesquisa> -s <nome_do_arquivo_de_saida> [-f <fontes>] [-p <proxy>] [-db <database>]
```

Exemplos:
```
# Buscar apenas no Google News (padrão) sem proxy e sem banco de dados
python .\src\main.py -t .\src\termos_pesquisa\termos_para_pesquisa.txt -s saida

# Buscar em múltiplas fontes (Google News e Portal A Tarde)
python .\src\main.py -t .\src\termos_pesquisa\termos_para_pesquisa.txt -s saida -f google_news portal_atarde

# Executar com uso de proxy e persistência em banco de dados
python .\src\main.py -t .\src\termos_pesquisa\termos_para_pesquisa.txt -s saida -p true -db true
```

O parâmetro `--fonte` ou `-f` permite especificar uma ou mais fontes de notícias suportadas. Se não for informado, o padrão é `google_news`. As opções atuais são:
- `google_news`
- `portal_atarde`

O parâmetro `--proxy` ou `-p` permite especificar se o script deve utilizar as configurações de proxy definidas no `.env`. O valor padrão é `false`. Exemplo: `-p true`.

O parâmetro `--database` ou `-db` permite especificar se o script deve realizar a persistência das notícias encontradas em um banco de dados (também configurado via `.env`). O valor padrão é `false`. Exemplo: `-db true`.

O parâmetro `--gerar-banco` é utilizado para criar automaticamente as tabelas necessárias (`NOTICIAS_MUNICIPIOS` e `LOG_EXECUCAO_NOTICIAS`) no banco de dados configurado no `.env`. Ele deve ser executado antes da primeira utilização do script com persistência ativada. Ao executar com esta flag, o script encerra após a criação/validação da estrutura. Exemplo: `python .\src\main.py --gerar-banco`.

Para mais detalhes ou ajuda utilize: ```python .\src\main.py --help```

3. O script irá, se executado sem argumentos:
   - Buscar notícias para múltiplos termos de pesquisa
   - Processar e identificar municípios citados
   - Coletar metadados completos
   - Salvar os resultados em `nome_arquivo_de_saida_(timestamp).xlsx`

## Saída

O arquivo `nome_arquivo_de_saida_(timestamp).xlsx` contém as seguintes informações para cada notícia:

- Título
- Conteúdo
- Municípios citados
- Fonte
- Data de publicação
- Link
- URL da imagem
- Palavra-chave utilizada na busca

## Exemplo de execução


``` 
Buscando notícias para: Desvio Milionário Bahia
Acessando: https://news.google.com/search?q=Fraude+Licitação+Bahia&hl=pt-BR&gl=BR&ceid=BR%3Apt-419
Notícias encontradas na página: 101
============================================== NOTÍCIA ===================================================
TÍTULO: Justiça Federal condena ex-prefeito de Riacho de Santana por desvio milionário do Fundeb
CONTEÚDO: Conteúdo não encontrado...
MUNICÍPIOS CITADOS (1): Riacho de Santana-2926400
FONTE: Agência Sertão
DATA: 04/09/2019
LINK: https://news.google.com/./read/CBMi1AFBVV95cUxNSGswUm9RUlRFR2Q1X0Z3bjFBalV5MVNVLXdES0tia1U4N25fMUhZOUdBRjFlclc1aDBZcnFwYzNQTEY3bEo3MV9DV181S1lxYWRFdEs0Z2MtRmNaeWtEQ3pzRnZGak1oeUl5QksxdlRNcG83Vlc1Tm0ydUN6TUdSOHFLdFdmS0lFZkl4UUswZHMxV1VPVlB0cHA0Qlh3RDUxbDhwRm5JOGRZbVVhUG9BZUQ4U2JUd29UTzBFY1UyYlI1blZwelVQalAzUjBzSTl5RUlVVtIB2gFBVV95cUxQaGdOZVRrLXJUM0V6X04taW9pTjEwbXQ3SU5OZGdCR29IS04xWUxKdFdweTFHWksyLXBwSWlxeG1ENkxOcnFTLV9TdDRzcHBpbWlOLTlrVVZuc3Z2VGh4c3lwV0VXR0xmRnBxbjhWcTVRY2JrVF9PUXNxOGVDRUpCSEtvTFAweEpXdjJ3V0UzeXlkQXp0N3V2ZkNMQTlWUUNTR1NnT2JxV2JveU9BQzduZkl3OXI5dk9hMXFHOFA2SVZaYVY0OVRFX21JMDg4ZDloTl8xV3Y0X2Rudw?hl=pt-BR&gl=BR&ceid=BR%3Apt-419
IMAGEM: https://news.google.com/api/attachments/CC8iJ0NnNTRlWEk0VDNCZk56QnBXak42VFJDa0F4amJCU2dLTWdNQmNRUQ=-w200-h112-p-df-rw
PALAVRA-CHAVE: Desvio Milionário Bahia
```


## Observações

- O script utiliza modo headless (sem interface gráfica) para melhor performance
- Inclui tratamento robusto de erros e timeouts
- Implementa scroll automático para carregar mais notícias
- Possui sistema inteligente para evitar duplicatas
- Realiza validação e normalização de dados
- A lógica de detecção de municípios foi aprimorada para:
   - Remover sufixos e padronizar nomes antes da extração
   - Verificar se nomes ambíguos aparecem em contexto geográfico (ex: "Prefeitura de Glória", "em Vitória")
   - Ignorar menções genéricas a "Bahia" e outros termos não relevantes
   - Priorizar o contexto do texto e do título para maior precisão
   - Tratar corretamente municípios compostos, evitando duplicidade de componentes

## Autor

Hugo Rios Brito
