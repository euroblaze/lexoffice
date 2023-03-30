from odoo import api, fields, models
import requests


class LexofficeProduct(models.Model):
    _name = 'lexoffice.product'
    _description = 'Lexoffice Product'

    name = fields.Char('Name')
    description = fields.Text('Description')
    price = fields.Float('Price')
    tax_rate = fields.Float('Tax Rate')

    @api.model
    def sync_lexoffice_products(self, api_key):
        base_url = 'https://api.lexoffice.io/v1/'
        headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
        url = f'{base_url}materials'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            products = response.json()['content']
            for product in products:
                self._create_update_product(product)
        else:
            raise ValueError(f'Error fetching products from Lexoffice API: {response.text}')

    def _create_update_product(self, product_data):
        name = product_data['name']
        description = product_data['description']
        price = product_data['purchasePrice']['amount']
        tax_rate = product_data['purchasePrice']['taxRate']

        vals = {
            'name': name,
            'description': description,
            'price': price,
            'tax_rate': tax_rate,
        }

        existing_product = self.search([('name', '=', name)], limit=1)
        if existing_product:
            existing_product.write(vals)
        else:
            self.create(vals)
