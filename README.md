# Projeto de Previsão de Preços de Casas

Este projeto visa a **previsão de preços de imóveis** com o objetivo de estimar os valores de mercado para casas listadas na OLX. Utilizando conceitos de **engenharia de dados** e **aprendizado de máquina**, o sistema foi desenvolvido para automatizar a coleta e análise dos dados, oferecendo previsões precisas e escaláveis para o mercado imobiliário.

## Tecnologias Utilizadas

- **Selenium**: Para automação na raspagem de dados de anúncios de imóveis na OLX.
- **Numpy** e **Pandas**: Para o tratamento e limpeza dos dados, garantindo consistência e preparação adequada para o modelo.
- **Keras** e **TensorFlow**: Para o desenvolvimento e treinamento de uma rede neural para a previsão dos preços dos imóveis.
- **Sklearn**: Para a implementação de uma regressão polinomial como comparação com o modelo de rede neural.
- **Docker**: Para containerização do projeto, garantindo a execução eficiente em diferentes ambientes.
- **Apache Airflow**: Para orquestrar o fluxo de tarefas, como raspagem de dados, processamento e atualização dos modelos de previsão.
- **FastAPI** e **Uvicorn**: Para criar uma API de consulta em tempo real, disponibilizando as previsões de preços de imóveis.

## Funcionalidades

- **Raspagem de Dados**: Automação da coleta de dados atualizados de anúncios de imóveis na OLX, utilizando Selenium para navegação e extração de informações relevantes.
- **Processamento de Dados**: Tratamento dos dados extraídos com **Numpy** e **Pandas**, garantindo que as informações estejam limpas e padronizadas para alimentar os modelos de aprendizado de máquina.
- **Modelagem de Preços**: Desenvolvimento de dois modelos de previsão de preços:
  - **Rede Neural**: Implementada com **Keras** e **TensorFlow**.
  - **Regressão Polinomial**: Implementada com **sklearn**, servindo como uma referência para comparação de desempenho.
- **Infraestrutura**: Uso de **Docker** para garantir que o projeto seja executado de forma consistente em diferentes ambientes e **Apache Airflow** para automatizar as tarefas de raspagem, processamento e atualização do modelo.
- **API e Servidor**: Exposição dos modelos por meio de uma API construída com **FastAPI** e **Uvicorn**, permitindo que as previsões sejam feitas em tempo real.
