# Django Firestore Integration

This is an example of a web application using Firebase Firestore and Authentication alongside Django.

## Requirements

* Python 3.8 (`python-venv` and `python-pip`)
* Django 3.1.7
* firebase_admin 2.13
* python-dotenv 0.15

## Iniciando o projeto

1. Clone this repository and create a virtual-env in the same directory
```sh
git clone https://github.com/thalescr/django-docx-import.git
cd django-docx-import
python3 -m venv venv
```

2. Activate your virtual-env:

Windows:
```sh
venv\Scripts\activate
```

Linux:
```sh
source venv/bin/activate
```

3. Install required Python modules
```sh
pip3 install -r requirements.txt
```

4. Create a file called `.env` in project's root directory:
```
SECRET_KEY=project_secret_key_here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/firebase/credentials.json
FIREBASE_CONFIG={ "storageBucket" : "firebase-bucket-link.appspot.com" }
FIREBASE_WEB_API_KEY=firebase_web_api_key_here
```

5. Finally run your server
```sh
python3 manage.py runserver
```