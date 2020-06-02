#!/usr/bin/env python3
#
# Autor: Danielle dos Reis
# Version: v1

from ldap3 import Server, Connection, ALL, NTLM
import os

def ldap(user):
    ip_ad = 'x.x.x.x'
    usr = 'dominio\\user'
    senha = 'senha'

    server = Server(ip_ad, get_info=ALL)
    print('1. Conectando ao ldap...')
    conn = Connection(server, user=usr, password=senha, authentication=NTLM, auto_bind=True)
    conn.search('OU=Unidade Organizacional,DC=dominio,DC=com,DC=br', '(objectclass=*)', attributes=['sAMAccountName'])

    lista = conn.entries
    print('2. Validando usuário ' + user +' no AD...')
    for i in lista:
        resultado = str(i)
        print(resultado)
        resultado = resultado.split(':')
        resultado = resultado[-1].strip("$\r\n ").lower()
        if resultado == user:
            print('3. Usuário encontrado no AD')
            print('')
            return True
