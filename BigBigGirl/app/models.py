from app import db
from datetime import datetime


#数据库模型
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(25), index=True, unique=True)
    password= db.Column(db.String(128))
    face_id = db.Column(db.Text)






class Report(db.Model):
    __tablename__='report'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text,nullable=False)
    content=db.Column(db.Text,nullable=False)
    #now函数是每一次创建一个博客就会有一个时间
    #now()是第一次执行这句语句的时间
    create_time=db.Column(db.DateTime,default=datetime.now)
    #增加admin外键
    admin_id= db.Column(db.Integer, db.ForeignKey('admin.id'))



db.create_all()