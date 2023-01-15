import tkinter as tk
from random import sample
from re import finditer
from tkinter import ttk


class LabelInput(tk.Frame):
    def __init__(self, parent, label='', input_class=ttk.Entry,
                 input_var=None, input_args=None, label_args=None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)
        self.error = getattr(self.input, 'error', tk.StringVar())
        self.error_label = ttk.Label(self, textvariable=self.error)
        self.error_label.grid(row=2, column=0, sticky=(tk.W + tk.E))

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            return ''

    def set(self, value, *args, **kwargs):
        if self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)


class Text(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.inputs = {'Text': LabelInput(
            self, "Text",
            input_class=tk.Text,
            input_args={"width": 75, "height": 10}
        )}
        self.inputs['Text'].grid(sticky="w", row=0, column=0)
        self.reset()

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        notes = self.inputs['Text'].get()
        self.inputs['Text'].set(notes)
        return notes


class SwappedText(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.inputs = {'Swapped': LabelInput(
            self, "Swapped",
            input_class=tk.Text,
            input_args={"width": 75, "height": 10}
        )}
        self.inputs['Swapped'].grid(sticky="w", row=0, column=0)
        self.reset('')

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self, notes_fct):
        Swapped = self.swap(notes_fct)
        self.inputs['Swapped'].set(Swapped)

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


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Swapping Text")
        self.resizable(width=True, height=True)

        ttk.Label(
            self,
            text="Swapping Text",
            font=("TkDefaultFont", 16)
        ).grid(row=0)

        self.recordframe = Text(self)
        self.recordframe.grid(row=1, padx=10)

        self.savebutton = ttk.Button(self, text="Swap", command=self.on_click)
        self.savebutton.grid(sticky="e", row=2, padx=10)

        self.swappedrecordframe = SwappedText(self)
        self.swappedrecordframe.grid(row=3, padx=10)

    def on_click(self):
        notes = self.recordframe.reset()
        self.swappedrecordframe.reset(notes)


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
