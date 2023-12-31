import telebot
import random
from time import time
TOKEN = '6072946813:AAH1AoAkuDlr6WxJfjt0Pm-2yndEfnD6Z5E'
bot = telebot.TeleBot(TOKEN)


def open_card(filename, list):
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
        self.number = number
        self.opened_characteristics = []
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

    def open_characteristic(self, char_number):
        if char_number not in self.opened_characteristics:
            self.opened_characteristics.append(char_number)

    def get_opened_characteristics(self):
        return self.opened_characteristics
    def get_open_count(self):
        return len(self.opened_characteristics)

    @classmethod
    def is_master(cls, message):
        user = message.from_user
        chat_member = bot.get_chat_member(message.chat.id, user.id)
        if chat_member.status in ('administrator', 'creator'):
            return True
        return False

    def appoint_master(self):
        self.master = True

    def ban_player(self):
        self.ban = True
        for characteristic in self.card:
            self.card[characteristic] = None
    def is_ban(self):
        return self.ban
    def update_characteristic(self, characteristic, new_value):
        if characteristic in self.card and new_value != None:
            self.card[characteristic] = new_value
            return True
        return False






class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.player_number = 0
        self.bunker_places = 0
        self.game_data = {
            'catastrophes': [random.choice(catas_card)],
            'bunkers': random.sample(bynker_card, 5),
            'player_cards': {},
            'threats': []
        }

    def catastrophes(self):
        return self.game_data['catastrophes']
    def change_catastrophes(self):
        self.game_data['catastrophes'] = [random.choice(catas_card)]

    def add_threats(self):
        self.game_data['threats'] += random.sample(threat_card, 1)

    def get_all_threats(self):
        return self.game_data['threats']

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
        if player and not player.is_ban():
            card_text = "Ваша карточка игрока:\n"
            for i, (key, value) in enumerate(player.card.items(), 0):
                card_text += f"{i} - {key}: {value}\n"
            bot.send_message(message.from_user.id, card_text)

    def send_player_cards(self):
        for player_id, player in self.game_data['player_cards'].items():
            if not player.is_ban():
                card_text = "Ваша карточка игрока:\n"
                for i, (key, value) in enumerate(player.card.items(), 0):
                    card_text += f"{i} - {key}: {value}\n"
                bot.send_message(player_id, card_text)

    def select(self, char):
        list_to_change = []
        try:
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
        except ValueError:
           print("Error select")

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

    def change_characteristic(self, player_number, char):
        player_id = None
        for pid, player in self.game_data['player_cards'].items():
            if player.number == player_number:
                player_id = pid
                break

        if player_id:
            return self.get_player_card(player_id).update_characteristic(char, random.choice(self.select(char)))
        return False

    def get_all_characteristics(self, characteristic):
        characteristic_values = [player.card[characteristic] for player in self.game_data['player_cards'].values()]
        return characteristic_values

    def shuffle_characteristic(self, charact):
        flag = False

        all_charact = self.get_all_characteristics(charact)
        random.shuffle(all_charact)

        for player in self.game_data['player_cards'].values():
            if player.update_characteristic(charact, all_charact.pop()):
                flag = True
            else:
                flag = False
                break
        return flag

    def swap_characteristic(self, player_number1, player_number2, char):
        player1 = None
        player2 = None

        for player_id, player in self.game_data['player_cards'].items():
            if player.number == player_number1:
                player1 = player
            elif player.number == player_number2:
                player2 = player

        if not (player1 and player2):
            return False

        if abs(player1.number - player2.number) != 1:
            return False

        char1_value = player1.card.get(char)
        char2_value = player2.card.get(char)

        if char1_value is None or char2_value is None:
            return False

        player1.card[char] = char2_value
        player2.card[char] = char1_value

        return True

    def ban_player(self, player_number):
        player_id = None
        for pid, player in self.game_data['player_cards'].items():
            if player.number == player_number:
                player_id = pid
                break

        if player_id:
            player = self.get_player_card(player_id)
            player.ban_player()
            return True
        return False

    def end_game(self):
        self.player_number = 0
        self.bunker_places = 0
        self.game_data.clear()

    def process_game(self):
        return self.start_game

games = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот, который помогает проводить сессии игры в "Бункер" онлайн прямо в телеграме! '
                                      'Для того, чтобы провести игру, добавьте меня в ваш чат\n'
                                      'Всем участникам игры необходимо написать боту в личные сообщения команду /start\n'
                                      'Начните игру с помощью команды /game\n'
                                      'Добавьтесь в игру командой /play\n'
                                      'Бот в личные сообщения отправит вам вашу карточку игрока.'
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
        if chat_id in games:
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
                                     "!!Вместо * ставится номер в соответсвии с выбранной характеристикой или номорм игрока, "
                                     "бот не следит за ходом игры и вашим выбором, будьте внимательны. "
                                     "(Коды характеристик: 1 - Профессия, 2 - Биологические параметры,"
                                     "3 - Состояние здоровья, 4 - Фобия, 5 - Багаж, 6 - Хобби, 8 - Факт 1, 9 - Факт 2\n"
                                     "Коды также указаны в вашей карточке игрока)!!\n"
                                     "Номер игрока указан в его карточке.\n\n\n"
                                     "/game - начните игру, вы получите 1 карту катастрофы и 5 карт бункера, "
                                     "введите команду в любое время, чтобы заново прочитать условия.\n\n"
                                     "/play - Вы вступите в игру и бот отправит вам в личные сообщения вашу карту игрока, "
                                     "используйте эту команду чтобы в любой момент увидеть свою обновленную карту игрока.\n\n"
                                     "/show * - Показывает в общем чате выбранную вами характеристику.\n\n"
                                     "/ban * - Изгоняет игрока с выбранным номером (доступно только администратору чата).\n\n"
                                     "/add_tr - Добавляет в игру 1 новую угрозу (доступно только администратору чата).\n\n"
                                     "/tr - Выводит все угрозы в игре на данный момент.\n\n"
                                     "/end удаляет из игры все карточки игроков и начинает игру заново (доступно только администратору чата)\n\n\n"
                                     "Команды карт действия (доступны только администратору чата):\n\n"
                                     "Чтобы воспользоваться любой из карт действия введите команду /show 10 или /show 11,"
                                     "в зависимости от того, какую карту вы хотите использовать. Когда вы покажите ведущему свою карту,"
                                     " он должен использовать одну из команд ниже."
                                     "/ch_all * - Меняет всем игрокам значение выбранной характеристики.\n\n"
                                     "/shuf * - Перемешивает между игроками значения выбранной характеристики.\n\n"
                                     "/ch *(номер характеристики) *(номер игрока) - изменяет выбранную характеристику игроку с указанным номером.\n\n"
                                     "/swap *(номер игрока 1) *(номер игрока 2) *(номер характеристики) - меняет между собой выбранные характеристики у"
                                     " указаных игроков. Обмен происходит только между игроками, чья разница номеров равна 1.\n\n"
                                     "/ch_cata - Изменяет текущую катастрофу в игре.\n\n\n")




@bot.message_handler(commands=['play'])
def card(message):
    chat_id = message.chat.id
    if chat_id in games:
        game = games[chat_id]
        player_id = message.from_user.id
        player = game.get_player_card(player_id)
        try:

            if player:
                        if player.is_ban():
                            bot.send_message(message.chat.id, "Вы забанены и не можете присоединиться к игре.")
                        else:
                            game.show_card(message, player_id)
            else:

                        if not player_id in game.get_all_player_cards():
                            game.add_player_card(player_id)
                            game.show_card(message, player_id)
                            user_info = bot.get_chat_member(chat_id, player_id).user
                            username = user_info.username
                            player_number = game.player_number
                            bot.send_message(message.chat.id, f"@{username} Вы присоединились к игре! Ваш номер игрока: {player_number}")
                        else:
                            game.show_card(message, player_id)
        except:
            bot.send_message(message.chat.id,"Для того чтобы присоединиться к игре, нужно разрешить отправлять боту личные сообщения, для этого отправьте ему в личной переписке команду /start")

    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")

@bot.message_handler(commands=['show'])
def show_characteristic(message):
    chat_id = message.chat.id
    try:
        command, char_number = message.text.split(maxsplit=1)
        char_number = int(char_number)
    except ValueError:
        bot.send_message(message.chat.id, "Введите команду и номер характеристики после неё, например: /show 1")
        return

    if chat_id in games:
        game = games[chat_id]
        player_id = message.from_user.id
        player = game.get_player_card(player_id)

        if player and not player.is_ban():
            char = select_command(char_number)
            if char and char in player.card:
                characteristic_value = player.card[char]
                opened_characteristics = player.get_opened_characteristics()

                if char_number not in opened_characteristics:
                    opened_characteristics.append(char_number)

                card_text = f"Карточка игрока номер {player.number}:\n"
                for i, (key, value) in enumerate(player.card.items(), 0):
                    if i == 0:
                        card_text += f"{i} - {key}: {player.number}\n"
                    elif i in opened_characteristics:
                        card_text += f"{i} - {key}: {value}\n"
                    else:
                        card_text += f"{i} - {key}:\n"

                bot.send_message(chat_id, card_text)
                player.open_characteristic(char_number)
            else:
                bot.send_message(message.chat.id, "Проверьте, что ввели правильный код характеристики.")
        else:
            bot.send_message(message.chat.id, "Вы не участвуете в игре.")
    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")

@bot.message_handler(commands=['ban'])
def ban_player(message):
    chat_id = message.chat.id
    try:
        command, player_number = message.text.split(maxsplit = 1)
        player_number = int(player_number)
    except ValueError:
        bot.send_message(message.chat.id,
                         "Введите команду и номер игрока после неё, например: /ban 1")
        return

    if chat_id in games:
        if Player.is_master(message):
            game = games[chat_id]
            if len(game.get_all_player_cards()) != 0:
                if game.ban_player(player_number):
                    bot.send_message(message.chat.id, f"Игрок с номером {player_number} был изгнан.")
                else:
                    bot.send_message(message.chat.id, f"Игрок с номером {player_number} не найден.")
            else:
                bot.send_message(message.chat.id,
                                 "В игре нет игроков, каждому участнику игры необходимо ввести команду /play")
        else:
            bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")
    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")



@bot.message_handler(commands=['add_tr'])
def threats(message):
    chat_id = message.chat.id
    if chat_id in games:
        if Player.is_master(message):
            game = games[chat_id]
            game.add_threats()
            _threats = game.get_all_threats()
            mes = "\n\n"
            bot.send_message(message.chat.id, f"Добавлена новая угроза:\n\n{mes.join(_threats)}")

        else:
            bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")
    else:

        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")


@bot.message_handler(commands=['tr'])
def show_threats(message):
    chat_id = message.chat.id
    if chat_id in games:
        game = games[chat_id]
        threats = game.get_all_threats()
        if threats:
            threat_list_text = "Список угроз в игре:\n"
            _threats = game.get_all_threats()
            mes = "\n\n"
            bot.send_message(message.chat.id, f"Угрозы:\n\n{mes.join(_threats)}")
        else:
            bot.send_message(chat_id, "В игре нет еще угроз.")
    else:
        bot.send_message(chat_id, "Вы не начали игру, введите /game")

def select_command( number):
    char_dict = {
        1: "Профессия",
        2: "Биологические параметры",
        3: "Состояние здоровья",
        4: "Фобия",
        5: "Багаж",
        6: "Хобби",
        7: "Человеческое качество",
        8: "Факт 1",
        9: "Факт 2",
    }
    if number in char_dict:
        char = char_dict[number]
        return char

@bot.message_handler(commands=['ch'])
def change_characteristic(message):
    chat_id = message.chat.id
    try:
        command, char_number, player_number = message.text.split(maxsplit = 2)
        char_number = int(char_number)
        player_number = int(player_number)
    except ValueError:
        bot.send_message(message.chat.id,
                         "Введите команду, номер характеристики и номер игрока после неё, например: /ch 1 2\n"
                         "Коды характеристик: 1 - Профессия, 2 - Биологические параметры, 3 - Состояние здоровья, 4 - Фобия, 5 - Багаж, 6 - Хобби, 8 - Факт 1, 9 - Факт 2\n"
                         "Коды также указаны в вашей карточке игрока")
        return

    if chat_id in games:
        if Player.is_master(message):
            game = games[chat_id]
            if len(game.get_all_player_cards()) != 0:
                    char = select_command(char_number)
                    if char and game.change_characteristic(player_number, char):
                        game.send_player_cards()
                        bot.send_message(message.chat.id,
                                         f"Характеристика '{char}' у игрока с номером {player_number} была изменена \n\n"
                                         f"Обновленную карточку вы можете получить командой /play")
                    else:
                        bot.send_message(message.chat.id, f"Ошибка при изменении характеристики. Проверьте, что ввели правильный код характеристики и номер игрока")
            else:
                bot.send_message(message.chat.id, "В игре нет игроков, каждому участнику игры необходимо ввести команду /play")
        else:
            bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")
    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")


@bot.message_handler(commands=['ch_all'])
def change1(message):
    chat_id = message.chat.id
    number = int
    try:
        command, number_str = message.text.split(maxsplit=1)
        number = int(number_str)
    except ValueError:
        bot.send_message(message.chat.id,
                         "Введите команду и число характеристики после неё, например: /ch_all 1\n"
                         "Коды характеристик: 1 - Профессия, 2 - Биологические параметры, 3 - Состояние здоровья, 4 - Фобия, 5 - Багаж, 6 - Хобби, 8 - Факт 1, 9 - Факт 2\n"
                         "Коды также указаны в вашей карточке игрока")
    if chat_id in games:
        if Player.is_master(message):
            game = games[chat_id]
            if len(game.get_all_player_cards()) != 0:
                        char = select_command(number)
                        if game.change_char_all(char):
                            player_id = message.from_user.id
                            game.send_player_cards()
                            bot.send_message(message.chat.id,
                                                f"Выбранная характеристика '{char}' в карточках всех игроков была изменена, "
                                                "новая карточка была отправлена вам в личные сообщения"
                                                " или получите обновленную карточку командой /play")
                        else:
                            bot.send_message(message.chat.id, "Ошибка при изменении характеристики")

            else:
                bot.send_message(message.chat.id, "В игре нет игроков, каждому участнику игры необходимо ввести команду /play")
        else:
            bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")
    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")



@bot.message_handler(commands=['shuf'])
def shuffle_characteristic(message):
    chat_id = message.chat.id
    number = int
    try:
        command, number_str = message.text.split(maxsplit=1)
        number = int(number_str)
    except ValueError:
        bot.send_message(message.chat.id,
                         "Введите команду и число характеристики после неё, например: /shuf 1\n"
                         "Коды характеристик: 1 - Профессия, 2 - Биологические параметры, 3 - Состояние здоровья, 4 - Фобия, 5 - Багаж, 6 - Хобби, 8 - Факт 1, 9 - Факт 2\n"
                         "Коды также указаны в вашей карточке игрока")

    if chat_id in games:
        game = games[chat_id]
        if Player.is_master(message):
            if len(game.get_all_player_cards()) != 0:
                        shuffle = select_command(number)
                        if game.shuffle_characteristic(shuffle):
                            game.send_player_cards()
                            bot.send_message(message.chat.id, f"Характеристика '{shuffle}' была перемешана в карточках всех игроков.\n\n"
                                                              f" Пожалуйста введите /play, чтобы обновить вашу карту")
                        else:
                            bot.send_message(message.chat.id, f"Ошибка при перемешивании характеристики.")
            else:
                bot.send_message(message.chat.id,
                                 "В игре нет игроков, каждому участнику игры необходимо ввести команду /play")
        else:
            bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")
    else:
        bot.send_message(message.chat.id, "Вы не начали игру, введите /game")

@bot.message_handler(commands=['swap'])
def swap_characteristic(message):
    chat_id = message.chat.id
    try:
        command, player_number1, player_number2, char_number = message.text.split(maxsplit=3)
        player_number1 = int(player_number1)
        player_number2 = int(player_number2)
        char_number = int(char_number)
    except ValueError:
        bot.send_message(
            chat_id,
            "Введите команду, номер первого игрока, номер второго игрока и номер характеристики после неё, например: /swap 1 2 5"
        )
        return

    if chat_id in games:
        game = games[chat_id]
        char = select_command(char_number)
        if game.swap_characteristic(player_number1, player_number2, char):
            bot.send_message(
                chat_id,
                f"Характеристика {char} игроков {player_number1} и {player_number2} была успешно обменена."
            )
            players = [game.get_player_card(player_number1), game.get_player_card(player_number2)]
            for player in players:
                if player:
                    player_id = player.user_id
                    game.show_card(message, player_id)
        else:
            bot.send_message(chat_id, "Ошибка при обмене характеристики. Убедитесь, что корректно ввели команду, обмен должен происходить между игроками чья разница в номерах равна одному.")
    else:
        bot.send_message(chat_id, "Вы не начали игру, введите /game")

@bot.message_handler(commands=['ch_cata'])
def change_cata(message):
    chat_id = message.chat.id
    if Player.is_master(message):
        game = games[chat_id]
        if chat_id in games:
            game.change_catastrophes()
            _catastrophes = game.game_data['catastrophes']
            mes = "\n\n"
            bot.send_message(message.chat.id, f"Ваша новая катастрофа:\n\n{mes.join(_catastrophes)}")

        else:
            bot.send_message(message.chat.id, "Вы не начали игру, введите /game")

    else:
        bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")

@bot.message_handler(commands=['end'])
def delete(message):
    if Player.is_master(message):
        chat_id = message.chat.id
        if chat_id in games:
            game = games[chat_id]
            winners = [player.number for player in game.get_all_player_cards().values() if not player.is_ban()]
            if winners:
                winners_text = "Номера победивших игроков:\n"
                for number in winners:
                    winners_text += f"{number} "
                bot.send_message(message.chat.id, winners_text)
            else:
                bot.send_message(message.chat.id, "Никто не победил.")

            game.end_game()
            games.pop(chat_id)
            bot.send_message(message.chat.id, "Игра окончена")
        else:
            bot.send_message(message.chat.id, "Вы не начали игру, введите /game")

    else:
        bot.send_message(message.chat.id, "Команда доступна только ведущему (администратору чата)")


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
