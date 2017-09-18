from tkinter import Tk
import time

import keyboard


class WordsRecord:

    def __init__(self):
        with open("words.txt", 'a', encoding='utf8') as f:
            f.write(time.strftime("%Y-%m-%d:", time.localtime())+'\n')
        self.root = Tk()
        self.root.withdraw()
        #keyboard.add_hotkey('alt+r', self.read_clip, trigger_on_release=True)
        keyboard.hook_key('f9',self.read_clip)
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
                f.write("  "+new + '\n')
                print(new)
        # self.root.clipboard_clear()

if __name__ == "__main__":
    print("Select the word and press F9 to save the words")
    print("Note: this may affect your clipboard")
    word_record = WordsRecord()
