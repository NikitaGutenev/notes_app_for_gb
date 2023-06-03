import datetime
import json



class Note:
    __id = []
    def __new__(cls):
        if len(cls.__id) == 0:
            cls.__id.append(1)
        else:
            cls.__id.append(cls.__id[-1]+1)
        return super().__new__(cls)

    def __init__(self):
        self.id = self.get_id()
        self.date = None
    
    @classmethod
    def get_id(cls):
        return cls.__id[-1]
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self,d):
        self._data = d

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self,t):
        self._title = t


class ListNotes:
    def __init__(self):
        self.notes = {}

    def edit(self):
        id = ''
        while not id.isdigit():
            id = input('''Введите id заметки которую хотите изменить либо print для вывода всех заметок в буффере
            Ваш выбор: ''')
            if id == 'print':
                self.print()
        note = self.notes[int(id)]
        choose = input(
        '''Что вы хотите изменить?
        0 - заголовок
        1 - тело заметки
        2 - всю заметку(и заголовок и тело)
        Любой другой символ - если хотите выйти без изменений
        Ваш выбор: ''')
        if choose == '0':
            print(f'Ваш текущий заголовок:\n{note.title}')
            tmp = note.title
            note.title = input('Введите новый(если хотите отменить,то введите 9): ')
            if note.title == '9':
                note.title = tmp
        elif choose == '1':
            print(f'Ваши текущие записи:\n{note.data}')
            tmp = note.data
            note.data = input('Введите новые записи(если хотите отменить,то введите 9): ')
            if note.data == '9':
                note.data = tmp
        elif choose == '2':
            print(f'Ваша текущая заметка:\n{note.title}\n{note.data}')
            tmp = (note.title,note.data)
            note.title = input('Введите новый заголовок(если хотите отменить,то введите 9): ')
            if note.title == '9':
                note.title = tmp[0]
            note.data = input('Введите новые записи(если хотите отменить,то введите 9): ')
            if note.data == '9':
                note.data = tmp[1]
        else:
            print('Выход без изменений...')
        if choose in ('0','1','2'):
            note.date = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")

    def add(self):
        tmp = Note()
        tmp.title = input('Введите заголовок: ')
        tmp.data = input('Введите тело заметки: ')
        tmp.date = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        self.notes[tmp.id] = tmp
        print('Заметка сохранена')

    def rm(self):
        id = ''
        while not id.isdigit():
            if id != 'print' and id != '':
                print('Выход без изменений...')
                return
            id = input('''Введите id заметки которую хотите удалить 
            либо print для вывода всех заметок в буффере
            либо другой символ чтобы выйти без изменений
            Ваш выбор: ''')
            if id == 'print':
                self.print()
        return self.notes.pop(id:=int(id),f'Заметка №{id} не найдена')
    
    def output(self):
        mode = None
        mode = input('''Вы хотите добавить в файл новые заметки или полностью перезаписать файл?
        (будут внесены только текущие заметки. Какие именно - команда print)
        1 - добавить
        0 - перезаписать
        print - посмотреть текущие заметки\nВаш выбор: ''')
        while mode not in ('1','0'):
            mode = input('''Вы хотите добавить в файл новые заметки или полностью перезаписать файл?
        (будут внесены только текущие заметки. Какие именно - команда print)
        1 - добавить
        0 - перезаписать
        print - посмотреть текущие заметки\nВаш выбор: ''')
            if mode == 'print':
                self.print()
        out = {}
        for i in self.notes.items():
            c = i[1]
            out[i[0]]={'id':c.id,
                       'Заголовок':c.title,
                       'Тело':c.data,
                       'Последнее изменение':c.date,
                       'Ссылка на объект': f'{c}'}
        if int(mode):
            mode = 'a'
        else:
            mode = 'w'

        with open('NOTES.json',f'{mode}+',encoding='UTF-8') as dt:
            res = []
            if mode == 'a':
                try:
                    tmp = json.loads(dt)
                    res.append(tmp)
                except:
                    pass
            open('NOTES.json','w').close()
            res.append(out)
            json.dump(res,dt,ensure_ascii=False,indent=4)
            
        
    def input(self):
        with open('NOTES.json','r',encoding='UTF-8') as dt:
            item = json.load(dt)
            for i in item:
                for _,j in i.items():
                    print('-------------')
                    for k in j.items():
                        print(f'{k[0]} - {k[1]}')

    def print(self):
        if len(self.notes)>0:
            for item in self.notes.items():
                print('----------------------')
                print(f'id:{item[0]}')
                print(item[1].title)
                print(item[1].data)
                print(f'Последняя дата изменения: {item[1].date}')
                print('----------------------\n')
        else:
            print('Ваш список заметок пустой')
        
    def clear(self):
        tmp = input('   вы уверены что хотите удалить ВСЕ заметки?\n1 - да\n0 - нет\nВаш выбор: ')
        if tmp:
            open('NOTES.json','w').close()
        else:
            print('Вы ничего не удалили')


def commands():
    print('''Доступные команды:
    add - создать заметку
    edit - редактировать заметку
    rm - удалить заметку
    ex - отправить все ваши заметки в json файл
    im - вывести в консоль все заметки из json файла
    clear - очистить json файл
    print - вывести все ваши заметки в консоль
    cmd - показать доступные команды
    exit - закрыть приложение "Заметки"''')


prog = True
print('Здравствуйте! Это приложение "Заметки"\n Чтобы показать список команд - введите cmd')
List = ListNotes()
while prog:
    print('Введите команду: ')
    tmp = input()
    match tmp:
        case 'add':
            List.add()
        case 'edit':
            List.edit()
        case 'rm':
            List.rm()
        case 'ex':
            List.output()
        case 'im':
            List.input()
            print('-------------')
        case 'clear':
            List.clear()
        case 'print':
            List.print()
        case 'cmd':
            commands()
        case 'exit':
            prog = False
        case _:
            print('Неверная команда')
print('Пока-пока))')