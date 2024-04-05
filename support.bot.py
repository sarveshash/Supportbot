from telethon import TelegramClient, events

# Your bot token and api_id/api_hash
API_ID = '23734455'
API_HASH = '40972650709e0e2b0aa58734f3524261'
BOT_TOKEN = '7152220317:AAEXfs2g4UiW91QQh1KT48lAmPpScvKy8s4'

# List of admin user IDs
admin_ids = ['1381668733', '1985764612', '5048444272']

# Initialize the Telegram client
client = TelegramClient('@HBG_HELP_BOT', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

banned_users = []
sudo_users = []
@client.on(events.NewMessage)
async def handle_message(event):
    if event.is_private:
        # ID of the admin group as an integer
        admin_group_id = -1001922948204  # Example ID, replace with your actual group ID
        
        # Parse the message for a user ID
        message_text = event.raw_text
        words = message_text.split()
        user_ids = [word for word in words if word.isdigit()]
        
        # Forward the message to the admin group only if a user ID is found in the message
        if user_ids:
            await client.forward_messages(admin_group_id, event.message)
            await event.reply("Thanks for your message. It has been granted.")
        else:
            # Optionally, send a message back to the user if no user ID is found in the message
            await event.reply("Please include a user ID in your message.")
# The reply functionality remains as previously described, allowing admins to reply to messages
@client.on(events.NewMessage(pattern='/reply'))
async def reply_to_user(event):
    # Split the message to extract the user ID and the reply message
    parts = event.raw_text.split(maxsplit=2)
    if len(parts) < 3:
        await event.reply('Usage: /reply <user_id> <message>')
        return

    user_id, message = parts[1], parts[2]

    # Check if the person sending the reply command is an admin
    if str(event.sender_id) in admin_ids:
        # Send the message to the user
        await client.send_message(int(user_id), message)
        await event.reply('Message sent!')
@client.on(events.NewMessage)
async def handle_message(event):
    # Check if the sender is banned
    if str(event.sender_id) in banned_users:
        return  # Ignore the message

    if event.is_private:
        admin_group_id = -1001821634604  # Example ID, replace with your actual group ID
        message_text = event.raw_text
        words = message_text.split()
        user_ids = [word for word in words if word.isdigit()]
        
        if user_ids:
            await client.forward_messages(admin_group_id, event.message)
        else:
            await event.reply("Please include a user ID in your message.")
@client.on(events.NewMessage(pattern='/ban'))
async def ban_user(event):
    # Split the message to extract the user ID
    parts = event.raw_text.split()
    if len(parts) < 2 or not str(event.sender_id) in admin_ids:
        return  # Ignore if the command format is wrong or the user is not an admin

    user_id = parts[1]
    banned_users.append(user_id)  # Add the user to the banned list
    await event.reply(f'User {user_id} has been banned.')

@client.on(events.NewMessage(pattern='/unban'))
async def unban_user(event):
    # Split the message to extract the user ID
    parts = event.raw_text.split()
    if len(parts) < 2 or not str(event.sender_id) in admin_ids:
        return  # Ignore if the command format is wrong or the user is not an admin

    user_id = parts[1]
    if user_id in banned_users:
        banned_users.remove(user_id)  # Remove the user from the banned list
        await event.reply(f'User {user_id} has been unbanned.')
@client.on(events.NewMessage(pattern='/sudo'))
async def add_sudo_user(event):
    # Ensure only admins can use this command
    if str(event.sender_id) not in admin_ids:
        await event.reply("You don't have permission to use this command.")
        return

    parts = event.raw_text.split()
    if len(parts) < 2:
        await event.reply("Usage: /sudo <user_id>")
        return

    user_id = parts[1]
    if user_id not in sudo_users:
        sudo_users.append(user_id)
        await event.reply(f'User {user_id} has been added to sudo users.')
    else:
        await event.reply(f'User {user_id} is already a sudo user.')

@client.on(events.NewMessage(pattern='/de-sudo'))
async def remove_sudo_user(event):
    # Ensure only admins can use this command
    if str(event.sender_id) not in admin_ids:
        await event.reply("You don't have permission to use this command.")
        return

    parts = event.raw_text.split()
    if len(parts) < 2:
        await event.reply("Usage: /de-sudo <user_id>")
        return

    user_id = parts[1]
    if user_id in sudo_users:
        sudo_users.remove(user_id)
        await event.reply(f'User {user_id} has been removed from sudo users.')
    else:
        await event.reply(f'User {user_id} is not a sudo user.')
# Run the client
client.run_until_disconnected()