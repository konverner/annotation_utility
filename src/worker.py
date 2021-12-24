import os
import collections

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

    def upload(self,PATH_TXT,PATH_DIR):
        name2label = dict()
        f = open(PATH_TXT, 'r', encoding='utf-8')
        txt = f.read()
        lines = txt.split('\n')
        for line in lines:
            try:
                name2label[PATH_DIR + '\\' + line.split('\t')[0]] = line.split('\t')[1]
            except:
                print("ERROR (bad line):",line)

        name2label = collections.OrderedDict(sorted(name2label.items()))

        self.name2label = list(name2label.items())
        self.first = self.name2label[0]
        self.N = len(self.name2label)
        f.close()
        return len(name2label)

    def save(self,PATH_TXT,PATH_DIR):
        counter = 0
        file_txt = open(PATH_TXT,'w')
        the_last = self.name2label[-1]
        for item in self.name2label:
            if item != None:
                counter += 1
                if item != the_last:
                    path = item[0]
                    path = path.replace(PATH_DIR,'')
                    try:
                        file_txt.write((path[1:]+'\t'+item[1]+'\n').encode('utf-8',"ignore").decode())
                    except:
                        print("ERROR:",item[1])
        path = the_last[0].replace(PATH_DIR,'')
        file_txt.write((path[1:]+'\t'+the_last[1]).encode('utf-8',"ignore").decode())
        file_txt.close()
        counter += 1
        return counter

    def next(self):
        self.current += 1
        if self.current >= len(self.name2label):
            self.current = 0
        while self.name2label[self.current] == None:
            print('skip',self.current)
            self.current += 1
        print('next:',self.name2label[self.current])
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

    def update(self,name,new_label):
        print('udpate:', name, new_label)
        for i in range(len(self.name2label)):
            if self.name2label[i] != None:
                if self.name2label[i][0] == name:
                    self.name2label[i] = list(self.name2label[i])
                    self.name2label[i][1] = new_label
                    self.name2label[i] = tuple(self.name2label[i])