# -*- coding: utf-8 -*-
import logging
import threading
import datetime

from odoo import api, models, tools, registry, exceptions
from .bn_2dfire import *

_logger = logging.getLogger(__name__)


class bn_2dfire_shops(models.Model):
    _name = 'bn.2dfire.shops'
    _description = 'bn.2dfire.shops'

    name = fields.Char(string=u'门店名称')
    code = fields.Char(string=u'门店编号')
    address = fields.Char(string=u'地址')
    entityId = fields.Char(string=u'门店entityId')
    memo = fields.Char(string=u'备注')
    isAdd = fields.Boolean(string=u'是否已经加入')

    import_register_branches_state = fields.Selection([('not_done', "Not done"),
                                                       ('just_done', "Just done"),
                                                       ('done', "Done"),
                                                       ('closed', "Closed")],
                                                      string="State of the Import onboarding panel",
                                                      default='not_done')

    binding_register_branches_state = fields.Selection([('not_done', "Not done"),
                                                        ('just_done', "Just done"),
                                                        ('done', "Done"),
                                                        ('closed', "Closed")],
                                                       string="State of the binding onboarding panel",
                                                       default='not_done')

    def get_2dfire_shop_from_api(self):
        print('get_2dfire_shop_from_api')
        _logger.info('get_2dfire_product_from_api')
        MY_URL = self.env['bn.2dfire.url'].search([('code', '=', 'shoplistv20')])
        MY_APPID = self.env['bn.2dfire.appid'].search([('code', '=', 'hq-it')])

        ewh_request = bn_2dfire_connect_Request()
        MY_DATA = {
            "method": str(MY_URL['bn_2dfire_function_method']),
            "appKey": MY_APPID['bn_2dfire_app_key'],
            "v": "1.0",
            "timestamp": str(int(time.time() * 1000)),
            "lang": '',
        }

        recordset = ewh_request.get_json(MY_URL['bn_2dfire_function_api'], MY_APPID, MY_DATA)
        if recordset is not None:
            if 'data' in recordset:
                _logger.info(recordset)
                self.insert_2dfire_shops(recordset['data']['data'])

        return True

    def insert_2dfire_shops(self, recordsets):
        if (len(recordsets) == 0):
            return
        for rec in recordsets:
            print(rec)
            shop = rec['shop']
            vals = []
            vals = {
                'entityId': shop['entityId'],
                'code': shop['code'],
                'name': shop['name'],
                'memo': shop['memo'],
            }

            if 'address' in shop:
                vals['address'] = rec['shop']['address']

            c01 = self.env['bn.2dfire.shops'].search([('entityId', '=', rec['shop']['entityId'])])
            if not c01:
                self.env['bn.2dfire.shops'].create(vals)
            else:
                print(rec['shop']['entityId'], rec['shop']['name'], "Already Done")

        return True

    @api.multi
    def btn_authorized_url(self):
        action = {
            "type": "ir.actions.act_url",
            "url": "https://open.2dfire.com/page/auth.html#/login?appId=35468986",
            "target": "new",
            # "target": "self",
        }
        return action




    @api.multi
    def get_authorize_binding_shops(self, storeids):

        bindinglist = []
        shoplist = self.env['bn.2dfire.shops'].search([('id', 'in', storeids)])
        for shop in shoplist:
            branch = self.env['bn.2dfire.branchs'].search([('code', '=', shop['entityId'])])
            val = {'shop_id': shop.id, 'branch_id': branch.id}
            bindinglist.append(val)

        return bindinglist

    @api.multi
    def btn_insert_branches(self):
        b01 = self.env['bn.2dfire.branchs'].search_bycode(self.entityId)
        if not b01:
            appids = self.env['bn.2dfire.appid'].search([('code', '=', 'hq-it')]).id
            companyids = self.env.user.company_id.id

            branch_ids = self.env['bn.2dfire.branchs'].create(
                {'code': self.entityId, 'name': self.name, 'appids': appids, 'company_id': companyids})

            action = {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                "views": [[False, "form"]],
                'res_model': 'bn.2dfire.branchs',
                'res_id': branch_ids.id,
                'target': 'new',
            }

            self.write({'isAdd': True})
            return action
        else:
            raise exceptions.RedirectWarning("该门店已经加入同步列表")

    @api.model
    def action_close_onboarding(self):
        """ Mark the onboarding panel as closed. """
        self.onboarding_state = 'closed'

    # @api.multi
    @api.model
    def action_binding_branches(self):
        action = self.env.ref('bn_2dfire.bn_2dfire_binding_shops_wizard_action').read()[0]
        return action

    @api.model
    def action_sync_data(self):
        action = self.env.ref('bn_2dfire.action_proc_sync_2dfire').read()[0]
        return action



    @api.model
    def action_2dfire_register_url(self):
        action = {
            "type": "ir.actions.act_url",
            "url": "https://open.2dfire.com/page/auth.html#/login?appId=35468986",
            "target": "new",
            # "target": "self",
        }
        return action


    @api.model
    def action_binding_branches_directly(self):
        action = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'src_model': 'bn.2dfire.shops',
            'res_model': 'bn.2dfire.binding.wizard',
            # 'res_id': self.id,
            'key2': 'client_action_multi',
            'target': 'new',
            'context': self.env.context,
            # 'flags': {'initial_mode': 'edit'},
        }
        return action

    def get_and_update_2dfire_onboarding_state(self):
        steps = [
            'import_register_branches_state',
            'binding_register_branches_state',
        ]
        rst = self.get_and_update_onbarding_state('import_register_branches_state', steps)
        # self.get_and_update_onbarding_state()
        print(rst)
        return rst

    def get_and_update_onbarding_state(self, onboarding_state, steps_states):
        """ Needed to display onboarding animations only one time. """
        old_values = {}
        all_done = True
        for step_state in steps_states:
            old_values[step_state] = self[step_state]
            if self[step_state] == 'just_done':
                self[step_state] = 'done'
            all_done = all_done and self[step_state] == 'done'
        #
        #     if self[onboarding_state] == 'not_done':
        #         # string `onboarding_state` instead of variable name is not an error
        #         old_values['onboarding_state'] = 'just_done'
        #     else:
        #         old_values['onboarding_state'] = 'done'
        #     self[onboarding_state] = 'done'
        # # print("get_and_update_onbarding_state ===> "+old_values)

        if all_done:
            if self[onboarding_state] == 'not_done':
                # string `onboarding_state` instead of variable name is not an error
                old_values['onboarding_state'] = 'just_done'
            else:
                old_values['onboarding_state'] = 'done'
            self[onboarding_state] = 'done'
            print("get_and_update_onbarding_state ===> " + old_values)
        return old_values
