from flask import  session,redirect,render_template,url_for
from functools import wraps
from app import routes


#登录限制
def login_required(func):
    @wraps(func)
    def wrapper1(*args,**kwargs):
        admin_login=session.get('admin_id')
        if admin_login:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('/face_login'))
    return wrapper1





