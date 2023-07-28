import telebot
import random

TOKEN = '6072946813:AAH1AoAkuDlr6WxJfjt0Pm-2yndEfnD6Z5E'
bot = telebot.TeleBot(TOKEN)


def open_card(filename, list=[]):
    file = open(filename, encoding="utf8")
    for line in file:
        list.append(line.rstrip())



# def show_card(message, player_id):
#     player = player_cards[player_id]
#     card_text = "Ваша карточка игрока:\n"
#
#     for i, (key, value) in enumerate(player.card.items(), 0):
#         card_text += f"{i} - {key}: {value}\n"
#
#     bot.send_message(message.from_user.id, card_text)


# def change_choise(message, command):
#     card_char = {
#         1 : "Профессия",
#         2 : "Биологические параметры",
#         3 : "Состояние здоровья",
#         4 : "Фобия",
#         5 : "Багаж",
#         6 : "Хобби",
#         7 : "Человеческое качество",
#         8 : "Факт 1",
#         9 : "Факт 2",
#         10 : "Карта действия 1",
#         11 : "Карта действия 2"
#     }
#     if command in card_char:
#         return card_char[command]
#     else:
#         bot.send_message(message.chat.id, "Указанная характеристика не найдена в карточке игрока.")

def is_player_number(message, command):
    pass




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
        self.open_count = 0
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

    @classmethod
    def is_master(cls, message):
        user = message.from_user
        chat_member = bot.get_chat_member(message.chat.id, user.id)
        if chat_member.status in ('administrator', 'creator'):
            return True

        user_id = user.id
        if user_id in player_cards and player_cards[user_id].is_master():
            return True

        return False

    def update_characteristic(self, characteristic, new_value):
        if characteristic in self.card:
            self.card[characteristic] = new_value
            return True
        return False




class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.start_game = True
        self.game_data = {
            'catastrophes': [random.choice(catas_card)],
            'bunkers': random.sample(bynker_card, 5),
            'player_cards': {},
            'threats': []
        }

    def catastrophes(self):
        return self.game_data['catastrophes']

    def bunkers(self):
        return self.game_data['bunkers']

    def add_player_card(self, player_id, player_card):
        self.game_data['player_cards'][player_id] = player_card

    def get_player_card(self, player_id):
        return self.game_data['player_cards'].get(player_id)

    def get_all_player_cards(self):
        return self.game_data['player_cards']
    def is_player(self, player_id ):
        return player_id in self.game_data['player_cards']

    def show_card(self, message, player_id):
        player = self.game_data['player_cards'].get(player_id)
        if player:
            card_text = "Ваша карточка игрока:\n"
            for i, (key, value) in enumerate(player.card.items(), 0):
                card_text += f"{i} - {key}: {value}\n"
            bot.send_message(message.from_user.id, card_text)
        else:
            bot.send_message(message.from_user.id, "Ваша карточка игрока не найдена.")


    def select(self, char):
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
            return list_to_change

    def change_char_all(self, message, char):
        list_to_change = self.select(char)
        if list_to_change:
            for player_id, player in self.game_data['player_cards'].items():
                if player.update_characteristic(char, random.choice(list_to_change)):
                    bot.send_message(message.chat.id,
                                     f"Выбранная характеристика '{char}' в карточках всех игроков была изменена,"
                                     "новая карточка была отправлена вам в личные сообщения"
                                     " или получите обновленную карточку командой /play")
                else:
                    bot.send_message(message.chat.id,"иди нахуй)))")
        else:
            bot.send_message(message.chat.id, "Список значений для выбранной характеристики пуст.")


    def end_game(self):
        self.start_game = False
        self.game_data['player_cards'].clear()

    def process_game(self):
        return self.start_game

games = {}

player_cards = {}
player_number = 0


#####


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

    global games
    chat_id = message.chat.id
    if Player.is_master(message):
        if chat_id not in games:

            game = Game(chat_id)
            games[chat_id] = game

            global catastrophes,bunkers
            catastrophes = game.game_data['catastrophes']
            bunkers = game.game_data['bunkers']

            bot.send_message(message.chat.id, "Вы начали новую игру")
            bot.send_message(message.chat.id, f"Катастрофа:\n\n{catastrophes[0]}")
            mes = "\n\n"
            bot.send_message(message.chat.id, f"Условия бункера:\n\n{mes.join(bunkers)}")
            bot.send_message(message.chat.id,"Всем желающим принять участие в игре нужно разрешить "
                                             "боту присылать личные сообщения, для этого отправьте ему в личные сообщения "
                                             "команду /start.\n\n"
                                             "Чтобы присоедениться к игре и получить карту игрока отправьте команду "
                                             "/play в общий чат.\n\n"
                                             "Чтобы закончить игру отправьте команду /delete\n\n"
                                             "Список всех команд для игры - /help")


        else:
            bot.send_message(message.chat.id, "Условия вашей игры:")
            bot.send_message(message.chat.id, f"Катастрофа:\n\n{catastrophes[0]}")
            mes = "\n\n"
            bot.send_message(message.chat.id, f"Условия бункера:\n\n{mes.join(bunkers)}")
    else:
        bot.send_message(message.chat.id,"Чтобы начать игру вам нужно быть ведущим или администратором чата")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,"Перед началом игры убедитесь, что у всех игроков есть личный чат с ботом.\n\n"
                                     "/game - начните игру, вы получите 1 карту катастрофы и 5 карт бункера, "
                                     "введите команду в любое время, чтобы заново прочитать условия\n\n"
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
    chat_id = message.chat.id

    if chat_id  in games:
        game = games[chat_id]
        player_id = message.from_user.id

        if game.is_player( player_id ):
            game.show_card(message, player_id)

        else:
            global player_number
            player_number += 1

            player = Player(player_id, player_number)
            game.add_player_card(player_id,player)
            game.show_card(message, player_id)


    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")


@bot.message_handler(commands=['change_all_1', 'change_all_2', 'change_all_3', 'change_all_4', 'change_all_5', 'change_all_6', 'change_all_7', 'change_all_8', 'change_all_9'])
def change1(message):
    command = message.text.split()[0]
    global start_game
    if Player.is_master(message):
        chat_id = message.chat.id
        if chat_id in games:
            game = games[chat_id]

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
                game.change_char_all(message, char)


            else:
                bot.send_message(message.chat.id, "В игре нет игроков, каждому участнику игры необходимо ввести команду /play")

        else:
            bot.send_message(message.chat.id, "Вы не начали игру, введите /game")
    else:
        bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")




@bot.message_handler(commands=['delete'])
def delete(message):
    if Player.is_master(message):
        chat_id = message.chat.id
        if chat_id in games:

            game = games[chat_id]

            game.end_game()
            games.pop(chat_id)
            global player_number
            player_number = 0

            bot.send_message(message.chat.id, "Все карточки игроков были удалены.")
            print(game.game_data['player_cards'])
        else:
            bot.send_message(message.chat.id, "Вы не начали игру, введите /game")

    else:
        bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")





if __name__ == "__main__":
    bot.polling(none_stop=True)