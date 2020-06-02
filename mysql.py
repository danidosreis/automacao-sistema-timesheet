#!/usr/bin/env python3
#
# Autor: Danielle dos Reis
# Version: v1

import pymysql
import os

# Função para conexão com o DB

def connection():
    host = os.environ.get('BD_IP')
    usr_db = os.environ.get('BD_USR')
    pass_db = os.environ.get('BD_PASS')
    db = os.environ.get('BD')
    conexao = pymysql.connect(host=host, user=usr_db, passwd=pass_db, db=db, charset='utf8mb4', )
    return conexao

# Funções de consultas para criação de acesso ao timesheet para novos colaboradores

def primeira_query_novos():
    print('1. Conectando na base de dados....')
    conexao = connection()
    mycursor = conexao.cursor()
    print('2. Realizando a primeira consulta no banco de dados...')
    mycursor.execute("SELECT CASE TRUE WHEN COUNT(0) > 0 THEN 1 ELSE 0 END AS Status \
    FROM BD_STAGE2.TB_CREDENCIAIS AS CRE JOIN ( \
    SELECT HI.Codigo AS Codigo FROM BD_STAGE2.TB_HIERARQUIA_SF AS HI \
    JOIN BD_DASHS_TIMESHEET.TB_TRIBO_ELEGIVEL AS TE ON TE.Tribo = HI.NomeDepartamento) \
    AS HI ON HI.Codigo = CRE.CodigoUsuario WHERE ISNULL(CRE.DataHroEnvio) = 1")
    resultado = mycursor.fetchall()
    resultado = str(resultado).strip("(),")
    resultado = int(resultado)
    mycursor.close()
    print('3. Fechando conexão com banco de dados...')
    print('')
    conexao.close()
    return resultado

def segunda_query_novos():
    print('1. Conectando na base de dados....')
    conexao = connection()
    mycursor = conexao.cursor()
    print('2. Realizando a segunda consulta no banco de dados...')
    mycursor.execute("SELECT HI.Codigo AS Codigo, CRE.Login AS Email, \
    CONVERT(CONVERT(AES_DECRYPT(CRE.Senha, 'Grut1') USING UTF8) USING LATIN1) \
    AS Senha FROM \
    BD_STAGE2.TB_CREDENCIAIS AS CRE JOIN (\
    SELECT HI.Codigo AS Codigo FROM BD_STAGE2.TB_HIERARQUIA_SF \
    AS HI JOIN BD_DASHS_TIMESHEET.TB_TRIBO_ELEGIVEL AS TE ON TE.Tribo = HI.NomeDepartamento) \
    AS HI ON HI.Codigo = CRE.CodigoUsuario \
    WHERE ISNULL(CRE.DataHroEnvio) = 1 AND ISNULL(CRE.Senha) = 0")
    resultado = mycursor.fetchall()
    mycursor.close()
    print('3. Fechando conexão com banco de dados...')
    print('')
    conexao.close()
    return resultado

def update_mysql_novos(codigo_sf):
    print('1. Conectando na base de dados...')
    conexao = connection()
    mycursor = conexao.cursor()
    print('2. Atualizando tabela da base de dados')
    mycursor.execute("UPDATE BD_STAGE2.TB_CREDENCIAIS SET DataHroEnvio = CURRENT_TIMESTAMP() \
    WHERE CodigoUsuario = (%s)", codigo_sf)
    conexao.commit()
    print('3. Fechando conexão com banco de dados...')
    print('')
    conexao.close()

# Funções de consultas para reset de senha de usuários do timesheet

def primeira_query_reset():
    print('1. Conectando na base de dados....')
    conexao = connection()
    mycursor = conexao.cursor()
    print('2. Realizando a primeira consulta no banco de dados...')
    mycursor.execute("SELECT CASE TRUE WHEN COUNT(0) > 0 THEN 1 ELSE 0 END AS Status \
    FROM BD_STAGE2.TB_RESET_SENHA AS RS \
    WHERE ISNULL(RS.DataHroEnvio) = 1 AND ISNULL(RS.NovaSenha) = 0;")
    resultado = mycursor.fetchall()
    resultado = str(resultado).strip("(),")
    resultado = int(resultado)
    mycursor.close()
    print('3. Fechando conexão com banco de dados...')
    print()
    conexao.close()
    return resultado

def segunda_query_reset():
    print('1. Conectando na base de dados....')
    conexao = connection()
    mycursor = conexao.cursor()
    print('2. Realizando a segunda consulta no banco de dados...')
    mycursor.execute("SELECT HI.Codigo AS Codigo, HI.Email AS Email, \
    CONVERT(CONVERT(AES_DECRYPT(RS.NovaSenha, 'Grut1') USING UTF8) USING LATIN1) AS NovaSenha \
    FROM BD_STAGE2.TB_RESET_SENHA AS RS JOIN BD_STAGE2.TB_HIERARQUIA_SF \
    AS HI ON HI.Codigo = RS.CodigoUsuario WHERE ISNULL(RS.DataHroEnvio)  = 1 AND ISNULL(RS.NovaSenha) = 0 \
    ORDER BY RS.DataHroSolicitacao")
    resultado = mycursor.fetchall()
    mycursor.close()
    print('3. Fechando conexão com banco de dados...')
    print('')
    conexao.close()
    return resultado

def update_mysql_reset_tblsenha(codigo_sf):
    print('1. Conectando na base de dados...')
    conexao = connection()
    mycursor = conexao.cursor()
    print('2. Atualizando tabela de senha da base de dados')
    mycursor.execute("UPDATE BD_STAGE2.TB_RESET_SENHA SET DataHroEnvio  = \
    CURRENT_TIMESTAMP(), NovaSenha  = NULL WHERE CodigoUsuario = (%s)", codigo_sf)
    conexao.commit()
    print('3. Fechando conexão com banco de dados...')
    print('')
    conexao.close()

def update_mysql_reset_tblcredeciais(codigo_sf, senha):
    print('1. Conectando na base de dados...')
    conexao = connection()
    mycursor = conexao.cursor()
    print('2. Atualizando tabela de credenciais do banco de dados')
    mycursor.execute("UPDATE BD_STAGE2.TB_CREDENCIAIS SET Senha = \
    AES_ENCRYPT(%s, 'Grut1') WHERE CodigoUsuario = %s", (senha, codigo_sf))
    conexao.commit()
    print('3. Fechando conexão com banco de dados...')
    print('')
    conexao.close()
