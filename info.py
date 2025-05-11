import re
import os
from os import environ

id_pattern = re.compile(r'^.\d+$')

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", "28519661"))
API_HASH = os.environ.get("API_HASH", "d47c74c8a596fd3048955b322304109d")
PICS = os.environ.get("PICS", "https://graph.org/file/2518d4eb8c88f8f669f4c.jpg https://graph.org/file/d6d9d9b8d2dc779c49572.jpg https://graph.org/file/4b04eaad1e75e13e6dc08.jpg https://graph.org/file/05066f124a4ac500f8d91.jpg https://graph.org/file/2c64ed483c8fcf2bab7dd.jpg").split()
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5518489725').split()]
DB_URL = os.environ.get("DB_URL", "mongodb+srv://voromil970:q9aLNL7nsD8EDzwL@cluster0.rlvax.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "Spidey")
RemoveBG_API = os.environ.get("RemoveBG_API", "")
IBB_API = os.environ.get("IBB_API", "5da37930f3445a1b7bfa775dcd50ab65")
FORCE_SUB = os.environ.get("FORCE_SUB", "-1002470391435")
PORT = os.environ.get('PORT', '8080')          
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002294764885'))
LOG_TEXT = """<i><u>👁️‍🗨️USER DETAILS</u>

○ ID : <code>{id}</code>
○ DC : <code>{dc_id}</code>
○ First Name : <code>{first_name}<code>
○ UserName : @{username}

By = {bot}</i>"""
