# RECIPE-BASED SHOPPING LIST
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![PyTest](https://img.shields.io/badge/Pytest-003A9B?style=for-the-badge&logo=pytest&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

Recipe-based shopping list is a Django-based web application that allows users to create shopping lists 
by marking recipes they want to cook. It's perfect for individuals who like to plan their meals in advance.

**Unfortunately, due to Railway database provider's temporary problems, the app is currently unavailable :(**

**App screenshots are available below.**

App deployed on Vercel: https://recipe-based-shopping-list.vercel.app/

Test account:
* username: testuser
* password: Testpass123

## Features

* **User Authentication:** Create user accounts and log in and out securely.
* **Recipe Management:** Add, edit, and delete recipes with dynamic ingredient handling.
* **Independent Ingredients:** Manage frequently purchased products independently, allowing you to create, delete and update items.
* **Shopping List:** Generate shopping lists by selecting recipes from your cookbook and adding items from your independent ingredient list. Check off purchased items.
* **List Display:** View shopping lists, recipes, and ingredient lists with detailed information.

## Recipe-based Shopping List App Preview

![ss_1](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/963a2939-89cd-49be-94d7-9fa7bb84d9fe)
![ss_2](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/091b1b01-d399-4241-b951-712291269978)
![ss_3](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/9bdfb223-cce6-403f-ab59-d2633fe7f560)
![ss_4](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/b8d2e07e-2bd0-4c88-b379-d36eed765caf)
![ss_5](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/cea35d72-1670-4ee5-9392-00b8a3b065b1)
![ss_6](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/123e8403-1407-4c79-b6bd-26de98eeeb85)
![ss_7](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/df2ad360-7940-4029-9b00-f72d1a69fcc8)
![ss_8](https://github.com/kamilakokoszka/Recipe-based-shopping-list/assets/127201515/81634b79-62a7-47af-b84e-088b2d32798d)

## Installation

Follow these steps to set up Recipe-based Shopping List on your local machine:

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
- `DATABASES`: Update `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` and `DB_PORT` and comment `DB_URL`
6. **Run the Application:** Start the development server by executing the following command:
```
python manage.py runserver
```
7. **Access the Application:** Open your web browser and navigate to http://localhost:8000/.

