import json
import random

class FlashCards():
    def __init__(self, path_to_file: str):
        with open(path_to_file, 'r', encoding='utf-8') as input_file:
            self.pairs = json.load(input_file)
        self.words = []
        for k in self.pairs.keys():
            self.words.append(k)
        '''
        Прочитает пары слов из указанного файла в формате json. 
        Создаст все требующиеся атрибуты.  
        '''
        pass

    def play(self) -> str:
        ready = []
        if len(self.words) == 0:
            print ('Dictionary is empty!')
        else:
            i = 0
            correct = 0
            while i < len(self.words):
                question = random.choice(self.words)
                if question not in ready:
                    i += 1
                    ready.append(question)
                    input_request = question + '\n'
                    answer = input(input_request)
                    if self.pairs.get(question) == answer.lower():
                        correct += 1
            all_words = len(self.words)
            print ('Done! {} of {} words correct!'.format(str(correct), str(all_words)))
        '''
        Выдает русские слова из словаря в рандомном порядке, 
        сверяет введенный пользователем перевод с правильным 
        (регистр введенного слова при этом не важен), 
        пока слова в словаре не закончатся. 
        Возвращает строку с количеством правильных ответов/общим количеством 
        слов в словаре (см пример работы). 
        '''

    def add_word(self, russian: str, english: str) -> str:
        new_word = {russian: english}
        if russian not in self.words:
            self.pairs.update(new_word)
            self.words.append(russian)
            print ("Succesfully added word '{}'.".format(russian))
        else:
            print("'{}' already in dictionary.".format(russian))
        '''
        Добавляет в словарь новую пару слов, 
        если русского слова еще нет в словаре.
        Возвращает строку в зависимоти от результата (см пример работы). 
        '''

    def delete_word(self, russian: str) -> str:
        if russian in self.words:
            self.pairs.pop(russian)
            print("Succesfully deleted word '{}'.".format(russian))
            self.words = []
            for k in self.pairs.keys():
                self.words.append(k)
        else:
            print("'{}' not in dictionary.".format(russian))
        '''
        Удаляет из словаря введенное русское слово
        и соответсвующее ему английское. 
        Возвращает строку в зависимоти от результата (см пример работы). 
        '''
