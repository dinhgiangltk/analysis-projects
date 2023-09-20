import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import requests
import json
import itertools
import regex as re
from googletrans import Translator
import aspect_based_sentiment_analysis as absa

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk import RegexpParser
from nltk import Tree
import pandas as pd

# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
chunker = RegexpParser(NP)

recognizer = absa.aux_models.BasicPatternRecognizer()
nlp_absa = absa.load(pattern_recognizer=recognizer)

def classify_noun(word):
    synsets = wordnet.synsets(word)
    
    if not synsets:
        return "Unknown"
    
    synset = synsets[0]
    if synset.pos() == "n":
        return "Concrete noun"
    elif synset.pos() == "s":
        return "Abstract noun"
    else:
        return "Unknown"

class data_scraping():
    def __init__(self, url_hotel:str, max_reviews = 1000, reviews_per_page = 10) -> None:
        self.URL_HOTEL = url_hotel
        self.HOTEL_ID = self.URL_HOTEL.split('/')[-1].split('-')[-1]
        self.URL_REVIEWS = 'https://www.traveloka.com/api/v2/hotel/getHotelReviews'
        self.SESSION = requests.Session()
        self.MAX_REVIEWS = max_reviews
        self.REVIEWS_PER_PAGE =  reviews_per_page
        self.MAX_PAGES = (self.MAX_REVIEWS // self.REVIEWS_PER_PAGE) + 1
        self.HEADERS = {
            'content-type': 'application/json',
            'origin': 'https://www.traveloka.com',
            'user-agent': 'Chrome/115.0.0.0',
            'x-domain': 'accomContent'
            }
    
    def get_cookie(self):
        req = self.SESSION.get(self.URL_HOTEL)
        cookie = dict(req.headers)['Set-Cookie'].replace(', tv', ';tv')
        return cookie
    
    def get_top_reviews(self, top, skip):
        self.HEADERS['cookie'] = self.get_cookie()
        payload = json.dumps({
            "fields": [],
            "data": {
                "filterSortSpec": {
                    "travelTheme": None,
                    "travelType": None,
                    "sortType": "HELPFULNESS",
                    "tagIds": []
                },
                "hotelReviewFilterClientSpec": {
                    "hasPhotos": False
                },
                "hotelReviewSortClientSpec": {
                    "sortType": "HELPFULNESS"
                },
                "ascending": True,
                "reviewLanguage": "ENGLISH",
                "hotelId": self.HOTEL_ID,
                "skip": skip,
                "top": top
            },
            "clientInterface": "desktop"
        })
        req = self.SESSION.post(url=self.URL_REVIEWS, headers=self.HEADERS, data=payload)
        data = req.json()
        
        return data

    def get_all_reviews(self):
        data_list = []
        for page in range(self.MAX_PAGES):
            top = self.REVIEWS_PER_PAGE
            skip = page*top
            try:
                data = self.get_top_reviews(top=top, skip=skip)
                data_list += data['data']['reviewList']
            except:
                break
        
        df = pd.DataFrame(data_list)
        return df

def teencode(path='data_teencode.txt') -> pd.DataFrame:
    df = pd.read_csv(path, delimiter='\t', header = None, names = ['teencode', 'meaning'])
    return df

TEENCODE = teencode()

class absa_english_text():
    def __init__(self, text:str) -> None:
        self.TEXT = text

    def teencode_replace(self, text:str = None, n=3):
        if text == None:
            text = self.TEXT
        iterable = text.split(' ')                                                      
        iters = itertools.tee(iterable, n)                                                     
        for i, it in enumerate(iters):                                               
            next(itertools.islice(it, i, i), None)                                               
        
        teencode = TEENCODE
        result = map(lambda x: (' '.join(x), teencode[teencode.teencode==' '.join(x)].meaning.iloc[0]),
                    filter(lambda gr: None not in gr and ' '.join(gr) in list(teencode.teencode), itertools.zip_longest(*iters))
                    )
        return dict(result)

    def truncate_first_words(self, text:str = None, separator=' ', threshold=400):
        if text == None:
            text = self.TEXT

        if len(text) <= threshold:
            return text
        else:
            return text[:threshold].rsplit(separator, maxsplit=1)[0]

    def words_tokenized(self, text:str = None, teencode_replaced=True):
        if text == None:
            text = self.TEXT
        
        tokenized = ''
        if text != None and text != float('nan'):
            tokenized = text
            tokenized = re.sub('\n', '. ', tokenized) # remove new lines
            tokenized = re.sub('[^\p{L}0-9.,() ]', '', tokenized) # remove not ascii characters
            tokenized = re.sub(r'(?<=[.,])(?=[^\s])', r' ', tokenized) # add space after dot or comma
            tokenized = re.sub(' +', ' ', tokenized) # remove consecutive spaces

        if teencode_replaced:
            tokenized = tokenized.lower()
            for n in [3,2,1]:
                teencodes_meanings = self.teencode_replace(tokenized, n)
                teencodes = teencodes_meanings.keys()
                for teencode in teencodes:
                    tokenized = tokenized.replace(teencode, teencodes_meanings[teencode])
                    
        return tokenized

    def translate_vi_to_en(self, text:str = None):
        if text == None:
            text = self.TEXT
        translator = Translator()
        try:
            translated = translator.translate(text, dest = 'en').text
        except:
            translated = ''
        return translated
    
    def unique_list(self, items:list):
        ls = []
        for item in items:
            if item not in ls:
                ls.append(item)
        return ls

    def nouns_extraction(self, text:str = None, chunk_func=chunker.parse):
        if text == None:
            text = self.TEXT

        chunked = chunk_func(pos_tag(word_tokenize(text)))
        continuous_chunk = []
        current_chunk = []
        text_np_removed = text

        for subtree in chunked:
            if type(subtree) == Tree:
                current_chunk.append(" ".join([token for token, _ in subtree.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    text_np_removed = text_np_removed.replace(named_entity, '')
                    current_chunk = []
            else:
                continue

        chunks = pos_tag(word_tokenize(text_np_removed))
        for token, pos in chunks:
            if pos in ('NN','NNS'):
                if token not in continuous_chunk:
                    continuous_chunk.append(token)
        
        return continuous_chunk

    def absa_by_np(self, text = None):
        if text == None:
            text = self.TEXT
        aspects = self.nouns_extraction(text)
        if len(aspects) > 0:
            completed_task = nlp_absa(text=text, aspects=aspects)
            sentiment_list = [{
                    'text':text,
                    'aspect':np.aspect,
                    'sentiment':np.sentiment.name,
                    'neu_score':np.scores[0],
                    'neg_score':np.scores[1],
                    'pos_score':np.scores[2],
                } 
                for np in completed_task.examples
            ]
            return sentiment_list
        else:
            return []