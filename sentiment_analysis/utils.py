import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import requests
import json
import itertools
import regex as re
from googletrans import Translator
import aspect_based_sentiment_analysis as absa
import spacy

recognizer = absa.aux_models.BasicPatternRecognizer()
nlp_absa = absa.load(pattern_recognizer=recognizer)
nlp_lg = spacy.load('en_core_web_lg')

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

def teencode(path='https://raw.githubusercontent.com/dinhgiangltk/stored_data/main/text_data/teencode.txt') -> pd.DataFrame:
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

    def trim_text(self, text:str = None):
        if text == None:
            text = self.TEXT
        _trim = re.sub(' +', ' ', text)
        return _trim

    def truncate_first_words(self, text:str = None, separator=' ', threshold=400):
        if text == None:
            text = self.TEXT

        if len(text) <= threshold:
            return text
        else:
            return text[:threshold].rsplit(separator, maxsplit=1)[0]

    def words_tokenized(self, text:str = None):
        if text == None:
            text = self.TEXT
        _lowercase = ''
        if text != None and text != float('nan'):
            _newline = re.sub('\n', '. ', text)
            _sub_re = re.sub('[^\p{L}0-9.,() ]', '', _newline)
            _trim = self.trim_text(_sub_re)
            _lowercase = _trim.lower()
            for n in [3,2,1]:
                teencodes_meanings = self.teencode_replace(_lowercase, n)
                teencodes = teencodes_meanings.keys()
                for teencode in teencodes:
                    _lowercase = _lowercase.replace(teencode, teencodes_meanings[teencode])
        return _lowercase

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

    def nouns_extraction(self, text = None):
        if text == None:
            text = self.TEXT

        if isinstance(text, str):
            doc = nlp_lg(text)
            nps = [token.lemma_ for token in doc if token.pos_ == 'NOUN']
            return self.unique_list(nps)
        else:
            return []

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