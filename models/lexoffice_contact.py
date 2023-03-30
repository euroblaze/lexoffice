


@api.model
def sync_new_lexoffice_data(self, api_key):
    self.sync_new_lexoffice_contacts(api_key)
    self.env['lexoffice.product'].sync_new_lexoffice_products(api_key)
    self.env['lexoffice.order'].sync_new_lexoffice_orders(api_key)
    self.env['lexoffice.invoice'].sync_new_lexoffice_invoices(api_key)
