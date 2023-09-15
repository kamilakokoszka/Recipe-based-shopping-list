# RECIPE BASED SHOPPING LIST
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![PyTest](https://img.shields.io/badge/Pytest-003A9B?style=for-the-badge&logo=pytest&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

Recipe based shopping list is a Django-based web application that allows users to create shopping lists 
by marking recipes they want to cook. It's perfect for individuals who like to plan their meals in advance.

## Features

* **User Authentication:** Create user accounts, log in, and log out securely.
* **Recipe Management:** Add, edit, and delete recipes with dynamic ingredient handling.
* **Independent Ingredients:** Manage frequently purchased products independently, allowing you to create, delete, and update items.
* **Shopping List:** Generate shopping lists by selecting recipes from your cookbook and adding items from your independent ingredient list. Check off purchased items.
* **List Display:** View shopping lists, recipes, and ingredient lists with detailed information.

## Recipe Based Shopping List App Preview


## Installation

Follow these steps to set up Recipe Based Shopping List on your local machine:

1. **Clone the Repository:** Download the project by running the following command in your terminal:
```
git clone https://github.com/kamilakokoszka/Recipe-based-shopping-list
```
2. **Create a Virtual Environment:** Navigate to the project directory and create a virtual environment:
```
python -m venv venv
```
3. **Activate the Virtual Environment:** Activate the virtual environment based on your operating system:
- On Windows:
    ```shell
    venv\Scripts\activate
    ```
    - On macOS/Linux:
    ```shell
    source venv/bin/activate
    ```
4. **Install Required Packages:** Install the project dependencies by running:
```
pip install -r requirements.txt
```
5. **Set Up Environment Variables:** Update the `settings.py` file with appropriate values for the following variables:
- `SECRET_KEY`
- `DATABASES`: Update `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` and `DB_PORT`
6. **Run the Application:** Start the development server by executing the following command:
```
python manage.py runserver
```
7. **Access the Application:** Open your web browser and navigate to http://localhost:8000/.

