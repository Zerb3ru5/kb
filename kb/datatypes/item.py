from datetime import date, datetime


class Item:

    def __init__(self, id, title, type, value, categories, parent):

        self.id = id
        self.title = title
        self.categories = categories
        self.type = type
        self.value = value
        self.parent = parent

        self.date = date.today().strftime('%d.%m.%Y')
        self.time = datetime.now().strftime('%H:%M:%S')
        self.author = 'me'
