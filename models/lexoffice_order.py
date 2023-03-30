from odoo import api, fields, models
import requests


class LexofficeOrder(models.Model):
    _name = 'lexoffice.order'
    _description = 'Lexoffice Order'

    name = fields.Char('Order Number')
    order_date = fields.Date('Order Date')
    partner_id = fields.Many2one('res.partner', 'Customer')
    order_line_ids = fields.One2many('lexoffice.order.line', 'order_id', 'Order Lines')

    @api.model
    def sync_lexoffice_orders(self, api_key):
        base_url = 'https://api.lexoffice.io/v1/'
        headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
        url = f'{base_url}voucherlist'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            orders = response.json()['content']
            for order in orders:
                if order['voucherType'] == 'salesinvoice':
                    self._create_update_order(order)
        else:
            raise ValueError(f'Error fetching orders from Lexoffice API: {response.text}')

    def _create_update_order(self, order_data):
        name = order_data['voucherNumber']
        order_date = order_data['voucherDate']
        partner_name = order_data['contact']['company']['name']
        partner = self.env['res.partner'].search([('name', '=', partner_name)], limit=1)

        if not partner:
            raise ValueError(f'Customer not found: {partner_name}')

        order_lines = []
        for line in order_data['voucherItems']:
            product_name = line['name']
            product = self.env['product.product'].search([('name', '=', product_name)], limit=1)

            if not product:
                raise ValueError(f'Product not found: {product_name}')

            order_line = {
                'product_id': product.id,
                'quantity': line['quantity'],
                'price_unit': line['unitPrice']['amount'],
            }
            order_lines.append((0, 0, order_line))

        vals = {
            'name': name,
            'order_date': order_date,
            'partner_id': partner.id,
            'order_line_ids': order_lines,
        }

        existing_order = self.search([('name', '=', name)], limit=1)
        if existing_order:
            existing_order.write(vals)
        else:
            self.create(vals)


class LexofficeOrderLine(models.Model):
    _name = 'lexoffice.order.line'
    _description = 'Lexoffice Order Line'

    order_id = fields.Many2one('lexoffice.order', 'Order')
    product_id = fields.Many2one('product.product', 'Product')
    quantity = fields.Float('Quantity')
    price_unit = fields.Float('Unit Price')
