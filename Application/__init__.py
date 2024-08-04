# Code is inspired by: https://realpython.com/flask-google-login/ 

from flask import Flask, redirect, render_template, url_for, request
from instance import IApplicationConfiguration
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
import json
from icecream import ic
import requests # type: ignore

class Base(MappedAsDataclass, DeclarativeBase):
    pass

db: SQLAlchemy = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
GOOGLE_OPENID_CONFIG_URL = 'https://accounts.google.com/.well-known/openid-configuration'

def create_app(config: IApplicationConfiguration, /) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    client = WebApplicationClient(app.config['GOOGLE_CLIENT_SECRETS']['client_id'])
    
    db.init_app(app)
    from Application.models import User
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    @app.get('/')
    def index():
        if current_user.is_authenticated:
            return render_template('welcome.html', user=current_user)
        return '<a class="button" href="/login">Google Login</a>'
    
    @app.get('/login')
    def login():
        provider_cfg = requests.get(GOOGLE_OPENID_CONFIG_URL).json()
        request_uri = client.prepare_request_uri(
            uri=provider_cfg['authorization_endpoint'],
            redirect_uri=app.config['GOOGLE_CLIENT_SECRETS']['redirect_uris'][0],
            scope=['openid', 'email', 'profile']
        )
        return redirect(ic(request_uri))
    
    @app.get('/callback')
    def callback():
        code = ic(request.args.get('code'))
        provider_cfg = requests.get(GOOGLE_OPENID_CONFIG_URL).json()
        token_url, headers, body = client.prepare_token_request(
            provider_cfg['token_endpoint'],
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(app.config['GOOGLE_CLIENT_SECRETS']['client_id'], app.config['GOOGLE_CLIENT_SECRETS']['client_secret']),
        )

        client.parse_request_body_response(ic(json.dumps(token_response.json())))
        uri, headers, body = client.add_token(provider_cfg['userinfo_endpoint'])
        userinfo_response = ic((requests.get(uri, headers=headers, data=body)).json())

        if userinfo_response.get("email_verified"):
            sub = userinfo_response["sub"]
            user_email = userinfo_response["email"]
            picture = userinfo_response["picture"]
            user_name = userinfo_response["name"]
        else:
            return "User email not available or not verified by Google.", 400

        user = User.query.filter_by(sub=sub).one_or_none() 
        if not user:
            user = User(sub=sub, email=user_email, dp_url=picture, name=user_name)
        else:
            user.name = user_name
            user.dp_url = picture
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index'))
    

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        ic('User logged out')
        return redirect(url_for("index"))
    
    @app.get("/delete")
    @login_required
    def delete_account():
        user = User.query.filter_by(sub=current_user.sub).one_or_none() 
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))


    return app