from tkinter import Tk
import time
import json

import urllib.request

import keyboard


class WordsRecord:

    def __init__(self):
        with open("words.txt", 'a', encoding='utf8') as f:
            f.write(time.strftime("\n\"%Y-%m-%d\":", time.localtime()) + '\n')
        self.root = Tk()
        self.root.withdraw()
        #keyboard.add_hotkey('alt+r', self.read_clip, trigger_on_release=True)
        keyboard.on_press_key('f9', self.read_clip)
        self.root.mainloop()

    def read_clip(self, *args):
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
            print("\a",end="")
            with open("words.txt", 'a', encoding='utf8') as f:
                f.write("- " + new)
                meanings, ipa = self.search_meaning(new)
                if meanings or ipa:
                    f.write(":\n")
                else:
                    f.write("\n")
                if ipa:
                    f.write("  - [" + ipa + "]\n")
                    
                if meanings:
                    for meaning in meanings.splitlines():
                        f.write("  - " + meaning + "\n")

                print(new)
                # print(self.search_meaning(new))
        # self.root.clipboard_clear()

    @staticmethod
    def search_meaning(words):

        # TODO：Add IPA and meaning
        # use this api：
        # url = "http://dict.youdao.com/jsonapi?xmlVersion=5.1&client=&q={0}&dicts={{\"count\":1,\"dicts\":[[\"ec\",\"simple\"]]}}"
        url = "http://dict.youdao.com/jsonapi?xmlVersion=5.1&client=&q={0}"

        # url = 'http://dict.youdao.com/suggest?q={}&num=1&doctype=json'
        # print(url.format(words))
        request = urllib.request.Request(url.format(words))
        request.add_header('content-type', 'application/json')
        request.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0')
        try:
            response = urllib.request.urlopen(request).read().decode('utf8')
        except:
            print("network error")
            return "", ""
        json_content = json.loads(response)
        # print(json_content)
        # if json_content.get('result').get('code') != 200:
        #     return ''
        # else:
        #     return json_content.get('data').get('entries')[0].get('explain')

        meaning = ""
        ipa = ""
        # print(json_content)
        if json_content.get("ec"):
            for i in json_content.get("ec").get("word")[0].get("trs"):
                meaning += WordsRecord.get_deep_meaning(i) + '\n'
                # print(i)
            ipa = json_content.get("simple").get("word")[0].get("usphone")

        return meaning, ipa

    @staticmethod
    def get_deep_meaning(dict_object):
        if isinstance(dict_object, dict):
            # print(dict_object.values()[0])
            return WordsRecord.get_deep_meaning(list(dict_object.values())[0])
        elif isinstance(dict_object, list):
            return WordsRecord.get_deep_meaning(dict_object[0])
        else:
            return dict_object


if __name__ == "__main__":
    print("Select the word and press F9 to save the words")
    print("Note: this may affect your clipboard")
    word_record = WordsRecord()
