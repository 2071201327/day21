from flask import Blueprint, redirect, session, render_template, request
from utils import db
from utils import cache
import logging

logger = logging.getLogger(__name__)

od = Blueprint('order', __name__)

@od.route('/order/list', methods=['GET', 'POST'])
def order_list():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    
    role = user_info.get('role')
    real_name = user_info.get('real_name', '')
    
    try:
        if role == 2:
            data_list = db.fetch_all("select * from `order` left join userinfo on `order`.user_id = userinfo.id",[])
        else:
            data_list = db.fetch_all("select * from `order` left join userinfo on `order`.user_id = userinfo.id where `order`.user_id = %s ",[user_info.get('id'), ])
    except Exception as e:
        logger.error(f"Failed to fetch orders: {e}")
        data_list = []

    static_dict = {
        1:{"text":"待执行","cls":"primary"},
        2:{"text":"正在执行","cls":"info"},
        3:{"text":"完成","cls":"success"},
        4:{"text":"失败","cls":"danger"}
    }

    return render_template("order_list.html", data_list=data_list, static_dict=static_dict, real_name=real_name)

@od.route('/order/create' , methods=['GET', 'POST'])
def order_create():
    if request.method == 'GET':
        return render_template('order_create.html')
    
    url = request.form.get('url')
    count = request.form.get('count')
    
    if not url or not count:
        return render_template('order_create.html', error="请填写完整信息")
    
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    
    try:
        params = [url, count, user_info['id']]
        order_id = db.insert("insert into `order`(url,count,user_id,status) values(%s,%s,%s,1)", params)
        cache.push_queue(order_id)
        logger.info(f"Order created: {order_id} by user {user_info.get('id')}")
    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        return render_template('order_create.html', error="创建订单失败")

    return redirect("/order/list")

@od.route('/order/delete')
def delete_list():
    order_id = request.args.get('id')
    if not order_id:
        return "缺少订单ID", 400
    
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    
    role = user_info.get('role')
    
    try:
        if role == 2:
            db.execute("delete from `order` where id = %s", [order_id,])
        else:
            db.execute("delete from `order` where id = %s and user_id = %s", [order_id, user_info['id']])
        logger.info(f"Order deleted: {order_id} by user {user_info.get('id')}")
    except Exception as e:
        logger.error(f"Failed to delete order {order_id}: {e}")
        return "删除失败", 500
    
    return redirect("/order/list")
