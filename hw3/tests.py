import unittest
from flash_cards import FlashCards

class FlashCardsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = FlashCards('input_file.json')

    def test_add_new_word(self):
        ideal_words = ['яблоко', 'хурма', 'банан']
        self.app.add_word('банан','banana')
        self.assertEqual(ideal_words, self.app.words)

    def test_add_old_word(self):
        ideal_words = ['яблоко', 'хурма']
        self.app.add_word('яблоко','apple')
        self.assertEqual(ideal_words, self.app.words)

    def test_delete_new_word(self):
        ideal_words = ['яблоко', 'хурма']
        self.app.delete_word('апельсин')
        self.assertEqual(ideal_words, self.app.words)

    def test_delete_old_word(self):
        ideal_words = ['яблоко']
        self.app.delete_word('хурма')
        self.assertEqual(ideal_words, self.app.words)

if __name__ == '__main__':
    unittest.main()
