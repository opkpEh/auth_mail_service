from flask import Flask, request, jsonify, session, url_for
from pymongo import MongoClient
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['MONGO_URI'] = 'mongodb+srv://kushagra:kushagra@testemailauth.qfdj8.mongodb.net/?retryWrites=true&w=majority&appName=testEmailAuth'
app.config['MONGO_DBNAME'] = 'emailauthtest'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config["SECURITY_PASSWORD_SALT"] = "DJ9x1"
app.config['MAIL_USERNAME'] = 'crisp.email.auth@gmail.com'
app.config['MAIL_PASSWORD'] = 'njyc nxkm kxsj mkms'
app.config['MAIL_DEFAULT_SENDER'] = 'crisp.email.auth@gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False


try:
    client = MongoClient(app.config['MONGO_URI'])
    mongo_db = client[app.config['MONGO_DBNAME']]
    client.server_info()
except Exception as e:
    print(e)

def send_email(to,subject, template):
    msg= Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )

    mail.send(msg)

@app.route('/')
def hello_world():
    return jsonify("Hello World!")


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        new_user = {
            'username': username,
            'email': email,
            'password': password,
            'is_confirmed': False,
            'confirmed_on': None
        }
        mongo_db.users.insert_one(new_user)
        session['email']=email
        token = generate_token(email)
        return jsonify({'status': 'ok', 'token': token})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    user = mongo_db.users.find_one({'email': email, 'password': password})
    if user['is_confirmed']:
        session['email'] = email
        session['username'] = username
        return jsonify({'status': 'logged in'})
    return jsonify({'status': 'failed'}), 401

@app.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return jsonify({'error': 'Invalid or expired token'}), 400

    user = mongo_db.users.find_one({"email": email})
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    mongo_db.users.update_one(
        {"email": email},
        {
            "$set": {
                "is_confirmed": True,
                "confirmed_on": datetime.now()
            }
        }
    )

    return jsonify({'message': "You have confirmed your account. Thanks!"})

@app.route('/register', methods=['GET','POST'])
def register():
    token= generate_token(session['email'])
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #fff;
                max-width: 600px;
                margin: 20px auto;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 15px;
                color: #fff;
                background-color: #007bff;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Welcome to Crisp!</h2>
            <p>Thank you for signing up. Please confirm your email address by clicking the button below:</p>
            <a href="{confirm_url}" class="btn">Confirm Email</a>
            <p>If the button above does not work, copy and paste the following URL into your web browser:</p>
            <p><a href="{confirm_url}">{confirm_url}</a></p>
            <p>Thanks,<br>The Crisp Team</p>
        </div>
    </body>
    </html>
    """
    subject = 'Welcome to crisp!'
    send_email(session['email'],subject,html)

    return jsonify({'message': 'Mail sent'})

@app.route('/profile')
def profile():
    if 'email' not in session:
        return jsonify({'error': 'You must be logged in to access this route'}), 401

    user = mongo_db.users.find_one({"email": session['email']})
    if user:
        if not user.get('is_confirmed', False):
            return jsonify({'error': 'Please confirm your email to access the profile'}), 403

        return jsonify({
            'username': user.get('username'),
            'email': user.get('email'),
            'is_confirmed': user.get('is_confirmed', False)
        })
    return jsonify({'error': 'User not found'}), 404

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'You have been logged out'})


if __name__ == '__main__':
    app.run()