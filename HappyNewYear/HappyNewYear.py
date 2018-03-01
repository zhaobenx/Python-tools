import json

import sys
import os

from time import sleep

import wxpy


class Greeting:

    def __init__(self, name, puid,  greeting='{name}新年快乐！狗年大吉！'):
        self.name = name
        self.puid = puid
        self._greeting = greeting

    def toJSON(self):
        # return str(self.__dict__)
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, ensure_ascii=False)

    def items(self):
        return {
            'name': self.name,
            'puid': self.puid,
            'greeting': self._greeting
        }

    @property
    def greeting(self):
        return self._greeting.format(name=self.name)


class Greetings(list):
    """docstring for Greetings."""

    def __init__(self):
        super(Greetings, self).__init__()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.items(),
                          sort_keys=True, indent=4, ensure_ascii=False)

    def fromJSON(self, json_object):
        self.clear()
        greetings = json.loads(json_object)
        for g in greetings:
            self.append(Greeting(**g))


def send_greeting(bot: wxpy.Bot, greeting: Greeting):
    people = wxpy.ensure_one(bot.friends().search(puid=greeting.puid))
    print("Sending {} to {}……".format(people.name, greeting.greeting))
    people.send(greeting.greeting)


def test():
    g = Greetings()
    g.append(Greeting('赵奔', '123', ''))
    g.append(Greeting('赵奔2', '232', '', '{}hao'))

    json_object = g.toJSON()
    # print(json_object)
    g.fromJSON(json_object)
    # print(g.toJSON())
    return g


def show_help():
    print('Usage:')
    print(os.path.basename(__file__), end=' ')
    print('[list] [send]')
    print('''  list\tgenerate friends list and keep that you want to send
  send\tsend message to those friends
    ''')


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    if ('list' not in sys.argv) and ('send' not in sys.argv):
        show_help()
        sys.exit(1)

    bot = wxpy.Bot(cache_path=True, console_qr=False)
    bot.enable_puid()

    if 'list' in sys.argv:
        greetings = Greetings()

        for friend in bot.friends():
            greetings.append(
                Greeting(
                    name=friend.name,
                    puid=friend.puid,
                )
            )

        with open('friends.json', 'w', encoding='utf8') as f:
            f.write(greetings.toJSON())

    if 'send' in sys.argv:
        greetings = Greetings()
        with open('friends.json', encoding='utf8') as f:
            greetings.fromJSON(f.read())
        for i in greetings:
            try:
                send_greeting(bot, i)
            except Exception as e:
                print(e)
            sleep(0.5)
    wxpy.embed()


if __name__ == "__main__":
    main()
