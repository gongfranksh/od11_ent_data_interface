# -*- coding: utf-8 -*-
from odoo import api, fields, models


class pos_order(models.Model):
    _inherit = 'pos.order'
    buid = fields.Many2one('bnc.business', u'事业部')
    lngcasherid = fields.Many2one('hr.employee', u'收银员')
    strstoreid = fields.Char(string=u'storeid', size=20)
    bn_2dire_orderid = fields.Char(string=u'二维火交易号')
    bn_2dfire_payVo = fields.One2many('pos.order.2dire.payvo', 'pos_order_id', string=u'实际支付清单')
    # contraontid
    # account_date
    # bill_date


class pos_order_line(models.Model):
    _inherit = 'pos.order.line'
    lngsaleid = fields.Many2one('hr.employee', u'导购')


class pos_order_2dire_payvo(models.Model):
    _name = 'pos.order.2dire.payvo'
    _description = 'pos.order.2dire.payvo'
    pos_order_id = fields.Many2one('pos.order', string=u'POS实际收款清单', ondelete='cascade')
    kindpay_id = fields.Many2one('bn.2dfire.kindpay', string=u'收款kingdpayID')
    kind_payment = fields.Float(string=u'金额', digits=0)
    kind_operator = fields.Char(string=u'操作人')
    payTime = fields.Datetime(string=u'收款时间')
    entityId = fields.Char(string=u'店entity号码')
    company_id = fields.Many2one('res.company', string='公司')
