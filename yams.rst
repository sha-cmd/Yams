                                
================================
 Swapping Words With Python GUI 
================================

This program is set to manipulate words in phrases so as to transform them in a way that it is in disorder but still readable by a human brain. In fact, the first and the last letter of the words are preserved. This seems unorthodox but as long as the first and the last letter stay the same in a word, the brain can predict the right word, whatever its letters order.
Here is a short presentation of Yams, my program to transform a phrase.
Coded in Python with Tkinter module, it is also released in version 0.01, for Windows Systems, the source code is on GitHub.

The application presents two texts frames and a swap action button, that transforms the text.


 Class Diagram 
---------------

@startuml
'https://plantuml.com/class-diagram

class tkinter.Button
class tkinter.Frame
class tkinter.Label
class tkinter.Tk
class Application
interface LabelInput
class SwappedText
class Text

tkinter.Tk <|-- Application
tkinter.Frame <|-- Text
tkinter.Frame <|-- SwappedText
tkinter.Frame <|-- LabelInput

Application --* Text
Application --* SwappedText
Application --* tkinter.Button
Application --o tkinter.Label

LabelInput o-- Text
LabelInput o-- SwappedText

object Application {
class tkinter.Label
class SwappedText
class Text
class tkinter.Button
{method} on_click()
}

interface LabelInput {
class tkinter.Label
{method} grid()
{method} get()
{method} set()
}

class Text {
Collection: class LabelInput
String {method} get()
String {method} reset()
}

class SwappedText {
Collection: class LabelInput
String {method} get()
void {method} reset(String)
void {method} swap(String)
}

@enduml


 The swap function 
-------------------

This function takes the string written in the text frame. When the swap button is clicked, then the swap function makes its actions to return a new swapped string in the swapped text frame.

 Activity Diagram 
------------------

@startuml
'https://plantuml.com/activity-diagram-beta

start
:tkinter.Button.on_click();
:swap(string: String);
if (string lenght <= 1) then (true)

else (false)
    :finditer non-word chars;
    :save their
{index:value};
    :replace non-word
chars by a space;
    :finditer words
of 4 chars;
    :swap middle
letters in words;
    :replace non-word chars
at the right index position;

endif
:return the string;
stop

@enduml


Code of swap function
---------------------

def swap(self, string):
        if len(string) <= 1:
            return string
        x_W = finditer("\W", string)
        dict_W = {}
        it = 0
        for l in x_W:
            dict_W[l.span()[0]] = string[l.span()[0]:l.span()[1]]
            it += 1
        x_w = finditer("\w+", string)
        dict_w = {}
        it = 0
        for l in x_w:
            dict_w[l.span()[0]] = string[l.span()[0]:l.span()[1]]
            it += 1
        sample_word = []
        for it in range(len(string)):
            try:
                if dict_w[it]:
                    if len(dict_w[it]) >= 3:
                        value = ''.join(sample(dict_w[it][1:-1], len(dict_w[it][1:-1])))
                        original = dict_w[it][1:-1]
                        if len(value) >= 2:
                            while value == original:
                                value = ''.join(sample(dict_w[it][1:-1], len(dict_w[it][1:-1])))
                        sample_word.append(dict_w[it][0] + value + dict_w[it][-1])
                    else:
                        sample_word.append(dict_w[it])
            except KeyError:
                pass
            try:
                if len(dict_W[it]) < 3:
                    sample_word.append(dict_W[it])
            except KeyError:
                continue
        return ''.join(sample_word)


 Conclusion 
------------

You can found this program at this page https://github.com/sha-cmd/Yams on GitHub. There is also a setup file for installing it on Windows.

Romain BOYRIE

