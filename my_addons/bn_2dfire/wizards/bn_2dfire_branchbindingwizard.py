# -*- coding: utf-8 -*-
from odoo import api, models, tools, registry, exceptions, fields


class bn_2dfire_binding_wizard(models.TransientModel):
    _name = "bn.2dfire.binding.wizard"
    _description = "bn.2dfire.binding.wizard"

    def _default_shops_ids(self):
        shops_ids = self._context.get('active_model') == 'bn.2dfire.shops' \
                    and self._context.get('active_ids') \
                    or []
        ##如果没有带入选定值，就导入所有记录
        if shops_ids == []:
            shops_ids = self.env['bn.2dfire.shops'].search([])

        bindingshoplist = self.env['bn.2dfire.shops'].get_authorize_binding_shops(shops_ids.ids)

        return [
            (0, 0, {'shop_id': shop['shop_id'], 'branch_id': shop['branch_id']})
            for shop in bindingshoplist]

    shop_ids = fields.One2many('bn.2dfire.binding.shops.wizard', 'wizard_id', string='Register Shops',
                               default=_default_shops_ids)

    @api.multi
    def binding_button(self):
        self.ensure_one()
        for bindgsetting in self.shop_ids:
            print(bindgsetting)
            shop = self.env['bn.2dfire.shops'].search([('id', '=', bindgsetting['shop_id'].id)])
            branch = self.env['bn.2dfire.branchs'].search([('id', '=', bindgsetting['branch_id'].id)])
            if branch:
                branch.write({'code': shop['entityId']})

class bn_2dfire_binding_shops_wizard(models.TransientModel):
    _name = "bn.2dfire.binding.shops.wizard"
    _description = "bn.2dfire.binding.shops.wizard"
    wizard_id = fields.Many2one('bn.2dfire.binding.wizard', string='Wizard', required=True, ondelete='cascade')
    shop_id = fields.Many2one('bn.2dfire.shops', string='授权门店', required=True, ondelete='cascade')
    branch_id = fields.Many2one('bn.2dfire.branchs', string='绑定门店', ondelete='cascade')
