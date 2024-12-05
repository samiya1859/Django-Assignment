# Property Management System (Django)

This is a Property Management System built using Django, PostgreSQL, and the PostGIS extension. The system allows property owners to manage their listings, register as buyers or owners, and offers functionalities for adding, editing, deleting properties.

## Features

- **User Registration**: Users can register as buyers or owners. 
- **Property Management**: Owners can add, edit, and delete their property listings.
- **Frontend**: Uses HTML, CSS, and Tailwind CSS for the frontend design.
- **GIS Integration**: PostgreSQL with PostGIS extension is used for location management.
- **Admin Panel**: Admin users can manage users and property listings.

- The project consists of three main apps:

- **`properties`**: Handles property-related models, views, and logic.
- **`users`**: Manages user authentication, including registration and login functionality.
- **`interfaces`**: Handles the front-end templates and static files for the user interface.

## Functionalities
- **`User`** : User can register on basis of user types like owner and buyer. and ine can override all functionalities through creating superuser. one user cannot do login until superuser makes that user active from admin pannel. 
  ```bash
  docker-compose exec web python manage.py createsuperuser
  ```
-**`Properties`**: Properties app has several models to handle accomodation, location and localized accomodation. Localized accomodation is used for generating information in different languages

-**`Interfaces`**: Interfaces app is used for handling all templates and images. 

## Requirements

- Python 3.12+
- Django 4.x+
- PostgreSQL 13+ with PostGIS extension
- GDAL library for geographic data processing
- Pillow (for handling images)
  
## Setup Instructions

Follow these steps to set up the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/samiya1859/Django-Assignment.git
cd Django-Assignment
```
## 2. Create virtual envrionment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```
## 3. Install Dependencies

```bash
pip install -r requirements.txt
```
## 4. Set up environment variables
```ini
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=localhost  # or your Docker container host if using Docker
POSTGRES_PORT=5432
```
## 5. Set up your docker
```bash
docker compose build up -d
```
## 6. Apply migrations
Run the migrations to set up the database:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
## 7. Run the development server 
```bash
docker-compose exec web python manage.py runserver
```
You can now access the application at http://127.0.0.1:8000/.
## 8. Tests
To run the tests with coverage:
```bash
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
docker-compose exec web coverage html
```


