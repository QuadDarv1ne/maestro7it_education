import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from app import db, create_app
from app.models import User, Notification, UserPreference
import asyncio
import threading
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

class TelegramBotService:
    def __init__(self):
        self.application = None
        self.bot_thread = None
        
    def start_bot(self):
        """Start the Telegram bot in a separate thread"""
        if not TELEGRAM_BOT_TOKEN:
            logger.warning("TELEGRAM_BOT_TOKEN not set. Telegram bot will not start.")
            return
            
        self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
        self.bot_thread.start()
        logger.info("Telegram bot thread started")
    
    def _run_bot(self):
        """Run the bot application"""
        try:
            # Create Flask app context
            app = create_app()
            
            async def run_bot_async():
                # Create the Application and pass it your bot's token
                self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
                
                # Add command handlers
                self.application.add_handler(CommandHandler("start", self.start_command))
                self.application.add_handler(CommandHandler("help", self.help_command))
                self.application.add_handler(CommandHandler("profile", self.profile_command))
                self.application.add_handler(CommandHandler("notifications", self.notifications_command))
                self.application.add_handler(CommandHandler("settings", self.settings_command))
                
                # Add callback query handler for inline buttons
                self.application.add_handler(CallbackQueryHandler(self.button_callback))
                
                # Add message handler for text messages
                self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
                
                # Run the bot until the user presses Ctrl-C
                await self.application.run_polling(allowed_updates=Update.ALL_TYPES)
            
            # Run the async function in the app context
            with app.app_context():
                asyncio.run(run_bot_async())
                
        except Exception as e:
            logger.error(f"Error running Telegram bot: {e}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Check if user exists in our database
        with create_app().app_context():
            db_user = User.query.filter_by(username=user.username).first()
            
            if db_user:
                # Link Telegram chat to user
                db_user.telegram_chat_id = str(chat_id)
                db.session.commit()
                
                welcome_message = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в систему профориентации Maestro7IT!

Ваши возможности:
• Получение уведомлений о вакансиях
• Напоминания о тестировании
• Обновления по карьерным целям
• Персональные рекомендации

Используйте команды:
/help - Справка по командам
/profile - Ваш профиль
/notifications - Настройки уведомлений
/settings - Настройки бота
                """
            else:
                welcome_message = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в систему профориентации Maestro7IT!

Для начала работы зарегистрируйтесь на сайте:
https://ваш-сайт.ru/register

После регистрации вы сможете получать персональные уведомления и рекомендации через Telegram.

/help - Справка по командам
                """
        
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 Команды бота:

/start - Начало работы
/help - Эта справка
/profile - Информация о вашем профиле
/notifications - Настройки уведомлений
/settings - Настройки бота

💡 Функции:
• Автоматические уведомления о вакансиях
• Напоминания о карьерных целях
• Персональные рекомендации
• Статус ваших тестов

Свяжитесь с поддержкой, если возникнут вопросы!
        """
        await update.message.reply_text(help_text)
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        with create_app().app_context():
            db_user = User.query.filter_by(telegram_chat_id=str(chat_id)).first()
            
            if not db_user:
                await update.message.reply_text(
                    "Профиль не найден. Зарегистрируйтесь на сайте и свяжите аккаунт с Telegram."
                )
                return
            
            # Get user statistics
            test_count = len(db_user.test_results)
            goal_count = len([g for g in db_user.career_goals if g.current_status != 'achieved'])
            achieved_count = len([g for g in db_user.career_goals if g.current_status == 'achieved'])
            
            profile_text = f"""
👤 Ваш профиль:

Имя: {db_user.username}
Email: {db_user.email}
Дата регистрации: {db_user.created_at.strftime('%d.%m.%Y')}

📊 Статистика:
• Пройдено тестов: {test_count}
• Активных целей: {goal_count}
• Достигнутых целей: {achieved_count}

📈 Последняя активность: {db_user.created_at.strftime('%d.%m.%Y %H:%M')}
            """
            
            # Create inline keyboard
            keyboard = [
                [InlineKeyboardButton("📊 Мои тесты", callback_data="my_tests")],
                [InlineKeyboardButton("🎯 Мои цели", callback_data="my_goals")],
                [InlineKeyboardButton("📚 Обучение", callback_data="learning_paths")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(profile_text, reply_markup=reply_markup)
    
    async def notifications_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /notifications command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        with create_app().app_context():
            db_user = User.query.filter_by(telegram_chat_id=str(chat_id)).first()
            
            if not db_user:
                await update.message.reply_text(
                    "Профиль не найден. Зарегистрируйтесь на сайте и свяжите аккаунт с Telegram."
                )
                return
            
            # Get user preferences
            preferences = UserPreference.query.filter_by(user_id=db_user.id).first()
            
            if not preferences:
                # Create default preferences
                preferences = UserPreference(user_id=db_user.id)
                db.session.add(preferences)
                db.session.commit()
            
            status_text = "включены" if preferences.vacancy_alerts_enabled else "выключены"
            
            notifications_text = f"""
🔔 Настройки уведомлений:

Статус: {status_text}
Уведомления о вакансиях: {'✅ Включены' if preferences.vacancy_alerts_enabled else '❌ Выключены'}

Настроить уведомления:
            """
            
            # Create inline keyboard
            keyboard = [
                [InlineKeyboardButton(
                    f"{'Выключить' if preferences.vacancy_alerts_enabled else 'Включить'} уведомления", 
                    callback_data="toggle_notifications"
                )],
                [InlineKeyboardButton("Предпочтения профессий", callback_data="job_preferences")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(notifications_text, reply_markup=reply_markup)
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settings command"""
        settings_text = """
⚙️ Настройки бота:

Здесь вы можете настроить:
• Частоту уведомлений
• Типы получаемых сообщений
• Время активности
• Язык интерфейса

Для изменения настроек используйте команду /notifications
        """
        await update.message.reply_text(settings_text)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button presses"""
        query = update.callback_query
        await query.answer()
        
        chat_id = query.message.chat_id
        
        with create_app().app_context():
            db_user = User.query.filter_by(telegram_chat_id=str(chat_id)).first()
            
            if not db_user:
                await query.edit_message_text("Профиль не найден.")
                return
            
            if query.data == "toggle_notifications":
                # Toggle vacancy alerts
                preferences = UserPreference.query.filter_by(user_id=db_user.id).first()
                if not preferences:
                    preferences = UserPreference(user_id=db_user.id)
                    db.session.add(preferences)
                
                preferences.vacancy_alerts_enabled = not preferences.vacancy_alerts_enabled
                db.session.commit()
                
                status = "включены" if preferences.vacancy_alerts_enabled else "выключены"
                await query.edit_message_text(f"🔔 Уведомления успешно {status}!")
                
            elif query.data == "my_tests":
                # Show user's test results
                test_results = db_user.test_results[-5:]  # Last 5 tests
                if not test_results:
                    await query.edit_message_text("Вы еще не проходили тесты.")
                    return

                message = "📊 Ваши последние тесты:\n\n"
                import ast
                for result in test_results:
                    try:
                        results_dict = ast.literal_eval(result.results) if result.results else {}
                        dominant = results_dict.get('dominant_category', 'Не определено')
                        message += f"• {result.methodology.title()}: {dominant}\n"
                        message += f"  Дата: {result.created_at.strftime('%d.%m.%Y')}\n\n"
                    except (ValueError, SyntaxError, AttributeError):
                        continue

                await query.edit_message_text(message)
                
            elif query.data == "my_goals":
                # Show user's career goals
                active_goals = [g for g in db_user.career_goals if g.current_status != 'achieved']
                achieved_goals = [g for g in db_user.career_goals if g.current_status == 'achieved']
                
                message = "🎯 Ваши карьерные цели:\n\n"
                
                if active_goals:
                    message += "📍 Активные цели:\n"
                    for goal in active_goals[:3]:  # Show first 3
                        message += f"• {goal.title} (приоритет: {goal.priority})\n"
                    message += "\n"
                
                if achieved_goals:
                    message += f"🏆 Достигнуто целей: {len(achieved_goals)}\n"
                    for goal in achieved_goals[:2]:  # Show first 2
                        message += f"• {goal.title}\n"
                
                if not active_goals and not achieved_goals:
                    message = "У вас пока нет карьерных целей. Создайте первую цель в календаре!"
                
                await query.edit_message_text(message)
                
            elif query.data == "learning_paths":
                # Show user's learning paths
                active_paths = [p for p in db_user.learning_paths if p.status == 'in_progress']
                completed_paths = [p for p in db_user.learning_paths if p.status == 'completed']
                
                message = "📚 Ваши образовательные траектории:\n\n"
                
                if active_paths:
                    message += "📖 В процессе:\n"
                    for path in active_paths[:3]:
                        message += f"• {path.title} ({path.difficulty_level})\n"
                    message += "\n"
                
                if completed_paths:
                    message += f"🎓 Завершено: {len(completed_paths)}\n"
                
                if not active_paths and not completed_paths:
                    message = "У вас пока нет образовательных траекторий. Создайте первую в календаре!"
                
                await query.edit_message_text(message)
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_message = update.message.text.lower()
        
        responses = {
            'привет': 'Здравствуйте! Используйте /help для получения списка команд.',
            'пока': 'До свидания! Буду рад помочь вам в любое время.',
            'спасибо': 'Пожалуйста! Рад быть полезным.',
            'help': 'Используйте команду /help для получения справки.',
        }
        
        for key, response in responses.items():
            if key in user_message:
                await update.message.reply_text(response)
                return
        
        # Default response
        await update.message.reply_text(
            "Извините, я не понимаю эту команду. Используйте /help для получения списка доступных команд."
        )
    
    def send_notification(self, user_id, title, message, notification_type='info'):
        """Send notification to user via Telegram"""
        if not TELEGRAM_BOT_TOKEN:
            return False
            
        try:
            with create_app().app_context():
                user = User.query.get(user_id)
                if not user or not user.telegram_chat_id:
                    return False
                
                # Create notification in database
                notification = Notification(
                    user_id=user_id,
                    title=title,
                    message=message,
                    type=notification_type
                )
                db.session.add(notification)
                db.session.commit()
                
                # Send via Telegram
                async def send_message_async():
                    try:
                        await self.application.bot.send_message(
                            chat_id=int(user.telegram_chat_id),
                            text=f"🔔 *{title}*\n\n{message}",
                            parse_mode='Markdown'
                        )
                        return True
                    except Exception as e:
                        logger.error(f"Error sending Telegram message: {e}")
                        return False
                
                # Run async function
                result = asyncio.run(send_message_async())
                return result
                
        except Exception as e:
            logger.error(f"Error in send_notification: {e}")
            return False
    
    def send_vacancy_alert(self, user_id, vacancy_data):
        """Send vacancy alert to user"""
        title = f"💼 Новая вакансия: {vacancy_data.get('profession', 'Не указана')}"
        message = f"""
Найдена подходящая вакансия!

🏢 Компания: {vacancy_data.get('firm_name', 'Не указана')}
📍 Город: {vacancy_data.get('town_title', 'Не указан')}
💰 Зарплата: {vacancy_data.get('payment', 'Не указана')}
📅 Дата публикации: {vacancy_data.get('date_published', 'Не указана')}

🔗 Подробнее: {vacancy_data.get('link', '#')}

Не упустите шанс! Удачи в отклике.
        """
        
        return self.send_notification(user_id, title, message, 'success')

# Global bot instance
telegram_bot = TelegramBotService()

def start_telegram_bot():
    """Start the Telegram bot service"""
    telegram_bot.start_bot()

def send_user_notification(user_id, title, message, notification_type='info'):
    """Send notification to user via Telegram"""
    return telegram_bot.send_notification(user_id, title, message, notification_type)

def send_vacancy_alert(user_id, vacancy_data):
    """Send vacancy alert to user"""
    return telegram_bot.send_vacancy_alert(user_id, vacancy_data)