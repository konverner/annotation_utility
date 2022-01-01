"""
Functions for data synchronization
"""
import os
import collections


def tsv_to_dict(PATH_TXT):
    name2label = dict()
    print(PATH_TXT)
    txt = open(r'{}'.format(PATH_TXT), 'r',encoding="ISO-8859-1").read()
    lines = txt.split('\n')
    for line in lines:
        try:
            name2label[line.split('\t')[0]] = line.split('\t')[1]
        except:
            print('ERROR (bad line):',line)
            pass

    name2label = collections.OrderedDict(sorted(name2label.items()))

    return name2label

def make_match(PATH_DIR, PATH_TXT,format=None):

    name2label = tsv_to_dict(PATH_TXT)

    files_removed = 0
    labels_removed = 0


    # number of files in directory
    N = len([name for name in os.listdir(PATH_DIR)])
    # number of labels in csv file
    M = len(name2label)

    count = 0

    print("FIRST STEP")
    for f in os.listdir(PATH_DIR):
        count += 1
        if count%1000 == 0:
            print(f"[{count}\{N}] files has been processed")

        remove = True
        for name in name2label.keys():
            if name == f:
                remove = False
        if remove:
            os.remove(PATH_DIR + '\\' + f)
            files_removed += 1
    new_name2label = dict()

    count = 0
    print("SECOND STEP")
    for name in name2label.keys():
        count += 1
        if count % 1000 == 0:
            print(f"[{count}\{M}] labels has been processed")
        remove = True
        for f in os.listdir(PATH_DIR):
            if name == f:
                remove = False
        if not remove:
            new_name2label[name] = name2label[name]
        else:
            labels_removed += 1

    file_txt = open(PATH_TXT,'w',encoding="ISO-8859-1")
    the_last = list(new_name2label.items())[-1]
    for item in new_name2label.items():
        if item != the_last:
            file_txt.write(item[0]+'\t'+item[1]+'\n')
    file_txt.write(the_last[0]+'\t'+the_last[1])
    file_txt.close()

    print(f'\nfiles removed: {files_removed}\nlabels removed {labels_removed}')

def rename_batch(PATH_IMAGES,PATH_LABELS,new_name,extension='png'):
    name2label = tsv_to_dict(PATH_LABELS)
    file_txt = open(PATH_LABELS, 'w',encoding="ISO-8859-1")
    new_name2label = dict()
    csv_content = open(PATH_LABELS,'r',encoding="ISO-8859-1").read()
    csv_file = open(PATH_LABELS,'w')

    index = 0

    for f in os.listdir(PATH_DIR):
        for name in name2label.keys():
            if name == f:
                os.rename(PATH_IMAGES + f, PATH_IMAGES + new_name + str(index) + '.' + extension)
                new_name2label[new_name+str(index)+'.'+extension] = name2label[name]
                index += 1

    the_last = list(new_name2label.items())[-1]
    for item in new_name2label.items():
        if item != the_last:
            file_txt.write(item[0]+'    '+item[1]+'\n')
    file_txt.write(the_last[0]+'    '+the_last[1])
    file_txt.close()

    csv_file.write(csv_content)
    csv_file.close()

    print('{} images have been renamed'.format(index))
