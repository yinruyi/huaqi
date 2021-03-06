#coding=utf-8

import os
import json
from flask import Flask
from flask import request
from flask import make_response
from flask import send_file
from pymongo import MongoClient
from flask.ext.pymongo import PyMongo, DESCENDING
from bson import Binary, Code, ObjectId
import shutil
ITEMS_PER_PAGE = 10

app = Flask("huaqi")
app.config.from_pyfile('config.cfg')
mongo = PyMongo(app)


conn = MongoClient('localhost', 27017)
db = conn.huaqi


@app.route('/')
def index():
    return make_response(open('index.html').read())

@app.route('/test')
def test():
    return "test"

@app.route('/test/<p_id>')
def test():
    return p_id

@app.route('/login', methods=['GET', 'POST'])
def login():
    print 'sss'
    req = json.loads(request.data)
    conn = MongoClient('localhost', 27017)
    print req
    db = conn.huaqi
    user = db.user_info.find_one({'name':req['name']})
    if user:
        if user['password']==req['password']:
            print "ok"
            return json.dumps({'status':'ok','user_id':str(user['id'])})
    print "error"
    return json.dumps({'status':'error'})



@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']

    return resp



@app.route('/api/mongo/<mdb>', methods=['GET', 'POST'])
def api_mongo(mdb):
    conn = MongoClient('localhost', 27017)
    db = conn.huaqi
    if request.method == 'POST':
        #print data
        data = json.loads(request.data)
        print data

        if '_id' not in data:
            data['_id'] = str(ObjectId())
        return mongo.db[mdb].save(data)
    elif request.method == 'GET':
        # 预备query
        r_query = request.args.to_dict()

        # 筛选条件
        if r_query.has_key('filters'):
            filters = json.loads(r_query['filters'])
            del r_query['filters']
        else:
            filters = {}

        # 分页条件
        if r_query.has_key('page'):
            page = int(r_query['page']) - 1
            del r_query['page']
        else:
            page = 0

        # 查找数据
        num_results = mongo.db[mdb].find(filters).count()
        total_pages = int(num_results / (ITEMS_PER_PAGE + 0.1)) + 1
        objects = mongo.db[mdb].find(filters).sort('_id', -1).skip(page * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE)

        # 返回数据
        res = {'objects': objects, 'num_results': num_results, 'page': page + 1, 'total_pages': total_pages}
        return dumps(res)
    else:
        return 'error'


@app.route('/api/mongo/<mdb>/<did>', methods=['GET', 'PUT', 'DELETE'])
def api_mongo_id(mdb, did):
    if request.method == 'PUT':
        data = json.loads(request.data)
        data_id = mongo.db[mdb].save(data)
        # 返回
        return 'update'
    elif request.method == 'GET':
        # 查找数据
        data = mongo.db[mdb].find_one({'id': did})
        del data['_id']
        # 返回
        data = json.dumps(data)
        print '###########'
        print data
        print '####'
        return data
    elif request.method == 'DELETE':
        # 查找数据
        data = mongo.db[mdb].remove({'id': did})
        # 返回
        return 'remove'
    else:
        return 'error'

@app.route('/api/mongodb/<mdb>', methods=['GET', 'POST'])
def api_mongo2(mdb):
    conn = MongoClient('localhost', 27017)
    db = conn.huaqi
    if request.method == 'POST':
        data = json.loads(request.data)
        return mongo.db[mdb].save(data)
    elif request.method == 'GET':
        # 预备query
        r_query = request.args.to_dict()

        # 筛选条件
        if r_query.has_key('filters'):
            filters = json.loads(r_query['filters'])
            del r_query['filters']
        else:
            filters = {}
        # 查找数据
        num_results = mongo.db[mdb].find(filters).count()
        objects = mongo.db[mdb].find(filters)

        objects_detil = list(objects)
        for i in objects_detil:
            del i['_id']

        # 返回数据
        res = {'objects': objects_detil, 'num_results': num_results}

        return json.dumps(res)
    else:
        return 'error'
#--------------------------------------------------
#android_api
@app.route('/api/register', methods=['GET', 'POST'])
def api_and_register():
    req = json.loads(request.data)
    conn = MongoClient('localhost', 27017)
    db = conn.huaqi
    if req.has_key('name') and req.has_key("email") and req.has_key("password"):
        if "@" not in req['email']:
            print "1001"
            return '1001'
        if db.user_info.find_one({'email':req['email']}):
            print "1002"
            return "1002"
        if db.user_info.find_one({"nick_name":req["name"]}):
            print "1003"
            return "1003"
        if len(req['password']) < 6 or len(req['password']) > 12:
            print "1004"
            return "1004"
        import random
        user_id = str(random.randint(100000,999999))
        id_find = db.user_info.find_one({'id':user_id})
        while id_find != []:
            user_id = str(random.randint(100000,999999))
            id_find = db.user_info.find_one({'id':user_id})
        req["id"] = user_id
        print req
        db.user_info.save(req)
        return "1000",user_id
    else:
        print "1005"
        return "1005"

@app.route('/api/register2', methods=['GET', 'POST'])
def api_and_register_update():
    req = json.loads(request.data)
    conn = MongoClient('localhost', 27017)
    db = conn.huaqi
    if req.has_key('id'):
        id_find = db.user_info.find_one({'id':req['id']})
        if str(id_find) == "None":
            return "1006"
        else:
            del req["id"]
            db.user_info.update({"id":id_find["id"]},{"$set":req})
            return "1007"

#实名认证TODO
@app.route('/api/upload', methods=['GET','POST'])
def api_upload():
    result = dict()

    # Process get request
    if request.method == "GET":
        return '未实现此功能',400

    # Process post request
    elif request.method == "POST":
        #{{{
        result['id'] = request.form['flowIdentifier']
        result['filename'] = request.form['flowFilename']
        result['current_chunk'] = request.form['flowChunkNumber']
        result['total_chunks'] = request.form['flowTotalChunks']
        result['file'] = request.files['file']
        #print result['current_chunk']
        if os.path.exists('upload/' + result['filename']):
            os.remove('upload/' + result['filename'])

        if not os.path.exists(result['id']):
            temp_path = os.mkdir(result['id'])

        with open( result['id']+'/'+result['filename']+'.'+result['current_chunk'], 'wb') as f:
            f.write(result['file'].read())

        if result['current_chunk'] == result['total_chunks']:
            filenames = os.listdir(result['id'])
            filenames.sort(key=lambda k: int(k.split('.')[-1]))
            with open('upload/' + result['filename'], 'ab') as fin:
                for filename in filenames:
                    with open(result['id']+'/'+filename, 'rb') as fout:
                        fin.write(fout.read())
            shutil.rmtree(result['id'])

        #}}}
        return result['filename']
    else:
        return 'err', 400
#推广
@app.route('/api/spread', methods=['GET','POST'])
def api_and_spread():
    data = json.loads(request.data)
    if data.has_key('qua'):
        kk = data['qua']
    else:
        kk = 3
    conn = MongoClient('localhost', 27017)
    db = conn.huaqi
    data_find = db.trans_info.find().sort("pe",pymongo.DESCENDING)
    if str(data_find) == "None":return "1008"
    data_find = data_find[0:kk]
    data2return = []
    for i in data_find:
        data_dic = {}
        data_dic["id"] = i['id']
        data_dic["pic"] = i["picture"][0]
        data2return.append(data_dic)
    res = {"id_pic":data2return}
    return json.dumps(res)

#获取某行业所有项目？TODO
@app.route('/api/project/<in_id>/<p_id>', methods=['GET','POST'])
def api_get_pro():
    #data = json.loads(request.data)
    if data.has_key("qua"):
        kk = int(p_id)
        conn = MongoClient('localhost', 27017)
        db = conn.huaqi
        data_find = db.trans_info.find({"industry_id":"in_id"}).sort("id",pymongo.DESCENDING)
        data_find = data_find[kk-20,kk]
        return data_find
    else:
        return "1009"
        
#获取某项目的信息
@app.route('/api/project/<p_id>', methods=['GET','POST'])
def api_get_project_detail():
    conn = MongoClient('localhost', 27017)
    db = conn.huaqi
    data_find = db.trans_info.find_one({"project_id":"p_id"})
    if str(data_find) != "None":
        res = {"info":data_find}
        return json.dumps(res)
    else:
        return "1010"


#获取我的购买
@app.route('/api/project/<my_id>', methods=['GET','POST'])
def api_get_mybuy():
    conn = MongoClient('localhost', 27017)
    db = conn.huaqi
    find = db.trade_info.find({"buyer_id":my_id})
    if str(find) == "None":
        return "1010"
    else:
        return 'test'
#        for i in find:
#            del i['_id']
#            temp = []
#            pro_find = db.trans_info.find_one("id":i['project_id'])
#            if 








if __name__ == "__main__":
    app.run()
