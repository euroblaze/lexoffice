from odoo import api, fields, models
import requests


class LexofficeContact(models.Model):
    _name = 'lexoffice.contact'
    _description = 'Lexoffice Contact'

    name = fields.Char('Name')
    street = fields.Char('Street')
    zip = fields.Char('ZIP')
    city = fields.Char('City')
    country_id = fields.Many2one('res.country', 'Country')
    phone = fields.Char('Phone')
    email = fields.Char('Email')

    @api.model
    def sync_lexoffice_contacts(self, api_key):
        base_url = 'https://api.lexoffice.io/v1/'
        headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
        url = f'{base_url}contacts'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            contacts = response.json()['content']
            for contact in contacts:
                self._create_update_contact(contact)
        else:
            raise ValueError(f'Error fetching contacts from Lexoffice API: {response.text}')

    def _create_update_contact(self, contact_data):
        name = contact_data['company']['name']
        address = contact_data['addresses'][0]
        country_code = address['countryCode']
        country = self.env['res.country'].search([('code', '=', country_code)], limit=1)

        vals = {
            'name': name,
            'street': address['street'],
            'zip': address['zip'],
            'city': address['city'],
            'country_id': country.id,
            'phone': address['phone'],
            'email': address['email'],
        }

        existing_contact = self.search([('name', '=', name)], limit=1)
        if existing_contact:
            existing_contact.write(vals)
        else:
            self.create(vals)


@api.model
def sync_lexoffice_contacts(self, api_key, existing_lexoffice_ids=None):
    # ...
    if response.status_code == 200:
        contacts = response.json()['content']
        for contact in contacts:
            if existing_lexoffice_ids and contact['id'] in existing_lexoffice_ids:
                continue
            self._create_update_contact(contact)
    # ...

@api.model
def sync_new_lexoffice_data(self, api_key):
    self.sync_new_lexoffice_contacts(api_key)
    self.env['lexoffice.product'].sync_new_lexoffice_products(api_key)
    self.env['lexoffice.order'].sync_new_lexoffice_orders(api_key)
    self.env['lexoffice.invoice'].sync_new_lexoffice_invoices(api_key)

@api.model
def sync_new_lexoffice_contacts(self, api_key):
    contacts = self.env['res.partner'].search([('lexoffice_id', '!=', False)])
    existing_lexoffice_ids = [contact.lexoffice_id for contact in contacts]
    self.sync_lexoffice_contacts(api_key, existing_lexoffice_ids)

