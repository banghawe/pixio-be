# Pixio - Image Forgery Detector

Pixio is website to detect image forgery detector, it was created for personal project.

# Getting Started

## How to run project on local environment

1. Please install docker on your machine
2. Create .env file based on .env.example
3. Running
   ```sh 
   docker-compose --env-file ./admin/.env up
   ```
4. Open backend terminal
   ```sh
   docker-compose --env-file ./admin/.env run backend sh
   ```
5. Add superuser for django admin
   ```sh
   python manage.py createsuperuser
   ```
   and follow the instructions
6. Migrate db schemes
   ```sh
   python manage.py migrate
   ```


