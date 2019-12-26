import nltk
import pymorphy2
from nltk.stem import WordNetLemmatizer 

class Sentence:
    """
    Class for sentence in English or Russian
    """
    
    def __init__(self, sentence):
        """
        Constructor
        """
        self.sentence = sentence

    def get_words(self):
        from nltk.tokenize import RegexpTokenizer
        """
        Getting words
        """
        tokenizer = RegexpTokenizer(r'\w+')
        words_regexp = tokenizer.tokenize(self.sentence)
        return words_regexp
    

    def check_affirm(self):
        """
        Checking if affirmative
        """
        length = len(self.sentence)
        if self.sentence[length - 1] == '!':
            sentence_type = 'Exclamation'
        elif self.sentence[length - 1] == '?':
            sentence_type = 'Question'
        else:
            sentence_type = 'Affirmation'
        return sentence_type
                

    def __del__(self, name = 'sentence'):
        """
        Destructor
        """
        print('Destructor called, %s deleted!' % self.name)

class RussianSentence(Sentence):
    
    def get_lemmas(self):
        """
        Getting lemmas
        """
        morph = pymorphy2.MorphAnalyzer()
        text = self.get_words()
        lemmas = []
        for word in text:
            p = morph.parse(word)[0]
            lemmas.append(p.normal_form)
        return lemmas

    def get_pos(self, pos):
        """
        Getting all the words of given POS.
        
        Possible POS:
        NOUN
        ADJF
        ADJS
        COMP
        VERB
        INFN
        PRTF
        PRTS
        GRND
        NUMR
        ADVB
        NPRO
        PRED
        CONJ
        PRCL
        INTJ
        
        More info about tags on
        https://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
        """
        morph = pymorphy2.MorphAnalyzer()
        text = self.get_words()
        word_with_pos = {}
        for word in text:
            p = morph.parse(word)[0]
            word_with_pos[word]=p.tag.POS
        pos_output = []
        for key, val in word_with_pos.items():
            if val == pos:
                pos_output.append(key)
        return pos_output

class EnglishSentence(Sentence):
    
    def get_lemmas(self):
        """
        Getting lemmas
        """
        lemmatizer = WordNetLemmatizer()
        text = self.get_words()
        lemmas = []
        for word in text:
            p = lemmatizer.lemmatize(word)
            lemmas.append(p)
        return lemmas

    def get_pos(self, pos):
        """
        Getting all the words of given POS.
        
        POS tag list:
        CC coordinating conjunction
        CD cardinal digit
        DT determiner
        EX existential there (like: "there is" ... think of it like "there exists")
        FW foreign word
        IN preposition/subordinating conjunction
        JJ adjective 'big'
        JJR adjective, comparative 'bigger'
        JJS adjective, superlative 'biggest'
        LS list marker 1)
        MD modal could, will
        NN noun, singular 'desk'
        NNS noun plural 'desks'
        NNP proper noun, singular 'Harrison'
        NNPS proper noun, plural 'Americans'
        PDT predeterminer 'all the kids'
        POS possessive ending parent's
        PRP personal pronoun I, he, she
        PRP$ possessive pronoun my, his, hers
        RB adverb very, silently,
        RBR adverb, comparative better
        RBS adverb, superlative best
        RP particle give up
        TO to go 'to' the store.
        UH interjection errrrrrrrm
        VB verb, base form take
        VBD verb, past tense took
        VBG verb, gerund/present participle taking
        VBN verb, past participle taken
        VBP verb, sing. present, non-3d take
        VBZ verb, 3rd person sing. present takes
        WDT wh-determiner which
        WP wh-pronoun who, what
        WP$ possessive wh-pronoun whose
        WRB wh-abverb where, when
        """
        text = self.get_words()
        word_with_pos = nltk.pos_tag(text)
        pos_output = []
        for word in word_with_pos:
            if word[1] == pos:
                pos_output.append(word[0])
        return pos_output

help(Sentence)
help(RussianSentence)
help(EnglishSentence)
