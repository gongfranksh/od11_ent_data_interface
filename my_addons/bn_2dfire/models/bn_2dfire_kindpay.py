# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# http://www.pospal.cn/openplatform/productapi.html
import json
import logging
import time
import datetime
import requests
import sys
from odoo import api, fields, models
# import hashlib
import types
from .bn_2dfire_common import *
from .bn_2dfire_tools import *
_logger = logging.getLogger(__name__)

class bn_2dfire_kindpay(models.Model):
    _name = 'bn.2dfire.kindpay'
    _description = 'bn.2dfire.kindpay'
    code = fields.Char(string=u'付款方式唯一标识')
    name = fields.Char(string=u'付款方式')
    sortname = fields.Char(string=u'付款归类')
    entityId = fields.Char(string=u'店entity号码')
    store_code = fields.Char(string=u'门店代号')
    store_name = fields.Char(string=u'门店名称')
    company_id = fields.Many2one('res.company', string='对应公司')

    @api.model
    def search_bycode(self, code):
        res = self.search([('code', '=', code)])
        return res




def get_2dfire_payment_from_api(self):
    print('get_2dfire_payment_from_api')
    _logger.info('get_2dfire_payment_from_api')
    MY_URL = self.env['bn.2dfire.url'].search([('code', '=', 'paymentlistv20')])
    stores = self.env['bn.2dfire.branchs'].get_vaild_branchs()
    for store in stores:
        appid = store['appids']
        para = {
            'para_my_url': MY_URL,
            'para_my_appid': appid,
            'para_my_store': store,
            'para_connection': self,
        }
        recordset = bn_2dfire_connect_api(para).Get_ResultAll_Payment()
        if recordset is not None:
            if 'data' in recordset:
                _logger.info(recordset)
                insert_2dfire_kindpay(self, recordset['data']['data'])
    return True

def insert_2dfire_kindpay(self, recordsets):
    if (len(recordsets) == 0):
        return
    for rec in recordsets:
        vals = {
            'code':  rec['id'],
            'name': rec['name'],
            'sortname': rec['kind'],
            'entityId': rec['entityId'],
            'store_code': rec['entityId'],
            'company_id': self.env['res.company'].search_bycode(rec['entityId']).id}

        c01 = self.env['bn.2dfire.kindpay'].search([('code', '=', rec['id'])])
        if not c01:
            _logger.info(rec['id']+rec['name']+"Need Insert")
            self.env['bn.2dfire.kindpay'].create(vals)
        # else:
        #     c01.write(vals)

    return

def insert_2dfire_kindpay_from_payvo(self, procdate):
    print('get_2dfire_kindpay_from_payvo')
    currdate = procdate.strftime("%Y-%m-%d").replace('-', '')
    ordervos = self.env['bn.2dfire.order.ordervo'].search([('innerCode', 'like', currdate + '____')])
    # range_vo=[]
    # for vo in ordervos:
    #     # range_vo.append(str(vo['orderId']))
    #     range_vo.append(ordervos.id)

    payvodetails = self.env['bn.2dfire.order.payvo'].search([('orderids', 'in', ordervos.ids)])
    for ord in payvodetails:
        print(ord)
        vals = {
            'code': ord.kindPayId,
            'name': ord.kindPayName,
            'sortname': ord.kindPaySortName,
            'entityId': ord.entityId,
            'store_code': ord.entityId,
            'company_id': self.env['res.company'].search_bycode(ord.entityId).id
        }
        c01 = self.env['bn.2dfire.kindpay'].search([('code', '=', ord.kindPayId)])
        if not c01:
            self.env['bn.2dfire.kindpay'].create(vals)
        else:
            c01.write(vals)

    print(procdate)
    return True
