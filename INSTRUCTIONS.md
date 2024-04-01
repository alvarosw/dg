# Instruções

Antes de rodar o servidor, tenha certeza de ter rodado as migrations e populado o banco de dados.

Para isso, digite no terminal na raiz do projeto:
```cmd
  python manage.py makemigrations
  python manage.py migrate
  python populate.py
```

Agora o servidor deve estar pronto para ser iniciado. No seu terminal, digite:
```cmd
  python manage.py runserver
```