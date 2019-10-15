from flask import Flask, config
from config import Config
from flask_sqlalchemy import SQLAlchemy
myapp= Flask(__name__)
myapp.config.from_object(Config)
db = SQLAlchemy(myapp)
#添加路由
from app import routes,models

