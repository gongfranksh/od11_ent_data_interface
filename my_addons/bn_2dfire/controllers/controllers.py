# -*- coding: utf-8 -*-
from odoo import http

class Bn2dfire(http.Controller):
    @http.route('/bn_2dfire/bn_2dfire_onboarding_panel/',  auth='user', type='json')
    def bn_2dfire_config_obboarding(self, **kw):
        company = http.request.env.user.company_id
        shops = http.request.env['bn.2dfire.shops'].search([])[0]

        result = {
            'html': http.request.env.ref('bn_2dfire.bn_2dfire_config_onboarding_panel').render({
                'company': company,
                'state': shops.get_and_update_2dfire_onboarding_state()
            })

        }
        print(result)
        return result
