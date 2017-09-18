from tkinter import Tk
import time
import json

import urllib.request

import keyboard


class WordsRecord:

    def __init__(self):
        with open("words.txt", 'a', encoding='utf8') as f:
            f.write(time.strftime("\"%Y-%m-%d\":", time.localtime()) + '\n')
        self.root = Tk()
        self.root.withdraw()
        #keyboard.add_hotkey('alt+r', self.read_clip, trigger_on_release=True)
        keyboard.hook_key('f9', self.read_clip)
        self.root.mainloop()

    def read_clip(self):
        # self.root.clipboard_clear()
        time.sleep(0.3)
        keyboard.send('ctrl+c')
        # keyboard.wait('c')
        time.sleep(0.1)
        try:
            new = self.root.clipboard_get()
        except:
            print('error')
        else:
            with open("words.txt", 'a', encoding='utf8') as f:
                f.write("- " + new)
                meaning = self.search_meaning(new)
                if meaning:
                    f.write(":\n  - " + meaning)
                f.write('\n')
                print(new)
                # print(self.search_meaning(new))
        # self.root.clipboard_clear()

    def search_meaning(self, words):
        url = 'http://dict.youdao.com/suggest?q={}&num=1&doctype=json'
        request = urllib.request.Request(url.format(words))
        request.add_header('content-type', 'application/json')
        request.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0')

        response = urllib.request.urlopen(request).read().decode('utf8')
        json_content = json.loads(response)
        # print(json_content)
        if json_content.get('result').get('code') != 200:
            return ''
        else:
            return json_content.get('data').get('entries')[0].get('explain')


if __name__ == "__main__":
    print("Select the word and press F9 to save the words")
    print("Note: this may affect your clipboard")
    word_record = WordsRecord()
