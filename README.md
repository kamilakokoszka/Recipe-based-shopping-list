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
* **Independent Ingredients:** Manage frequently purchased products independently, allowing you to create, delete and update items.
* **Shopping List:** Generate shopping lists by selecting recipes from your cookbook and adding items from your independent ingredient list. Check off purchased items.
* **List Display:** View shopping lists, recipes and ingredient lists with detailed information.

## Recipe Based Shopping List App Preview
<<<<<<< HEAD

=======
>>>>>>> a33d335b0175878cdd5f53bcd52dc4dd9695a88b
![ss_1](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/293aaaaf-c70a-49a1-aadc-64c78282ee96)
![ss_2](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/f6fe193f-c0b6-4ed7-833d-18721de60f7e)
![ss_3](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/134cfcd3-cd53-44d6-8a0e-0e3db170314c)
![ss_4](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/325e3055-ecd9-423e-87ee-d53b6e73ec44)
![ss_5](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/a21c5c54-1c58-4937-91e5-6de74a20bf63)
![ss_6](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/d8001107-c760-4398-8af8-90e2143c6abc)
![ss_7](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/a5c9b9d8-6f5e-439e-855d-09618d0f2b0d)
![ss_8](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/7f2e489b-a2c3-44c1-9b0f-ea87daf26b43)

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

