# -*- coding: utf-8 -*-
import logging
import threading
import datetime

from odoo import api, models, tools, registry, exceptions
from ..models.bn_2dfire import *

# from odoo.addons.bn_pospal.models import  *


# from idlelib.SearchEngine import get

_logger = logging.getLogger(__name__)

# begin_day = 7
begin_day = TOTAL_DAY
end_day = 1


class proc_sync_2dfire(models.TransientModel):
    _name = 'proc.sync.2dfire'
    _description = 'proc.sync.2dfire'

    # 获取事业部代码
    @api.model
    def _get_business(self):
        res = self.env['bn.business'].get_bnc_business_bycode('2dfire')
        return res

    def sync_2dfire_interface_v20(self):
        MY_URL = self.env['bn.2dfire.url'].search([('code', '=', 'menulistv20')])
        stores = self.env['bn.2dfire.branchs'].get_vaild_branchs()
        tmp_data=[]
        for store in stores:
            appid = store['appids']
            para = {
                'para_my_url': MY_URL,
                'para_my_appid': appid,
                'para_my_store': store,
                'para_connection': self,
            }
            recordset = bn_2dfire_connect_api(para).Get_ResultAll_ProductMenu()
            if recordset is not None:
                if 'data' in recordset:
                    tmp_data.append(recordset['data']['data'])
        raise exceptions.RedirectWarning(json.dumps(tmp_data, sort_keys=True, indent=2,ensure_ascii=False))
        return True

    def sync_2dfire_product_v20(self):
        print('sync_2dfire_menu_v20')
        sync_product_from_api(self)
        bnc_insert_product(self)
        return True

    def sync_2dfire_payment_v20(self):
        print('sync_2dfire_payment_v20')
        sync_payment_from_api(self)
        return True

    def sync_2dfire_shop_v20(self):
        print('sync_2dfire_shop_v20')
        self.env['bn.2dfire.shops'].get_2dfire_shop_from_api()
        return True

    def sync_2dfire_sales(self):
        print('sync_2dfire_sales')

        # bg = '2019-01-17 00:00:00'
        # beg=datetime.datetime.strptime(bg, "%Y-%m-%d %H:%M:%S")
        #
        # ed = '2019-01-17 23:59:59'
        # end = datetime.datetime.strptime(bg, "%Y-%m-%d %H:%M:%S")
        # period ={
        #     'begin':beg,
        #     'end':end,
        #     }

        period = {
            'begin': datetime.datetime.now() - datetime.timedelta(days=begin_day),
            'end': datetime.datetime.now()
            # 'begin': datetime.datetime.now() - datetime.timedelta(days=2),
            # 'end': datetime.datetime.now() -  datetime.timedelta(days=2),
            # 'end': datetime.datetime.now() - datetime.timedelta(days=end_day),

        }

        sync_sales_from_api(self, period)
        sync_order_detail_from_api(self, period)
        return True

    def sync_2dfire_category(self):
        print('sync_2dfire_category')
        #        get_2dfire_catagory_from_api(self)
        return True

    def sync_2dfire_product(self):
        print('sync_2dfire_product')
        period = {
            'begin': datetime.datetime.now() - datetime.timedelta(days=begin_day),
            # 'end': datetime.datetime.now() - datetime.timedelta(days=end_day),
            'end': datetime.datetime.now(),
        }

        sync_product_from_orderlist(self, period)

        return True

    def sync_2dfire_kindpay(self):
        print('sync_2dfire_kindpay')
        period = {
            'begin': datetime.datetime.now() - datetime.timedelta(days=begin_day),
            # 'end': datetime.datetime.now() - datetime.timedelta(days=end_day),
            'end': datetime.datetime.now(),
        }

        sync_kindpay_from_payvo(self, period)
        return True

    def sync_2dfire(self):
        print('sync_2dfire_all')
        #      self.sync_2dfire_category()
        #      self.sync_2dfire_product()
        #      self.sync_2dfire_member()
        #      self.sync_2dfire_sales()
        return True

    def interface_2dfire_to_bnc_category(self):
        print('interface_2dfire_to_bnc_category')
        sync_category_to_bnc(self)
        return True

    def interface_2dfire_to_bnc_product(self):
        print('interface_2dfire_to_bnc_product')
        sync_product_to_bnc(self)
        return True

    def interface_2dfire_to_bnc_sales(self):
        print('interface_2dfire_to_bnc_sales')
        bnc_insert_sales(self)
        return True

    def proc_sync_2dfire_all(self):
        self.env['proc.sync.2dfire'].sync_2dfire_shop_v20()
        self.env['proc.sync.2dfire'].sync_2dfire_product_v20()
        self.env['proc.sync.2dfire'].sync_2dfire_payment_v20()
        self.env['proc.sync.2dfire'].sync_2dfire_sales()
        self.env['proc.sync.2dfire'].sync_2dfire_product()
        self.env['proc.sync.2dfire'].sync_2dfire_kindpay()
        self.env['proc.sync.2dfire'].interface_2dfire_to_bnc_category()
        self.env['proc.sync.2dfire'].interface_2dfire_to_bnc_product()
        self.env['proc.sync.2dfire'].interface_2dfire_to_bnc_sales()


        return True
