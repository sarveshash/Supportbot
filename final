from telethon import TelegramClient, events
import sqlite3

API_ID = '23734455'
API_HASH = '40972650709e0e2b0aa58734f3524261'
BOT_TOKEN = '7160432819:AAF0i_v4rjTZDv7uZ4l2Daez7mrxaPxTYEE'

conn = sqlite3.connect('participant_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS participants (user_id TEXT PRIMARY KEY, username TEXT)''')
conn.commit()

conn = sqlite3.connect('updated_participants_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS updated_participants (username TEXT PRIMARY KEY)''')
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS pending_commands (user_id TEXT, command_type TEXT, parameters TEXT)''')
conn.commit()




admin_ids = ['1381668733', '1985764612', '5048444272']
updated_list = []


client = TelegramClient('@HBG_NAME_SUPPORT_BOT', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

banned_users = []
sudo_users = []

async def process_pending_commands():
    c.execute("SELECT * FROM pending_commands")
    pending_commands = c.fetchall()

    for command in pending_commands:
        user_id, command_type, parameters = command
        
        c.execute("DELETE FROM pending_commands WHERE user_id = ?", (user_id,))
        conn.commit()

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

@client.on(events.NewMessage(pattern='/submit'))
async def submit_command(event):
    if event.is_private:
        sender_id = str(event.sender_id)
        user_id = str(event.sender_id)
        command_type = '/submit'
        parameters = '' 
        sender_username = '@' + event.sender.username if event.sender.username else sender_id


        if sender_username in updated_list:
            await event.reply("You have already submitted your name.")
        else:
            
            if sender_username in participants or sender_username in submitted_users:
                await event.reply("Your name has already been submitted.")
            else:
            
                c.execute("SELECT username FROM updated_participants WHERE username = ?", (sender_username,))
                existing_username = c.fetchone()
                c.execute("INSERT INTO pending_commands (user_id, command_type, parameters) VALUES (?, ?, ?)", (user_id, command_type, parameters))
                conn.commit()
                

                if existing_username:
                    await event.reply("This username is already in the updated list.")
                else:
                    updated_list.append(sender_username)
                    c.execute("INSERT INTO updated_participants (username) VALUES (?)", (sender_username,))
                    conn.commit()
                    await event.reply("Your participation has been submitted.")
                    message_to_admin = f"New participant joined: {sender_username}"
                    await client.send_message(admin_group_id, message_to_admin)


admin_group_id = -1001821634604  
submitted_users = []  
participants = {}
submitted_users = set()
current_page = 1 


total_participants = 0  

@client.on(events.NewMessage(pattern='/list 1'))
async def list_page_1(event):
    if str(event.sender_id) in admin_ids:
        c.execute("SELECT username FROM updated_participants ORDER BY username ASC")
        updated_participants = c.fetchall()

        if updated_participants:
            message = "Updated List (Page 1):\n"

            # Display the first page data only
            page_size = len(updated_participants) // 2
            page_1 = updated_participants[:page_size]

            for idx, item in enumerate(page_1, start=1):
                message += f"{idx}. {item[0]}\n"

            await event.reply(message)
            await event.reply("Type /list 2 to view the second page.")
        else:
            await event.reply("No participants have been submitted yet.")

@client.on(events.NewMessage(pattern='/list 2'))
async def list_page_2(event):
    if str(event.sender_id) in admin_ids:
        c.execute("SELECT username FROM updated_participants ORDER BY username ASC")
        updated_participants = c.fetchall()

        if updated_participants:
            message = "Updated List (Page 2):\n"

            # Display the second page data only
            page_size = len(updated_participants) // 2
            page_2 = updated_participants[page_size:]

            for idx, item in enumerate(page_2, start=page_size + 40):
                message += f"{idx}. {item[0]}\n"

            await event.reply(message)
        else:
            await event.reply("No participants have been submitted yet.")

submitted_users.clear()
participants.clear()

@client.on(events.NewMessage(pattern='/clear_data'))
async def clear_data(event):
    global updated_list  
    if str(event.sender_id) in admin_ids:
        
        updated_list.clear()

        
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='updated_participants'")
        table_exists = c.fetchone()

        if table_exists:
        
            c.execute("DELETE FROM updated_participants")
            conn.commit()

            await event.reply("All data has been cleared.")
        else:
            await event.reply("No data to clear.")
    else:
        await event.reply("You do not have permission to use this command.")

@client.on(events.NewMessage(pattern='/update'))
async def update_list(event):
    if str(event.sender_id) in admin_ids:
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.reply('Usage: /update {list}')
            return

        new_list = parts[1].split(', ')

        existing_users = [username for username in new_list if username in updated_list]

        if existing_users:
            await event.reply(f"The following users have already submitted their names: {', '.join(existing_users)}")
        else:
            
            for username in new_list:
                c.execute("SELECT username FROM updated_participants WHERE username = ?", (username,))
                existing_username = c.fetchone()
                if not existing_username:
                    updated_list.append(username)
                    c.execute("INSERT INTO updated_participants (username) VALUES (?)", (username,))
            conn.commit()

            await event.reply('List updated successfully.')
    else:
        await event.reply("You do not have permission to use this command.")


async def main():
    await client.start()
    await process_pending_commands()
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())