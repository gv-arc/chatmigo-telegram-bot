import telebot
import pytz
import random
import requests
import time
import google.generativeai as genai
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

Token = "8032558207:AAEbnBzuP9uY5PUv8ECpyi0oKQWb70d58RI"
bot = telebot.TeleBot(Token)

# Commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "👋 Welcome to ChatMigo!\n\n"
        "🆘 /help - Tap on help to see commands")

# Gemini AI Configuration
GEMINI_API_KEY = "AIzaSyCgZq13rzLm-Ou35q02cFXVX_J2jo6sK8U"
genai.configure(api_key=GEMINI_API_KEY)

conversation_active = {}


# Gemini AI Command
@bot.message_handler(commands=['gemini_AI'])
def gemini_ai(message):
    conversation_active[message.chat.id] = True
    msg = bot.reply_to(message, "🤖 Ask me anything! Type /end_gemini to stop.")
    bot.register_next_step_handler(msg, process_gemini_question)

# Handle Gemini questions
def process_gemini_question(message):
    if conversation_active.get(message.chat.id, False):
        question = message.text
        if question.lower() == '/end_gemini':
            # End conversation if /end_gemini is typed
            conversation_active[message.chat.id] = False
            bot.reply_to(message, "🛑 Gemini AI conversation ended. Type /gemini_AI to start again.")
        else:
            # Get response from Gemini AI if it's not the end command
            answer = ask_gemini(question)
            bot.reply_to(message, f"🤖 AI: {answer}")
            msg = bot.reply_to(message, "You can ask another question or type /end_gemini to stop.")
            bot.register_next_step_handler(msg, process_gemini_question)
    else:
        bot.reply_to(message, "Gemini conversation has ended. Type /gemini_AI to start again.")

# Ask Gemini AI
def ask_gemini(question):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)
        return response.text if response.text else "🤖 I'm still learning! Try rephrasing."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# Time Feature
@bot.message_handler(commands=['time'])
def send_current_time(message):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_timezone).strftime("%H:%M:%S")
    bot.reply_to(message, f"🕒 The current time (IST) is: {current_time}")

# Weather Feature
API_KEY = "1f84f7822cedb19a745af07318adfa65"

@bot.message_handler(commands=['weather'])
def weather_info(message):
    msg = bot.reply_to(message, "🌆 Enter the city name:")
    bot.register_next_step_handler(msg, fetch_weather)

def fetch_weather(message):
    city = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        bot.reply_to(message, f"🌤️ Weather in {city}: {weather.capitalize()}, Temp: {temp}°C")
    else:
        bot.reply_to(message, "🌧️ City not found. Please try again.")

# News Feature
NEWS_API_KEY = "pub_659667b803284e1d7bc1d2041acf7c67a9353"

@bot.message_handler(commands=['news'])
def fetch_india_news(message):
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&country=in&language=en"
    response = requests.get(url).json()

    articles = response.get('results', [])
    if articles:
        headlines = "\n".join(f"{i+1}. {article['title']}" for i, article in enumerate(articles[:5]))
        bot.reply_to(message, f"📰 Top India News:\n\n{headlines}")
    else:
        bot.reply_to(message, "🚫 No news available right now. Please try again later.")

# Countdown Timer
@bot.message_handler(commands=['countdown_timer'])
def countdown(message):
    msg = bot.reply_to(message, "⏳ Please enter the countdown time in seconds:")
    bot.register_next_step_handler(msg, process_countdown_time)

def process_countdown_time(message):
    try:
        time_in_seconds = int(message.text.strip())
        for remaining in range(time_in_seconds, 0, -1):
            bot.reply_to(message, f"⏲️ Time remaining: {remaining} seconds")
            time.sleep(1)
        bot.reply_to(message, "🎉 Time's up!")
    except ValueError:
        bot.reply_to(message, "⚠️ Please enter a valid number for the countdown time.")

# Calculator
@bot.message_handler(commands=['calculator'])
def calculator(message):
    msg = bot.reply_to(message, "🧮 Enter expression (e.g., 2+3, 5-5, 4*3, 10/2):")
    bot.register_next_step_handler(msg, calculate)

def calculate(message):
    try:
        result = eval(message.text)
        bot.reply_to(message, f"🔢 Result: {result}")
    except ZeroDivisionError:
        bot.reply_to(message, "🚫 Error: Division by zero!")
    except Exception:
        bot.reply_to(message, "⚠️ Invalid input, use only +, -, *, /.")

# Age Calculator
@bot.message_handler(commands=['age_calculator'])
def age_calculator(message):
    bot.reply_to(message, "🎂 Please enter your date of birth in the format DD-MM-YYYY (e.g., 12-07-2002):")
    bot.register_next_step_handler(message, calculate_age)

def calculate_age(message):
    try:
        dob = datetime.strptime(message.text, "%d-%m-%Y")
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        bot.reply_to(message, f"🎉 You are {age} years old.")
    except ValueError:
        bot.reply_to(message, "⚠️ Invalid input. Please enter your date of birth in the format DD-MM-YYYY.")

# Study Material Feature
@bot.message_handler(commands=['study_material'])
def study_material(message):
    bot.reply_to(
        message,
        "📚 Here are some IT sector study resources to boost your knowledge:\n\n"
        "1. 📖 [Python Full Course](https://youtu.be/ERCMXc8x7mc?si=GzOTdwiyDKCgjm8T)\n\n"
        "2. 📘 [C Language Complete Course](https://youtu.be/irqbmMNs2Bo?si=yNY2AXZp-VKZByXd)\n\n"
        "3. 📙 [Complete Java + DSA Course](https://www.youtube.com/watch?v=yRpLlJmRo2w&list=PLfqMhTWNBTe3LtFWcvwpqTkUSlB32kJop)\n\n"
        "4. 📗 [Complete HTML,CSS & Java Script Course](https://www.youtube.com/watch?v=HcOc7P5BMi4&list=PLfqMhTWNBTe0PY9xunOzsP5kmYIz2Hu7i)\n\n"
        "5. 📒 [Complete MongoDB Tutorial](https://youtu.be/J6mDkcqU_ZE?si=jzK82Kt-YhF9gdw2)\n\n"
        "6. 📓 [Complete MySQL Course](https://youtu.be/hlGoQC332VM?si=G8plfjtDYZbAN_v8)\n\n"
        "7. 📔 [Complete Git & GitHub Tutorial](https://youtu.be/Ez8F0nW6S-w?si=lja0oLdXod21uaOA)\n\n"
    )

# Exam strategy
@bot.message_handler(commands=['examstrategy'])
def exam_preparation(message):
    strategies = [
        "📝 Start revising at least a few weeks before the exam to avoid last-minute cramming.",
        "🧑‍🎓 Use past exam papers for practice to familiarize yourself with the format.",
        "👩‍🏫 Teach the material to someone else to reinforce your understanding.",
        "💪 Stay healthy: get enough sleep, eat well, and stay hydrated."
    ]
    strategy = random.choice(strategies)
    bot.reply_to(message, f"📖 Exam Preparation Strategy: {strategy}")

# Quote Feature
@bot.message_handler(commands=['quote'])
def motivational_quote(message):
    quotes = [
        "💪 Believe you can and you're halfway there.",
        "🗣️ Be a voice, not an echo.",
        "⏰ Don't watch the clock; do what it does. Keep going.",
        "🍰 Life is short; make it sweet.",
        "🌟 Dream big and dare to fail.",
        "✨ Less perfection, more authenticity.",
        "🧠 Your only limit is your mind.",
    ]
    quote = random.choice(quotes)
    bot.reply_to(message, quote)

# Joke Feature
@bot.message_handler(commands=['joke'])
def tell_joke(message):
    jokes = [
        "😂 If the USA is so great, then why did someone make a USB? The system is rigged.",
        "👴 My grandfather has the heart of a lion and a lifetime ban from the zoo.",
        "📚 Why was the math book sad? It had too many problems.",
        "🎂 You know you're getting old when the candles cost more than the cake.",
        "💸 If money doesn’t grow on trees, why do banks have branches?"
    ]
    joke = random.choice(jokes)
    bot.reply_to(message, joke)

# About
@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(
        message,
        "🤖 I'm a simple chatbot created for interacting and replying to people.\n"
        "👨‍💻 I was developed by Gaurav Singh, student of Galgotias University."
    )

# Help Command
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(
        message,
        "🆘 Here are the commands you can use:\n\n"
        "/start - Start the bot\n\n"
        "/gemini_AI - 🤖 Ask me anything!\n\n"
        "/end_gemini - 🤖 For stop gemini\n\n"
        "/date - 📅 Get the current date\n\n"
        "/time - 🕒 Get the current time\n\n"
        "/weather - 🌤️ Get the current weather\n\n"
        "/news - 📰 Get the news\n\n"
        "/countdown_timer - ⏳ Set a countdown timer\n\n"
        "/calculator - 🧮 Perform calculations\n\n"
        "/age_calculator - 🎂 Calculate your age\n\n"
        "/study_material - 📚 Get some IT sector Courses\n\n"
        "/examstrategy - 📖 Make exam preparation plan\n\n"
        "/quote - 💬 Get a motivational quote\n\n"
        "/joke - 😂 Get a joke\n\n"
        "/about - ℹ️ About the bot\n\n"
    )

# Menu
@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = ReplyKeyboardMarkup(row_width=2)
    btn1 = KeyboardButton('/gemini_AI')
    btn2 = KeyboardButton('/date')
    btn3 = KeyboardButton('/time')
    btn4 = KeyboardButton('/weather')
    btn5 = KeyboardButton('/news')
    btn6 = KeyboardButton('/countdown_timer')
    btn7 = KeyboardButton('/calculator')
    btn8 = KeyboardButton('/age_calculator')
    btn9 = KeyboardButton('/study_material')
    btn10 = KeyboardButton('/examstrategy')
    btn11 = KeyboardButton('/quote')
    btn12 = KeyboardButton('/joke')
    btn13 = KeyboardButton('/about')
    btn14 = KeyboardButton('/end_gemini')
    markup.add(btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8,btn9,btn10,btn11,btn12,btn13,btn14)
    bot.send_message(message.chat.id, "🔍 Choose an option:", reply_markup=markup)

# Polling
bot.polling(non_stop=True, interval=0, timeout=120)