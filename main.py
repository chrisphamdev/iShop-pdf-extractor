import pdfplumber
import csv
import time


# This function take a pdf filename as input, and will output the content page by page as a list
# The input filename should include the file extension if there exist one
def pdfextract(filename):
    all_pages = []

    with pdfplumber.open(filename) as pdf:
        num_of_pages = len(pdf.pages)
        for i in range(num_of_pages):
            first_page = pdf.pages[i]
            content = first_page.extract_text()
            all_pages += [content]

    return all_pages


# This function access the file 'product.csv' and returns a dictionary
# The key-value pair of this dictionary is in the form of {productID:productName}
def get_products_db():
    with open('productdb.csv', mode='r') as file:
        reader = csv.reader(file)
        mydict = {rows[0]:rows[1] for rows in reader}
    return mydict


# This function take in a list of texts, each list item is a full order
# The function outputs a dictionary, with order ID as the key
# The value corresponds to each key are in the form [customer_name, order_timeslot, required_items]
# required_items being all of the items that the customer ordered
def process_data(all_pages):
    output = {}
    for page in all_pages:
        content = page.split('\n')
        order_number = content[1].split()[-1]
        order_timeslot = content[3].split()[-1]
        customer_name = content[4][10:]

        items_index_start = content.index('Aisle Bay Shelf Slot Product ID Product Name Unit Price $ Value $ Status')
        items_index_end = content.index("Picker's notes on the Order")

        all_requested_items = []
        required_items = content[items_index_start+2:items_index_end]
        
        for i in range(len(required_items)-1, -1, -1):
            if required_items[i] == 'FRESH':
                required_items.pop(i)
        
        for item in required_items:
            if item[:4].isdigit():
                all_requested_items.append(item)

        output[order_number] = [customer_name, order_timeslot, all_requested_items]

    return output


def crosscheck_productdb(orders_dict, product_dict):
    items_by_orderid = []
    output = ''
    for orderid in orders_dict.keys():
        # extract the order information
        customer_name, timeslot, required_items = orders_dict[orderid][0], orders_dict[orderid][1], orders_dict[orderid][2]

        for item in required_items:
            # The data is in the string, format: AISLE BAY SHELF SLOT PRODUCT_ID PRODUCT_NAME QUANTITY PRICE VALUE
            # Some line may not have SHELF and SLOT, needs filtering
            # All product ID (PLU) has more than 5 digits, while SHELF and SLOT has 4 digits
            splitted_data = item.split()
            item_id, quantity = splitted_data[2], splitted_data[-3]

            # if index 2 is SHELF (less than 5 digits), move to index 4 which is the true product ID
            if len(item_id) < 5:
                item_id = splitted_data[4]

            if item_id in product_dict:
                output += '{},{},{},{},{},{}'.format(orderid, customer_name, timeslot, item_id, product_dict[item_id], quantity)
                output += '\n'
    
    return output

def generate_output_file(filename, to_write):
    try:
        f = open('FRESH orders.csv', 'x')
    except:
        f = open('FRESH orders.csv', 'w')
        f.truncate(0)
    finally:
        f.write(to_write)
        f.close()


def main():
    print('_'*63)
    print()
    print('           New World Stonefields iShop PDF Extractor           ')
    print('_'*63)
    print()
    print('          This program was written by Chris Pham, 2022')
    print('_'*63)
    print()
    while True:
        try:
            prompt = input('Enter input file name (the filename is likely to be in the format "download (number)"): ')
            print('Processing...')
            file_pages = pdfextract(prompt)
        except:
            print('Filename does not exist. Please try again.')
            continue
        break
    
    orders = process_data(file_pages)
    product_db = get_products_db()
    generate_output_file('output_file', crosscheck_productdb(orders, product_db))

    print('File has been processed! The filename is "FRESH orders.csv".')
    print('The program will close itself in 5 seconds.')

    time.sleep(5)


main()