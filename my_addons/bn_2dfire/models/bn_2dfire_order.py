# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# http://www.pospal.cn/openplatform/productapi.html
import json
import time
import datetime
import requests
import sys
# from source.odoo

from odoo import api, fields, models
import _hashlib
import types


from .bn_2dfire_common import *
from .bn_2dfire_tools import *
from .bn_2dfire_constant import *




class bn_2dfire_order(models.Model):
    _name = 'bn.2dfire.order'
    _description = '2dfire order'
    ordersn = fields.Char(string=u'订单编号')
    orderVo = fields.One2many('bn.2dfire.order.ordervo', 'orderids', string=u'订单流水号')
    orderlist = fields.One2many('bn.2dfire.order.orderlist', 'orderids', string=u'商品清单')
    totalPayVo = fields.One2many('bn.2dfire.order.totalpayvo', 'orderids', string=u'实际支付')
    payVo = fields.One2many('bn.2dfire.order.payvo', 'orderids', string=u'支付金额清单')
    serviceBillVo = fields.One2many('bn.2dfire.order.servicebillvo', 'orderids', string=u'账单')
    kindpayvo = fields.One2many('bn.2dfire.order.kindpayvolist', 'orderids', string=u'kindpayvo支付方式清单')
    entityId = fields.Char(string=u'店entity号码')
    store_code = fields.Char(string=u'门店代号')
    store_name = fields.Char(string=u'门店名称')


class bn_2dfire_order_ordervo(models.Model):
    _name = 'bn.2dfire.order.ordervo'
    _description = '2dfire order ordervo'
    orderids = fields.Many2one('bn.2dfire.order', u'订单', ondelete='cascade')
    openTime = fields.Datetime(string=u'开单时间')
    seatName = fields.Char(string=u'座位名称')
    seatCode = fields.Char(string=u'座位CODE')
    peopleCount = fields.Char(string=u'就餐人数')
    orderId = fields.Char(string=u'订单Id')
    innerCode = fields.Char(string=u'账单号')
    code = fields.Char(string=u'单号 ')
    simpleCode = fields.Char(string=u'全局单号')
    orderType = fields.Char(string=u'订单类型')
    endTime = fields.Datetime(string=u'结单时间')

    orderFrom = fields.Char(string=u'单据来源    ')
    memo = fields.Char(string=u'备注')
    entityId = fields.Char(string=u'店entity号码')
    store_code = fields.Char(string=u'门店代号')
    store_name = fields.Char(string=u'门店名称')


class bn_2dfire_order_TotalPayVo(models.Model):
    _name = 'bn.2dfire.order.totalpayvo'
    _description = 'bn.2dfire.order.totalpayvo'
    orderids = fields.Many2one('bn.2dfire.order', u'订单', ondelete='cascade')
    currDate = fields.Datetime(string=u'发生日期')
    sourceAmount = fields.Float(string=u'原始费用')
    discountAmount = fields.Float(string=u'折后费用')
    resultAmount = fields.Float(string=u'应付总额')
    receiveAmount = fields.Float(string=u'实收总额')
    outFee = fields.Float(string=u'外送费')
    operateDate = fields.Datetime(string=u'结账时间 ')
    simpleCode = fields.Char(string=u'开发票额')
    invoice = fields.Float(string=u'结单时间')
    couponDiscount = fields.Float(string=u'券优惠金额   ')
    entityId = fields.Char(string=u'店entity号码')
    store_code = fields.Char(string=u'门店代号')
    store_name = fields.Char(string=u'门店名称')


class bn_2dfire_order_PayVo(models.Model):
    _name = 'bn.2dfire.order.payvo'
    _description = 'bn.2dfire.order.payvo'

    orderids = fields.Many2one('bn.2dfire.order', u'订单', ondelete='cascade')
    kindPayId = fields.Char(string=u'付款带吗 ')
    kindPayName = fields.Char(string=u'付款方式')
    kindPaySortName = fields.Char(string=u'支付类型')
    fee = fields.Float(string=u'实收额')
    type = fields.Char(string=u'类型方式')
    operatorCode = fields.Char(string=u'收银员编码')
    operator = fields.Char(string=u'收银员')
    payTime = fields.Datetime(string=u'收银时间')
    pay = fields.Float(string=u'现收金额')
    charge = fields.Float(string=u'找零')
    entityId = fields.Char(string=u'店entity号码')
    store_code = fields.Char(string=u'门店代号')
    store_name = fields.Char(string=u'门店名称')


class bn_2dfire_order_kindPayVoList(models.Model):
    _name = 'bn.2dfire.order.kindpayvolist'
    _description = 'bn.2dfire.order.kindpayvolist'
    orderids = fields.Many2one('bn.2dfire.order', u'订单', ondelete='cascade')
    name = fields.Char(string=u'Name')
    kind = fields.Char(string=u'kind')
    kindPaySortNm = fields.Char(string=u'kindPaySortNm')
    code = fields.Char(string=u'code')
    kindid = fields.Char(string=u'kindid')
    entityId = fields.Char(string=u'店entity号码')
    store_code = fields.Char(string=u'门店代号')
    store_name = fields.Char(string=u'门店名称')


class bn_2dfire_order_ServiceBillVo(models.Model):
    _name = 'bn.2dfire.order.servicebillvo'
    _description = 'bn.2dfire.order.servicebillvo'
    orderids = fields.Many2one('bn.2dfire.order', u'订单', ondelete='cascade')
    originAmount = fields.Float(string=u'原始消费金额    ')
    discountAmount = fields.Float(string=u'折后费用')
    originServiceCharge = fields.Float(string=u'原始服务费金额')
    originLeastAmount = fields.Float(string=u'原始最低消费')
    agioAmount = fields.Float(string=u'折后消费金额')
    agioServiceCharge = fields.Float(string=u'折后服务费')
    agioLeastAmount = fields.Float(string=u'折后最低消费')
    originReceivablesAmount = fields.Float(string=u'原始应收金额')
    agioReceivablesAmount = fields.Float(string=u'折后应收金额')
    finalAmount = fields.Float(string=u'最终应收金额')
    originTotal = fields.Float(string=u'原始总金额')
    agioTotal = fields.Float(string=u'折后总金额')
    reserveAmount = fields.Float(string=u'预付金额')
    outFee = fields.Float(string=u'外送费')
    notIncludeAmount = fields.Float(string=u'不计营业额总额')
    entityId = fields.Char(string=u'店entity号码')
    store_code = fields.Char(string=u'门店代号')
    store_name = fields.Char(string=u'门店名称')


class bn_2dfire_order_OderList(models.Model):
    _name = 'bn.2dfire.order.orderlist'
    _description = 'bn.2dfire.order.orderlist'
    # 订单详情列表
    orderids = fields.Many2one('bn.2dfire.order', u'订单', ondelete='cascade')
    orderId = fields.Char(string=u'订单ID')
    kind = fields.Char(string=u'点菜类型')
    name = fields.Char(string=u'品名', size=1500)
    makeName = fields.Char(string=u'做法')
    accountNum = fields.Float(string=u'结账数量')
    price = fields.Float(string=u'单价')
    ratio = fields.Float(string=u'折扣率')
    fee = fields.Float(string=u'金额')
    ratioFee = fields.Float(string=u'折后金额')
    specDetailName = fields.Char(string=u'规格名')
    accountUnit = fields.Char(string=u'结账单位')
    isMemberPrice = fields.Float(string=u'是否使用会员价(1.00表示使用会员价，0.00表示不使用)')
    menuId = fields.Char(string=u'商品编码')
    num = fields.Char(string=u'num')
    kindMenuName = fields.Char(string=u'菜类名 ', size=1500)
    rootKindMenuName = fields.Char(string=u'根类名 ', size=1500)
    giveDish = fields.Boolean(string=u'是否赠')
    canceled = fields.Boolean(string=u'是否取消（true：取消 false：没有取消）')
    memo = fields.Char(string=u'备注（退/赠理由）', size=1500)
    opUserName = fields.Char(string=u'操作人姓名（退/赠操作人）')
    entityId = fields.Char(string=u'店entity号码')
    store_code = fields.Char(string=u'门店代号')
    store_name = fields.Char(string=u'门店名称')


def get_2dfire_order_from_api(self, procdate):
    print('get_2dfire_order_from_api')
    print(procdate)
    MY_URL = self.env['bn.2dfire.url'].search([('code', '=', 'orderlist')])
    # MY_URL = self.env['bn.2dfire.url'].search([('code', '=', 'orderlist-v20')])

    #        procdate= datetime.datetime.now() - datetime.timedelta(days=1)
    stores = self.env['bn.2dfire.branchs'].get_vaild_branchs()
    # stores = self.env['bn.2dfire.branchs'].search_bycode('00401742')
    for store in stores:
        appid = store['appids']
        para = {
            'para_my_url': MY_URL,
            'para_my_appid': appid,
            'para_my_store': store,
            'para_connection': self,
        }

        data = {
            "currdate": procdate,
            "orderids": None
        }

        recordset = bn_2dfire_connect_api(para).Get_ResultAll(data)
        if recordset is not None:
            if 'model' in recordset:
                insert_2dfire_order(self, recordset['model'], store)

    return True


def get_2dfire_order_detail_from_api(self, procdate):
    print('get_2dfire_order_detail_from_api')
    MY_URL = self.env['bn.2dfire.url'].search([('code', '=', 'orderdetail')])

    #        procdate= datetime.datetime.now() - datetime.timedelta(days=1)
    currdate = procdate.strftime("%Y-%m-%d").replace('-', '')
    print(procdate)
    stores = self.env['bn.2dfire.branchs'].get_vaild_branchs()
    for store in stores:
        #            print store['code']+'===>'+store['name']
        appid = store['appids']
        #            print appid
        para = {
            'para_my_url': MY_URL,
            'para_my_appid': appid,
            'para_my_store': store,
            'para_connection': self,
        }

        orderlist = self.env['bn.2dfire.order.ordervo'].search(
            [('innerCode', 'like', currdate + '____'), ('entityId', '=', store['code'])])
        ld_by_orderid = []
        for rec in orderlist:
            ld_by_orderid.append(str(rec['orderId']))

        local_reord_number = get_local_record_number_2dfire_order_detail(self, str(ld_by_orderid))

        split_orderlist = split_order_byMaxNum(ld_by_orderid)
        ords = []
        remote_records = []
        #           r001=[]
        for rec in split_orderlist:

            data = {
                "currdate": procdate,
                "orderids": str(rec)
            }

            recordset = bn_2dfire_connect_api(para).Get_ResultAll(data)

            if recordset is not None:
                if 'model' in recordset:

                    #                        r001.append(recordset['model'])
                    for rc in recordset['model']:
                        remote_records.append(rc)
        #                        print remote_records
        print(len(remote_records))
        if len(remote_records) != 0 and local_reord_number != len(remote_records):
        # if len(remote_records) != 0 and local_reord_number == 0:
            print('local_reord_number')
            print(local_reord_number)

            print('remote_records')
            print(len(remote_records))

            insert_2dfire_order_detail(self, remote_records)

    return True


def insert_2dfire_order(self, recordsets, certifate):
    if (len(recordsets) == 0):
        return

    vals_order_insert = []
    vals_order_insert = {
        'entityId': certifate['code'],
        'store_code': certifate['code'],
        'store_name': certifate['name'],
        'ordersn': None,
        'orderVo': None,
        'totalPayVo': None,
        'payVo': None,
        'serviceBillVo': None,
        'kindpayvo': None,
    }

    for rec in recordsets:

        vals_ordervo = []
        ov = rec['orderVo']
        r01 = self.env['bn.2dfire.order'].search([('ordersn', '=', ov['orderId'])])
        print(ov['innerCode'])

        if r01:
            continue

        print ( ov['entityId'],
                ov['innerCode'],
                bn_timestamp_to_date(ov['openTime']).strftime(BN_DATAFORMAT),
                bn_timestamp_to_date(ov['endTime']).strftime(BN_DATAFORMAT))

        ordevo_set = {
            'orderId': ov['orderId'],
            "innerCode": ov['innerCode'],
            "entityId": ov['entityId'],
            "openTime": bn_timestamp_to_date(ov['openTime']).strftime(BN_DATAFORMAT),
            "peopleCount": ov['peopleCount'],
            "code": ov['code'],
            # "simpleCode": ov['simpleCode'],
            "endTime": bn_timestamp_to_date(ov['endTime']).strftime(BN_DATAFORMAT),
            "orderFrom": ov['orderFrom'],
            "orderType": ov['orderType'],
            "memo": ov.get('memo', ''),
        }
        vals_ordervo.append((0, 0, ordevo_set))
        vals_order_insert.update({"ordersn": ov['orderId']})
        vals_order_insert.update({"orderVo": vals_ordervo})

        vals_totalPayVo = []
        if 'totalPayVo' in rec:
            totalPayVo = rec['totalPayVo']

            totalPayVo_set = {
                'currDate': bn_timestamp_to_date(totalPayVo['currDate']).strftime(BN_DATAFORMAT),
                "sourceAmount": totalPayVo['sourceAmount'],
                "discountAmount": totalPayVo['discountAmount'],
                "resultAmount": totalPayVo['resultAmount'],
                "receiveAmount": totalPayVo['receiveAmount'],
                "outFee": totalPayVo['outFee'],
                "operateDate": bn_timestamp_to_date(totalPayVo['operateDate']).strftime(BN_DATAFORMAT),
                "invoice": totalPayVo['invoice'],
                "couponDiscount": totalPayVo['couponDiscount'],
            }
            vals_totalPayVo.append((0, 0, totalPayVo_set))
            vals_order_insert.update({"totalPayVo": vals_totalPayVo})

        #插入支付清单
        vals_payVoList = []

        if 'payVoList'  in rec:
        # if not rec['payVoList']:
        #     print ('hello')

            for payVoList in rec['payVoList']:
                payVoList_set = {
                    'entityId': payVoList['entityId'],
                    "type": payVoList['type'],
                    "kindPayId": payVoList['kindPayId'],
                    "kindPayName": payVoList['kindPayName'],
                    "kindPaySortName": payVoList['kindPaySortName'],
                    "fee": payVoList['fee'],
                    "operator": payVoList['operator'],
                    "payTime": bn_timestamp_to_date(payVoList['payTime']).strftime(BN_DATAFORMAT),
                    "pay": payVoList['pay'],
                    "charge": payVoList['charge'],
                }
                vals_payVoList.append((0, 0, payVoList_set))
            vals_order_insert.update({"payVo": vals_payVoList})

        #插入收款方式清单
        vals_kindPayVoList = []
        if 'kindPayVoList'  in rec:

            for kindPayVoList in rec['kindPayVoList']:
                kindPayVoList_set = {
                    'name': kindPayVoList['name'],
                    "kind": kindPayVoList['kind'],
                    "kindid": kindPayVoList['id'],
                    "kindPaySortNm": kindPayVoList['kindPaySortNm'],
                }
                vals_kindPayVoList.append((0, 0, kindPayVoList_set))
            vals_order_insert.update({"kindpayvo": vals_kindPayVoList})

        #插入账单明细
        vals_serviceBillVo = []
        serviceBillVo = rec['serviceBillVo']
        serviceBillVo_set = {
            'agioAmount': serviceBillVo['agioAmount'],
            "agioLeastAmount": serviceBillVo['agioLeastAmount'],
            "agioReceivablesAmount": serviceBillVo['agioReceivablesAmount'],
            "agioServiceCharge": serviceBillVo['agioServiceCharge'],
            'agioTotal': serviceBillVo['agioTotal'],
            "discountAmount": serviceBillVo['discountAmount'],
            "entityId": serviceBillVo['entityId'],
            "finalAmount": serviceBillVo['finalAmount'],
            "notIncludeAmount": serviceBillVo['notIncludeAmount'],
            "originAmount": serviceBillVo['originAmount'],
            "originLeastAmount": serviceBillVo['originLeastAmount'],
            "originReceivablesAmount": serviceBillVo['originReceivablesAmount'],
            "originServiceCharge": serviceBillVo['originServiceCharge'],
            "originTotal": serviceBillVo['originTotal'],
            "outFee": serviceBillVo['outFee'],
            "reserveAmount": serviceBillVo['reserveAmount'],
        }
        vals_serviceBillVo.append((0, 0, serviceBillVo_set))
        vals_order_insert.update({"serviceBillVo": vals_serviceBillVo})

        print(vals_order_insert)
        self.env['bn.2dfire.order'].create(vals_order_insert)
    return True


def insert_2dfire_order_detail(self, recordsets):
    if (len(recordsets) == 0):
        return
    vals = []
    for rec in recordsets:
        r01 = self.env['bn.2dfire.order.orderlist'].search([('orderId', '=', rec['orderId'])])

        print(rec['orderId'])

        if r01:
            continue


        vals = {
            'entityId': rec['entityId'],
            'kind': rec['kind'],
            'fee': rec['fee'],
            'ratio': rec['ratio'],
            'accountNum': rec['accountNum'],
            'isMemberPrice': rec['isMemberPrice'],
            'menuId': rec['menuId'],
            'price': rec['price'],
            'giveDish': rec['giveDish'],
            'num': rec['num'],
            'canceled': rec['canceled'],
            'ratioFee': rec['ratioFee'],
            'accountUnit': rec['accountUnit'],
            'entityId': rec['entityId'],
            'rootKindMenuName': rec['rootKindMenuName'],
            'kindMenuName': rec['kindMenuName'],
            'name': rec['name'],
            'orderId': rec['orderId'],
            'orderids':self.env['bn.2dfire.order'].search([('ordersn','=',rec['orderId'])]).id
        }
        r01 = self.env['bn.2dfire.order.orderlist'].create(vals)

    return True


def get_local_record_number_2dfire_order_detail(self, orders):
    if len(orders) == 2:
        return 0
    else:
        orders = orders.replace('[', '(')
        orders = orders.replace(']', ')')
        sql = """ 
                        select count(*) 
                        FROM bn_2dfire_order_orderlist
                        WHERE "orderId" in {0}
                              """
        sql = sql.format(orders.replace('[', '('))
        cr = self._cr
        cr.execute(sql)
        res = cr.fetchall()
        if len(res) != 0:
            recno = res[0][0]
            return recno
        else:
            return 0
