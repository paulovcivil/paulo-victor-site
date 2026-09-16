# Projeto Flask — Passo a Passo

Este documento explica o que foi feito até agora no projeto e por quê, acompanhando os tópicos do curso (HTML, CSS, Flask, páginas estáticas x dinâmicas).

> **Nota:** este arquivo é um **log cronológico** — cada seção reflete o estado do projeto *no momento em que foi escrita*. A partir da seção 13, todo o código (rotas, nomes de arquivo, variáveis) foi traduzido para inglês. Por isso, trechos de código nas seções anteriores a ela ainda podem mostrar nomes antigos em português (`/sobre`, `sobre.html`, `dados`, etc.) — são registro histórico das decisões tomadas naquele passo, não o estado atual do código. Para ver o estado atual, veja a seção 1 (estrutura de pastas, sempre mantida atualizada) e a seção 13.

## 1. Estrutura de pastas

```
Samsung Ocean/
├── app.py                 # servidor Flask (o "cérebro" da aplicação)
├── requirements.txt       # lista de dependências Python do projeto
├── .gitignore              # arquivos/pastas que não devem ir para o git (ex: venv/)
├── .env                     # variáveis de ambiente reais (segredos) — não vai para o git
├── .env.example             # modelo do .env, sem segredos reais — esse vai para o git
├── Procfile                 # diz ao Render (ou Heroku) como iniciar o site em produção
├── venv/                   # ambiente virtual Python isolado deste projeto
├── contacts.csv            # arquivo de teste da fase em que o formulário gravava em disco (não é mais escrito)
├── templates/              # HTML fica aqui (Flask procura nesta pasta por padrão)
│   ├── base.html           # esqueleto comum (cabeçalho + menu) herdado pelas outras páginas
│   ├── index.html
│   ├── about.html
│   ├── projects.html
│   └── contact.html
└── static/                 # CSS, imagens e JS ficam aqui
    ├── style.css
    ├── pdfs/
    │   ├── shear-building-thermal-stability.pdf
    │   ├── vertical-riser-parametric-instability.pdf
    │   └── steel-fiber-pullout-modeling.pdf
    └── img/
        ├── fundo.png       # imagem de fundo da seção hero da página inicial
        ├── eu.png          # foto de perfil usada na página About
        ├── eu_contato.png  # foto usada na página Contact
        ├── ufjf.png        # logo da UFJF (seção Education)
        ├── usp.png         # logo da USP (seção Education)
        ├── pendulum_rotating_plane.gif  # original enviado pelo usuário (não usado na página)
        └── pendulum_rotating_plane.mp4  # versão comprimida, usada na página Projects
```

O Flask tem essa convenção fixa: arquivos HTML dentro de `templates/`, e arquivos estáticos (CSS/JS/imagens) dentro de `static/`. Não é obrigatório, mas é o padrão que o framework espera sem precisar configurar nada extra.

## 2. Instalando o Flask

```
pip install flask
```

Isso instalou o Flask e suas dependências (Werkzeug, Jinja2, Click, etc). O comando abaixo registrou tudo isso no `requirements.txt`, para que qualquer pessoa (ou você em outro computador) consiga reinstalar exatamente as mesmas versões com `pip install -r requirements.txt`:

```
pip freeze > requirements.txt
```

## 2.1. Ambiente virtual (venv)

Em vez de instalar o Flask direto no Python "global" do sistema, criamos um ambiente virtual isolado só para este projeto:

```
python -m venv venv
```

Isso gera a pasta `venv/` com uma cópia isolada do Python + gerenciador de pacotes. Instalando o Flask dentro dela, ele não interfere (nem sofre interferência) de outros projetos que usem versões diferentes de bibliotecas.

**Por quê:** projetos diferentes podem precisar de versões diferentes da mesma biblioteca; sem isolamento, instalar algo em um projeto pode quebrar outro. O venv também deixa o projeto reprodutível: qualquer pessoa recria o ambiente exato com `pip install -r requirements.txt`.

Para usar o venv no terminal, é preciso **ativá-lo** a cada sessão nova:

```powershell
.\venv\Scripts\Activate.ps1
```

O prompt do terminal passa a mostrar `(venv)` no começo da linha, indicando que os comandos `python` e `pip` agora apontam para o ambiente isolado do projeto. A pasta `venv/` foi adicionada ao `.gitignore`, pois não deve ser versionada (cada pessoa gera a sua localmente).

No VS Code, é preciso apontar o editor para esse interpretador: `Ctrl+Shift+P` → "Python: Select Interpreter" → escolher o que aponta para `venv\Scripts\python.exe`.

## 2.2. `.gitignore`

Arquivo de configuração do **Git** (sistema de controle de versão) que lista arquivos/pastas que o Git deve ignorar — nunca rastrear nem enviar para o repositório:

```
venv/
__pycache__/
*.pyc
```

- **`venv/`** — o ambiente virtual é grande e depende da máquina; cada pessoa deve gerá-lo localmente com `pip install -r requirements.txt`, em vez de versionar os arquivos prontos.
- **`__pycache__/`** e **`*.pyc`** — cache interno que o Python gera automaticamente ao executar o código, não é código-fonte.

**Por quê:** sem isso, um `git add .` tentaria versionar milhares de arquivos desnecessários, deixando o repositório pesado. O `.gitignore` só tem efeito depois de existir um repositório Git no projeto (`git init`), o que ainda não foi feito aqui.

## 3. `app.py` — o servidor

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html", nome="Paulo")

if __name__ == "__main__":
    app.run(debug=True)
```

Explicando linha por linha:

- `Flask(__name__)` cria a aplicação. O `__name__` diz ao Flask onde o arquivo está, para ele conseguir localizar as pastas `templates/` e `static/`.
- `@app.route("/")` é um **decorator**: associa uma URL a uma função Python. Sempre que alguém acessar `http://seusite.com/`, a função logo abaixo (`home`) é executada.
- `render_template("index.html")` procura o arquivo `templates/index.html`, processa (caso tenha alguma lógica Jinja2) e devolve o HTML pronto como resposta ao navegador.
- Na rota `/sobre`, além de renderizar o template, passamos uma variável (`nome="Paulo Victor"`) que fica disponível dentro do HTML.
- `app.run(debug=True)` liga o servidor local. `debug=True` faz o servidor reiniciar sozinho a cada alteração salva no código, e mostra erros detalhados no navegador — ótimo para desenvolvimento, mas **nunca deve ir para produção**.

Isso é a base de **página dinâmica**: o conteúdo do HTML é montado pelo Python antes de ser enviado ao navegador (diferente de uma página estática, que é um arquivo `.html` fixo, sempre igual).

## 4. Templates (`templates/index.html` e `templates/sobre.html`)

Os arquivos usam **Jinja2**, o motor de templates do Flask, que permite misturar HTML com comandos Python dentro de chaves duplas `{{ }}`.

Pontos importantes usados nos templates:

- `{{ url_for('static', filename='style.css') }}` — gera o caminho correto para o arquivo CSS (`/static/style.css`), em vez de escrever o caminho na mão. Se um dia a estrutura de pastas mudar, o link se ajusta sozinho.
- `{{ url_for('home') }}` e `{{ url_for('sobre') }}` — geram os links de navegação a partir do **nome da função** Python (`home`, `sobre`), não da URL escrita à mão. Assim, se a rota mudar de endereço no `app.py`, os links no HTML continuam funcionando.
- `{{ nome }}` (em `sobre.html`) — imprime o valor da variável `nome` que foi enviada pela função `sobre()` no `app.py`. É aqui que Python "entra" dentro do HTML.

## 5. `static/style.css`

CSS comum, sem nenhuma mágica do Flask — só precisa estar dentro da pasta `static/` para ser servido automaticamente pelo Flask em `/static/style.css`.

## 6. Formulário e `request.form` (rota `/contato`)

Até aqui as páginas só mostravam conteúdo — o usuário não conseguia mandar nada de volta para o servidor. Para isso existe o `request.form`.

Na rota `/contato`, o Python decide se deve **mostrar o formulário vazio** ou **mostrar os dados enviados**, olhando para o método da requisição:

```python
@app.route("/contato", methods=["GET", "POST"])
def contato():
    dados = None
    if request.method == "POST":
        dados = {
            "nome": request.form["nome"],
            "telefone": request.form["telefone"],
            "email": request.form["email"],
        }
    return render_template("contato.html", dados=dados)
```

- `methods=["GET", "POST"]` — por padrão uma rota só aceita `GET` (pedir uma página). Aqui liberamos também `POST` (enviar dados).
- **GET**: quando o usuário só abre a página `/contato` pela primeira vez, `dados` continua `None` e o template mostra apenas o formulário vazio.
- **POST**: quando o usuário preenche o formulário e clica em "Enviar", o navegador reenvia a própria página, mas com `method="POST"`. Nesse caso, `request.form["nome"]` (e os outros campos) trazem o que foi digitado — a chave é o atributo `name` de cada `<input>` no HTML. Esses valores vão para o dicionário `dados`, que é passado ao template.

No `templates/contato.html`, o formulário aponta para a própria rota (`action="{{ url_for('contato') }}"`, `method="POST"`), e um bloco condicional do Jinja2 só aparece quando existe `dados`:

```html
{% if dados %}
<section class="resultado">
    <p><strong>Nome:</strong> {{ dados.nome }}</p>
    ...
</section>
{% endif %}
```

Ou seja, a **mesma página e a mesma rota** cuidam de exibir o formulário e de exibir o resultado — não precisamos de uma página separada para "confirmação".

Também foi adicionado o link "Contato" no menu de navegação de todas as páginas, e um estilo simples para formulário e para o card de resultado em `static/style.css`.

**Importante:** nessa primeira versão os dados só existiam durante aquela requisição — assim que o Flask respondia, eram esquecidos. Nada ficava salvo de fato (veja seção 7 abaixo para a solução).

## 7. Persistindo os dados em `contatos.csv`

Para os dados do formulário não sumirem depois da resposta, passamos a **gravá-los em um arquivo CSV** a cada envio:

```python
import csv
import os

CSV_PATH = "contatos.csv"
CSV_CAMPOS = ["nome", "telefone", "email"]

@app.route("/contato", methods=["GET", "POST"])
def contato():
    dados = None
    if request.method == "POST":
        dados = {
            "nome": request.form["nome"],
            "telefone": request.form["telefone"],
            "email": request.form["email"],
        }

        arquivo_ja_existe = os.path.isfile(CSV_PATH)
        with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=CSV_CAMPOS)
            if not arquivo_ja_existe:
                escritor.writeheader()
            escritor.writerow(dados)

    return render_template("contato.html", dados=dados)
```

Explicando as partes novas:

- **`csv.DictWriter`** — escreve linhas de um CSV a partir de dicionários, usando `fieldnames` (`CSV_CAMPOS`) para saber a ordem das colunas e casar cada chave do dicionário com a coluna certa.
- **`os.path.isfile(CSV_PATH)`** — verifica se o arquivo já existe *antes* de abrir/escrever. Isso decide se precisamos escrever o cabeçalho (`nome,telefone,email`) ou não — ele só deve aparecer uma vez, na primeira linha do arquivo.
- **`mode="a"`** (append) — abre o arquivo para **adicionar** conteúdo no final, em vez de sobrescrever (`mode="w"` apagaria tudo que já estava salvo a cada novo envio).
- **`newline=""`** — parâmetro recomendado pela documentação do módulo `csv` no Windows, evita que cada linha fique com uma quebra de linha extra em branco.
- **`with open(...) as arquivo:`** — garante que o arquivo é fechado automaticamente ao final do bloco, mesmo se der algum erro no meio do caminho.

Cada envio do formulário agora vira uma nova linha em `contatos.csv`, e esses dados sobrevivem a atualizações de página e a reinícios do servidor — diferente da versão anterior, que só existia durante aquela resposta.

O arquivo `contatos.csv` foi adicionado ao `.gitignore`: ele guarda dados reais preenchidos por quem usa o site (não é código-fonte), então não deve ir para o repositório Git.

## 8. Redesenho da página inicial (hero + imagem de fundo)

A página inicial (`templates/index.html`) virou a landing page pessoal do site (tema: engenharia civil e modelagem computacional), com uma seção **hero** em destaque:

- A imagem `fundo.png` (fornecida pelo usuário) foi movida para `static/img/fundo.png` — precisa estar dentro de `static/` para o Flask conseguir servi-la.
- No `style.css`, a seção `.hero` usa essa imagem como fundo via `background-image: url("img/fundo.png")`. O caminho é relativo ao próprio arquivo CSS (que está em `static/`), por isso `img/fundo.png` e não `static/img/fundo.png`.
- Um **degradê escuro** (`linear-gradient`) é aplicado por cima da imagem, misturado no mesmo `background-image` (CSS aceita várias camadas de fundo separadas por vírgula). Isso escurece o lado esquerdo da imagem para o texto branco ficar legível, mantendo a imagem mais visível à direita.
- Dentro do hero: uma tag pequena, um título (`<h2>`), um parágrafo de apresentação e dois botões (`.btn-primario` e `.btn-secundario`) que levam para `/sobre` e `/contato` usando `url_for`, igual aos links do menu.

Abaixo do hero, uma seção `.cards` usa **CSS Grid** (`display: grid; grid-template-columns: repeat(3, 1fr)`) para organizar três cartões lado a lado (Método dos Elementos Finitos, Modelagem Computacional, Análise Estrutural). Uma `@media (max-width: 800px)` empilha os cards em uma coluna só e reduz o título do hero em telas pequenas, para não quebrar o layout no celular.

**Por que não colocar a imagem direto no HTML com `{{ url_for(...) }}` dentro do `style="..."`:** funcionaria, mas como o caminho da imagem é sempre o mesmo (não depende de dado do usuário/banco), faz mais sentido deixar isso fixo no CSS — separa melhor "estrutura" (HTML) de "aparência" (CSS) e evita misturar Jinja dentro de atributos de estilo.

## 9. Como rodar o projeto

```
python app.py
```

O terminal vai mostrar algo como `Running on http://127.0.0.1:5000`. Basta abrir esse endereço no navegador.

Para testar sem abrir o navegador manualmente, também validamos as rotas via requisições HTTP (`/`, `/sobre`, `/contato` — GET e POST — e os arquivos estáticos `style.css` e `img/fundo.png`, todos retornando status 200).

## 10. Marca "Paulo Victor" clicável no cabeçalho

O nome "Paulo Victor" agora aparece no cabeçalho de **todas** as páginas (`index.html`, `sobre.html`, `contato.html`), como um link (`<a class="marca">`) que sempre volta para a página inicial:

```html
<header>
    <a class="marca" href="{{ url_for('home') }}">Paulo Victor</a>
    <nav>
        <a href="{{ url_for('home') }}">Início</a>
        <a href="{{ url_for('sobre') }}">Sobre</a>
        <a href="{{ url_for('contato') }}">Contato</a>
    </nav>
</header>
```

- Como o `header` usa `display: flex; justify-content: space-between;`, o primeiro elemento no HTML fica encostado na esquerda e o último na direita, sem precisar de nenhum posicionamento especial. A marca "Paulo Victor" vem primeiro no HTML (canto superior **esquerdo**) e o menu (`nav`) vem depois (direita).
- Antes, `sobre.html` e `contato.html` usavam um `<h1>` (Sobre / Contato) no cabeçalho como título da página. Esse título foi movido para dentro do `<main>`, como um `<h2>` — o cabeçalho agora é só navegação + marca, igual em toda página, e o título específico de cada página fica no conteúdo dela.

**Observação:** o mesmo bloco de `<header>` agora está copiado e colado em 3 arquivos HTML. Se um dia precisarmos mudar o menu (adicionar uma página, por exemplo), teremos que editar os 3 arquivos. É exatamente esse tipo de repetição que a herança de templates do Jinja2 (`{% extends %}` / `{% block %}`, item pendente na lista abaixo) resolve — todas as páginas herdariam um único `header` de um arquivo "base".

## 11. Conteúdo real na página Sobre / About

A página `sobre.html`, que até então só exibia um texto de exemplo (`Olá, {{ nome }}!`), virou a bio real do site, com o texto profissional fornecido pelo usuário (currículo/LinkedIn).

**Decisão de idioma:** o restante do site (menu, formulário, textos da home) está em português, mas o conteúdo enviado veio em inglês. Perguntei e o usuário optou por manter essa seção em **inglês**, então o site passa a ser bilíngue por enquanto (chrome/navegação em português, conteúdo pessoal em inglês) — vale revisitar isso mais pra frente se quiser padronizar tudo num só idioma.

O que foi feito:

- `<html lang="en">` e `<title>` da página ajustados para inglês, já que o conteúdo da página é em inglês (o atributo `lang` ajuda leitores de tela e o navegador a escolherem o dicionário/pronúncia certos).
- A variável `{{ nome }}` (já vinda do `app.py`, `nome="Paulo Victor"`) passou a ser usada como **cabeçalho da bio** (`<h1>{{ nome }}</h1>`), reaproveitando o mesmo conceito de variável dinâmica visto antes, agora aplicado a um caso de uso real.
- O texto enviado virou 3 parágrafos (`<p>`) dentro de uma seção `.sobre`.
- As ferramentas técnicas citadas (Python, MS Project, AutoCAD, Revit, ABAQUS, Ftool, Power BI) foram destacadas separadamente como uma lista de "chips" (`<ul class="skills">`), em vez de ficarem só soltas no meio do parágrafo — fica mais fácil de escanear visualmente.
- No CSS, a seção `.sobre` ganhou uma largura máxima (`max-width: 700px`) centralizada, pensada para leitura de texto corrido (colunas muito largas cansam a leitura), e os `.skills li` viraram "pílulas" (bordas arredondadas, fundo branco) com `display: flex; flex-wrap: wrap;` na lista, para se ajustarem sozinhas ao tamanho da tela.

## 12. Foto de perfil e formação acadêmica

Três imagens fornecidas pelo usuário (`EU.png`, `ufjf.png`, `usp.png`) foram movidas para `static/img/` (a foto foi renomeada para `eu.png`, seguindo o padrão de nomes em minúsculo já usado no projeto).

**Foto de perfil:** o cabeçalho da página `sobre.html` passou a ser um cartão com a foto ao lado do nome/cargo:

```html
<div class="sobre-cabecalho">
    <img class="foto-perfil" src="{{ url_for('static', filename='img/eu.png') }}" alt="Photo of {{ nome }}">
    <div>
        <h1>{{ nome }}</h1>
        <p class="cargo">...</p>
    </div>
</div>
```

No CSS, `.sobre-cabecalho` usa `display: flex; align-items: center;` para colocar foto e texto lado a lado, e `.foto-perfil` usa `border-radius: 50%` para deixar a imagem redonda (um truque comum de foto de perfil: qualquer imagem quadrada vira um círculo).

**Seção Education:** nova seção com dois cartões (`.formacao`), um para cada instituição, cada um com o logo da universidade ao lado do texto — mesmo padrão visual dos cards da página inicial (fundo branco, borda colorida à esquerda, sombra leve):

- **USP** — Mestrado em Engenharia Civil (estruturas), em andamento (2026–2028).
- **UFJF** — Graduação em Engenharia Civil (2019–2025), incluindo atuação como monitor de programação e pesquisador de iniciação científica em modelagem computacional.

O texto dessas duas entradas foi escrito a partir das informações que o usuário mandou (prints do LinkedIn), reescrito em frases completas — os prints tinham trechos cortados com "...more", então o texto final não é uma cópia literal, mas resume as mesmas informações.

**Responsividade:** foi adicionada uma media query para telas pequenas (`max-width: 600px`) que empilha a foto/nome e o logo/texto dos cards de formação em coluna, centralizados, em vez de lado a lado — evita que a imagem "aperte" o texto em telas estreitas.

## 13. Tradução completa para inglês e limpeza da estrutura do código

Até aqui o site estava misturado: navegação/formulário em português, página About em inglês. O usuário pediu para revisar toda a estrutura e padronizar tudo em inglês — não só o texto visível, mas também nomes internos do código (rotas, variáveis, classes CSS, nomes de arquivo), para o projeto ficar mais fácil de mexer no futuro.

**Por quê isso importa:** código com nomes em um idioma e conteúdo em outro (ex: rota `/sobre` servindo uma página "About") é uma fonte comum de confusão à medida que o projeto cresce. Manter tudo consistente facilita achar as coisas e evita esse tipo de dissonância.

O que mudou:

**Rotas e arquivos (`app.py` + `templates/`)**

| Antes | Depois |
|---|---|
| rota `/sobre`, função `sobre()` | rota `/about`, função `about()` |
| rota `/contato`, função `contato()` | rota `/contact`, função `contact()` |
| `templates/sobre.html` | `templates/about.html` |
| `templates/contato.html` | `templates/contact.html` |
| variável `nome` | variável `name` |
| variável `dados` | variável `submitted` |
| campos do formulário `nome`, `telefone` | campos `name`, `phone` |
| `contatos.csv`, colunas `nome,telefone,email` | `contacts.csv`, colunas `name,phone,email` |

Os dados que já existiam em `contatos.csv` foram migrados manualmente para `contacts.csv` com o novo cabeçalho, em vez de perdidos.

**Classes CSS (`static/style.css`)** — cada classe em português virou sua versão em inglês, mantendo o mesmo visual:

`.marca`→`.brand` · `.hero-conteudo`→`.hero-content` · `.hero-botoes`→`.hero-buttons` · `.btn-primario`→`.btn-primary` · `.btn-secundario`→`.btn-secondary` · `.sobre`→`.about` · `.sobre-cabecalho`→`.about-header` · `.cargo`→`.role` · `.foto-perfil`→`.profile-photo` · `.educacao`→`.education` · `.formacao`→`.education-entry` · `.logo-formacao`→`.education-logo` · `.periodo`→`.period` · `.resultado`→`.result`

**Menu de navegação** — traduzido em todas as páginas: Início→Home, Sobre→About, Contato→Contact.

**Conteúdo da home page (`index.html`)** — reescrito, além de traduzido: agora fala especificamente da área de interesse do usuário (não é mais um texto genérico de "engenharia civil"):

- Tag do hero: "Civil Engineering · Computational & AI-Driven Structural Modeling"
- Texto do hero menciona explicitamente Método dos Elementos Finitos (FEM), modelagem computacional **e inteligência artificial** aplicada à engenharia estrutural — conectando com a pesquisa de mestrado (USP) e o projeto de análise fractal (Petrobras) já descritos na página About.
- Os 3 cards foram reescritos: "Finite Element Method", "Computational & AI-Driven Modeling" (citando a análise fractal) e "Structural Analysis & Project Controls" (unindo a experiência de obra com controle de custo/prazo, que também aparece no About).

Isso cria uma conexão de conteúdo entre a home e a página About — a home dá o resumo, o About detalha.

## 14. Página de contato com foto e informações diretas

A página `contact.html` ganhou uma seção de apresentação antes do formulário, com uma foto (`static/img/eu_contato.png`) e as informações de contato diretas do usuário:

```html
<div class="contact-intro">
    <img class="profile-photo" src="{{ url_for('static', filename='img/eu_contato.png') }}" alt="Photo of Paulo Victor">
    <div>
        <p>Feel free to reach out directly...</p>
        <ul class="contact-info">
            <li><strong>Email:</strong> <a href="mailto:...">...</a></li>
            <li><strong>Phone:</strong> <a href="tel:...">...</a></li>
        </ul>
    </div>
</div>
```

- A foto reaproveita a classe `.profile-photo` (a mesma da página About), mantendo a mesma "moldura" circular em todo o site.
- Os links usam os esquemas `mailto:` e `tel:` — não são URLs de páginas, mas instruções para o sistema abrir o programa de e-mail ou o discador do celular já preenchidos com o destino. `tel:+5532999720148` no formato internacional (sem espaços/parênteses) para funcionar em qualquer dispositivo.
- A página passou a ter duas partes bem distintas: a introdução com **suas** informações de contato (`<h2>Contact</h2>` + `.contact-intro`) e o formulário para a pessoa que está visitando o site entrar em contato (`<h3>Send a message</h3>` + `<form>`).
- Todo o conteúdo da página foi envolvido numa seção `.contact` com `max-width: 700px`, no mesmo padrão de largura de leitura já usado na página About.

## 15. Variáveis de ambiente com `.env`

Um arquivo `.env` apareceu na raiz do projeto com:

```
FLASK_APP=app.py
FLASK_DEBUG=True
SECRET_KEY=chave-super-secreta-para-aulas-ocean-2026
```

**O que é:** um arquivo de configuração com variáveis de ambiente — pares `CHAVE=valor` disponíveis para o programa em tempo de execução, mas mantidos **fora do código-fonte**.

**Por que isso existe separado do `app.py`:**

- **Segredos não devem ir para o Git.** A `SECRET_KEY` é usada pelo Flask para assinar sessões, cookies e tokens de proteção (CSRF). Se ela fosse escrita direto no código e o projeto fosse para o GitHub, qualquer pessoa veria a chave. Guardando no `.env` (que fica fora do Git, via `.gitignore`), ela nunca é exposta.
- **Configuração muda por ambiente.** Em desenvolvimento queremos `FLASK_DEBUG=True` (recarrega sozinho, mostra erros detalhados); em produção isso deveria ser `False`, por segurança. O mesmo código funciona nos dois lugares, só troca o `.env`.

O arquivo existia mas **não estava sendo lido por nada** — foi preciso conectar ele ao Flask:

```python
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DEBUG_MODE = os.getenv("FLASK_DEBUG", "False") == "True"

# ...

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
```

- **`python-dotenv`** (pacote instalado via `pip`) fornece `load_dotenv()`, que lê o arquivo `.env` e coloca cada `CHAVE=valor` nas variáveis de ambiente do processo Python — depois disso, `os.getenv("NOME_DA_CHAVE")` funciona normalmente.
- **`os.getenv("FLASK_DEBUG", "False")`** — lê a variável; o segundo argumento é o valor padrão caso a variável não exista (assim o projeto não quebra se alguém esquecer de criar o `.env`, só volta pro modo mais seguro).
- **`app.secret_key`** — fica configurada a partir de agora, mas ainda não é usada por nenhuma funcionalidade do site (não temos login nem mensagens "flash" ainda). Ela é necessária para esses recursos no futuro; deixamos pronta desde já.
- Testamos rodando o servidor: o log mostrou `Debug mode: on`, confirmando que o valor veio do `.env` e não de um `True` fixo no código como antes.

**Boas práticas aplicadas:**

- `.env` foi adicionado ao `.gitignore` — cada pessoa/máquina tem o seu, com valores possivelmente diferentes, e nunca deve ir para o repositório.
- Foi criado um `.env.example` (esse sim **vai** para o Git) com as mesmas chaves, mas com um valor de exemplo no lugar do segredo real. É assim que outras pessoas (ou você em outra máquina) sabem quais variáveis o projeto precisa, sem que o segredo real seja exposto — o processo normal é copiar esse arquivo para `.env` e preencher os valores reais.

## 16. Herança de templates com `{% extends %}` / `{% block %}`

O `<header>` (marca + menu) estava copiado e colado em `index.html`, `about.html` e `contact.html`. Criamos um template "base" que os outros passam a **herdar**:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Paulo Victor{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <a class="brand" href="{{ url_for('home') }}">Paulo Victor</a>
        <nav>
            <a href="{{ url_for('home') }}">Home</a>
            <a href="{{ url_for('about') }}">About</a>
            <a href="{{ url_for('contact') }}">Contact</a>
        </nav>
    </header>

    {% block content %}{% endblock %}
</body>
</html>
```

Cada página agora só declara o que é **diferente** dela — o resto vem do `base.html`:

```html
<!-- templates/about.html -->
{% extends "base.html" %}

{% block title %}About | {{ name }}{% endblock %}

{% block content %}
<main>
    ...
</main>
{% endblock %}
```

- **`{% block nome %}...{% endblock %}`** no `base.html` marca um "espaço vazio" que cada página filha pode preencher. Criamos dois: `title` (o `<title>` da aba do navegador) e `content` (tudo que vem depois do cabeçalho).
- **`{% extends "base.html" %}`**, sempre na primeira linha do arquivo, diz ao Jinja2 "esta página usa o `base.html` como esqueleto".
- Se um bloco não for preenchido pela página filha, o Jinja2 usa o conteúdo padrão escrito dentro do `{% block %}` no próprio `base.html` (por isso `{% block title %}Paulo Victor{% endblock %}` tem um valor padrão).

**Por que isso é melhor:** antes, mudar o menu (adicionar uma página nova, por exemplo) exigia editar 3 arquivos manualmente — e era fácil esquecer um deles e deixar o site inconsistente. Agora existe **uma única fonte de verdade** para o cabeçalho; qualquer mudança nele se propaga automaticamente para todas as páginas.

## 17. Otimização do CSS (variáveis e remoção de duplicação)

Revisando o `static/style.css`, encontramos três tipos de repetição e resolvemos cada um:

**1. Cores/tamanhos "mágicos" repetidos várias vezes** — a cor `#2c3e50` (azul petróleo) aparecia sozinha em pelo menos 10 lugares diferentes (cabeçalho, títulos, bordas, botão). Se um dia você quisesse trocar a cor principal do site, teria que caçar cada ocorrência. Isso foi resolvido com **variáveis CSS** (custom properties), declaradas uma vez no topo do arquivo:

```css
:root {
    --color-primary: #2c3e50;
    --color-primary-dark: #1a252f;
    --color-text: #333;
    --color-text-muted: #5a6b7b;
    --color-bg: #f4f4f4;
    --color-border: #ccc;
    --color-accent: #5fd0ff;
    --color-accent-hover: #8adfff;
    --radius-sm: 4px;
    --radius-md: 6px;
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

E usadas assim, no lugar do valor fixo: `background-color: var(--color-primary);`. Agora, para trocar a cor principal do site inteiro, basta editar **uma linha**.

**2. Regras idênticas escritas duas vezes** — `.about` e `.contact` tinham exatamente o mesmo `max-width: 700px; margin: 0 auto;`; o mesmo acontecia com a cor dos `<h2>`/`<h3>` de cada seção. Isso foi unificado agrupando os seletores com vírgula:

```css
.about,
.contact {
    max-width: 700px;
    margin: 0 auto;
}
```

**3. Duas media queries diferentes fazendo a mesma coisa** — `.about-header`/`.education-entry` e `.contact-intro` tinham blocos `@media (max-width: 600px)` **separados**, mas com a regra idêntica (empilhar em coluna e centralizar). Foram unificados em um único bloco:

```css
@media (max-width: 600px) {
    .about-header,
    .education-entry,
    .contact-intro {
        flex-direction: column;
        text-align: center;
    }
}
```

O resultado visual não muda em nada — é a mesma aparência de antes. A diferença é só na **manutenção**: menos código repetido, menos risco de alterar uma cor/regra num lugar e esquecer de replicar em outro.

## 18. Meta tag `viewport` (responsividade de verdade no celular)

Adicionada ao `<head>` do `templates/base.html`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**O problema que ela resolve:** por padrão, navegadores de celular assumem que sites são feitos para tela de desktop. Sem essa tag, o navegador renderiza a página numa largura "virtual" bem maior que a tela real (geralmente 980px) e depois dá zoom out pra caber tudo — o que faz o site *parecer* responsivo (nada corta), mas na prática nossas media queries como `@media (max-width: 600px)` **nunca disparam**, porque o navegador nunca reporta uma largura pequena de verdade.

- **`width=device-width`** — diz ao navegador para usar a largura real do dispositivo como referência, em vez daquela largura virtual de desktop.
- **`initial-scale=1.0`** — a página começa sem zoom nenhum aplicado (escala 1:1 entre pixel CSS e pixel de tela).

Como essa tag entrou no `base.html`, ela passou a valer para as três páginas do site de uma vez — outro exemplo prático de por que a herança de templates (seção 16) compensa.

## 19. Link do LinkedIn na página de contato

Adicionado mais um item na lista `.contact-info` de `templates/contact.html`:

```html
<li><strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/paulovsales/" target="_blank" rel="noopener">linkedin.com/in/paulovsales</a></li>
```

Diferente dos links de e-mail/telefone (que usam `mailto:`/`tel:` para abrir outro programa), esse é um link normal para outro site — por isso dois atributos extras:

- **`target="_blank"`** — abre o LinkedIn numa aba nova, em vez de navegar para fora do seu site na mesma aba (prática comum para links externos, para não "perder" o visitante do seu site).
- **`rel="noopener"`** — recomendação de segurança para usar junto de `target="_blank"`. Sem ela, a página aberta (linkedin.com) ganha acesso via JavaScript à aba de origem (`window.opener`) e, em teoria, poderia redirecioná-la para outro lugar. `noopener` bloqueia esse acesso.

## 20. Nova página "Projects"

Adicionada uma quarta página ao site, mostrando trabalhos de modelagem computacional — começando com uma animação (`.gif`) de uma simulação de pêndulo esférico.

**Nova rota, sem nenhuma lógica extra** (é uma página só de conteúdo, como a About):

```python
@app.route("/projects")
def projects():
    return render_template("projects.html")
```

**Menu atualizado em um lugar só:** o link "Projects" foi adicionado ao `<nav>` do `templates/base.html` — e, graças à herança de templates (seção 16), apareceu automaticamente nas 4 páginas do site sem precisar tocar em `index.html`, `about.html` ou `contact.html`.

**Estrutura da página:** segue o mesmo padrão visual já estabelecido nas páginas About/Contact — um "card" (`.project-entry`) com uma imagem de um lado e o texto explicativo do outro, igual aos cartões de `.education-entry`. A classe `.projects` foi incluída no grupo de seletores compartilhados que já existia para `.about`/`.contact` (mesma largura máxima de leitura, mesma cor de títulos) — outro exemplo de reaproveitar CSS em vez de duplicar.

```html
<img class="project-media" src="{{ url_for('static', filename='img/pendulum_rotating_plane.gif') }}" alt="...">
```

- **`.project-media`** — parecido com `.education-logo`, mas maior (`width: 260px`) e sem virar quadrado com fundo branco, já que aqui a imagem é o próprio conteúdo (um gráfico), não uma logomarca.
- Um `<img>` normal já é suficiente para exibir um `.gif` animado — o navegador reproduz a animação em loop automaticamente, sem precisar de JavaScript ou de tags de vídeo.
- O texto (`alt="..."`) descreve o que a animação mostra, para quem usa leitor de tela ou caso a imagem não carregue.

**Ponto de atenção (tamanho do arquivo):** o `pendulum_rotating_plane.gif` tem cerca de **6,4 MB** — pesado para uma página web (a home inteira, com foto de fundo em PNG, pesa menos que isso). Isso não trava nada agora, mas quando o site for hospedado de verdade (seção de próximos passos), vale considerar comprimir o gif ou convertê-lo para vídeo (`.mp4`/`.webm`), que costuma pesar uma fração disso para a mesma qualidade visual.

## 21. Convertendo o gif para vídeo (`.mp4`)

Resolvendo o ponto de atenção da seção anterior: em vez de só comprimir o `.gif`, ele foi **convertido para vídeo**, que é uma solução bem mais eficaz para esse tipo de conteúdo.

**Ferramenta:** o `ffmpeg` (programa de linha de comando para converter/editar áudio e vídeo) foi instalado no sistema via `winget` (gerenciador de pacotes do Windows), já que não vem instalado por padrão.

**Comando usado:**

```
ffmpeg -i pendulum_rotating_plane.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -crf 28 pendulum_rotating_plane.mp4
```

- **`-c:v libx264`** — codec de vídeo H.264, o mais compatível com navegadores.
- **`-crf 28`** — "Constant Rate Factor", controla a qualidade/compressão (escala de 0 a 51; menor = mais qualidade e arquivo maior). 28 é um valor comum para vídeos onde qualidade perfeita não é essencial.
- **`-pix_fmt yuv420p`** — formato de cor com compatibilidade máxima entre navegadores/dispositivos.
- **`-movflags faststart`** — reorganiza o arquivo para começar a tocar assim que os primeiros bytes chegam, sem esperar o download completo (importante para vídeo na web).
- **`-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`** — garante que largura e altura sejam números pares (exigência do codec H.264); praticamente nunca é perceptível, é só uma correção técnica.

**Resultado:** de **6,4 MB (gif) para 321 KB (mp4)** — quase 20x menor, com a mesma qualidade visual.

**HTML atualizado** (`templates/projects.html`) — trocamos `<img>` por `<video>`:

```html
<video
    class="project-media"
    src="{{ url_for('static', filename='img/pendulum_rotating_plane.mp4') }}"
    autoplay
    loop
    muted
    playsinline
    aria-label="..."
></video>
```

- **`autoplay loop muted`** — reproduz sozinho, em loop, sem som — visualmente se comporta como um gif tocando infinitamente.
- **`muted` é obrigatório para `autoplay` funcionar** — navegadores modernos bloqueiam vídeo com som tocando sozinho automaticamente (por experiência do usuário), mas permitem se estiver mudo.
- **`playsinline`** — evita que o vídeo abra em tela cheia automaticamente em iPhones/iPads.
- **`aria-label`** — como `<video>` não tem atributo `alt`, esse é o equivalente para leitores de tela descreverem o conteúdo.

O `pendulum_rotating_plane.gif` original continua em `static/img/` (não está mais referenciado em nenhuma página) — pode ser removido quando quiser.

## 22. Artigos para download na página Projects

Três PDFs (artigos acadêmicos escritos pelo usuário) foram movidos de uma pasta `pdfs/` na raiz para `static/pdfs/` — precisam estar dentro de `static/` para o Flask conseguir servi-los, mesma regra já usada para imagens e CSS. Os nomes dos arquivos também foram padronizados (minúsculo, com hífen, sem espaço) para ficarem "limpos" numa URL:

| Original | Novo nome |
|---|---|
| `Linear dynamic stability of a three-story shear.pdf` | `shear-building-thermal-stability.pdf` |
| `ParametricInstabilityofaVerticalRiserunderHarmonic.pdf` | `vertical-riser-parametric-instability.pdf` |
| `steel_fiber_pullout_article.pdf` | `steel-fiber-pullout-modeling.pdf` |

O resumo de cada artigo em `projects.html` foi escrito a partir do **abstract** de cada PDF (lido pelo assistente antes de escrever o texto), não inventado.

**Link de download:**

```html
<a class="btn-download" href="{{ url_for('static', filename='pdfs/shear-building-thermal-stability.pdf') }}" download>
    Download PDF (3.2 MB)
</a>
```

- **`url_for('static', filename='pdfs/...')`** — mesmo mecanismo já usado para imagens/CSS; o Flask serve qualquer arquivo que esteja dentro de `static/`, não só imagens.
- **`download`** — atributo HTML que instrui o navegador a **baixar** o arquivo em vez de tentar abri-lo/exibi-lo na aba (o que aconteceria por padrão com PDF, já que a maioria dos navegadores tem visualizador de PDF embutido). É essa palavra sozinha, sem valor, que faz o "Salvar como" acontecer automaticamente.
- O tamanho aproximado do arquivo foi incluído no texto do link (ex: "3.2 MB") — boa prática de UX: a pessoa sabe o que esperar antes de clicar, especialmente em conexões mais lentas.

Nova seção `.publications` no CSS, com cards no mesmo padrão visual já usado no site (fundo branco, borda colorida à esquerda, sombra leve) — reaproveitando o "vocabulário visual" já estabelecido em vez de inventar um estilo novo.

## 23. Identidade visual do cabeçalho e novo rodapé

Como tudo isso vive no `base.html`, uma edição só valeu para as 4 páginas do site.

**Ícone da marca (SVG inline):** ao lado de "Paulo Victor" no cabeçalho, um pequeno desenho de triângulo com "nós" nos vértices e no centro — uma referência visual a uma malha de elementos finitos (o mesmo tema da seção "Finite Element Method" da home):

```html
<svg class="brand-icon" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
    <path d="M12 3 L21 19 H3 Z" fill="none" stroke="currentColor" .../>
    <circle cx="12" cy="3" r="1.6" fill="currentColor"/>
    ...
</svg>
```

- **SVG inline** (o código do desenho direto no HTML, em vez de um arquivo `.png`/`.svg` separado) permite colorir o ícone só com CSS (`color: var(--color-accent)`), porque `stroke="currentColor"` e `fill="currentColor"` fazem o desenho herdar a cor do texto ao redor — não precisa de um arquivo de imagem diferente para cada cor.
- **`aria-hidden="true"`** — diz a leitores de tela para ignorar o ícone (ele é só decorativo; o nome "Paulo Victor" ao lado já identifica o link).

**Link da página atual em destaque:** cada link do menu ganha a classe `active` quando é a página que está sendo exibida:

```html
<a href="{{ url_for('about') }}" class="{{ 'active' if request.endpoint == 'about' }}">About</a>
```

- **`request`** é um objeto que o Flask já disponibiliza automaticamente dentro de qualquer template (não precisa passar como variável do `render_template`) — representa a requisição HTTP atual.
- **`request.endpoint`** é o nome da função Python da rota que está respondendo agora (`home`, `about`, `projects` ou `contact`). Comparando com o nome de cada link, sabemos qual deles é "a página atual" e aplicamos um estilo diferente (cor de destaque + sublinhado).

**Rodapé novo**, com marca + frase de efeito, links rápidos (Projects, e-mail, LinkedIn) e uma linha de copyright com o **ano atual gerado automaticamente**:

```python
@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}
```

- **`@app.context_processor`** registra uma função que roda antes de *qualquer* template ser renderizado, injetando as variáveis que ela retorna (aqui, `current_year`) automaticamente em todos eles — sem precisar passar `current_year=...` em cada `render_template()` das 4 rotas. É o "modo certo" de compartilhar um dado (como o ano do copyright) entre todas as páginas.
- No template: `&copy; {{ current_year }} Paulo Victor.` — o ano nunca fica desatualizado, porque é calculado a cada requisição.

**Rodapé "grudado" embaixo (sticky footer):** em páginas com pouco conteúdo (como About), sem esse ajuste o rodapé ficaria "flutuando" no meio da tela em monitores grandes, em vez de ficar sempre na base. Resolvido com Flexbox no `body`:

```css
body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.page-content {
    flex: 1 0 auto;
}
```

- `body` vira uma coluna flex com altura mínima igual à tela inteira (`100vh`).
- `.page-content` (a `<div>` que envolve o `{% block content %}` no `base.html`, entre o header e o footer) recebe `flex: 1 0 auto`, ou seja, "cresça para ocupar todo o espaço sobrando". Isso empurra o `<footer>` para o final da tela sempre, mesmo quando o conteúdo da página é curto.

## 24. Links das instituições na página About

Os títulos das duas entradas em "Education" viraram links para os sites oficiais dos programas:

```html
<h3><a href="https://www.poli.usp.br/ppgec/" target="_blank" rel="noopener">University of São Paulo (USP)</a></h3>
<h3><a href="https://www2.ufjf.br/engenhariacivil/" target="_blank" rel="noopener">Federal University of Juiz de Fora (UFJF)</a></h3>
```

Mesmo padrão já usado no link do LinkedIn (seção 19): `target="_blank"` abre em nova aba, `rel="noopener"` por segurança.

**Detalhe de CSS:** por padrão, um link (`<a>`) dentro de um `<h3>` ignora a cor do título e aparece azul (cor padrão do navegador para links). Para o título continuar com a mesma cor de antes, adicionamos:

```css
.education-entry h3 a {
    color: inherit;
    text-decoration: none;
}
```

- **`color: inherit`** — em vez de definir uma cor nova, diz "use a mesma cor do elemento pai" (o `<h3>`, que já é `var(--color-primary)`). Sublinhado só aparece no `:hover`, como sinalização de que é clicável.

## 25. Ícone da marca trocado (malha &rarr; engrenagem)

O usuário mandou uma imagem (foto de engrenagens/automação) para trocar o ícone ao lado do nome no cabeçalho. Como o ícone é pequeno (22x22px), usar a foto direto ficaria ilegível — fotos têm muito detalhe para um espaço tão pequeno. A solução foi **recriar a ideia como um ícone simples**, no mesmo estilo de traço fino do ícone anterior (a malha triangular), só que agora representando uma engrenagem:

```html
<svg class="brand-icon" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
    <g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5.5"/>
        <circle cx="12" cy="12" r="2"/>
        <line x1="12" y1="3" x2="12" y2="5.3"/>
        <!-- mais 7 linhas, uma para cada "dente" da engrenagem -->
    </g>
</svg>
```

- Dois círculos concêntricos (o corpo da engrenagem e o furo central) mais 8 linhas radiais (os "dentes"), espaçadas a cada 45°.
- Continua usando `stroke="currentColor"`, então herda a cor definida em `.brand-icon` (a mesma técnica da seção 23) sem precisar de um arquivo de imagem.

**Por que não usar a foto enviada:** além do problema de tamanho, uma imagem `.png`/`.jpg` colada na conversa não existe como arquivo no projeto — eu não tenho como "baixar" uma imagem do chat para o disco sozinho. Se um dia você quiser usar essa foto de verdade em algum lugar do site (num card maior, por exemplo, onde os detalhes não se perdem), é só salvar o arquivo dentro da pasta do projeto e me avisar.

## 26. Corrigindo reenvio duplicado do formulário (padrão Post/Redirect/Get)

**O problema:** o usuário percebeu contatos duplicados no `contacts.csv` (ex: "Leonardo Florentino" repetido várias vezes). A causa é um comportamento clássico de navegador: na versão anterior, a resposta ao `POST` (envio do formulário) já vinha com a página de confirmação **na mesma resposta**. Se a pessoa desse **F5** nessa página de confirmação, o navegador reenviava o mesmo `POST` — gravando o mesmo contato de novo no CSV.

**A solução — padrão "Post/Redirect/Get" (PRG):** depois de processar o `POST` e salvar no CSV, o servidor não renderiza mais a confirmação direto. Em vez disso, ele **redireciona** o navegador para a mesma página via `GET`:

```python
from flask import Flask, redirect, render_template, request, session, url_for

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        submitted = { ... }
        # ... salva no CSV ...

        session["submitted"] = submitted
        return redirect(url_for("contact"))

    submitted = session.pop("submitted", None)
    return render_template("contact.html", submitted=submitted)
```

- **`redirect(url_for("contact"))`** — em vez de devolver HTML, o Flask responde com um status `302` e um cabeçalho `Location`, instruindo o navegador a fazer uma **nova requisição `GET`** para `/contact`. O navegador atualiza a barra de endereço e o histórico como se a pessoa tivesse simplesmente "visitado" a página — um F5 a partir daqui só refaz o `GET`, não reenvia o formulário.
- **`session`** — como o `GET` do redirecionamento é uma requisição *separada* do `POST` original, os dados enviados (`submitted`) não estariam mais disponíveis para mostrar "Dados recebidos". A `session` do Flask (um cookie assinado criptograficamente, por isso precisa do `SECRET_KEY` que configuramos na seção 15) guarda esse dado **temporariamente**, associado ao navegador da pessoa, entre uma requisição e outra.
- **`session.pop("submitted", None)`** — lê o valor e **remove** da sessão no mesmo passo. Assim, a confirmação aparece uma única vez (na página que vem logo após o envio); se a pessoa der F5 de novo depois disso, o valor já não está mais lá e o formulário volta a aparecer vazio, sem repetir a mensagem.

**Teste realizado:** simulamos um `POST` e confirmamos que a resposta é um redirecionamento (302); a página seguinte mostra a confirmação; uma segunda leitura da mesma página (simulando F5) não mostra mais a confirmação; e só **uma** linha foi gravada no CSV para aquele envio.

As linhas duplicadas que já existiam no `contacts.csv` (geradas antes dessa correção) foram removidas manualmente, mantendo uma ocorrência de cada contato real.

## 27. Removendo a gravação em CSV (preparando o deploy no Render)

**Contexto da decisão:** o `contacts.csv` foi criado para *testar* a captura de dados do formulário (seções 7 e 26), não como a solução definitiva de armazenamento. Na maioria dos serviços de hospedagem gratuita — incluindo o Render, que o usuário escolheu por ter um fluxo de deploy mais moderno (deploy automático a partir do GitHub) — o disco é **efêmero**: qualquer arquivo escrito durante a execução (como o `contacts.csv` crescendo a cada envio) é **apagado** no próximo redeploy ou reinício do servidor. Ou seja, o código como estava não funcionaria de forma confiável no Render.

**Decisão:** em vez de já resolver a persistência "de verdade" (um banco de dados) antes mesmo de ter o site no ar, removemos a gravação em arquivo por enquanto. O formulário continua funcionando normalmente — recebe os dados, valida, mostra a confirmação (via `session`, como na seção 26) — só não grava mais em lugar nenhum. Isso desbloqueia o deploy agora; a persistência real entra depois, como uma melhoria incremental (ex: um banco de dados gerenciado, ver próximos passos).

`app.py` ficou mais enxuto — os imports (`csv`), constantes (`CSV_PATH`, `CSV_FIELDS`) e o bloco de escrita do arquivo foram removidos por completo (não deixamos código "comentado" morto no meio do arquivo):

```python
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        submitted = {
            "name": request.form["name"],
            "phone": request.form["phone"],
            "email": request.form["email"],
        }

        session["submitted"] = submitted
        return redirect(url_for("contact"))

    submitted = session.pop("submitted", None)
    return render_template("contact.html", submitted=submitted)
```

O arquivo `contacts.csv` (com os testes já feitos) continua no projeto — só não recebe mais linhas novas.

## 28. Roteiro do deploy no Render

Detalhando o que ainda falta fazer, em ordem, com o porquê de cada etapa.

### 28.1. Preparar o projeto para "modo produção" ✅

- [x] **Adicionar um servidor WSGI de produção** (`gunicorn`) ao `requirements.txt`. O servidor que usamos até agora (`app.run()`, do próprio Flask) é só para desenvolvimento — o aviso que aparece toda vez que rodamos (`Do not use it in a production deployment`) é literal: ele não foi feito pra lidar com tráfego real, várias conexões ao mesmo tempo, nem é tão seguro. O Render precisa de um comando de start baseado em `gunicorn`.
- [x] **Definir o "Start Command"** que o Render vai executar para subir o site: algo como `gunicorn app:app` (o primeiro `app` é o arquivo `app.py`, o segundo é a variável `app = Flask(__name__)` dentro dele).
- [x] **Garantir que o modo debug fique desligado em produção.** Hoje isso já é controlado pela variável `FLASK_DEBUG` (seção 15) — no Render, vamos configurar essa variável como `False` (ou simplesmente não defini-la, já que o padrão do código já é `False`). Debug mode ligado em produção é um risco de segurança real: a página de erro do Flask nesse modo inclui um console interativo que permite **executar código Python** — ótimo pra desenvolvimento, perigoso se exposto na internet.

**O que foi feito:**

- `gunicorn` instalado no `venv` e adicionado ao `requirements.txt`.
- Criado um `Procfile` na raiz do projeto:
  ```
  web: gunicorn app:app
  ```
  Esse é um arquivo de convenção (usado pelo Render, Heroku e outros) que declara como iniciar a aplicação. `web:` diz que é o processo principal que atende requisições HTTP; `gunicorn app:app` é o comando de fato.
- **`WSGI`** é o "protocolo" padrão em Python que define como um servidor (gunicorn) conversa com uma aplicação web (o Flask) — é por isso que o comando é `app:app`: o gunicorn importa o módulo `app.py` e procura dentro dele por um objeto chamado `app` (nossa instância do Flask) que segue esse protocolo.
- **Testado:** tentamos rodar `gunicorn app:app` localmente e, como esperado, ele falhou — o gunicorn depende de um módulo exclusivo de sistemas Unix/Linux (`fcntl`), que não existe no Windows. Isso **não é um problema**: o Render roda em Linux, então vai funcionar lá; continuamos usando `python app.py` (o servidor de desenvolvimento do Flask) para testar localmente, só o Render é que vai usar o gunicorn de verdade.
- Nada mudou no modo debug: já estava controlado por `FLASK_DEBUG` desde a seção 15, com `False` como padrão caso a variável não exista — exatamente o que queremos em produção.
- Confirmado que o site continua funcionando normalmente em desenvolvimento (`python app.py`) depois dessas mudanças — as 4 rotas respondendo 200.

### 28.2. Versionar o projeto com Git

- [ ] **`git init`** — o projeto ainda não é um repositório Git (só temos o `.gitignore` pronto desde a seção 2.2, esperando por isso).
- [ ] **Primeiro commit** — o `.gitignore` já existente garante que `venv/`, `.env`, `contacts.csv` e `__pycache__/` não sejam versionados.
- [ ] **Criar um repositório no GitHub** (na sua conta) e enviar o código (`git push`). O Render se conecta diretamente ao GitHub e reimplanta automaticamente a cada `push` na branch principal — é essa a "modernidade" do fluxo comparado ao PythonAnywhere.

### 28.3. Configurar o serviço no Render

- [ ] Criar conta gratuita no Render e conectar ao repositório do GitHub.
- [ ] Configurar **Build Command** (`pip install -r requirements.txt`) e **Start Command** (`gunicorn app:app`).
- [ ] Configurar as **variáveis de ambiente no painel do Render** (`SECRET_KEY`, e opcionalmente `FLASK_DEBUG`) — o `.env` local nunca vai para o Git nem para o Render; cada ambiente (sua máquina, o Render) tem sua própria cópia dessas variáveis, configurada no lugar certo.

### 28.4. Deploy e verificação

- [ ] Deploy inicial, acompanhar os logs de build/start no painel do Render.
- [ ] Testar as 4 páginas e o formulário de contato já no ar (numa URL pública tipo `algumacoisa.onrender.com`).

### Depois do site estar no ar (não bloqueia o deploy)

- [ ] **Reintroduzir a persistência dos contatos**, agora com uma solução compatível com disco efêmero. Opções, da mais simples à mais robusta:
  - **Enviar um e-mail a cada envio** (ex: com o serviço de e-mail transacional do Render ou uma biblioteca como `Flask-Mail`) — evita precisar de armazenamento, mas não gera um histórico consultável.
  - **Serviço externo pronto** (ex: Formspree, Airtable) — pouco código, mas depende de um serviço de terceiros.
  - **Banco de dados de verdade** (ex: PostgreSQL gerenciado, que o Render oferece com um plano gratuito) — solução mais robusta e a que mais se parece com o que se usa profissionalmente, mas exige aprender o básico de bancos de dados relacionais e um ORM (ex: SQLAlchemy).
- [ ] Estudar diferença entre Django e Flask (Flask é "micro-framework": você escolhe as peças; Django já vem com muita coisa pronta).
- [ ] Domínio customizado (opcional).

## Glossário rápido

| Termo | O que é |
|---|---|
| **Framework** | Conjunto de ferramentas prontas que organiza como a aplicação é construída (aqui, o Flask). |
| **Rota (route)** | Associação entre uma URL e uma função Python que responde a ela. |
| **Template** | Arquivo HTML com "buracos" que o Python preenche dinamicamente. |
| **Jinja2** | Motor de templates usado pelo Flask para misturar Python com HTML. |
| **Servidor** | Programa que fica escutando requisições (pedidos) do navegador e devolve respostas (páginas). |
| **Debug mode** | Modo de desenvolvimento do Flask que recarrega o servidor automaticamente e mostra erros detalhados. |
| **GET** | Método HTTP usado para *pedir* uma página/recurso (ex: abrir uma URL no navegador). |
| **POST** | Método HTTP usado para *enviar* dados ao servidor (ex: submeter um formulário). |
| **`request.form`** | Dicionário do Flask com os dados enviados por um formulário HTML via POST, indexado pelo atributo `name` de cada campo. |
| **Persistir dados** | Guardar dados de forma duradoura (arquivo, banco de dados), sobrevivendo ao fim da requisição/execução — diferente de só exibir algo na tela uma vez. |
| **CSV** | "Comma-Separated Values": formato de arquivo de texto simples para tabelas, onde cada linha é um registro e as colunas são separadas por vírgula. Abre em Excel, Google Sheets, etc. |
| **Hero** | Seção de destaque no topo de uma página (geralmente com imagem/título grande), pensada para causar a primeira impressão do site. |
| **CSS Grid** | Sistema do CSS (`display: grid`) para organizar elementos em linhas e colunas, usado aqui para os cards da página inicial. |
| **Media query** | Regra do CSS (`@media (...)`) que aplica estilos diferentes conforme o tamanho da tela, usada para o site funcionar bem também no celular. |
| **Variável de ambiente** | Valor de configuração disponível para o programa em tempo de execução, mas guardado fora do código-fonte (ex: num arquivo `.env`). |
| **`.env`** | Arquivo com variáveis de ambiente reais do projeto (segredos, configuração local). Nunca deve ir para o Git. |
| **`SECRET_KEY`** | Chave usada pelo Flask para assinar sessões, cookies e tokens de proteção (CSRF). Deve ser secreta e vir de uma variável de ambiente, nunca escrita direto no código. |
| **Herança de templates** | Técnica do Jinja2 (`{% extends %}` / `{% block %}`) em que uma página reaproveita a estrutura de um template "base", preenchendo só as partes que mudam. |
| **Variável CSS (custom property)** | Valor nomeado (`--nome: valor;`) declarado uma vez em `:root` e reaproveitado em várias regras via `var(--nome)`, evitando repetir o mesmo valor várias vezes. |
| **Viewport** | A "janela" visível da página no dispositivo. A meta tag `viewport` controla como o navegador mapeia essa janela para os pixels reais da tela, essencial para media queries funcionarem no celular. |
| **Atributo `download`** | Atributo HTML de um link (`<a>`) que faz o navegador baixar o arquivo em vez de tentar exibi-lo na própria aba. |
| **SVG inline** | Código de um desenho vetorial (`<svg>`) escrito direto no HTML, em vez de referenciado como arquivo de imagem. Permite estilizar o desenho com CSS, como mudar sua cor. |
| **`request` (Flask)** | Objeto disponível automaticamente em qualquer template Flask, representando a requisição HTTP atual (ex: `request.endpoint` diz qual rota está respondendo). |
| **Context processor** | Função registrada com `@app.context_processor` que roda antes de qualquer template ser renderizado, injetando variáveis (ex: o ano atual) automaticamente em todos eles, sem repetir código em cada rota. |
| **Sticky footer** | Técnica de layout (geralmente com Flexbox) que mantém o rodapé sempre no final da tela, mesmo quando o conteúdo da página é curto demais para preenchê-la. |
| **Post/Redirect/Get (PRG)** | Padrão em que, após um `POST`, o servidor responde com um redirecionamento para uma página `GET`, em vez de devolver o resultado direto. Evita que um F5 na página de confirmação reenvie o formulário. |
| **`session` (Flask)** | Mecanismo do Flask para guardar dados temporários associados a um navegador específico, entre uma requisição e outra, usando um cookie assinado com o `SECRET_KEY`. |
| **WSGI** | Padrão em Python que define como um servidor (ex: gunicorn) se comunica com uma aplicação web (ex: o Flask). É o que permite trocar o servidor por baixo do código sem reescrever a aplicação. |
| **Gunicorn** | Servidor WSGI de produção para aplicações Python — usado no lugar do servidor de desenvolvimento embutido do Flask quando o site vai para o ar de verdade. Só roda em sistemas Unix/Linux. |
| **Procfile** | Arquivo de convenção (usado por Render, Heroku etc.) que declara o comando para iniciar a aplicação em produção. |
| **Disco efêmero** | Sistema de arquivos que é apagado a cada reinício/redeploy do servidor — comum em planos gratuitos de hospedagem. Qualquer arquivo escrito durante a execução (como um CSV) some depois. |
