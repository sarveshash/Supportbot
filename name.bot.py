from telethon import TelegramClient, events


API_ID = '23734455'
API_HASH = '40972650709e0e2b0aa58734f3524261'
BOT_TOKEN = '7160432819:AAF0k20em9U0u-MuKApTzUqur2OrpnRbZ90'


admin_ids = ['1381668733', '1985764612', '5048444272']


client = TelegramClient('@HBG_NAME_SUPPORT_BOT', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

banned_users = []
sudo_users = []

@client.on(events.NewMessage(pattern='/reply'))
async def reply_to_user(event):

    parts = event.raw_text.split(maxsplit=2)
    if len(parts) < 3:
        await event.reply('Usage: /reply <user_id> <message>')
        return

    user_id, message = parts[1], parts[2]


    if str(event.sender_id) in admin_ids:

        await client.send_message(int(user_id), message)
        await event.reply('Message sent!')

    if event.raw_text.startswith('/submit'):
        return

    if event.is_private:
        admin_group_id =  -1001821634604 
        message_text = event.raw_text
        words = message_text.split()
        user_ids = [word for word in words if word.isdigit()]
        
        if user_ids:
            await client.forward_messages(admin_group_id, event.message)
        else:
            await event.reply("Please include a user ID in your message.") 



admin_group_id = -1001821634604  
submitted_users = []  
participants = {}

@client.on(events.NewMessage(pattern='/submit'))
async def submit_command(event):
    if event.is_private:
        sender_id = str(event.sender_id)
        sender_username = '@' + event.sender.username if event.sender.username else sender_id
        
        
        if sender_id in participants:
            await event.reply("You have already submitted your participation.")
        else:
            
            participants[sender_id] = sender_username
            
            
            message_to_admin = f"New participant joined: {sender_username}"
            await client.send_message(admin_group_id, message_to_admin)
            
            #
            await event.reply("Your participation has been submitted.")

@client.on(events.NewMessage(pattern='/list'))
async def list_participants(event):
    
    if str(event.sender_id) in admin_ids:
        if participants:
            message = "List of participants:\n"
            for user_id, username in participants.items():
                message += f"{username}\n"
            await event.reply(message)
        else:
            await event.reply("No participants have been submitted yet.")
    else:
        await event.reply("You do not have permission to use this command.")

client.run_until_disconnected()