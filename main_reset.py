from mysql import primeira_query_reset, segunda_query_reset, update_mysql_reset_tblsenha, update_mysql_reset_tblcredeciais
from sendmail import send_email

query_1 = primeira_query_reset()

if query_1 != 0:
    query_2 = segunda_query_reset()
    for i in query_2:
        lista = list(i)
        cod_sf = lista[0]
        usuario = lista[1].replace("@dominio.com.br", "")
        senha = lista[2]
        send_email(usuario, senha, 'Nova senha para acesso ao Timesheet')
        print(f'2. E-mail enviado para o usuário {usuario}')
        print('')
        update_mysql_reset_tblsenha(cod_sf)
        update_mysql_reset_tblcredeciais(cod_sf, senha)
else:
    print(f'O resultado da primeira query é {query_1}, não há o que executar.')
