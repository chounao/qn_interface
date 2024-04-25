import requests
import json
import random
import time
import os
# import yaml

class Custom_Print:
    def __init__(self):
        self.url = 'https://qnjy.xyy001.com/'
        self.token = "%7EUwMIBAFVAQNUVgNSHwYDG1ddDAxUVQoDAgEV04WShrTy1rGj09qGWx8HHwNSWEBSSlUUVxYJXxgAAQkHDgBSCVFUAQUCUgdWXwEGUQFRCwNXAQ9bUT9pBVVXDg8KVlANAlFaBFUCDwVeVgZSAw0EA1RdCQ%3D%3D%7E1%7E"
        self.headers = {"Content-Type":"application/x-www-form-urlencoded;charset = UTF-8"}
        self.customPrintAddress_path = 'customPrint/getSellerCustomPrintAddressPaging.do' #发货地址
        self.ConsigneePrintAddress_path = 'customPrint/getSellerConsigneePrintAddressPaging.do'#收件地址



        self.saveSellerCustomPrint_path = 'customPrint/saveSellerCustomPrintTradeWait.do'#自定义保存
        self.waybillGet_path = 'customPrint/cainiao/waybillGet.do'#获取面单
        self.updateSellerCustomPrintTradePrintInfo = 'customPrint/updateSellerCustomPrintTradePrintInfo.do'#把面单更新到界面上
        self.saveWaybillLogs = 'print/saveWaybillLogs.do'
        self.getSellerTradePrintsSimpleInfo = 'printv2/getSellerTradePrintsSimpleInfo.do'
        self.updateSellerCustomPrintTradePrint = 'customPrint/updateSellerCustomPrintTradePrint.do'#打印后更新
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.yamlpath = self.path + '\print_count.yaml'

    def update_session(self):
        self.s = requests.session()
        self.s.headers.update(self.headers)
        return self.s
    def get_custom_data(self):#随机获取一个发货地址和收件地址并存储在yaml文件
        data1 = {
            'page': 1,
            'pageSize': 100,
            'queryAddress': None,
            'token': self.token
        }
        r1 = self.update_session().post(url=self.url + self.customPrintAddress_path, data=data1)
        d1 = json.loads(r1.text)

        l1 = d1['data']['list']

        sender_content = random.choice(l1)  # 随机选择发件人

        data2 = {
            "page": 1,
            "pageSize": 100,
            "token": self.token
        }
        r2 = self.update_session().post(url=self.url + self.ConsigneePrintAddress_path, data=data2)
        d2 = json.loads(r2.text)
        l2 = d2['data']['list']
        print(l2)
        consignee_content = random.choice(l2)  # 随机选择一个

        content_data_value = {
            'sender_content': sender_content,
            'consignee_content':consignee_content
        }
        # with open(self.yamlpath, 'w', encoding='utf-8') as f:
        #     yaml.dump(content_data_value, f, Dumper=yaml.Dumper)


    def read_content(self):
        self.get_custom_data()
        path = os.path.join(self.yamlpath)
        r = open(path)
        a = r.read()
        self.data = yaml.safe_load(a)
        return self.data



    def add_CustomPrint(self):
        self.sender_content = self.read_content()['sender_content']
        self.consignee_content = self.read_content()['consignee_content']
        self.Address = self.consignee_content['consigneeProvince']+self.consignee_content['consigneeProvince']+self.consignee_content['consigneeArea']+self.consignee_content['consigneeAddress']
        self.people_content =  self.consignee_content['consigneeName']+'，'+self.consignee_content['consigneePhone']+self.consignee_content['consigneeMobile']
        self.consigneeAddressText = self.people_content+'，'+self.Address
        # print(dict)
        self.trades = [{"info": {"itemInfo": "","orderInfo": {"postFee": 0, "buyerMessage": "", "sellerMemo": ""}},
                  "shippingName": self.sender_content['shippingName'],
                    "shippingWW": self.sender_content['shippingWW'],
                        "shippingZip":self.sender_content['shippingZip'],
                        "shippingShopName": self.sender_content['shippingShopName'],
                  "shippingMobile": self.sender_content['shippingMobile'],
                        "shippingPhone": self.sender_content['shippingPhone'],
                        "shippingProvince": self.sender_content['shippingProvince'],
                  "shippingCity": self.sender_content['shippingCity'],
                        "shippingArea": self.sender_content['shippingArea'],
                        "shippingAddress": self.sender_content['shippingAddress'],
                        "shippingTown": self.sender_content['shippingTown'],
                  "consigneeName": self.consignee_content['consigneeName'],
                        "consigneeWW": self.consignee_content['consigneeWW'],
                        "consigneeMobile": self.consignee_content['consigneeMobile'],
                        "consigneePhone": self.consignee_content['consigneePhone'],
                  "consigneeZip": self.consignee_content['consigneeZip'],
                        "consigneeProvince": self.consignee_content['consigneeProvince'],
                        "consigneeCity": self.consignee_content['consigneeCity'],
                        "consigneeArea": self.consignee_content['consigneeArea'],
                  "consigneeAddress":self.consigneeAddressText,
                    "isWait": True,
                    "orderInfoEdit": True,
                    "source": "",
                    "tradeId": "",
                    "tid": ""
                  }]
        # print(self.trades)
        data = {
            "trades": json.dumps(self.trades),
            "token": self.token
        }
        # print(data)
        r = self.update_session().post(url= self.url+self.saveSellerCustomPrint_path,data=data)
        # print(r.text)
        d = json.loads(r.text)
        datas = d['data']
        times = d['nowTime']
        # print(''.join(datas))
        return datas,times

    def get_cainiao_waybill(self):
        self.consignee_content = self.read_content()['consignee_content']
        self.Address = self.consignee_content['consigneeProvince']+self.consignee_content['consigneeProvince']+self.consignee_content['consigneeArea']+self.consignee_content['consigneeAddress']

        add_count = self.add_CustomPrint()
        datas = add_count[0]
        # print(type(datas))
        times = add_count[1]
        data1 = str(''.join(datas))
        nowTime = int(time.time())
        NowTime = "FHDP" + str(nowTime) + 'dn0'
        O_id = str(random.randint(1000000000, 9999999999))

        get_cainiao_waybill_data = {
            "isShare": True,
            "need_encrypt":True,
            "cp_code":"CN7000001003751",
            "branch_name":"临安三墩点部",
            "branch_code":"571HE",
            "segment_code":"NORMAL",
            "use_share_quantity":True,
            "before_get_opt_quantity":True,
            "sender":
                {"address":{"city":"杭州市","detail":"文三路252号伟星大厦9D","district":"西湖区","province":"浙江省","town":None},"name":"bbb","mobile":"15727785927","phone":"0371451551"},
            "trade_order_info_dtos":[{"object_id": O_id, "logistics_services": {"SVC-INSURE": {"value": 111}, "SVC-COD": {"value": 0},"SVC-RECEIVER-PAY": {"value": 100}},
              "order_info": {"order_channels_type":"OTHERS","trade_order_list":datas,"real_trade_order_list":datas,"real_trade_order_map":{data1:{"createTime":times}}},
              "package_info": {"items": [{"count": 1, "item_name": "FHDDUMMY", "name": "FHDDUMMY"}],"total_packages_count": 1, "id": NowTime}, "recipient": {"address": {"province": self.consignee_content['consigneeProvince'],"city": self.consignee_content['consigneeCity'],"district": self.consignee_content['consigneeArea'],"town":'',"detail": self.Address},
            "name": self.consignee_content['consigneeName'],"mobile":self.consignee_content['consigneeMobile'],"phone": self.consignee_content['consigneePhone']}, "user_id": 1845709742,
              "template_url":"http://cloudprint.cainiao.com/template/standard/181603/11"}]}


        data = {
            "requestObj":json.dumps(get_cainiao_waybill_data),
            'token':self.token
        }
        # print(data)
        rs = self.update_session().post(url='https://qnjy.xyy001.com/cainiao/waybillGet.do', data=data, )
        d = json.loads(rs.text)
        return d,datas,times,data1,self.Address

    def update_seller_custom_print_trade_print_info(self):
        self.sender_content = self.read_content()['sender_content']
        self.consignee_content = self.read_content()['consignee_content']


        a = self.get_cainiao_waybill()
        address = a[4]
        d = a[0]['data'][0]
        id = a[1]
        times = a[2]
        id_str = a[3]
        cpCode = d['cpCode']
        extraInfo = d['extraInfo']
        objectId = d['objectId']
        parentWaybillCode = d['parentWaybillCode']
        printData = d['printData']
        realCpCode = d['realCpCode']
        waybillCode = d['waybillCode']
        printInfo = {"tradeId":id_str, "isWait":True,"month":"202206","printType":1,"expressType":2,"companieCode":"CN7000001003751","companieName":"跨越速运","outSid":waybillCode,
                     "template":{"templateId":2274162,"templateName":"跨越速运","templateType":4},
                     "printInfo":{"tid":id_str,
                                  "expressType":2,
                                  "companieCode":"CN7000001003751",
                                  "companieName":"跨越速运",
                                  "cp_code":"CN7000001003751",
                                  "outSid":waybillCode,
                                  "branch_name":"临安三墩点部",
                                  "branch_code":"571HE",
                                  "segment_code":"NORMAL",
                                  "can_not_arrive":"",
                                  "apply_info":{"cpCode":cpCode,"extraInfo":extraInfo,"objectId":objectId,"parentWaybillCode":parentWaybillCode,"realCpCode":cpCode,"waybillCode":waybillCode,"waybill_code":waybillCode,"parent_waybill_code":realCpCode,"print_data":printData,
                                                "target_waybill_code":waybillCode,
                                                "cp_code":"CN7000001003751",
                                                "branch_name":"临安三墩点部",
                                                "branch_code":"571HE",
                                                "segment_code":"NORMAL",
                                                "brand_code":"default",
                                                "isShare":True,
                                                "trade_user_id":1845709742,
                                                "sender":{"address":{"city":"杭州市","detail":"文三路252号伟星大厦9D","district":"西湖区","province":"浙江省","town":''},"name":"aaaAVVV","mobile":"18538049779","phone":""},
                                                "recipient":{"address":{"province":self.consignee_content['consigneeProvince'],"city":self.consignee_content['consigneeCity'],"district":self.consignee_content['consigneeArea'],"detail":address},"name":self.consignee_content['consigneeName'],"mobile":self.consignee_content['consigneeMobile'],"phone": self.consignee_content['consigneePhone']},
                                                "logistics_services":{"SVC-INSURE":{"value":111},"SVC-COD":{"value":0},"SVC-RECEIVER-PAY":{"value":100}},
                                                "package_info":{"items":[{"count":1,"item_name":"FHDDUMMY","name":"FHDDUMMY"}],"total_packages_count":1},
                                                "order_info":{"order_channels_type":"OTHERS","trade_order_list":id,"real_trade_order_list":id,"real_trade_order_map":{id_str:{"createTime":times}}},
                                                "real_trade_order_list":id,
                                                "real_trade_order_map":{id_str:{"createTime":times}},
                                                "shipping_address":{"city":"杭州市","detail":"文三路252号伟星大厦9D","district":"西湖区","province":"浙江省","town":''}}}}





        data = {
            'printInfo':json.dumps(printInfo),
            'token':self.token
        }
        # print(data)
        r= self.update_session().post(self.url+self.updateSellerCustomPrintTradePrintInfo,data)
        print(r.status_code)

        waybillLogs = [{
            'wlbCode': waybillCode,
            'type': 1,
            'optType': 2,
            'wlbCodeInfo': printInfo['printInfo']['apply_info'],
            'useType': 2}]
        print(waybillLogs)
        data1 = {
            'waybillLogs' :json.dumps(waybillLogs),
            'token': self.token
        }
        r1= self.update_session().post(self.url+self.saveWaybillLogs, data1)
        print(r1.text,r1.status_code)

        tradePrints = [{'tid':id_str,'time':None}]
        data2 = {
            'tradePrints':json.dumps(tradePrints),
            'token':self.token
        }
        r2 = self.update_session().post(self.url+self.getSellerTradePrintsSimpleInfo,data2)
        print('+++++++++++++r2++++++++++++++',r2.text,r2.status_code)



        data3 = {
            'printInfos': json.dumps(printInfo),
            'operator': '你卖我买oye',
            'token':self.token

        }
        print(data3)
        r3 = self.update_session().post(self.url+self.updateSellerCustomPrintTradePrint,data3)
        print('+++++++++++++r3+++++++++++++++',r3.text)

if __name__ == '__main__':
    a = Custom_Print()
    a.get_custom_data()