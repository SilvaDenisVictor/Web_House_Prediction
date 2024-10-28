Projeto de Previsão de Preços de Casas

Desenvolvi um sistema de previsão de preços de imóveis com o objetivo de estimar valores de mercado para casas listadas na OLX, aplicando conceitos de data engineering e aprendizado de máquina. Principais etapas do projeto:

Raspagem de Dados: Automatizei a coleta de dados de anúncios de imóveis usando Selenium para navegar na OLX, garantindo uma base de dados rica e atualizada para o modelo.

Processamento de Dados: Realizei o tratamento dos dados com as bibliotecas numpy e pandas, padronizando e limpando as informações para maximizar a precisão dos modelos de previsão.

Modelagem: Desenvolvi e treinei dois modelos de regressão — uma rede neural com Keras e TensorFlow e uma regressão polinomial com sklearn. Ambos alcançaram cerca de 70% de acurácia, com potencial para melhoria conforme o volume de dados aumenta.

Infraestrutura: Utilizei Docker para containerizar o projeto, facilitando a execução em diferentes ambientes, e Apache Airflow para orquestrar as tarefas de raspagem, processamento e atualização dos modelos.

API e Servidor: Criei uma API usando FastAPI e Uvicorn para disponibilizar o modelo de forma acessível, implementando um servidor para chamadas em tempo real.

Esse projeto reforçou minha compreensão prática em raspagem de dados, engenharia de dados, e criação de APIs, além de expandir minhas habilidades em infraestrutura com Docker e Airflow.
