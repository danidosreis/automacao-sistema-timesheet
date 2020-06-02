# automacao-sistema-timesheet
Automação para o envio de e-mail automatico de acordo com criterios estabelecidos.

Essa automação foi criada para suprir a necessidade de um sistema de enviar e-mail automaticamente para novos colaboradores com as suas credenciais de acesso ao sistema.

Dentre os destaques dos scripts, estão o trabalho com modularização, funções e bibliotecas específicas como:

- ldap3 para validação de usuario no active directory
- smtplib e email para o envio de e-mails utilizando template html
- pymysql para realização de consultas e update em base mysql


