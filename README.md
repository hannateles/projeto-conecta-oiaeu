♡ Conecta OIAEU

Plataforma de conexão entre profissionais voluntários e oportunidades de atuação social.

O Conecta OIAEU é uma aplicação web desenvolvida com o objetivo de facilitar a conexão entre profissionais voluntários e as necessidades de atuação social da instituição OIAEU.

A plataforma permite cadastrar voluntários, divulgar oportunidades, realizar inscrições e gerenciar solicitações por meio de um painel administrativo.

Projeto desenvolvido individualmente como MVP (Produto Mínimo Viável), com foco em organização, acessibilidade, responsividade e facilidade de utilização.

📌 Sobre o projeto

O projeto surgiu a partir da identificação de uma dificuldade enfrentada pela OIAEU: localizar profissionais com habilidades específicas para colaborar com suas atividades sociais.

O Conecta OIAEU busca solucionar esse problema por meio de uma plataforma digital que centraliza o cadastro de voluntários e o gerenciamento de oportunidades.

Instituição parceira: OIAEU

🎯 Objetivos
Facilitar o cadastro de profissionais voluntários.
Divulgar oportunidades de atuação social.
Permitir a consulta de vagas disponíveis.
Facilitar as inscrições dos voluntários.
Organizar o gerenciamento das solicitações.
Permitir que administradores aprovem ou recusem inscrições.
Centralizar informações em um único sistema.

✨ Funcionalidades
👤 Área do voluntário
Cadastro de voluntários.
Login e autenticação.
Cadastro de informações pessoais e profissionais.
Consulta de oportunidades disponíveis.
Visualização dos requisitos das vagas.
Inscrição em oportunidades de voluntariado.
Impedimento de inscrições duplicadas na mesma vaga.

🛠️ Área administrativa
Login administrativo.
Painel de gerenciamento.
Cadastro de novas oportunidades.
Consulta de vagas cadastradas.
Gerenciamento do status das oportunidades.
Consulta das inscrições realizadas.
Aprovação ou recusa de solicitações.
Consulta de indicadores gerais do sistema.

💻 Tecnologias utilizadas
Frontend
HTML5 — estrutura das páginas.
CSS3 — estilização e responsividade.
Backend
Python — linguagem de programação.
Flask — framework para desenvolvimento web.
Werkzeug Security — geração e verificação de hashes de senhas.
Regex — validação de informações.
Banco de dados
Microsoft SQL Server — armazenamento das informações.
SQL Server Management Studio (SSMS) — gerenciamento do banco.
PyODBC — conexão entre Python e SQL Server.

🗄️ Banco de dados

O banco de dados utilizado é denominado CONECTA_OIAEU e possui quatro tabelas principais:

Tabela	Descrição
Voluntario	Armazena os dados pessoais e profissionais dos voluntários.

Administrador	Armazena os dados dos administradores do sistema.
Vaga	Armazena as oportunidades de voluntariado.

Inscricao	Registra as inscrições realizadas pelos voluntários.
Relacionamentos

Um voluntário pode realizar várias inscrições.

Uma vaga pode receber várias inscrições.

A tabela Inscricao relaciona voluntários e oportunidades.

As tabelas possuem chaves primárias e estrangeiras para garantir a integridade dos dados.

Regras de negócio
Cada voluntário deve possuir cadastro para acessar as oportunidades.
Somente administradores podem cadastrar e gerenciar vagas.
Voluntários podem se inscrever apenas em vagas abertas.
Não são permitidas inscrições duplicadas na mesma oportunidade.
Toda inscrição começa com o status pendente.
Administradores podem aprovar ou recusar inscrições.
As vagas podem ser abertas ou encerradas.

📁 Estrutura do projeto
text
projeto-conecta-oiaeu/
│
├── app.py
├── database.py
│
├── templates/
│   ├── index.html
│   ├── cadastro.html
│   ├── login.html
│   ├── painel.html
│   ├── cadastrar_vaga.html
│   ├── vagas.html
│   └── inscricoes.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── images/
        └── logo.png

Principais arquivos
app.py: arquivo principal da aplicação, responsável pelas rotas, autenticação, sessões e regras de negócio.

database.py: responsável pela conexão com o SQL Server e pelas operações de consulta e persistência dos dados.

templates/: contém as páginas HTML.

static/css/style.css: contém os estilos e regras de responsividade.

static/images/: armazena as imagens utilizadas na aplicação.

🎨 Identidade visual

A identidade visual foi desenvolvida com uma proposta acolhedora, colorida e intuitiva, buscando transmitir confiança e proximidade.

Elemento	Cor	Código
Cabeçalho	Roxo	#7952B3
Destaques	Coral	#F36F55
Destaques secundários	Amarelo	#FFC400


## Revisão técnica

Este projeto passou por uma etapa de auto-revisão técnica,
com análise da organização, legibilidade e segurança do código.
