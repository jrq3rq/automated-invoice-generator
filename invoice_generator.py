
import csv
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime  # Added for dynamic dates


def generate_invoice_number(sequence):
    current_date = datetime.now().strftime("%Y%m%d")
    return f"INV-{current_date}-{sequence:03d}"


def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_items(file_path):
    items = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Total'] = float(row['Unit Price']) * int(row['Quantity']) - float(row['Discount'])
            items.append(row)
    return items

def calculate_totals(items, tax_rate):
    subtotal = sum(item['Total'] for item in items)
    tax = subtotal * tax_rate / 100
    total = subtotal + tax
    return subtotal, tax, total

def render_invoice_to_html(config, items, subtotal, tax, total, invoice_number, customer_info):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('invoice_template.html')
    html_content = template.render(
        company_name=config['company_name'],
        company_address=config['company_address'],
        items=items,
        subtotal=subtotal,
        tax=tax,
        total=total,
        invoice_number=invoice_number,
        invoice_date=datetime.now().strftime("%Y-%m-%d"),  # Dynamic date
        customer_name=customer_info['name'],
        customer_address=customer_info['address']
    )
    with open('generated_invoice.html', 'w') as file:
        file.write(html_content)

def main():
    config = load_config('config.json')
    items = load_items('data/items_data.csv')
    subtotal, tax, total = calculate_totals(items, config['tax_rate'])

    # Example customer info
    customer_info = {
        "name": "John Doe",
        "address": "1234 Main St, Anytown, AT 12345"
    }

    # Generate invoice number
    sequence_number = 1  # This should be dynamically determined based on your application's logic
    invoice_number = generate_invoice_number(sequence_number)

    render_invoice_to_html(config, items, subtotal, tax, total, invoice_number, customer_info)
    print("Invoice generated successfully.")


if __name__ == "__main__":
    main()
