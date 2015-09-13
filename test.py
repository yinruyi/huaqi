# -*- coding: UTF-8 -*-
import os
import app
import unittest
import json
import time
from pymongo import MongoClient
from bson import Binary, Code, ObjectId

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_login(self):
        #print '####'
        k = {"name":"zed","password":"985674"}
        k = json.dumps(k)
        #print k
        #rrr = self.app.post('/login',data = k)
        #print rrr
        #print '####'

    def test_api_mongodb_post(self):
        k = {"name":"admin","password":"123"}
        k = json.dumps(k)
        #print k
        #rrr = self.app.post('/api/mongodb/user',data = k)
        #print rrr
    def test_api_mongo_id_get(self):
        pass
        #rrr = self.app.get('/api/mongo/user_info/10000',data = {})

    def test_api_register(self):
        k = {"name":"yinruyi","password":"qwertyuiop","email":"1234@qq.com"}
        k = json.dumps(k)
        #rrr = self.app.post("/api/register",data = k)

    def test_test2(self):
        k = {}
        k = json.dumps(k)
        #print 'start'
        #rr = self.app.get("/test/aa",data = {})
    def test_mydetil(self):
        k = {}
        k = json.dumps(k)
        #rr = self.app.get("/api/mydetil/10000",data = {})

    def test_api_reg(self):
        k = {"name":"yinruyi","email":"9@qq.com","password":"1234567"}
        k = json.dumps(k)
        #rr = self.app.post("/api/register",data = k)

    def test_api_reg2(self):
        k = {"id":"699926","age":"18"}
        k = json.dumps(k)
        #rr = self.app.post("/api/register2",data = k)
    
    def test_api_spread(self):
        #rr = self.app.get("/api/spread",data = {})
        pass

    def test_api_project_inid_pid(self):
        #rr = self.app.get("/api/project/05/20",data = {})
        pass

    def test_api_project_pid(self):
        #rr = self.app.get("/api/project/10004",data = {})
        pass

    def test_api_api_trans_myid(self):
        rr = self.app.get("/api/trans/10000")






    '''
    def test_result_new_create(self):
        k = {'params':{'model_method':'decision_tree'}, 'method':'data_analysis.DiseaseDiscriminantModelCompared', 'dataset':{'feature':['55a61cdd816a9519fc494adc', '55a71c35816a950cc839405f'], 'target':'55a61cd6816a9522e8bd062b'}}
        k = json.dumps(k)
        j = {'params':{'model_method':'svm'}, 'method':'data_analysis.DiseaseDiscriminantModelSingle', 'dataset':{'feature':'55a61cdd816a9519fc494adc', 'target':'55a61cd6816a9522e8bd062b'}}
        j = json.dumps(j)
        self.app.get('/api/dataset_new/feature', query_string = {'file':'test_result_data.csv'})
        rrr = self.app.post('/api/result_new/create', data = k)


        ddd = self.app.post('/api/result_new/create', data = j)
        sleep(100)

    #   rr = self.app.post
    '''
if __name__ == '__main__':
    unittest.main()
