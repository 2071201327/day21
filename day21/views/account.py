from flask import Blueprint, render_template, request, redirect, session
from utils.db import fetch_one
import logging

logger = logging.getLogger(__name__)

ac = Blueprint('account', __name__)

@ac.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    role = request.form.get("role")
    mobile = request.form.get("mobile")
    pwd = request.form.get("pwd")

    if not all([role, mobile, pwd]):
        return render_template("login.html", error="请填写完整信息")

    try:
        user_dict = fetch_one(
            "select * from userinfo where role=%s and mobile=%s and password=%s",
            (role, mobile, pwd)
        )
    except Exception as e:
        logger.error(f"Login database error: {e}")
        return render_template("login.html", error="系统错误，请稍后重试")

    if user_dict:
        session["user_info"] = {
            "role": user_dict["role"],
            "real_name": user_dict["real_name"],
            "id": user_dict["id"]
        }
        logger.info(f"User {user_dict['id']} logged in as role {role}")
        return redirect('/order/list')
    
    return render_template("login.html", error="用户名/密码错误")


@ac.route('/users')
def users():
    return "用户列表"

@ac.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
