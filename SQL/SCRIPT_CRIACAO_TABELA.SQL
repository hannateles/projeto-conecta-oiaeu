
-- ============================================
-- PROJETO: CONECTA OIAEU
-- BANCO DE DADOS: CONECTA_OIAEU
-- SGBD: MICROSOFT SQL SERVER
-- ============================================


-- ============================================
-- 1. CRIAR BANCO DE DADOS
-- ============================================

IF DB_ID('CONECTA_OIAEU') IS NULL
BEGIN
    CREATE DATABASE CONECTA_OIAEU;
END;
GO

USE CONECTA_OIAEU;
GO


-- ============================================
-- 2. TABELA: VOLUNTARIO
-- ============================================

CREATE TABLE Voluntario (

    id_voluntario INT IDENTITY(1,1) PRIMARY KEY,

    nome VARCHAR(120) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    telefone VARCHAR(20) NOT NULL,

    formacao VARCHAR(100) NOT NULL,

    habilidades VARCHAR(255) NOT NULL,

    disponibilidade VARCHAR(100) NOT NULL,

    data_cadastro DATETIME2 NOT NULL
        DEFAULT SYSDATETIME()

);
GO


-- ============================================
-- 3. TABELA: ADMINISTRADOR
-- ============================================

CREATE TABLE Administrador (

    id_administrador INT IDENTITY(1,1) PRIMARY KEY,

    nome VARCHAR(120) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    senha_hash VARCHAR(255) NOT NULL,

    data_cadastro DATETIME2 NOT NULL
        DEFAULT SYSDATETIME(),

    ativo BIT NOT NULL
        DEFAULT 1

);
GO


-- ============================================
-- 4. TABELA: VAGA
-- ============================================

CREATE TABLE Vaga (

    id_vaga INT IDENTITY(1,1) PRIMARY KEY,

    titulo VARCHAR(120) NOT NULL,

    descricao VARCHAR(500) NOT NULL,

    area_atuacao VARCHAR(100) NOT NULL,

    requisitos VARCHAR(255) NOT NULL,

    data_publicacao DATETIME2 NOT NULL
        DEFAULT SYSDATETIME(),

    status VARCHAR(20) NOT NULL
        DEFAULT 'aberta',

    CONSTRAINT CK_Vaga_Status
        CHECK (status IN ('aberta', 'encerrada'))

);
GO


-- ============================================
-- 5. TABELA: INSCRICAO
-- ============================================

CREATE TABLE Inscricao (

    id_inscricao INT IDENTITY(1,1) PRIMARY KEY,

    id_voluntario INT NOT NULL,

    id_vaga INT NOT NULL,

    data_inscricao DATETIME2 NOT NULL
        DEFAULT SYSDATETIME(),

    status VARCHAR(20) NOT NULL
        DEFAULT 'pendente',

    CONSTRAINT FK_Inscricao_Voluntario
        FOREIGN KEY (id_voluntario)
        REFERENCES Voluntario(id_voluntario),

    CONSTRAINT FK_Inscricao_Vaga
        FOREIGN KEY (id_vaga)
        REFERENCES Vaga(id_vaga),

    CONSTRAINT UQ_Inscricao_Voluntario_Vaga
        UNIQUE (id_voluntario, id_vaga),

    CONSTRAINT CK_Inscricao_Status
        CHECK (status IN ('pendente', 'aprovado', 'recusado'))

);
GO


-- ============================================
-- 6. CONSULTAR TABELAS CRIADAS
-- ============================================

SELECT
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
GO


-- ============================================
-- 7. CONFERIR ESTRUTURA DAS TABELAS
-- ============================================

SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN (
    'Voluntario',
    'Administrador',
    'Vaga',
    'Inscricao'
)
ORDER BY TABLE_NAME, ORDINAL_POSITION;
GO


-- ============================================
-- FIM DO SCRIPT
-- PROJETO CONECTA OIAEU
-- ============================================
