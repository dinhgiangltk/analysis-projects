import pandas as pd
import requests
import json

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