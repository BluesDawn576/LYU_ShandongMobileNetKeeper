from win10toast_persist import ToastNotifier


def show(text, title):
    toaster = ToastNotifier()
    toaster.show_toast(
        title,
        text,
        icon_path=None,
        duration=None
    )
