import telebot
import random

TOKEN = '6072946813:AAH1AoAkuDlr6WxJfjt0Pm-2yndEfnD6Z5E'
bot = telebot.TeleBot(TOKEN)


def open_card(filename, list=[]):
    file = open(filename, encoding="utf8")
    for line in file:
        list.append(line.rstrip())


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
        self.ban = False
        self.open_count = 0
        self.number = number
        self.card = {
            "Номер игрока": self.number,
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
        return False

    def ban_player(self):
        self.ban = True
    def is_ban(self):
        return self.ban
    def update_characteristic(self, characteristic, new_value):
        if characteristic in self.card:
            self.card[characteristic] = new_value
            return True
        return False




class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.start_game = True
        self.player_number = 0
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

    def add_player_card(self, player_id):
        self.player_number += 1
        player_card = Player(player_id,  self.player_number)
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

    def change_char_all(self, char):
        list_to_change = self.select(char)
        flag = False
        if list_to_change:
            for player_id, player in self.game_data['player_cards'].items():
                if player.update_characteristic(char, random.choice(list_to_change)):
                    flag = True
                else:
                    flag = False
                    break
        else:
            return flag
        return flag

    def get_all_characteristics(self, characteristic):
        characteristic_values = [player.card[characteristic] for player in self.game_data['player_cards'].values()]
        print(characteristic_values)
        return characteristic_values




    def shuffle_characteristic(self, characteristic):
        flag = False

        all_characteristics = self.get_all_characteristics(characteristic)
        random.shuffle(all_characteristics)

        for player in self.game_data['player_cards'].values():
            if player.update_characteristic(characteristic, all_characteristics.pop()):
                flag = True
            else:
                flag = False
                break
        return flag

    def end_game(self):
        self.start_game = False
        self.game_data.clear()

    def process_game(self):
        return self.start_game

games = {}
global player_number
player_number = 1


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
    _catastrophes = []
    _bunkers = []
    if Player.is_master(message):
        if chat_id not in games:
            game = Game(chat_id)
            games[chat_id] = game

            _catastrophes = (game.game_data['catastrophes'])
            _bunkers = (game.game_data['bunkers'])

            bot.send_message(message.chat.id, "Вы начали новую игру")
            mes = "\n\n"
            bot.send_message(message.chat.id, f"Катастрофа:\n\n{mes.join(_catastrophes)}")
            bot.send_message(message.chat.id, f"Условия бункера:\n\n{mes.join(_bunkers)}")
            bot.send_message(message.chat.id,"Всем желающим принять участие в игре нужно разрешить "
                                             "боту присылать личные сообщения, для этого отправьте ему в личные сообщения "
                                             "команду /start.\n\n"
                                             "Чтобы присоедениться к игре и получить карту игрока отправьте команду "
                                             "/play в общий чат.\n\n"
                                             "Чтобы закончить игру отправьте команду /delete\n\n"
                                             "Список всех команд для игры - /help")



        else:
            _catastrophes = games[chat_id].game_data['catastrophes']
            _bunkers = games[chat_id].game_data['bunkers']
            bot.send_message(message.chat.id, "Условия вашей игры:")
            mes = "\n\n"
            bot.send_message(message.chat.id, f"Катастрофа:\n\n{mes.join(_catastrophes)}")

            bot.send_message(message.chat.id, f"Условия бункера:\n\n{mes.join(_bunkers)}")
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
                                     "/end удаляет из игры все карточки игроков и начинает игру заново (доступно только администратору чата)")



@bot.message_handler(commands=['play'])
def card(message):
    chat_id = message.chat.id
    if chat_id in games:
        game = games[chat_id]
        player_id = message.from_user.id

        if game.is_player( player_id ):
            game.show_card(message, player_id)

        else:
            game.add_player_card(player_id)
            game.show_card(message, player_id)
            print(games)
    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")


@bot.message_handler(commands=['change_all_1', 'change_all_2', 'change_all_3', 'change_all_4', 'change_all_5', 'change_all_6', 'change_all_7', 'change_all_8', 'change_all_9'])
def change1(message):
    command = message.text.split()[0]
    if Player.is_master(message):
        chat_id = message.chat.id
        if chat_id in games:
            game = games[chat_id]
            if len(game.get_all_player_cards()) != 0:
                    char_dict = {
                        '/change_all_1': "Профессия",
                        '/change_all_1@bynker_bot': "Профессия",
                        '/change_all_2': "Биологические параметры",
                        '/change_all_2@bynker_bot': "Биологические параметры",
                        '/change_all_3': "Состояние здоровья",
                        '/change_all_3@bynker_bot': "Состояние здоровья",
                        '/change_all_4': "Фобия",
                        '/change_all_4@bynker_bot': "Фобия",
                        '/change_all_5': "Багаж",
                        '/change_all_5@bynker_bot': "Багаж",
                        '/change_all_6': "Хобби",
                        '/change_all_6@bynker_bot': "Хобби",
                        '/change_all_7': "Человеческое качество",
                        '/change_all_7@bynker_bot': "Человеческое качество",
                        '/change_all_8': "Факт 1",
                        '/change_all_8@bynker_bot': "Факт 1",
                        '/change_all_9': "Факт 2",
                        '/change_all_9@bynker_bot': "Факт 2"
                    }

                    if command in char_dict:
                        char = char_dict[command]
                        if game.change_char_all(char):
                            player_id = message.from_user.id
                            game.show_card(message, player_id)
                            bot.send_message(message.chat.id,
                                             f"Выбранная характеристика '{char}' в карточках всех игроков была изменена, "
                                             "новая карточка была отправлена вам в личные сообщения"
                                             " или получите обновленную карточку командой /play")
                        else:
                            bot.send_message(message.chat.id, "Ошибка при изменении характеристики")

            else:
                bot.send_message(message.chat.id, "В игре нет игроков, каждому участнику игры необходимо ввести команду /play")
        else:
            bot.send_message(message.chat.id, "Вы не начали игру, введите /game")
    else:
        bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")

@bot.message_handler(commands=['shuf_1','shuf_2','shuf_3','shuf_4','shuf_5','shuf_6','shuf_7','shuf_8','shuf_9',])
def shuffle_characteristic(message):
    chat_id = message.chat.id
    command = message.text.split()[0]
    if chat_id in games:
        game = games[chat_id]
        if Player.is_master(message):
            if len(game.get_all_player_cards()) != 0:
                char_dict = {
                    '/shuf_1': "Профессия",
                    '/shuf_1@bynker_bot': "Профессия",
                    '/shuf_2': "Биологические параметры",
                    '/shuf_2@bynker_bot': "Биологические параметры",
                    '/shuf_3': "Состояние здоровья",
                    '/shuf_3@bynker_bot': "Состояние здоровья",
                    '/shuf_4': "Фобия",
                    '/shuf_4@bynker_bot': "Фобия",
                    '/shuf_5': "Багаж",
                    '/shuf_5@bynker_bot': "Багаж",
                    '/shuf_6': "Хобби",
                    '/shuf_6@bynker_bot': "Хобби",
                    '/shuf_7': "Человеческое качество",
                    '/shuf_7@bynker_bot': "Человеческое качество",
                    '/shuf_8': "Факт 1",
                    '/shuf_8@bynker_bot': "Факт 1",
                    '/shuf_9': "Факт 2",
                    '/shuf_9@bynker_bot': "Факт 2"
                }

                if command in char_dict:
                    characteristic_to_shuffle = 'Хобби'
                    if game.shuffle_characteristic(characteristic_to_shuffle):
                        bot.send_message(message.chat.id, f"Характеристика '{characteristic_to_shuffle}' была перемешана в карточках всех игроков.")
                    else:
                        bot.send_message(message.chat.id, f"Ошибка при перемешивании характеристики '{characteristic_to_shuffle}'.")

            else:
                bot.send_message(message.chat.id,
                                 "В игре нет игроков, каждому участнику игры необходимо ввести команду /play")
        else:
            bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")
    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")



@bot.message_handler(commands=['end'])
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