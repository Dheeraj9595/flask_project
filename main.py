from flask import Flask, render_template
from users import users_bp
from orders import orders_bp
from uploads import uploads_bp


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Flask App', welcome_message='Welcome to the....',
                           content='Home Page.')


# Register users_bp and orders_bp with the app
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(uploads_bp, url_prefix='/upload')

if __name__ == "__main__":
    app.run(debug=True)
