from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# 确保在数据库初始化之前推送应用程序上下文
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': '登录成功', 'user_id': user.id}), 200
    return jsonify({'message': '用户名或密码错误'}), 401

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_data = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(user_data)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5001)
