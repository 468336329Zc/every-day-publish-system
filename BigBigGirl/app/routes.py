from app import myapp
from flask import render_template, request, redirect, session, jsonify
from app.models import Admin, Report
from app import db
from app.decorators import login_required
from app.Util import Face_check
import datetime
import base64
import os




@myapp.route('/')
def home():
    return render_template("auth/home.html")


@myapp.route("/login", methods=['GET', "POST"])
def login():
    if request.method == 'GET':
        return render_template("admin/admin_login.html")
    else:
        # 获取登陆输入的数据
        name = request.form.get('username')
        password = request.form.get('password')
        # 查找数据库中表数据进行比对
        user_have = Admin.query.filter(Admin.name == name)
        user = Admin.query.filter(Admin.name == name, Admin.password == password).first()
        # 如果有这个用户
        if user_have:
            if user:
                # 保存cookie信息  31天内不用重复登陆
                session['admin_id'] = user.id
                session.permanent = True
                return redirect('/own_center')
            else:
                return render_template('admin/admin_login.html')
        else:
            return render_template("admin/admin_login.html")


@myapp.route('/face_login',methods=['GET'])
def face_login():
    if request.method=="GET":
        return render_template('admin/face-login.html')

@myapp.route('/face_login/get_face',methods=['POST'])
def get_face():
    if request.method=='POST':
        time = datetime.datetime.now().strftime('%Y%m%d&%H%M%S')
        strs = request.form.get('face_id')
        # 解码base64
        imgdata = base64.b64decode(strs)

        try:
            file = open('app/static/images/facedata/confirm/' + time + '.jpg', 'wb')

            file.write(imgdata)
            file.close()
        except:
            # json数据返回
            data = {"status": "-1"}
            return data
        # 查询所有的face_id
        try:
            bases64 = db.session.query(Admin.face_id).all()
        except:
            data = {'status': '-1'}
            return data
        for b64 in bases64:
            # 对每一个取出来的进行解码，写入register文件，之后在于confirm中的图片进行对比
            b64 = str(b64[0])
            img = base64.b64decode(b64)
            try:
                file2 = open('app/static/images/facedata/register/' + time + '.jpg', 'wb')
                file2.write(img)
                file2.close()
            except:
                # json数据返回
                data = {"status": "-1"}
                # 对比一次就把照片删除了，防止占内存
                os.remove("app/static/images/facedata/register/" + time + '.jpg')
                os.remove("app/static/images/facedata/confirm/" + time + '.jpg')
                return data
            time = datetime.datetime.now().strftime('%Y%m%d&%H%M%S')

            known_face_encoding = Face_check.register_encoding_face('app/static/images/facedata/register/' + time + '.jpg')

            try:
                match_results = Face_check.check_face(known_face_encoding,
                                                      "app/static/images/facedata/confirm/" + time + '.jpg')
            except:
                data = {"status": '-2'}
                # 对比一次就把照片删除了，防止占内存
                os.remove("app/static/facedata/register/" + time + '.jpg')
                os.remove("app/static/facedata/confirm/" + time + '.jpg')
                return data

            if match_results[0] == True:

                # 登录成功就加入session
                user = Admin.query.filter(Admin.face_id == b64).first()
                session['admin_id'] =user.id
                session.permanent = True
                data = {'status': '1'}
                # 对比一次就把照片删除了，防止占内存
                os.remove("app/static/images/facedata/register/" + time + '.jpg')
                os.remove("app/static/images/facedata/confirm/" + time + '.jpg')
                return data
            else:
                # 由于浏览器还是认为是text/html数据 因此使用mimetype说明是json数据
                data = jsonify({"status": "0", "face_distance": 'not one person'})
                # 对比一次就把照片删除了，防止占内存
                os.remove("app/static/images/facedata/register/" + time + '.jpg')
                os.remove("app/static/images/facedata/confirm/" + time + '.jpg')
                return data


@myapp.route('/report_show')
def report_show():
    params = {
        # 展示最新1天的，就是6条数据
        'reports': Report.query.order_by(Report.create_time.desc()).limit(6),
        'latest_time':Report.query.order_by(Report.create_time.desc()).first()
    }
    return render_template('auth/report_show.html', **params)


###############################################admin#########################################
@myapp.route('/own_center')
@login_required
def own_center():
    return render_template("admin/own_center_base.html")



@myapp.route('/publish', methods=["GET", "POST"])
@login_required
def publish():
    if request.method == "GET":
        admin_id = session.get('admin_id')
        admin_name = Admin.query.filter(Admin.id == admin_id).first().name
        contexts={"admin_name":admin_name}
        return render_template("admin/publish.html",**contexts)
    else:
        #每次写新报告之前删除之前的报告,根据登录id删除之前的记录
        admin_id = session.get('admin_id')
        old_record=Report.query.filter(Report.id==admin_id).first()
        try:
            db.session.delete(old_record)
            db.session.commit()
            #获取新的report并添加进数据库
        except:
           pass
        name=Admin.query.filter(Admin.id==admin_id).first().name
        content=request.form.get('content')

        report=Report(id=admin_id,content=content,name=name,admin_id=admin_id)
        db.session.add(report)
        db.session.commit()
        return redirect('/report_show')




@myapp.route('/republish/',methods=['GET','POST'])
def republish():
    if request.method=='GET':
        # # 获取当前登录账户信息，根据登录时的session
        admin_id = session.get('admin_id')
        admin_name = Admin.query.filter(Admin.id == admin_id).first().name
        # 在report表里找到当前用户的admin_id，这样就能找到这个用户的记录了。
        newest_content= Report.query.filter(Report.admin_id == admin_id).order_by(Report.create_time.desc()).first()
        contexts = {"admin_name": admin_name,
                    "newest_content":newest_content}
        return render_template('admin/republish.html', **contexts)
    else:
        try:
            #获取之前最新写的数据，然后替换
            admin_id = session.get('admin_id')
            admin_name = Admin.query.filter(Admin.id == admin_id).first().name
            re_content=request.form.get('re_content')
            report= Report.query.filter(Report.id == admin_id).order_by(Report.create_time).first()
            report.name =admin_name
            report.content=re_content
            db.session.add(report)
            db.session.commit()

            return redirect('/report_show')
        except:
            return "后台错误"


@myapp.route('/alter_pwd',methods=['GET','POST'])
def alter_pwd():
    if request.method=='GET':
        return render_template('admin/alter_pwd.html')
    else:
        try:
            #根据获取session得知是哪个管理员，然后修改其密码
            admin_id=session.get('admin_id')
            new_pwd=request.form.get('new_pwd')
            admin=Admin.query.filter(Admin.id==admin_id).first()
            admin.password=new_pwd
            db.session.add(admin)
            db.session.commit()
            return render_template('admin/Redenglu_tiaozhuan.html')
        except:
            return "后台错误，请重新登录"



