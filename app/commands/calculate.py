from utils.sort import extract_date_time
from config import SHEET_NAME
from utils.excel import ExcelWriter
from utils.calculate import calculate_salary, clear_data


def register_commands(bot):
    messages = []

    @bot.message_handler(commands=['start'])
    def start(message):
        messages.clear()
        bot.reply_to(message, 'Отправьте мне сообщения, и я составлю отчет по зарплатам. Используйте /calculate для отправки отчета.')

    @bot.message_handler(commands=['calculate'])
    def calculate(message):
        clear_data()
        sorted_messages = sorted(messages, key=extract_date_time)
        with ExcelWriter() as writer:
            for msg in sorted_messages:
                result = calculate_salary(msg)
                if result is None:
                    messages.pop(messages.index(msg))
                    bot.send_message(message.chat.id, f"Неправильный формат отчета по смене:\n{msg}\nИсправьте и пришлите снова")
                else:
                        writer.write_general_data(result)

            writer.write_total_data()
        bot.send_document(message.chat.id, open(f"data/{SHEET_NAME}.xlsx", "rb"))


    @bot.message_handler(content_types=["text", "photo"])
    def collect(message):
        if message.content_type == "photo":
            messages.append(message.caption)
        else:
            messages.append(message.text)
