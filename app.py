from flask import Flask, render_template, request
from users import User
from weather import fetch_weather

app = Flask(__name__)


# Инициализируем экземпляр класса User для работы с пользователями
user_manager = User()


# Основной маршрут для отображения главной страницы
@app.route('/', methods=['GET', 'POST'])
def index():
    # Получаем информацию о пользователях из базы данных
    users_info = user_manager.get_all_users()
    return render_template('index.html', users_info=users_info)


# Путь для добавления нового пользователя
@app.route('/add_user', methods=['POST'])
def add_user():
    """Получаем данные для создания нового пользователя из запроса"""
    username = request.form['username']
    balance = request.form['balance']
    user_manager.add_user(username=username, balance=balance)
    return render_template('user_management.html')


# Путь для страницы управления пользователями
@app.route('/user_management', methods=['GET', 'POST'])
def user_management():
    return render_template('user_management.html')


# Путь для обновления данных пользователя
@app.route('/update_user', methods=['POST'])
def update_user():
    """Получаем ID и новый username для обновления"""
    user_id = request.form['user_id']
    username = request.form['username']
    user_manager.update_user(user_id, new_username=username)
    return render_template('user_management.html')


# Путь для удаления пользователя
@app.route('/delete_user', methods=['POST'])
def delete_user():
    """Получаем ID пользователя для удаления"""
    user_id = request.form['user_id']
    user_manager.delete_user(user_id)
    return render_template('user_management.html')


# Путь для обновления баланса пользователя
@app.route('/update_balance', methods=['GET', 'POST'])
def update_balance():
    """ Получаем ID пользователя и новый баланс из запроса.
        Вычисляем обновленный баланс и отправляем новое значение в базу"""
    if request.method == 'POST':
        user_id = request.form['user_id']
        city = request.form['city']
        temperature = int(fetch_weather(city))
        current_balance = user_manager.get_balance(user_id)
        if current_balance and current_balance + temperature > 0:
            current_balance += temperature
        user_manager.update_balance(user_id, current_balance)
        return render_template('/update_balance.html', weatherInfo=f'Temp in {city} = {temperature}')
    else:
        return render_template('/update_balance.html')


if __name__ == '__main__':
    app.run(debug=True)
    