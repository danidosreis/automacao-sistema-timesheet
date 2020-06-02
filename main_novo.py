#!/usr/bin/env python3
#
# Autor: Danielle dos Reis
# Version: v1

from mysql import primeira_query_novos, segunda_query_novos, update_mysql_novos
from sendmail import send_email
from ldap import ldap

query_1 = primeira_query_novos()

if query_1 != 0:
    query_2 = segunda_query_novos()
    for i in query_2:
        lista = list(i)
        cod_sf = lista[0]
        usuario = lista[1].replace("@dominio.com.br", "")
        senha = lista[2]
        usr_ad = ldap(usuario)
        if usr_ad == True:
            send_email(usuario, senha, 'Acesso ao Timesheet')
            print(f'2. E-mail enviado para o usuário {usuario}')
            print('')
            update_mysql_novos(cod_sf)
        else:
            print(f'3. O usuário {usuario} não foi encontrado no AD')
            print('')
else:
    print(f'O resultado da primeira query é {query_1}, não há o que executar.')
