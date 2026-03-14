from flask import Flask, request, session, redirect, template_rendered
import logging
from utils.config import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def auth():
    if request.path.startswith('/static'):
        return
    
    if request.path == '/login':
        return

    user_info = session.get('user_info')
    if user_info:
        return
    
    logger.warning(f"Unauthorized access attempt: {request.path}")
    return redirect('/login')

def get_real_name():
    user_info = session.get('user_info')
    if not user_info:
        return ''
    return user_info.get('real_name', '')

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.secret_key = app.config['SECRET_KEY']

    from .views import account
    from .views import order
    app.register_blueprint(account.ac)
    app.register_blueprint(order.od)
    app.template_global()(get_real_name)

    app.before_request(auth)
    
    logger.info("Application started")

    return app
