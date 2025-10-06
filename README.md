# Curso de Python Flask

Este repositório contém os exercícios e exemplos de código desenvolvidos durante o curso de Python com o framework Flask.
Cada diretório representa um exercício ou um tópico específico abordado no curso.

## Como Executar os Exercícios

Para executar cada projeto de exercício, siga os passos abaixo. Todos os comandos devem ser executados no terminal, dentro do diretório do exercício correspondente (por exemplo, `cd "Hello World"`).

### Passo 1: Criar o Ambiente Virtual (Virtual Environment)

Um ambiente virtual isola as dependências do seu projeto, evitando conflitos com outros projetos Python em sua máquina.

Navegue até o diretório do exercício que deseja executar e crie o ambiente virtual:

```bash
python -m venv venv
```

Ou, se você tiver múltiplas versões do Python instaladas e quiser usar a versão 3:

```bash
python3 -m venv venv
```

Isso criará um diretório chamado `venv` contendo os arquivos do ambiente virtual.

### Passo 2: Ativar o Ambiente Virtual

Antes de instalar as dependências ou executar a aplicação, você precisa ativar o ambiente virtual.

**No Linux ou macOS:**

```bash
source venv/bin/activate
```

**No Windows (PowerShell ou CMD):**

```bash
venv\Scripts\activate
```

Após a ativação, o nome do ambiente virtual (`(venv)`) aparecerá no início do seu prompt de comando, indicando que ele está ativo.

### Passo 3: Instalar as Dependências

Cada exercício possui um arquivo `requirements.txt` que lista todas as bibliotecas Python necessárias. Com o ambiente virtual ativado, instale as dependências com o seguinte comando:

```bash
pip install -r requirements.txt
```

### Passo 4: Executar a Aplicação Flask

Após instalar as dependências, você pode iniciar o servidor de desenvolvimento do Flask. O arquivo principal da aplicação em cada exercício é o `app.py`.

Existem duas maneiras comuns de executar a aplicação:

#### Método 1: Configurando Variáveis de Ambiente (Recomendado)

Esta é a forma mais prática para desenvolvimento, pois permite usar comandos simplificados como `flask run` e comandos customizados como `flask test`. Configure as seguintes variáveis de ambiente no seu terminal:

*   `FLASK_APP`: Aponta para o arquivo principal da sua aplicação (geralmente `app.py` ou, em projetos mais complexos, `flasky.py`).
*   `FLASK_ENV`: Define o ambiente. Use `development` para ativar o modo de depuração (debug mode com recarregamento automático).

**No Linux ou macOS:**
```bash
export FLASK_APP=app.py # ou flasky.py, dependendo do exercício
export FLASK_ENV=development
```

**No Windows (CMD):**
```bash
set FLASK_APP=app.py
set FLASK_ENV=development
```

**No Windows (PowerShell):**
```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
```

Com as variáveis configuradas, você pode iniciar o servidor com o comando simplificado:
```bash
flask run
```

E executar os testes (nos projetos que os possuem) com:
```bash
flask test
```

#### Método 2: Usando o comando `flask` com flags

Se não quiser configurar variáveis de ambiente, você pode passar a informação diretamente na linha de comando.

```bash
flask --app app run
```
#### Método 2: Usando o comando `python` 

Para iniciar a aplicação, execute o script principal diretamente com o interpretador Python. Certifique-se de que você está no diretório raiz do projeto.

```bash
python app.py
```

Após executar o comando, o terminal mostrará o endereço onde a aplicação está rodando, geralmente `http://127.0.0.1:5000`. Abra este endereço no seu navegador para ver a aplicação em funcionamento.