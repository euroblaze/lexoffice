from odoo import api, fields, models
import requests


class LexofficeInvoice(models.Model):
    _name = 'lexoffice.invoice'
    _inherit = ['account.move']
    _description = 'Lexoffice Invoice'

    lexoffice_id = fields.Char('Lexoffice ID', readonly=True)

    @api.model
    def sync_lexoffice_invoices(self, api_key):
        base_url = 'https://api.lexoffice.io/v1/'
        headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
        url = f'{base_url}invoices'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            invoices = response.json()['content']
            for invoice in invoices:
                self._create_update_invoice(invoice)
        else:
            raise ValueError(f'Error fetching invoices from Lexoffice API: {response.text}')

    def _create_update_invoice(self, invoice_data):
        lexoffice_id = invoice_data['id']
        partner_name = invoice_data['contact']['company']['name']
        partner = self.env['res.partner'].search([('name', '=', partner_name)], limit=1)

        if not partner:
            raise ValueError(f'Customer not found: {partner_name}')

        invoice_lines = []
        for line in invoice_data['voucherItems']:
            product_name = line['name']
            product = self.env['product.product'].search([('name', '=', product_name)], limit=1)

            if not product:
                raise ValueError(f'Product not found: {product_name}')

            invoice_line = {
                'product_id': product.id,
                'quantity': line['quantity'],
                'price_unit': line['unitPrice']['amount'],
                'name': product_name,
                'account_id': self.env['account.account'].search([('user_type_id', '=', 'Income')], limit=1).id,
            }
            invoice_lines.append((0, 0, invoice_line))

        vals = {
            'lexoffice_id': lexoffice_id,
            'partner_id': partner.id,
            'invoice_line_ids': invoice_lines,
            'move_type': 'in_invoice',
        }

        existing_invoice = self.search([('lexoffice_id', '=', lexoffice_id)], limit=1)
        if existing_invoice:
            existing_invoice.write(vals)
        else:
            self.create(vals)
