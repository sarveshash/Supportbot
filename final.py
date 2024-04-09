from telethon import TelegramClient, events
import sqlite3

API_ID = '23734455'
API_HASH = '40972650709e0e2b0aa58734f3524261'
BOT_TOKEN = '7160432819:AAF0i_v4rjTZDv7uZ4l2Daez7mrxaPxTYEE'




conn = sqlite3.connect('updated2_participants_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS updated2_participants (username TEXT PRIMARY KEY)''')
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS players2 (username TEXT PRIMARY KEY)''')
conn.commit()

conn = sqlite3.connect('participant_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS participants (user_id TEXT PRIMARY KEY, username TEXT)''')
conn.commit()

conn = sqlite3.connect('your_database.db')
c = conn.cursor()

# Create the updated_participants table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS updated_participants (
                username TEXT PRIMARY KEY
            )''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS updated2_participants (
                username TEXT PRIMARY KEY
            )''')
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS pending_commands (user_id TEXT, command_type TEXT, parameters TEXT)''')
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS submitted_users (username TEXT PRIMARY KEY)''')
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS players (username TEXT PRIMARY KEY)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS user_data (user_id TEXT PRIMARY KEY, username TEXT)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS user_data (user_id TEXT PRIMARY KEY, username TEXT)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS user_data (user_id TEXT PRIMARY KEY, username TEXT, added_number INTEGER DEFAULT 0)''')
conn.commit()

c.execute("PRAGMA table_info(user_data)")
columns = c.fetchall()
column_names = [column[1] for column in columns]

if 'added_number' not in column_names:
    c.execute('''ALTER TABLE user_data ADD COLUMN added_number INTEGER DEFAULT 0''')
    conn.commit()
else:
    print("Column 'added_number' already exists in the user_data table.")
# Check if the column already exists in the user_data table




async def process_pending_commands():
    conn = sqlite3.connect('your_database.db')
    c = conn.cursor()

    # Create the pending_commands table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS pending_commands (user_id TEXT, command_type TEXT, parameters TEXT)''')
    conn.commit()

    # Select data from the pending_commands table
    c.execute("SELECT * FROM pending_commands")
    pending_commands = c.fetchall()

    for command in pending_commands:
        user_id, command_type, parameters = command
        
        c.execute("DELETE FROM pending_commands WHERE user_id = ?", (user_id,))
        conn.commit()




admin_ids = ['1381668733', '1985764612', '5048444272' , '7025637676']
updated_list = []
updated2_list = []
added_number = []
submitted_users = []

client = TelegramClient('@HBG_NAME_SUPPORT_BOT', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
profile_data = []
banned_users = []
sudo_users = []
players = {}
players2 = {}

@client.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    if event.is_private:
        sender_id = str(event.sender_id)
        command_type = '/start'
        parameters = '' 
        sender_username = '@' + event.sender.username if event.sender.username else sender_id

        try:
            c.execute("INSERT INTO user_data (user_id, username) VALUES (?, ?)", (sender_id, sender_username))
            conn.commit()
            await event.reply("Your data has been stored.")
        except sqlite3.IntegrityError:
            await event.reply("Your data is already stored.")

async def is_bot_admin(client, chat_id):
    try:
        chat = await client.get_entity(chat_id)
        participant = await client.get_participants(chat)
        for user in participant:
            if user.id == client.get_me().id:
                return user.admin_rights
    except Exception as e:
        print(f"Error checking admin status: {e}")
    return False

@client.on(events.NewMessage(pattern='/profile'))
async def profile_command(event):
    sender_id = str(event.sender_id)

    # Retrieve user data from the database based on user_id
    c.execute("SELECT * FROM user_data WHERE user_id = ?", (sender_id,))
    user_data = c.fetchone()

    if user_data:
        user_id, username, added_number, profile_data = user_data  # Unpack the user_data tuple
        user = await client.get_entity(int(user_id))

        user_info = f"User info:\n"
        user_info += f"ID: {user_id}\n"
        user_info += f"First Name: {user.first_name}\n"
        user_info += f"Username: @{user.username}\n"
        user_info += f"User link: [User Profile](tg://user?id={user_id})\n"
        user_info += f"Added Number: {added_number}\n"  # Display the added number
        user_info += f"Profile Data: {profile_data}\n"  # Display the profile data

        await event.reply(user_info)
    else:
        await event.reply("No user data found.")
async def is_bot_admin(client, chat_id):
    try:
        chat = await client.get_entity(chat_id)
        participant = await client.get_participants(chat)
        for user in participant:
            if user.id == (await client.get_me()).id:  # Await get_me() to access the id attribute
                return user.admin_rights
    except Exception as e:
        print(f"Error checking admin status: {e}")
    return False


previous_added_numbers = {}  # Dictionary to store previous added numbers for users

@client.on(events.NewMessage(pattern='/add'))
async def add_command(event):
    if event.is_reply and str(event.sender_id) in admin_ids:
        reply_msg = await event.get_reply_message()
        user_id = str(reply_msg.sender_id)
        added_number = int(event.raw_text.split()[1])  # Extract the number from the command

        # Store the previous added number for the user
        if user_id in previous_added_numbers:
            previous_added_numbers[user_id].append(added_number)
        else:
            previous_added_numbers[user_id] = [added_number]

        # Update the user's profile data with the added number
        c.execute("UPDATE user_data SET added_number = added_number + ? WHERE user_id = ?", (added_number, user_id))
        conn.commit()

        await event.reply(f"Added {added_number} to the user's profile data.")
    else:
        await event.reply("You need to be a bot admin and reply to a message to use this command.")


@client.on(events.NewMessage(pattern='/undo'))
async def undo_command(event):
    if event.is_reply and str(event.sender_id) in admin_ids:
        reply_msg = await event.get_reply_message()
        user_id = str(reply_msg.sender_id)

        if user_id in previous_added_numbers:
            previous_numbers = previous_added_numbers.get(user_id, [])
            if previous_numbers:
                history_message = "History of Added/Subtracted Numbers:\n"
                for idx, number in enumerate(previous_numbers, start=1):
                    if number < 0:
                        history_message += f"{idx}. -{-number}\n"  # Display subtracted number with a '-' sign
                    else:
                        history_message += f"{idx}. {number}\n"  # Display added number

                await event.reply(history_message)
            else:
                await event.reply("No previous added/subtracted number found for the user.")
        else:
            await event.reply("No previous added/subtracted number found for the user.")
    else:
        await event.reply("You need to be a bot admin and reply to a message to use this command.")

@client.on(events.NewMessage(pattern='/12'))
async def delete_added_number(event):
    if str(event.sender_id) in admin_ids:
        reply_msg = await event.get_reply_message()
        user_id = str(reply_msg.sender_id)

        # Delete the added number data for the user
        c.execute("UPDATE user_data SET added_number = 0 WHERE user_id = ?", (user_id,))
        conn.commit()

        await event.reply("Added number data deleted for the user.")
    else:
        await event.reply("You need to be a bot admin to use this command.")

@client.on(events.NewMessage(pattern='/minus'))
async def minus_command(event):
    if event.is_reply and str(event.sender_id) in admin_ids:
        reply_msg = await event.get_reply_message()
        user_id = str(reply_msg.sender_id)
        minus_number = int(event.raw_text.split()[1])  # Extract the number to subtract from the command

        # Update the user's profile data by subtracting the specified number
        c.execute("SELECT added_number FROM user_data WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        current_added_number = result[0] if result is not None else 0

        new_added_number = current_added_number - minus_number

        c.execute("UPDATE user_data SET added_number = ? WHERE user_id = ?", (new_added_number, user_id))
        conn.commit()

        # Store the subtracted number in the previous_added_numbers dictionary with a '-' sign
        if user_id in previous_added_numbers:
            previous_added_numbers[user_id].append(-minus_number)
        else:
            previous_added_numbers[user_id] = [-minus_number]

        await event.reply(f"Subtracted {minus_number} from the user's profile data.")
    else:
        await event.reply("You need to be a bot admin and reply to a message to use this command.")

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

@client.on(events.NewMessage(pattern='/update'))
async def update(event):
    if str(event.sender_id) in admin_ids:
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.reply('Usage: /update_list {list}')
            return

        new_list = parts[1].split(', ')

        try:
            c.execute('''CREATE TABLE IF NOT EXISTS updated_participants (username TEXT PRIMARY KEY)''')
            conn.commit()

            # Update list with new data
            for username in new_list:
                try:
                    c.execute("INSERT INTO updated_participants (username) VALUES (?)", (username,))
                except sqlite3.IntegrityError:
                    pass  # Skip if username already exists
            conn.commit()

            await event.reply('List updated successfully.')
        except sqlite3.OperationalError as e:
            print(f"Error creating updated_participants table: {e}")
            await event.reply("An error occurred while updating the list.")
    else:
        await event.reply("You do not have permission to use this command.")

@client.on(events.NewMessage(pattern='/update1'))
async def update1(event):
    if str(event.sender_id) in admin_ids:
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.reply('Usage: /update1_list {list}')
            return

        new_list = parts[1].split(', ')

        try:
            c.execute('''CREATE TABLE IF NOT EXISTS updated2_participants (username TEXT PRIMARY KEY)''')
            conn.commit()

            # Update list with new data
            for username in new_list:
                try:
                    c.execute("INSERT INTO updated2_participants (username) VALUES (?)", (username,))
                except sqlite3.IntegrityError:
                    pass  # Skip if username already exists
            conn.commit()

            await event.reply('List updated successfully.')
        except sqlite3.OperationalError as e:
            print(f"Error creating updated2_participants table: {e}")
            await event.reply("An error occurred while updating the list.")
    else:
        await event.reply("You do not have permission to use this command.")


@client.on(events.NewMessage(pattern='/submit'))
async def submit_command(event):
    if event.is_private:
        sender_id = str(event.sender_id)
        command_type = '/submit'
        parameters = '' 
        sender_username = '@' + event.sender.username if event.sender.username else sender_id

        try:
            c.execute("INSERT INTO submitted_users (username) VALUES (?)", (sender_username,))
            conn.commit()
            await event.reply("Your participation has been submitted.")
            message_to_admin = f"New participant joined: {sender_username}"
            await client.send_message(admin_group_id, message_to_admin)
        except sqlite3.IntegrityError:
            await event.reply("You have already submitted your name.")


admin_group_id = -1001821634604  
submitted_users = []  
participants = {}
submitted_users = set()
current_page = 1 


total_participants = 0  

@client.on(events.NewMessage(pattern='/list'))
async def list(event):
    if str(event.sender_id) in admin_ids:
        c.execute("SELECT username FROM submitted_users ORDER BY username ASC")
        submitted_participants = c.fetchall()

        if submitted_participants:
            message = "Submitted Participants:\n"

            for idx, item in enumerate(submitted_participants, start=1):
                message += f"{idx}. {item[0]}\n"

            await event.reply(message)
        else:
            await event.reply("No participants have been submitted yet.")
    else:
        await event.reply("You do not have permission to use this command.")



submitted_users.clear()
participants.clear()

@client.on(events.NewMessage(pattern='/clear_data'))
async def clear_data(event):
    # Updated code to clear player data from the database
    updated_list.clear()
    players.clear()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='updated_participants'")
    table_exists = c.fetchone()

    if table_exists:
        c.execute("DELETE FROM updated_participants")
        c.execute("DELETE FROM players")  # Clear player data
        conn.commit()

        await event.reply("All data has been cleared.")
    else:
        await event.reply("No data to clear.")

@client.on(events.NewMessage(pattern='/clear'))
async def clear(event):
    # Updated code to clear player data from the database
    updated2_list.clear()
    players2.clear()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='updated2_participants'")
    table_exists = c.fetchone()

    if table_exists:
        c.execute("DELETE FROM updated2_participants")
        c.execute("DELETE FROM players2")  # Clear player data
        conn.commit()

        await event.reply("All data has been cleared.")
    else:
        await event.reply("No data to clear.")


@client.on(events.NewMessage(pattern='/players'))
async def list_players(event):
    if str(event.sender_id) in admin_ids:
        message = "Players List:\n"
        c.execute("SELECT username FROM updated_participants ORDER BY username ASC")
        player_list = c.fetchall()

        if player_list:
            for idx, player in enumerate(player_list, start=1):
                message += f"{idx}. {player[0]}\n"
        else:
            message = "No players found."

        await event.reply(message)
    else:
        await event.reply("You do not have permission to use this command.")
@client.on(events.NewMessage(pattern='/45'))
async def list_45(event):
    if str(event.sender_id) in admin_ids:
        message = "Players List:\n"
        c.execute("SELECT username FROM updated2_participants ORDER BY username ASC")
        player_list = c.fetchall()

        if player_list:
            for idx, player in enumerate(player_list, start=1):
                message += f"{idx}. {player[0]}\n"
        else:
            message = "No players found."

        await event.reply(message)
    else:
        await event.reply("You do not have permission to use this command.")

@client.on(events.NewMessage(pattern='/dlt'))
async def delete_submit_data(event):
    if str(event.sender_id) in admin_ids:
        c.execute("DELETE FROM submitted_users")
        conn.commit()
        await event.reply("Submitted user data has been deleted.")
    else:
        await event.reply("You do not have permission to use this command.")

conn = sqlite3.connect('participant_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_data (user_id TEXT PRIMARY KEY, username TEXT, added_number INTEGER DEFAULT 0, profile_data TEXT)''')
conn.commit()


@client.on(events.NewMessage(pattern='/cap'))
async def cap_command(event):
    if event.is_reply and str(event.sender_id) in admin_ids:
        reply_msg = await event.get_reply_message()
        user_id = str(reply_msg.sender_id)

        # Check if the profile_data column exists in the user_data table
        c.execute("PRAGMA table_info(user_data)")
        columns = c.fetchall()
        column_names = [column[1] for column in columns]

        if 'profile_data' not in column_names:
            c.execute("ALTER TABLE user_data ADD COLUMN profile_data TEXT DEFAULT ''")
            conn.commit()

        # Add the special emoji to the user's profile data
        special_emoji = "🧢"  # Special emoji to add
        c.execute("UPDATE user_data SET profile_data = ? WHERE user_id = ?", (special_emoji, user_id))
        conn.commit()

        await event.reply("Special emoji added to the user's profile data.")
    else:
        await event.reply("You need to be a bot admin and reply to a message to use this command.")

@client.on(events.NewMessage(pattern='/69'))
async def uncap_command(event):
    if event.is_reply and str(event.sender_id) in admin_ids:
        reply_msg = await event.get_reply_message()
        user_id = str(reply_msg.sender_id)

        # Delete the profile_data for the user
        c.execute("UPDATE user_data SET profile_data = '' WHERE user_id = ?", (user_id,))
        conn.commit()

        await event.reply("Profile data deleted for the user.")
    else:
        await event.reply("You need to be a bot admin and reply to a message to use this command.")

async def main():
    await client.start()
    await process_pending_commands()
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())