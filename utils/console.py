import eel


def log(text):
    print(text)
    eel.log(text)


def alert(text, title, and_print=False):
    if and_print:
        eel.log(text)
    eel.alert(text, title)
