
# ☁️ App de Clima Interativo

Um aplicativo de desktop moderno e funcional para consulta de clima, construído com **Python** e sua biblioteca de interface gráfica **Tkinter**, consumindo dados em tempo real da **OpenWeatherMap API** 💻✨

Este projeto é ideal para praticar e aprofundar conhecimentos em:

* **Consumo de APIs REST:** Realizando requisições HTTP e manipulando dados JSON.
* **Desenvolvimento de Interface Gráfica (GUI):** Criando layouts dinâmicos e interativos com Tkinter.
* **Manipulação de Imagens:** Carregando e exibindo ícones de forma programática.
* **Persistência de Dados:** Salvando e carregando informações em arquivos JSON.
* **Boas Práticas de Design:** Aplicando princípios de UI/UX para um visual limpo e moderno.

-----

## ✨ Funcionalidades

* **Conexão com API Externa:** Busca e exibe dados climáticos em tempo real da [OpenWeatherMap API](https://openweathermap.org/api).
* **Interface Gráfica Intuitiva:** Design minimalista e moderno com elementos bem organizados, simulação de sombras e fontes agradáveis.
* **Busca por Cidade:** Campo de entrada para pesquisar o clima de qualquer cidade globalmente.
* **Exibição de Ícones do Clima:** Mostra ícones dinâmicos que representam as condições climáticas atuais.
* **Informações Detalhadas:** Além da temperatura e descrição, exibe:
    * Sensação Térmica
    * Umidade
    * Pressão Atmosférica
    * Velocidade do Vento
* **Seleção de Unidade de Temperatura:** Permite alternar entre Celsius (°C) e Fahrenheit (°F).
* **Histórico de Buscas Recentes:** Armazena e exibe as últimas 5 cidades pesquisadas, permitindo acesso rápido com um clique.
* **Persistência do Histórico:** O histórico de buscas é salvo em um arquivo local (`.json`) e carregado automaticamente ao reiniciar o aplicativo.
* **Janela Expansível:** A interface se ajusta e pode ser maximizada para preencher a tela inteira, otimizando o espaço.

-----

## 🛠️ Tecnologias Utilizadas

* **Python**: A linguagem de programação principal para toda a lógica do aplicativo.
* **Tkinter**: Biblioteca padrão do Python para a criação da interface gráfica de usuário (GUI).
* **Requests**: Biblioteca Python para realizar requisições HTTP de forma simples e eficiente para a API externa.
* **Pillow (PIL Fork)**: Biblioteca para manipulação de imagens, utilizada para carregar e redimensionar os ícones do clima.
* **Módulo `json`**: Módulo padrão do Python para serialização e desserialização de dados em formato JSON, usado para persistir o histórico de buscas.
* **OpenWeatherMap API**: A API RESTful que fornece os dados climáticos em tempo real.

-----

## 🚀 Como executar localmente

Para rodar este projeto em sua máquina, siga os passos abaixo:

1.  **Clone este repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
    ```
    (Lembre-se de substituir `SEU-USUARIO/SEU-REPOSITORIO` pelo caminho real do seu repositório no GitHub).

2.  **Acesse a pasta do projeto:**
    ```bash
    cd nome-do-repositorio # ou meu_app_clima
    ```

3.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    # No Windows (Command Prompt):
    venv\Scripts\activate.bat
    # No macOS/Linux:
    source venv/bin/activate
    ```

4.  **Instale as dependências:**
    ```bash
    pip install requests Pillow
    ```

5.  **Obtenha sua Chave de API da OpenWeatherMap:**
    * Vá para [https://openweathermap.org/](https://openweathermap.org/) e crie uma conta gratuita.
    * Após o login, navegue até a seção "API keys" e copie sua chave.

6.  **Insira sua Chave de API no código:**
    * Abra o arquivo `app_clima.py`.
    * Localize a linha `API_KEY = "SUA_CHAVE_DE_API_AQUI"` e substitua `"SUA_CHAVE_DE_API_AQUI"` pela sua chave real, mantendo as aspas.

7.  **Execute o aplicativo:**
    ```bash
    python app_clima.py
    ```

E pronto! O aplicativo de clima será iniciado.

-----

## 📂 Estrutura do Projeto

A estrutura de arquivos é simples e direta:

````

meu\_app\_clima/
├── app\_clima.py
└── search\_history.json  \# Criado automaticamente após a primeira busca

```
