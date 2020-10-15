# Certhub

Certhub é uma aplicação web multiusuário destinada a armazenar suas aptidões, além de certificados de cursos e especializações. Este projeto foi escrito em Django usando os seguintes requerimentos:

## Requerimentos

* Python 3.8 (`python-venv` e `python-pip`)
* Django 3.1
* firebase_admin 4.4.0

## Iniciando o projeto

1. Primeiramente, crie uma venv utilizando o seguinte comando:

```sh
python -m venv venv
```

2. Em seguida, é necessário ativar a venv criada:

Windows:
```sh
venv/Scripts/activate
```

Linux:
```sh
source venv/bin/activate
```

3. Depois, instale os requerimentos especificados em `requirements.txt`:

```sh
pip install -r requirements.txt
```

4. Crie um arquivo chamado `.env` na raiz do projeto no seguinte formato:
```
SECRET_KEY=insira_uma_chave_secreta_aqui
GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/credenciais/do_firebase.json
FIREBASE_CONFIG={ "storageBucket" : "link-do-bucket-do-firebase.appspot.com" }
FIREBASE_WEB_API_KEY=CHAVE_DA_API_WEB
```

5. Inicie o servidor:
```sh
python manage.py runserver
```