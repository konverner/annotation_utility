"""
Class for handling data: switch, remove, change, etc.
"""
import collections
from yaspeller import check

class Worker:
    def __init__(self):
        self.name2label = None
        self.first = None
        self.current = 0
        self.N = None

    def get_curr_idx(self):
        if self.current >= len(self.name2label):
            self.current = 0
        return self.current

    def remove_current(self):
        print('remove:', self.name2label[self.current])
        self.name2label[self.current] = None
        self.current += 1

    def upload(self, PATH_TXT, PATH_DIR):
        name2label = dict()
        f = open(PATH_TXT, 'r', encoding='utf-8')
        txt = f.read()
        lines = txt.split('\n')
        N = len(lines)
        print("THIRD STEP: checking spelling")
        for i,line in enumerate(lines):
            if (i%1000 == 0):
                print(f"[{i}\{N}] labels has been processed")
            try:
                label = line.split('\t')[1]
                PATH = PATH_DIR + '\\' + line.split('\t')[0]
                name2label[PATH] = {'label' : label, 'spelling_ok' : self.spelling_correct(label)}
            except:
                print("ERROR (bad line):", line)
        name2label = collections.OrderedDict(sorted(name2label.items()))

        self.name2label = list(name2label.items())
        self.first = self.name2label[0]
        self.N = len(self.name2label)
        f.close()
        print("END")
        return len(name2label)

    def save(self, PATH_TXT, PATH_DIR):
        counter = 0
        file_txt = open(PATH_TXT, 'w')
        the_last = self.name2label[-1]
        for item in self.name2label:
            if item != None:
                counter += 1
                if item != the_last:
                    path = item[0]
                    path = path.replace(PATH_DIR, '')
                    label = item[1]['label']
                    try:
                        file_txt.write((path[1:]+'\t'+label+'\n').encode('utf-8', "ignore").decode())
                    except:
                        print("ERROR:", label)
        path = the_last[0].replace(PATH_DIR, '')
        file_txt.write((path[1:]+'\t'+the_last[1]['label']).encode('utf-8', "ignore").decode())
        file_txt.close()
        counter += 1
        return counter

    def next(self):
        self.current += 1
        if self.current >= len(self.name2label):
            self.current = 0
        while self.name2label[self.current] == None:
            print('skip', self.current)
            self.current += 1
        print('next:', self.name2label[self.current][0], self.name2label[self.current][1]['label'])
        return self.name2label[self.current]

    def get_current(self):
        while self.name2label[self.current] == None:
            self.current += 1
        return self.name2label[self.current]

    def previous(self):
        self.current -= 1
        if self.current < 0:
            self.current = len(self.name2label) - 1
        while self.name2label[self.current] == None:
            print('skip', self.current)
            self.current -= 1
        return self.name2label[self.current]

    def update(self, name, new_label):
        print('udpate:', name, new_label)
        for i in range(len(self.name2label)):
            if self.name2label[i] != None:
                if self.name2label[i][0] == name:
                    self.name2label[i] = list(self.name2label[i])
                    self.name2label[i][1]['label'] = new_label
                    self.name2label[i][1]['spelling_ok'] = self.spelling_correct(new_label)
                    self.name2label[i] = tuple(self.name2label[i])

    # check spelling of phrase
    def spelling_correct(self, phrase, lang='ru'):
        phrase = phrase.strip()
        if '-' not in phrase and phrase != '':
            res = check(phrase, lang=lang)
            return res.is_ok
        return True