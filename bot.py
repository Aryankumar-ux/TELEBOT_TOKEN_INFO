import json
import requests
import telebot as t
token= 'YOUR_BOT_TOKEN_HERE'      
owner = "YOUR TELEGRAM USERNAME WITH '@'"
def get_bot_info(token):
    """
    Get bot information from Telegram API and return as formatted string.
    
    Args:
        token (str): Telegram bot token
        
    Returns:
        str: Formatted bot information or error message
    """
    try:
        response = requests.get(f'https://api.telegram.org/bot{token}/getme')
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            
            # Define emojis for each field
            emojis = {
                'id': '🆔',
                'username': '👤',
                'first_name': '📛',
                'last_name': '📛',
                'is_bot': '🤖',
                'can_join_groups': '👥',
                'can_read_all_group_messages': '📋',
                'supports_inline_queries': '🔍'
            }
            
            # Map field names to display names
            display_names = {
                'id': 'ID',
                'username': 'Username',
                'first_name': 'First Name',
                'last_name': 'Last Name',
                'is_bot': 'Bot Type',
                'can_join_groups': 'Can Join Groups',
                'can_read_all_group_messages': 'Can Read All Messages',
                'supports_inline_queries': 'Supports Inline Queries'
            }
            
            extracted_data = {
                'id': bot_info.get('id'),
                'username': bot_info.get('username'),
                'first_name': bot_info.get('first_name'),
                'last_name': bot_info.get('last_name'),
                'is_bot': bot_info.get('is_bot'),
                'can_join_groups': bot_info.get('can_join_groups'),
                'can_read_all_group_messages': bot_info.get('can_read_all_group_messages'),
                'supports_inline_queries': bot_info.get('supports_inline_queries')
            }
            
            result_lines = []
            for key, value in extracted_data.items():
                if value is not None:
                    emoji = emojis.get(key, '📌')
                    display_name = display_names.get(key, key.replace('_', ' ').title())
                    
                    # Special formatting for specific fields
                    if key == 'username':
                        value = f"@{value}"
                    elif key == 'is_bot':
                        value = "Yes" if value else "No"
                    elif key in ['can_join_groups', 'can_read_all_group_messages', 'supports_inline_queries']:
                        value = "✅ Yes" if value else "❌ No"
                    
                    result_lines.append(f"{emoji} {display_name}: {value}")
            
            return "\n".join(result_lines)
            
        else:
            error_msg = data.get('description', 'Unknown error')
            return f"❌ API Error: {error_msg}"
            
    except requests.exceptions.RequestException as e:
        return f"❌ Request failed: {e}"
    except json.JSONDecodeError as e:
        return f"❌ Failed to parse JSON: {e}"
    except KeyError as e:
        return f"❌ Missing expected key in response: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"


# Alternative version with more fancy formatting
def get_bot_info_fancy(token):
    """
    Get bot information with decorative formatting.
    
    Args:
        token (str): Telegram bot token
        
    Returns:
        str: Formatted bot information or error message
    """
    try:
        response = requests.get(f'https://api.telegram.org/bot{token}/getme')
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            
            # Build the result string with header
            result_lines = ["🤖 *Bot Information* 🤖", "=" * 25]
            
            # Add bot ID and username first (most important)
            if bot_info.get('id'):
                result_lines.append(f"🆔 *Bot ID:* {bot_info['id']}")
            
            if bot_info.get('username'):
                result_lines.append(f"👤 *Username:* @{bot_info['username']}")
            
            # Add name
            name_parts = []
            if bot_info.get('first_name'):
                name_parts.append(bot_info['first_name'])
            if bot_info.get('last_name'):
                name_parts.append(bot_info['last_name'])
            
            if name_parts:
                result_lines.append(f"📛 *Name:* {' '.join(name_parts)}")
            
            # Add bot status
            if bot_info.get('is_bot') is not None:
                bot_status = "🤖 Bot Account" if bot_info['is_bot'] else "👤 User Account"
                result_lines.append(f"*Type:* {bot_status}")
            
            # Add capabilities
            capabilities = []
            if bot_info.get('can_join_groups'):
                capabilities.append("👥 Join Groups")
            if bot_info.get('can_read_all_group_messages'):
                capabilities.append("📋 Read All Messages")
            if bot_info.get('supports_inline_queries'):
                capabilities.append("🔍 Inline Queries")
            
            if capabilities:
                result_lines.append("")
                result_lines.append("⚡ *Capabilities:*")
                for cap in capabilities:
                    result_lines.append(f"  ✅ {cap}")
            
            return "\n".join(result_lines)
            
        else:
            error_msg = data.get('description', 'Unknown error')
            return f"❌ *Error:* {error_msg}"
            
    except Exception as e:
        return f"❌ *Error:* {str(e)}"


bot=t.TeleBot(token)
@bot.message_handler(commands=['start','help'])
def start(msg):
 bot.reply_to(msg, '''This bot can find Bot information from token. Just type the token below and send it to me''')
@bot.message_handler(func=lambda message: True)
def find(msg):
    if ':' in msg.text:
        check=msg.text.split(':')
    else:
        bot.reply_to(msg, 'Tmkc Plz Enter a valid token!') 
        return      
    if not (check[1]!= 35 and check[0].isnumeric()):
        bot.reply_to(msg, 'Tmkc Plz Enter a valid token!') 
        return
    info=get_bot_info(msg.text)
    print(info)
    if 'Username' not in info:
        bot.reply_to(msg,f'''
Bot not found, Try Another
Possibilities:-
1.Wrong Token
2.Token changed or revoked
3.Bot deleted

Developed by : {owner}''')
        return
    r=f'''    
    {info}
    
Developed by : {owner}
    '''
    bot.reply_to(msg,r)
while True:
    try:
        bot.infinity_polling()
    except:
        bot.infinity_polling()             
