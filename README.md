# Cálculo do Índice de Similaridade à Terra (ESI) para Exoplanetas

Este projeto é uma aplicação em Python que permite calcular o **Índice de Similaridade à Terra (ESI)** para exoplanetas com base em três parâmetros: **raio**, **densidade** e **temperatura**. Os dados são obtidos do [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/).

O ESI é uma medida de quão similar um exoplaneta é à Terra, com base nos parâmetros fornecidos. O programa permite ao usuário definir pesos para cada parâmetro e calcular o ESI, exibindo os 10 exoplanetas mais semelhantes à Terra.

## Como Usar

### Passo 1: Preparação do Ambiente

Antes de rodar o programa, você precisará instalar as dependências necessárias. Felizmente, isso pode ser feito facilmente com um arquivo de requisitos que já incluímos no projeto.

### Passo 2: Clonar o Repositório

1. **Baixar o código**: Para baixar o código do projeto, você precisa clonar o repositório. Se você não tem o Git instalado, pode baixar o código manualmente clicando no botão **"Code"** no repositório do GitHub e selecionando **"Download ZIP"**.

Se você já tem o Git instalado, pode clonar o repositório usando o seguinte comando:

```
git clone https://github.com/FellipFB/Out-of-This-Orbit.git
```

### Passo 3: Instalar as Dependências

2. **Instalar as bibliotecas necessárias**: O projeto usa bibliotecas como `requests` e `pandas` para funcionar corretamente. Para instalá-las, basta rodar o seguinte comando dentro da pasta do projeto (onde está o arquivo `requirements.txt`):

```
pip install -r requirements.txt
```

Esse comando irá instalar automaticamente todas as dependências necessárias.

### Passo 4: Executar o Código

3. **Rodar o programa**: Após instalar as dependências, você pode rodar o programa. Para isso, basta executar o seguinte comando dentro da pasta do projeto:

```
python main.py
```

Isso abrirá uma interface gráfica onde você poderá:
- Inserir os valores dos pesos para os parâmetros de raio, densidade e temperatura (entre 0 e 1).
- Clicar no botão **"Calcular ESI"** para calcular o Índice de Similaridade à Terra.
- Visualizar os exoplanetas mais semelhantes à Terra com base no ESI calculado.

### Passo 5: Visualização dos Resultados

- Após calcular o ESI, os 10 exoplanetas com maior ESI serão exibidos em uma tabela na interface gráfica.
- Você poderá ver o nome de cada exoplaneta e seu ESI correspondente.

## Problemas Comuns

- **Erro ao baixar os dados**: Se o programa não conseguir acessar o banco de dados da NASA, verifique se você está com uma conexão à internet estável.
- **Entradas inválidas**: Se você digitar um valor não numérico ou negativo para os pesos, o programa exibirá uma mensagem de erro.

Se você encontrar algum outro problema ou tiver dúvidas, pode conferir a seção de [Problemas (Issues)](https://github.com/FellipFB/Out-of-This-Orbit/issues) ou abrir uma nova issue.
