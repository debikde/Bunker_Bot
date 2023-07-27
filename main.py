import telebot
import random

TOKEN = '6072946813:AAH1AoAkuDlr6WxJfjt0Pm-2yndEfnD6Z5E'
bot = telebot.TeleBot(TOKEN)


def open_card(filename, list=[]):
    file = open(filename, encoding="utf8")
    for line in file:
        list.append(line.rstrip())

def is_admin(message):
    user = message.from_user
    chat_member = bot.get_chat_member(message.chat.id, user.id)
    if chat_member.status in ('administrator', 'creator'):
        return True

    user_id = user.id
    if user_id in player_cards and player_cards[user_id].is_master:
        return True

    return False


def show_card(message, player_id):
    player = player_cards[player_id]
    card_text = "Ваша карточка игрока:\n"

    for i, (key, value) in enumerate(player.card.items(), 0):
        card_text += f"{i} - {key}: {value}\n"

    bot.send_message(message.from_user.id, card_text)


def change_choise(message, command):
    card_char = {
        1 : "Профессия",
        2 : "Биологические параметры",
        3 : "Состояние здоровья",
        4 : "Фобия",
        5 : "Багаж",
        6 : "Хобби",
        7 : "Человеческое качество",
        8 : "Факт 1",
        9 : "Факт 2",
        10 : "Карта действия 1",
        11 : "Карта действия 2"
    }
    if command in card_char:
        return card_char[command]
    else:
        bot.send_message(message.chat.id, "Указанная характеристика не найдена в карточке игрока.")

def is_player_number(message, command):
    pass

def change_char(message, char):
    if char not in player_cards[next(iter(player_cards))].card:
        bot.send_message(message.chat.id, "Указанная характеристика не найдена в карточке игрока.")
        return

    list_to_change = []
    if char == "Профессия":
        list_to_change = professions_card
    elif char == "Биологические параметры":
        list_to_change = biological_parameters_card
    elif char == "Состояние здоровья":
        list_to_change = health_status_card
    elif char == "Фобия":
        list_to_change = phobias_card
    elif char == "Багаж":
        list_to_change = baggage_card
    elif char == "Хобби":
        list_to_change = hobbies_card
    elif char == "Человеческое качество":
        list_to_change = human_qualities_card
    elif char == "Факт 1":
        list_to_change = facts_card
    elif char == "Факт 2":
        list_to_change = facts_card

    if list_to_change:
        for card in player_cards.values():
            card.update_characteristic(char, random.choice(list_to_change))

        bot.send_message(message.chat.id, f"Выбранная характеристика '{char}' в карточках всех игроков была изменена,"
                                          " получите обновленную карточку командой /play")
    else:
        bot.send_message(message.chat.id, "Список значений для выбранной характеристики пуст.")


professions_card = []
biological_parameters_card = []
health_status_card = []
phobias_card = []
baggage_card = []
hobbies_card = []
human_qualities_card = []
facts_card = []
action_card1 = []
action_card2 = []
bynker_card = []
catas_card = []
threat_card = []
open_card("cards/prof.txt", professions_card)
open_card("cards/action_card1.txt", action_card1)
open_card("cards/action_card2.txt", action_card2)
open_card("cards/hobbi.txt", hobbies_card)
open_card("cards/health.txt", health_status_card)
open_card("cards/bio.txt", biological_parameters_card)
open_card("cards/bag.txt", baggage_card)
open_card("cards/phobia.txt", phobias_card)
open_card("cards/humanq.txt", human_qualities_card)
open_card("cards/facts.txt", facts_card)
open_card("cards/benker.txt", bynker_card)
open_card("cards/catas.txt", catas_card)
open_card("cards/threat.txt", threat_card)


class Player:

    def __init__(self, user_id, number):
        self.user_id = user_id
        self.number = number
        self.master = False
        self.card = {
            "Номер игрока": number,
            "Профессия": random.choice(professions_card),
            "Биологические параметры": random.choice(biological_parameters_card),
            "Состояние здоровья": random.choice(health_status_card),
            "Фобия": random.choice(phobias_card),
            "Багаж": random.choice(baggage_card),
            "Хобби": random.choice(hobbies_card),
            "Человеческое качество": random.choice(human_qualities_card),
            "Факт 1": random.choice(facts_card),
            "Факт 2": random.choice(facts_card),
            "Карта действия 1": random.choice(action_card1),
            "Карта действия 2": random.choice(action_card2),
        }

    def set_master(self):
        self.master = True

    def is_master(self):
        return self.master

    def update_characteristic(self, characteristic, new_value):
        if characteristic in self.card:
            self.card[characteristic] = new_value


player_cards = {}
player_number = 0
start_game = False
catastrophes = []
bunkers = []
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Всем участникам игры необходимо написать боту в личные сообщения команду /start\n'
                                      'Начните игру с помощью команды /game\n'
                                      'Добавьтесь в игру командой /play\n'
                                      'Бот в личные сообщения отправит вам вашу карточку игрока.'
                                      '\nЧтобы посмотреть свою карточку в любой момент снова введите /play'
                                      '\nСписок всех команд доступен по команде /help')

@bot.message_handler(commands=['game'])
def start(message):
    global start_game
    global bunkers
    global catastrophes
    if not start_game:
        start_game = True
        catastrophes = [random.choice(catas_card)]
        bunkers = random.sample(bynker_card, 5)
        bot.send_message(message.chat.id, "Вы начали новую игру")
        bot.send_message(message.chat.id, f"Катастрофа:\n\n{catastrophes[0]}")
        mes = ""
        for i in bunkers:
            mes += str(i) + "\n\n"

        bot.send_message(message.chat.id, f"Условия бункера:\n\n{mes}")

    else:
        bot.send_message(message.chat.id, "Условия вашей игры:")
        bot.send_message(message.chat.id, f"Катастрофа:\n\n{catastrophes[0]}")
        mes = ""
        for i in bunkers:
            mes += str(i) + "\n\n"

        bot.send_message(message.chat.id, f"Условия бункера:\n\n{mes}")



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,"Перед началом игры убедитесь, что у всех игроков есть личный чат с ботом.\n\n"
                                     "/game - начните игру, вы получите 1 карту катастрофы и 5 карт бункера, "
                                     "ввыедите команду в любое время, чтобы заново прочитать условия\n\n"
                                     "/play - Вы вступите в игру и бот отправит вам в личные сообщения вашу карту игрока, "
                                     "используйте эту команду чтобы в любой момент увидеть свою обновленную карту игрока\n\n"
                                     "/change_all_1 - меняет всем игрокам значение Профессии (доступно только администратору чата)\n\n"
                                     "/change_all_2 - меняет всем игрокам значение Биологических параметров (доступно только администратору чата)\n\n"
                                     "/change_all_3 - меняет всем игрокам значение Состояния здоровья (доступно только администратору чата)\n\n"
                                     "/change_all_4 - меняет всем игрокам значение Фобии (доступно только администратору чата)\n\n"
                                     "/change_all_5 - меняет всем игрокам значение Багажа (доступно только администратору чата)\n\n"
                                     "/change_all_6 - меняет всем игрокам значение Хобби (доступно только администратору чата)\n\n"
                                     "/change_all_7 - меняет всем игрокам значение Человеческого качества (доступно только администратору чата)\n\n"
                                     "/change_all_8 - меняет всем игрокам значение Факта 1 (доступно только администратору чата)\n\n"
                                     "/change_all_9 - меняет всем игрокам значение Факта 2 (доступно только администратору чата)\n\n"
                                     "/delete удаляет из игры все карточки игроков и начинает игру заново (доступно только администратору чата)")



@bot.message_handler(commands=['play'])
def card(message):
    global start_game
    if start_game:
        player_id = message.from_user.id

        if player_id in player_cards:
            show_card(message, player_id)

        else:
            global player_number
            player_number += 1

            player = Player(player_id, player_number)
            player_cards[player_id] = player

            show_card(message, player_id)
    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")


@bot.message_handler(commands=['change_all_1', 'change_all_2', 'change_all_3', 'change_all_4', 'change_all_5', 'change_all_6', 'change_all_7', 'change_all_8', 'change_all_9'])
def change1(message):
    command = message.text.split()[0]
    global start_game
    if is_admin(message):
        if start_game:
            if len(player_cards) !=0:
                char_dict = {
                    '/change_all_1': "Профессия",
                    '/change_all_2': "Биологические параметры",
                    '/change_all_3': "Состояние здоровья",
                    '/change_all_4': "Фобия",
                    '/change_all_5': "Багаж",
                    '/change_all_6': "Хобби",
                    '/change_all_7': "Человеческое качество",
                    '/change_all_8': "Факт 1",
                    '/change_all_9': "Факт 2"
                }

                if command in char_dict:
                    char = char_dict[command]
                    change_char(message, char)
            else:
                bot.send_message(message.chat.id, "В игре нет игроков, каждому участнику игры необходимо ввести команду /play")

        else:
            bot.send_message(message.chat.id, "Вы не начали игру, введите /game")
    else:
        bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")




@bot.message_handler(commands=['delete'])
def delete(message):
    if is_admin(message):
        global start_game
        if start_game:
            start_game = False
            global player_cards
            player_cards.clear()
            global player_number
            player_number = 0
            bot.send_message(message.chat.id, "Все карточки игроков были удалены.")
        else:
            bot.send_message(message.chat.id, "Вы не начали игру, введите /game")

    else:
        bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")





if __name__ == "__main__":
    bot.polling(none_stop=True)