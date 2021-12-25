## Annotation Utility

GUI program that facilitates annotation of image data 

## Running



## Usage

<img src="https://github.com/conwerner/annotation_utility/blob/main/images/interface.png" width="324" height="324">

fields:

img dir : path to the directory with images

labels : path to the \*.tsv file with annotations

buttons:

save : save current changes

upload : upload images and labels into the program

remove : remove a image from the directory and the correspondent label in \*.csv file

next : the next pair (image, label)

previous : the previous pair (image, label)

hot keys:

*shift + left arrow* : previous

*shift + right arrow* : next

*shift + space* : remove

## Get started

Prepare a directory with images. For, example,

<img src="https://github.com/conwerner/annotation_utility/blob/main/images/interface3.png" width="512" height="200">

Prepare a \*.tvs document with the list of image files. For, example

```
pe10.png	
pe1000.png	наз-ся
pe10001.png	то есть
pe10003.png	смещение
pe10005.png	движения
pe10008.png	Ищем
pe1001.png	равномерно
pe10015.png	
pe1002.png	наиболее
pe10024.png	больших
pe10026.png	чему ещё
```

the second column is an annotation, it can be empty
