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

