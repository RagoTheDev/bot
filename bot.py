import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define your bot token
TOKEN = '6575581312:AAGXGXJcdN1nfDOtQ7EaV6v6wu7wGAgPlj8'

# Create a Bot object with your token
bot = telebot.TeleBot(TOKEN)

# List of token options with their corresponding prices
token_options = [
    {'id': 1, 'tokens': 5, 'price': 50},  # Example: 5 tokens for $50
    {'id': 2, 'tokens': 10, 'price': 90},  # Example: 10 tokens for $90
    # Add more options as needed
]

# Dictionary of cryptocurrency wallets
crypto_wallets = {
    'Bitcoin': 'BTC_ADDRESS',
    'Ethereum': 'ETH_ADDRESS',
    # Add more cryptocurrencies and their addresses as needed
}

# Dictionary to store customer email addresses
customer_emails = {}

# Function to handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for option in token_options:
        button_text = f'{option["tokens"]} tokens for ${option["price"]}'
        callback_data = f'option_{option["id"]}'
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard.add(button)
    bot.send_message(message.chat.id, 'Welcome to the Token Sale Bot! Please choose an option:', reply_markup=keyboard)

# Function to handle callback queries (button clicks)
@bot.callback_query_handler(func=lambda call: call.data.startswith('option_'))
def option_selected(call):
    option_id = int(call.data.split('_')[1])
    for option in token_options:
        if option['id'] == option_id:
            customer_chat_id = call.message.chat.id
            customer_emails[customer_chat_id] = None  # Initialize email to None
            bot.send_message(customer_chat_id, f'You have chosen {option["tokens"]} tokens for ${option["price"]}.\n\n'
                                                f'Please send your email address.')
            return

# Function to handle email messages
@bot.message_handler(func=lambda message: message.text and '@' in message.text)
def handle_email(message):
    customer_chat_id = message.chat.id
    if customer_chat_id in customer_emails:
        customer_emails[customer_chat_id] = message.text
        addresses_text = '\n'.join([f'{crypto}: {address}' for crypto, address in crypto_wallets.items()])
        bot.send_message(customer_chat_id, f'Thank you! Your email address has been recorded.\n\n'
                                            f'Please send payment to one of the following cryptocurrency wallets:\n'
                                            f'{addresses_text}')
    else:
        bot.send_message(customer_chat_id, 'Please select an option first.')

# Start the bot
bot.polling()
