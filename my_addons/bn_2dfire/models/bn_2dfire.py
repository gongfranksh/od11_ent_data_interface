# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from .bn_2dfire_kindpay import *
from .bn_2dfire_order import   *
from .bn_2dfire_product import   *
from .bn_common import *
from .bn_2dfire_constant import *
import logging

_logger = logging.getLogger(__name__)

TOTAL_DAY=BN_INTERFACE_INTERVAL



def _get_business(self):
    res=self.env['bn.business'].get_bnc_business_bycode('2dfire')
    return res
    

def sync_category_to_bnc(self):
    res=self.env['bn.business'].get_bnc_business_bycode('2dfire')
    bnc_root_category(self,res)
    #
    # res=self.env['bnc.business'].get_bnc_business_bycode('cof')
    # bnc_root_category(self,res)
    return True

def sync_product_to_bnc(self):
#    bnc_root_category(self,self._get_business())
    bnc_insert_product(self)

    return True

def sync_sales_from_api(self,period):
    begin=period['begin']
    end=period['end']
    
    for i in range((end - begin).days+1):
        procday = begin + datetime.timedelta(days=i)
        get_2dfire_order_from_api(self,procday)
    return True

def sync_order_detail_from_api(self,period):
    begin=period['begin']
    end=period['end']
    
    for i in range((end - begin).days+1):
        procday = begin + datetime.timedelta(days=i)    
        get_2dfire_order_detail_from_api(self,procday)
    return True

def sync_kindpay_from_payvo(self, period):
    begin = period['begin']
    end = period['end']
    for i in range((end - begin).days + 1):
        procday = begin + datetime.timedelta(days=i)
        insert_2dfire_kindpay_from_payvo(self, procday)
    return True

def sync_product_from_orderlist(self,period):
    begin=period['begin']
    end=period['end']
    
    for i in range((end - begin).days+1):
        procday = begin + datetime.timedelta(days=i)
        get_2dfire_product_from_orderdetail(self,procday)
    return True


def sync_product_from_api(self):
    get_2dfire_product_from_api(self)
    return True


def sync_payment_from_api(self):
    get_2dfire_payment_from_api(self)
    return True


def sync_sales_to_bnc(self):
#    bnc_root_category(self,self._get_business())
#    bnc_insert_sales(self)
    return True


def bnc_setparent_category(self):
        return True
    
def bnc_insert_product(self):
#    buids=self.env['bnc.business'].search([('strBuscode','in',['btw'])])
    buids=self.env['bn.business'].search([('strBuscode','in',['2dfire'])])
    for buid in buids:
    
        productids=bnc_get_NeedUpdateProduct_byBussinessUnit(self,buid)
        i=0
        for pids in productids:
                i=i+1
                print (i,len(productids),pids['store_code'],pids['name'])
                res= {
                    'code' : pids['code'],
                    'name' : pids['name'],
    #                'spec':spec,
    #                'brand_id':b01,
                    'list_price':pids['Price'],
                    'price':pids['Price'],
    #                'bn_barcode':tmp_code,
                    'sale_ok':True,
                    'available_in_pos':True,
                    'default_code': pids['code'],
                    'categ_id':self.env['product.category'].search_bycode(pids['store_code']).id,
    #                'b_category':self.env['product.category'].search_bycode(store_code+'-'+classid[0:4]).id,
    #                'm_category':self.env['product.category'].search_bycode(store_code+'-'+classid[0:6]).id,
    #                'b_sup_id':s01.id,
    #                'timestamp': timestamp,
                    'buid':buid['id'],
                    'company_id':self.env['res.company'].search_bycode(pids['store_code']).id,
                    'store_id':self.env['res.company'].search_bycode(pids['store_code']).id,
                    }
                #检查是插入还是更新            
                r01=self.env['product.template'].search_bycode(pids['code'])
                if r01:            
                    r01.write(res)
    #                print 'update'
    #                print res            
                else:
                    self.env['product.template'].create(res)
    #                print 'create'
    #                print res
    #        self.set_jsport_category_parent()  

    
    return True
def bnc_insert_sales(self):  
        print ('bnc_insert_sales')
            #proc_days 往前处理几天
        proc_days=TOTAL_DAY
        buids=self.env['bn.business'].search([('strBuscode','in',['2dfire'])])
        for buid in buids:

            proc_date_task=check_pos_data_daily(self,proc_days,buid)
#            if db['store_code'] =='02002':
            for d in proc_date_task:
                    if (d['local_records_count'] != d['remote_records_count']) or (d['local_records_count']==0):
                       _logger.info("bn=>2dfire bn_insert_sales"+d['proc_date']+'====>'+'local have====>'+str(d['local_records_count'])+'     remote have====>'+str(d['remote_records_count'])+'==>need to sync')
                       print( d['proc_date']+'====>'+'local have====>'+str(d['local_records_count'])+'     remote have====>'+str(d['remote_records_count'])+'==>need to sync')

                       # 涉及结算就不能直接删除原来的pos.order记录了
                       # delete_pos_data_daily(self,d['proc_date'],buid)

                       insert_pos_data_daily(self,d['proc_date'],buid) 
                    else :
                       _logger.info("bn=>2dfire bn_insert_sales"+d['proc_date'] +'====>'+'already done!!!')
                       print (d['proc_date'] +'====>'+'already done!!!')
    
        return 
    
    
def delete_pos_data_daily(self,ymd,business):
            exec_sql=""" 
                        delete from pos_order 
                        where to_char(date_order,'yyyy-mm-dd')='{0}' and buid ={1}
                    """
            exec_sql=exec_sql.format(ymd,business.id)  
            cr = self._cr 
            cr.execute(exec_sql)

            return True
                
 
def insert_pos_data_daily(self,procdate,business):
    
        #获取事业部代码
        stores=bnc_get_storescode_byBussinessUnit(self,business)
        currdate=procdate.replace('-','')

        #获取待处理，该日的所有销售单
        order_vo_list = self.env['bn.2dfire.order.ordervo'].search([('innerCode', 'like',currdate+'____'),('entityId','in',stores)])
        i=0
        for  ov in order_vo_list:
            i=i+1

            print  (i,len(order_vo_list),ov.orderids,ov['entityId'],ov['endTime'])

            #获取订单号ID

            vals = []
            res = []
            tmp_payvo = []

            #获取数据所属公司ID
            br01 = self.env['res.company'].search_bycode(ov['entityId']).id

            #获取实际支付合计金额
            tmp_totalpayno=0.0
            ordertotalpayno=self.env['bn.2dfire.order.totalpayvo'].search([('orderids', 'in',ov.orderids.ids)])
            if ordertotalpayno:
                for opl in ordertotalpayno:
                    tmp_totalpayno+=opl.receiveAmount

            #获取应付支付合计金额
            tmp_total=0.0
            orderservicebillvo=self.env['bn.2dfire.order.servicebillvo'].search([('orderids', 'in',ov.orderids.ids)])
            if orderservicebillvo:
                for osbl in orderservicebillvo:
                    tmp_total+=osbl.finalAmount


            #获取实际支付明细
            orderpayno=self.env['bn.2dfire.order.payvo'].search([('orderids', 'in',ov.orderids.ids)])
            if orderpayno:
                for opdl in orderpayno:
                    print (opdl.kindPayId)
                    print (opdl.fee)
                    tmp_payvo.append((0, 0, {
                        'kindpay_id': self.env['bn.2dfire.kindpay'].search([('code', '=', opdl.kindPayId)]).id,
                        'kind_payment': opdl.fee,
                        'kind_operator': opdl.operator,
                        'payTime': opdl.payTime,
                        'entityId': opdl.entityId,
                        'company_id': br01,
                    }))


            m01=None
            saledate= bnc_char_to_date(ov['endTime'])

            #处理产生 posorderline的记录
            pos_order_line = self.env['bn.2dfire.order.orderlist'].search([('orderId','=',ov['orderId'])])
            for pl in pos_order_line:
                inter_pcode= pl['menuId']
                tmp_price=pl['price']
                tmp_qty=float(pl['num'])
                tmp_subtotal=pl['ratioFee']

                res.append((0,0,{
                    'product_id':self.env['product.product'].search([('default_code', '=',inter_pcode)]).id,
                    'price_unit':tmp_price,
                    'price_subtotal':tmp_subtotal,
                    'price_subtotal_incl':tmp_subtotal,
                    'qty':tmp_qty,
                    }))

            #准备产生pos.order
            vals={
                'date_order': ov['endTime'],
                # 'date_order': saledate,

                'company_id': br01,
                'pricelist_id': 1,
                'user_id':self.env['res.users'].search([('login', '=','auto-import-2dfire-users')]).id,
                'amount_tax':tmp_total * 0.16,
                'amount_total':tmp_total,
                'amount_paid':tmp_totalpayno,
                'amount_return':0.00,
                'bn_2dire_orderid':ov['orderId'],
                'note':ov['orderId'],
                'pos_reference':ov['entityId']+'-'+ov['innerCode']+'-'+ov['code'],
                # 'partner_id':m01,

                'lines':res,
                'bn_2dfire_payVo':tmp_payvo,
                'state':'done',
                'buid':business.id,
                'strstoreid':ov['entityId'], 
                }


            #检查是否已经导入按订单号
            checkorderid=self.env['pos.order'].search([('bn_2dire_orderid', '=',ov['orderId'])])
            if not checkorderid:
                master=self.env['pos.order'].create(vals)
        
        return True

      
def check_pos_data_daily(self,para_interval,business):
        vals=[]           
        end_date= datetime.datetime.now()        
        # for i in range(1,para_interval+1):
        for i in range(0,para_interval):
            servercnt=0
            localcnt=0
            day= end_date - datetime.timedelta(days=i)
            # day= end_date - datetime.timedelta(days=0)
            currdate=day.strftime('%Y-%m-%d').replace('-','')
            print( day)
            exec_sql=""" 
                        select count(*)  from pos_order 
                        where to_char(date_order,'yyyy-mm-dd')='{0}' and buid ={1} 
                    """
            exec_sql=exec_sql.format(day.strftime('%Y-%m-%d'),business.id)  
            cr = self._cr 
            cr.execute(exec_sql)
            
            for local_count  in cr.fetchall():
                localcnt=local_count[0]
            stores=bnc_get_storescode_byBussinessUnit(self,business)            
            orderlist=self.env['bn.2dfire.order.ordervo'].search([('innerCode', 'like',currdate+'____'),('entityId','in',stores)])
            remote_cnt = len(orderlist)
            vals.append({'proc_date':day.strftime('%Y-%m-%d'),'local_records_count':localcnt,'remote_records_count':remote_cnt})       

        return vals
    


