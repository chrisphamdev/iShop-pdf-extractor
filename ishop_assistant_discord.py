import discord
from discord.ext.commands import Bot
from discord.ext import commands
import requests

import os
import os.path
from os import path

from main import *



bot = commands.Bot(command_prefix='.')

@bot.command()
async def fresh(ctx):

    # remove file if existed
    if path.exists('fresh orders'):
        os.remove('fresh orders')

    attachment_url = ctx.message.attachments[0].url
    file_request = requests.get(attachment_url)
    open('fresh orders', 'wb').write(file_request.content)
    
    file_pages = pdfextract('fresh orders')
    orders = process_data(file_pages)
    product_db = get_products_db()
    output_file = generate_output_file('output_file', crosscheck_productdb(orders, product_db))

    # This is a very bad way of generating file directory, will be fixed in the future
    current_dir = os.getcwd()
    if '/' in current_dir:
        output_file_dir = current_dir + '/' + 'FRESH orders.csv'
    else:
        output_file_dir = current_dir + '\\' + 'FRESH orders.csv'


    await ctx.send(file=discord.File(output_file_dir))

    


token = 'token goes here'
bot.run(token)