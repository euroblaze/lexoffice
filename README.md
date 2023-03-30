# Lexoffice Connector

This Odoo module connects to the Lexoffice API and retrieves contacts, products, orders, and invoices. It provides an easy way to synchronize your Lexoffice data with your Odoo instance.

## Features

- Import contacts from Lexoffice to Odoo as partners
- Import products from Lexoffice to Odoo as products
- Import orders from Lexoffice to Odoo as sales orders
- Import invoices from Lexoffice to Odoo as invoices
- Scheduled action to synchronize new data from Lexoffice every hour

## Installation

1. Place the `lexoffice_connector` folder in your Odoo addons directory.
2. Go to the Odoo Apps menu and click on "Update Apps List."
3. Search for "Lexoffice Connector" in the search bar and click "Install."

## Configuration

Make sure to replace `'your_api_key_here'` in the `data/scheduled_actions.xml` file with your actual Lexoffice API key before installing the module.

## Author

Simplify-ERP™, PowerOn™

## Website

https://simplify-erp.de

```
lexoffice_connector/
├── controllers/
│   └── __init__.py
├── models/
│   ├── __init__.py
│   ├── lexoffice_contact.py
│   ├── lexoffice_product.py
│   ├── lexoffice_order.py
│   └── lexoffice_invoice.py
├── views/
│   ├── lexoffice_contact_views.xml
│   ├── lexoffice_product_views.xml
│   ├── lexoffice_order_views.xml
│   └── lexoffice_invoice_views.xml
├── data/
│   └── scheduled_actions.xml
├── __init__.py
├── __manifest__.py
└── README.md
´´´
