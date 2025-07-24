import requests
import time
import random
import uuid
import re
import json
import httpx
from lxml import html
import urllib.parse
from datetime import datetime,timedelta
from unidecode import unidecode
from parsel import Selector
from urllib.parse import urlparse, urlunparse
from ..schemas.search_schemas import CrawlerPostItem

USER_AGENTS = [
    # Chrome desktop
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",

    # Firefox desktop
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",

    # Edge desktop
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36 Edg/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36 Edg/120.0",

    # Mobile Android
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Mi 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Mobile Safari/537.36",

    # Mobile iOS Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",

    # Mobile iOS Chrome
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.116 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.109 Mobile/15E148 Safari/604.1",

    # Android Firefox
    "Mozilla/5.0 (Android 12; Mobile; rv:110.0) Gecko/110.0 Firefox/110.0"
]

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
def formatTimestamp(timestamp):
        datetime = time.strftime(DATETIME_FORMAT, time.localtime(int(timestamp)))
        return datetime
def replace_ig_host(url: str) -> str:
    u = urlparse(url)
    new_netloc = "scontent.cdninstagram.com"
    u = u._replace(netloc=new_netloc)
    return urlunparse(u)

def get_data_post_hastag_ig_recent(res,keyword):
        data=res['node']
        try:
            post_id=data['shortcode']
            url_post="https://www.instagram.com/p/"+post_id
        except:
            post_id=''
            url_post=''
        try:
            message=data['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            message=''
        try:
            post_image=replace_ig_host(data['display_url'])
        except:
            post_image=''
        try:
            post_created_timestamp=data['taken_at_timestamp']
            post_created=formatTimestamp(post_created_timestamp)
        except:
            post_created=formatTimestamp(1748937706)
            post_created_timestamp=1748937706
        try:
            like_count=data['edge_liked_by']['count']
        except:
            like_count=0
        try:
            comment_count=data['edge_media_to_comment']["count"]
        except:
            comment_count=0
        try:
            # url=url_post+"/embed"
            # response =  requests.get(url)
            # tree = html.fromstring(response.content)
            # # ✅ Lấy username
            # author_username = tree.xpath('//a[contains(@class, "Username")]/span/text()')
            # author_username = author_username[0] if author_username else None

            # # ✅ Lấy avatar URL
            # author_image = tree.xpath('//div[contains(@class, "AvatarContainer")]//img/@src')
            # author_image = author_image[0] if author_image else None
            author_username=''
            author_image=''
            author_id=''
        except Exception as e:
            author_username=''
            author_image=''
            author_id=''
            raise e
            
        try:
            author_id=data['owner']['id']
        except:
            author_id=''
        #Object Item
        item = CrawlerPostItem(
            post_id=post_id,
            post_type="instagram",
            post_keyword=keyword,
            post_url=url_post,
            message=message,
            type=0,
            post_image=post_image,
            post_created=post_created,
            post_created_timestamp=post_created_timestamp,
            post_raw="",
            count_like=like_count,
            count_share=0,
            count_comments=comment_count,
            comments="",
            brand_id="",
            object_id="",
            service_id="",
            parent_post_id="",
            parent_object_id="",
            parent_service_id="",
            page_id="",
            page_name="",
            author_id=author_id,
            author_name=author_username,
            author_username=author_username,
            author_image=author_image,
            data_form_source=0,
        )
        return item

async def get_request_data_instagram( keyword: str )  -> list[CrawlerPostItem]:
    """
    Fetch data from a given URL with optional parameters.
    
    :keyword: The keyword to fetch data from instagram.
    :return: Response object containing the fetched data.
    """
    keyword = unidecode(keyword).replace(" ", "").lower()
    user_agent = random.choice(USER_AGENTS)
    try:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "dpr": "1",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
            "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"138.0.7204.158\", \"Microsoft Edge\";v=\"138.0.3351.95\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"10.0.0\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": user_agent,
            "viewport-width": "1150"
        }

        cookies = {
            "datr": "FH0uaE9jzr2zLPSntS6XVb6y",
            "ig_did": "48AD0009-93BC-4E50-BA2B-33B54567EDFC",
            "ig_nrcb": "1",
            "fbm_124024574287414": "base_domain=.instagram.com",
            "ps_l": "1",
            "ps_n": "1",
            "ig_lang": "vi",
            "fbsr_124024574287414": "m8RX1dYSpPgjGzoAH5HLhR786cizwGWtLpeROZjj3Pk.eyJ1c2VyX2lkIjoiMTAwMDAyODI0Njc4NTA4IiwiY29kZSI6IkFRQnFGRWthdUJVcUl0Mm5COS1uSGpWNFlGTjE5NEpnM3lLb2xCQjU0elcwSXB3VnJlZG53TkVMcWxVenRUZUFKeEYtdTRmNmpaY0lkSzFKMWZoSjVxVU9SQXYwSC1pMVRrdWRLa2VWZkdMX0VEWnBxODF5a0ttWEZRXzctdGkzdHczanZFYUFUUkJidWgtUVI3TWdsdjhnMmFhVHREaG5QVTNYRUI2MzVteVVQeFJjTlkxZWFzVDlZVWNtdXRtQVZ5WFYtUktNcGpPcG1sbFQtUTFwczZkS09seUdJOVJBNjZrZjdTaG9CS0tFelI1dF9fQjVxU0NSS3NjY3QtV2RYZVVDczBCYlpGRUxzLVJoYW9tUkNLUUtjZTdhWm05eFJyQVBFYWZHeEtjSkwxb2NOb0owWDQ2Z0FnLVIzQ3B1VHpFIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCUEZ0dzB6MEs0U1Y3cnhtdGlPUmRESFBGQVpDWFdKQU5GZDNENnFaQTZHUkdaQmF1VVBmVmpmVlVEazRXUzNYWkNPQm03Y1FKamRTbURFSEJveTB1a251NDAwOGh3OFdtajBYNWhXaVd2UnFIWkM0VFlFZTFTUjR6VHR6eW1SN1JaQm9ubjdoWkFwNkFPOGVmYnN4N2FLbHNFQ3psdzdxbGFNU2kwakNBeUNZUEZXd0ZhWkNyZTc3bjFWc2c5ZHk2TG9zYXlQbmZINFFhN214c1pCcGNaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzUzMjU3NjE0fQ",
            "ds_user_id": "58448736471",
            "mid": "aBrbfwALAAH1NWVE7cTEg4yVEsQc",
            "dpr": "1",
            "csrftoken": "CUEbi6MWe2To1WElGSRr59thsBzxNMAm",
            "sessionid": "58448736471%3AAZp34uzqvIWt4H%3A10%3AAYdFUF0NoU5Gx7dhAfxxayRXFAH6QRtHO_-jin0eBA",
            "wd": "1150x932",
            "rur": "\"HIL\\05458448736471\\0541784866071:01fed3895ddf732e879aeee12902518d7d031f74e202f2d474a630efd23105395497db8e\""
        }
        #url_rq =f"https://www.instagram.com/graphql/query/?query_hash=9b498c08113f1e09617a1703c22b2f32&variables=%7B%22tag_name%22%3A%22{keyword}%22%2C%22first%22%3A24%2C%22after%22%3Anull%7D"
        url_rq = f'https://www.instagram.com/graphql/query/?query_hash=9b498c08113f1e09617a1703c22b2f32&variables=%7B%22tag_name%22%3A%22{keyword}%22%2C%22first%22%3A24%2C%22after%22%3Anull%7D'
        print("Crawl Instagram")
        response = requests.get(url=url_rq, headers=headers, cookies=cookies)
        #print(response.text)
        if response.status_code != 200  :  # Raise an error for bad responses
            print(f"[ERROR] Failed to fetch data from Instagram: {response.status_code}")
            return [],str(response.status_code)
        data_res = json.loads(response.text)
        #print(data_res)
        try:
            list_post=data_res['data']['hashtag']['edge_hashtag_to_media']['edges']
        except:
            list_post=[]
        
        if not list_post:
            print
            return [],str(response.status_code)
        list_post_res = []
        for post in list_post:       
            item = get_data_post_hastag_ig_recent(post,keyword)
            list_post_res.append(item)
        print("list_post_res")
        print(len(list_post_res))
        return list_post_res,str(response.status_code)
    except requests.RequestException as e:
        raise Exception(f"Error fetching data from instagram: {str(e)}")

def get_data_user_ig(res,keyword):
        data=res['user']
        try:
            post_id=data['username']
            url_post="https://www.instagram.com/"+post_id
        except:
            post_id=''
            url_post=''
        try:
            message=data['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            message=''
        try:
            post_image=replace_ig_host(data['display_url'])
        except:
            post_image=''
        try:
            post_created_timestamp=data['taken_at_timestamp']
            post_created=formatTimestamp(post_created_timestamp)
        except:
            post_created=formatTimestamp(1748937706)
            post_created_timestamp=1748937706
        try:
            like_count=data['edge_liked_by']['count']
        except:
            like_count=0
        try:
            comment_count=data['edge_media_to_comment']["count"]
        except:
            comment_count=0
        try:
            # url=url_post+"/embed"
            # response =  requests.get(url)
            # tree = html.fromstring(response.content)
            # # ✅ Lấy username
            # author_username = tree.xpath('//a[contains(@class, "Username")]/span/text()')
            # author_username = author_username[0] if author_username else None

            # # ✅ Lấy avatar URL
            # author_image = tree.xpath('//div[contains(@class, "AvatarContainer")]//img/@src')
            # author_image = author_image[0] if author_image else None
            author_username=''
            author_image=''
            author_id=''
        except Exception as e:
            author_username=''
            author_image=''
            author_id=''
            raise e
            
        try:
            author_id=data['pk']
        except:
            author_id=''
        #Object Item
        item = CrawlerPostItem(
            post_id=post_id,
            post_type="instagram",
            post_keyword=keyword,
            post_url=url_post,
            message=message,
            type=0,
            post_image=post_image,
            post_created=post_created,
            post_created_timestamp=post_created_timestamp,
            post_raw="",
            count_like=like_count,
            count_share=0,
            count_comments=comment_count,
            comments="",
            brand_id="",
            object_id="",
            service_id="",
            parent_post_id="",
            parent_object_id="",
            parent_service_id="",
            page_id="",
            page_name="",
            author_id=author_id,
            author_name=author_username,
            author_username=author_username,
            author_image=author_image,
            data_form_source=0,
        )
        return item


async def get_request_user_profile_instagram( keyword: str )  -> list[CrawlerPostItem]:
    """
    Fetch data from a given URL with optional parameters.
    
    :keyword: The keyword to fetch data from instagram.
    :return: Response object containing the fetched data.
    """
    #keyword = unidecode(keyword).replace(" ", "").lower()
    user_agent = random.choice(USER_AGENTS)
    try:
        url = "https://www.instagram.com/graphql/query"
        headers = {
            "accept": "*/*",
            "accept-language": "vi,en-US;q=0.9,en;q=0.8,fr-FR;q=0.7,fr;q=0.6",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.instagram.com",
            "priority": "u=1, i",
            "referer": "https://www.instagram.com/hdsaisonfinancevn/",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "sec-ch-ua-full-version-list": "\"Chromium\";v=\"136.0.7103.154\", \"Google Chrome\";v=\"136.0.7103.154\", \"Not.A/Brand\";v=\"99.0.0.0\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"10.0.0\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": user_agent,
            "x-asbd-id": "359341",
            "x-bloks-version-id": "b029e4bcdab3e79d470ee0a83b0cbf57b9473dab4bc96d64c3780b7980436e7a",
            "x-csrftoken": "CUEbi6MWe2To1WElGSRr59thsBzxNMAm",
            "x-fb-friendly-name": "PolarisProfilePostsTabContentQuery_connection",
            "x-fb-lsd": "yelNJ0Yn0p_QnffS677ugb",
            "x-ig-app-id": "936619743392459",
            "x-root-field-name": "xdt_api__v1__feed__user_timeline_graphql_connection"
        }


        cookies = {
                    "ig_nrcb": "1",
                    "ig_did": "48AD0009-93BC-4E50-BA2B-33B54567EDFC",
                    "mid": "aBrbfwALAAH1NWVE7cTEg4yVEsQc",
                    "datr": "YFcIaNU0Vt8W6cCT755Js56V",
                    "fbm_124024574287414": "base_domain=.instagram.com",
                    "csrftoken": "CUEbi6MWe2To1WElGSRr59thsBzxNMAm",
                    "ds_user_id": "58448736471",
                    "ps_l": "1",
                    "ps_n": "1",
                    "sessionid": "74122845781%3AaGelD550sc1k5H%3A18%3AAYcO-thLzGyqENkixatK7U1ErHmG2WVdscqVjzfZoA",
                    "wd": "851x778",
                    "rur": "\"HIL\\05458448736471\\0541782263402:01fe4bbc47bf5290a5de153875f0c524bfb546bcea10b2e93908ded3810d2f9f0dc74f85\""
        }
        
        body = 'av=17841458334146092&__d=www&__user=0&__a=1&__req=13&__hs=20279.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1024608489&__s=al53u2%3Avem5lm%3A6p3xd2&__hsi=7525342165906477118&__dyn=7xeUjG1mxu1syUbFp41twWwIxu13wvoKewSAwHwNw9G2S7o2vwpUe8hw2nVE4W0qa0FE2awgo9oO0n24oaEnxO1ywOwv89k2C1Fwc60AEC1TwQzXwae4UaEW2G0AEco5G1Wxfxm16wUwtE1wEbUGdG1QwTU9UaQ0z8c86-3u2WE5B08-269wr86C1mgcEed6goK2O4Xxui2qi7E5y4UrwHwGwa6byohw4rxO7EG3a&__csr=iMoWn2IpMRqMh5RbsBmj6cZeViYWBQGy4WFpOK8Gv8dl2nlmilfyJeVaAHCFvSturiWmEx24XgCRCo_BKmjHQWDiF5ChutF2q-4FUOaDxh2Q4Ehjx68BAGAurGiiTRhaAAzoy49fKeLDuiUV4zUrVApe4p8B3pBBUiz9VUtAx54xaqt5DCHngy00lkOXwtStwbkwfy0qo1uU45wj88E4upa0oy42K8gG0J20OwcG0TE0TK1Aw1NA8wxU4Cu1Uw58ws4m8Bsw3jwPwBA9849U6Ol1502ZEx2Fm1Gxa0qqp015S00wxE0RC02WC&__hsdp=gePX95TT2D36PaALqkbxvLH8D4h2E2j2Dshd4EMxAkx2eimAgjKgOAhpPsB5wmm7ln6xaeyUrzkfIkEroVx3wmEG22R8dzEaoRFe8Dwru6bwn8AiUeo8U4a2Gu7rw-yUB6UfEcUkwfiu0wo1yU3rw5Zxe0FU8E9o9U3ywkoa8461Pwba0GP0_g2wg8o621Yw-wfy2e1HUwS2W&__hblp=0kpEW2C1hxq7XAQ68O1MyUhyV8oxG0DEd8tGcLxnxKXyQ7odk5p9EGucCzomhV8jzpoiAKAUNbDAx62WcUoKcyF43WUvDwxWxqvwPKWLAwyiAK6rDwIVVF8CuawRx916dxi0xEcoa8iDxG10wBw45yE7G0LotwlonG0w87N4hUjw9a58W4U9p88E9UO0HodUpwEwYAwsU2ewzwiEG1lc227A1uwg7xOErwh4789EdVUdEkgnwyxe7t0seexi2l0CgOfUwSE99Eiw&__sjsp=gePX95-T2D36PaALqkbxvLH8D4h2E2j2DshdPEMxAkx229qh4iUlwzwukr5xa3qdg-NixJwaGQ&__comet_req=7&fb_dtsg=NAft7f1PKnxMVSUcCPmJz3WqD8k24SapIWCdPnISYWNbnuv0I3jMCBQ%3A17843676607167008%3A1747877953&jazoest=26196&lsd=B8K0DxfdDOgtIkJ5oWgCmY&__spin_r=1024608489&__spin_b=trunk&__spin_t=1752130260&__crn=comet.igweb.PolarisFeedRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisSearchBoxRefetchableQuery&variables=%7B%22data%22%3A%7B%22context%22%3A%22blended%22%2C%22include_reel%22%3A%22true%22%2C%22query%22%3A%22'+keyword+'%22%2C%22rank_token%22%3A%22%22%2C%22search_session_id%22%3A%229e9878b4-f0f1-4f3a-ac99-7816ae24bbe5%22%2C%22search_surface%22%3A%22user%22%7D%2C%22hasQuery%22%3Atrue%7D&server_timestamps=false&doc_id=9523870587735596'

       
        response = requests.get(url=url, headers=headers, cookies=cookies,data=body)
        #print(response.text)
        if response.status_code != 200  :  # Raise an error for bad responses
            print(f"[ERROR] Failed to fetch user data from Instagram: {response.status_code}")
            return [],str(response.status_code)
        data_res = json.loads(response.text)
        #print(data_res)
        try:
            list_user=data_res['data']['xdt_api__v1__fbsearch__topsearch_connection']['users']
        except:
            list_user=[]
        
        if not list_user:
            print
            return [],str(response.status_code)
        list_post_res = []
        for post in list_user:       
            item = get_data_user_ig(post,keyword)
            list_post_res.append(item)
        print("list_post_res")
        print(len(list_post_res))
        return list_post_res,str(response.status_code)
    except requests.RequestException as e:
        raise Exception(f"Error fetching data from instagram: {str(e)}")




def handle_parse_data_threads(item_post,keyword):
    content_created = datetime.fromtimestamp(item_post["taken_at"]).strftime(
                                DATETIME_FORMAT)
    try:
        username =item_post["user"]["username"]
    except:
        username=''
    try:
        message =item_post["caption"]["text"]
    except:
        message = ""
    try:
        post_image = replace_ig_host(item_post["image_versions2"]["candidates"][0]["url"])
    except:
        post_image = ""
    item = CrawlerPostItem(
            post_id=item_post["code"],
            post_type="threads",
            post_keyword=keyword,
            post_url="https://www.threads.com/@hourlytna/post/" + item_post["code"],
            message=message,
            type=0,
            post_image= post_image,
            post_created=content_created,
            post_created_timestamp=item_post["taken_at"],
            post_raw="",
            count_like=item_post["like_count"],
            count_share=item_post["text_post_app_info"]["repost_count"],
            count_comments=item_post["text_post_app_info"]["reshare_count"],
            comments="",
            brand_id="",
            object_id="",
            service_id="",
            parent_post_id="",
            parent_object_id="",
            parent_service_id="",
            page_id="",
            page_name="",
            author_id=item_post["user"]["pk"],
            author_name=username,
            author_username=username,
            author_image=item_post["user"]["profile_pic_url"],
            data_form_source=0,
        )
    return item

async def get_request_data_threads( keyword: str )  -> list[CrawlerPostItem]:
    user_agent = random.choice(USER_AGENTS)
    url = f"https://www.threads.com/search?q={keyword}&serp_type=default&filter=recent"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi',
        'cache-control': 'max-age=0',
        'dpr': '1',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.158", "Microsoft Edge";v="138.0.3351.95"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent,
        'viewport-width': '1216',
        'x-csrftoken': 'bxnPHzr0MtAMBOhKY9aH5UrrTmCM1klF',
        }
    cookies = {
        'csrftoken': 'bxnPHzr0MtAMBOhKY9aH5UrrTmCM1klF',
        'sessionid': '63394927242%3AJDmvNYQQKoPZCB%3A17%3AAYeLbeEfVZCsdSi-lJ-Bwd7G1AURHsfrJvJUHVtcsQ',
        'ig_did': 'A4D874AA-7ECF-4A7B-A059-052619E4D90D',
        'mid': 'aHyWcAALAAHf-l_l_LAN5z3lb_4o',
        'ps_l': '1',
        'ps_n': '1'
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, cookies=cookies)
        #resp.raise_for_status()
    print(f"INFO:{str(resp.status_code)}")
    if resp.status_code != 200:
        print(f"[ERROR] Failed to fetch data from Threads: {resp.status_code}")
        return [],str(resp.status_code)
    sel = Selector(text=resp.text)
    data_threads = sel.xpath(".//script[@type='application/json']/text()").getall()
    list_post_res = []
    for data in data_threads:
        try:
            if "searchResults" in data and "thread_items" in data:
                data_json = json.loads(data)
                with open("threads.json", "w", encoding="utf-8") as f:
                    json.dump(data_json, f, ensure_ascii=False, indent=4)
                data_posts = \
                    data_json["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]["data"][
                        "searchResults"]["edges"]
                for post in data_posts:
                        item_post = post["node"]["thread"]["thread_items"][0]["post"]
                        item = handle_parse_data_threads(item_post, keyword)
                        list_post_res.append(item)

        except json.JSONDecodeError:
            continue

    if not list_post_res:
        return [],str(resp.status_code)
    return list_post_res,str(resp.status_code)

def tweet_id_to_timestamp(tweet_id: int) -> int:
    """
    Convert Twitter Snowflake ID (tweet ID) to Unix timestamp (in seconds).
    """
    twitter_epoch = 1288834974657  # in milliseconds
    timestamp_ms = (tweet_id >> 22) + twitter_epoch
    return timestamp_ms // 1000  # convert to seconds

def tweet_id_to_datetime_str(tweet_id: int) -> str:
    """
    Convert Twitter Snowflake ID (tweet ID) to datetime string in '%Y-%m-%d %H:%M:%S' format.
    """
    twitter_epoch = 1288834974657  # in milliseconds
    timestamp_ms = (tweet_id >> 22) + twitter_epoch
    dt = datetime.utcfromtimestamp(timestamp_ms / 1000)
    return dt.strftime(DATETIME_FORMAT)

def handle_parse_data_x(entry,keyword):
    tweet_info = entry['content']['itemContent']['tweet_results']['result']
    legacy = tweet_info.get('legacy', {})
    user_data = tweet_info.get('core', {}).get('user_results', {}).get('result', {})
    user_info = user_data.get('core', {})
    try:
        tweet_id = tweet_info['rest_id']
    except KeyError:
        tweet_id = ''
    tweet_text = legacy.get('full_text') or legacy.get('text') or ''
    like_count = legacy.get('favorite_count', 0)
    reply_count = legacy.get('reply_count', 0)
    retweet_count = legacy.get('retweet_count', 0)
    

    author_username = user_info.get('screen_name', '')
    author_name = user_info.get('name', '')
    author_id = user_data.get('rest_id', '')
    profile_image = user_data.get('avatar', {}).get('image_url', '')
    try:
        post_image = entry['media']['media_url_https']
    except KeyError:
        post_image = ''
    # Convert thời gian
    created_at = tweet_id_to_timestamp(tweet_id)
    timeFormatStr = tweet_id_to_datetime_str(tweet_id)
    item = CrawlerPostItem(
            post_id=tweet_id,
            post_type="x",
            post_keyword=keyword,
            post_url="https://x.com/avaloonhoot/status/" + tweet_id,
            message=tweet_text,
            type=0,
            post_image= post_image,
            post_created=timeFormatStr,
            post_created_timestamp=created_at,
            post_raw="",
            count_like=like_count,
            count_share=retweet_count,
            count_comments=reply_count,
            comments="",
            brand_id="",
            object_id="",
            service_id="",
            parent_post_id="",
            parent_object_id="",
            parent_service_id="",
            page_id="",
            page_name="",
            author_id=author_id,
            author_name=author_name,
            author_username=author_username,
            author_image=profile_image,
            data_form_source=0,
        )
    return item

async def get_request_data_x( keyword: str )  -> list[CrawlerPostItem]:
    user_agent = random.choice(USER_AGENTS)
    url = f"https://x.com/i/api/graphql/9jF8Lh7Kh_Wr956PRIJcdg/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{keyword}%22%2C%22count%22%3A40%2C%22cursor%22%3A%22DAADDAABCgABGwSjG_yawZgKAAIbBKKTBBsAKwAIAAIAAAABCAADAAAAAAgABAAAAAAKAAUbBKMdpcAnEAoABhsEox2lv9jwAAA%22%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22rweb_video_screen_enabled%22%3Afalse%2C%22payments_enabled%22%3Afalse%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22responsive_web_grok_analyze_button_fetch_trends_enabled%22%3Afalse%2C%22responsive_web_grok_analyze_post_followups_enabled%22%3Atrue%2C%22responsive_web_jetfuel_frame%22%3Atrue%2C%22responsive_web_grok_share_attachment_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22responsive_web_grok_show_grok_translated_post%22%3Afalse%2C%22responsive_web_grok_analysis_button_from_backend%22%3Atrue%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_grok_image_annotation_enabled%22%3Atrue%2C%22responsive_web_grok_community_note_auto_translation_is_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    headers = {
        "accept": "*/*",
        "accept-language": "vi,en-US;q=0.9,en;q=0.8",
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "content-type": "application/json",
        "priority": "u=1, i",
        "referer": "https://x.com/search?q=vietnam&src=typed_query&f=live",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user_agent,
        "x-client-transaction-id": "3mc7q6k9MMaJ9OL0xaXCMVO951+S+jJwtFMfsvbIBncGQKsWR0/d/r21z6RYUnNbG/SR89obFA+V3KwPa6yRF5ypAiew3Q",
        "x-csrf-token": "8227e304a4c8d7b67a49777dabd639e9fb59ea00494792613175684683686d50880456acb7341e0c6b4c52573f9f9b4325cbcde92daf00f05e784530337a843fbbab49bfcdbdd378fb4ecaeb76101e04",
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "x-xp-forwarded-for": "aa7b2f4ccb1da3595c042e672d6ca25afc83079df38c5ad6bc6a8453945421ea5fc96b16a935e4c7da2ab207f2296dbcc05bbf4c7221264aea78ee8db4f266f037c8811e3352ad6a860f11579a7994d42ceb35974c6c5a66805f01c99ecc154899b1a4c53958d396a053fb8af10f1db55580113e225de56233af24676db0b44fb326b0b43ed64686980a8a23bd25de924643702f0fe776b016fa26ea5fbdda0064d8e19fa215dbd7f3dc99e68ac2aeb78ef8346f4609c892809a5b960b3e7234f594d62d70fac00f6d4ff4616258b5c0306dfec03c68f51eb6433cbc3b783720509d73ea6cea1289e2797457d81707a45cd3bcaefe8d18f0444dcbe73560835d8e1fb1fb593ccac08b"
    }

    cookies = {
        "guest_id_marketing": "v1%3A174681123752632959",
        "guest_id_ads": "v1%3A174681123752632959",
        "guest_id": "v1%3A174681123752632959",
        "personalization_id": "\"v1_wv7w0+AjvNlM5v1d/vGacw==\"",
        "g_state": "{\"i_l\":0}",
        "kdt": "pOAodJuPjSPpDEJdSQIaxIgg56lLpNvDcddxzNjO",
        "auth_token": "694f7d6ef78ee0379d91bfe1eac4a97b653ca87b",
        "ct0": "8227e304a4c8d7b67a49777dabd639e9fb59ea00494792613175684683686d50880456acb7341e0c6b4c52573f9f9b4325cbcde92daf00f05e784530337a843fbbab49bfcdbdd378fb4ecaeb76101e04",
        "twid": "u%3D1919969636952768512",
        "dnt": "1",
        "lang": "en",
        "__cf_bm": "O1_pLYXu9smQTxJbuK5YUG4fBGM73XaW0olrPr32q4Q-1753007062-1.0.1.1-9FcosXGNJOypT44G.QOVkdQi.X4Fx8DTysyEqEieyFu50OthkC_48Fjbrh_iXze.w6CigQWQgM0tCnMdR8RwY6SQSaynu..S26JwJqTc.H8"
    }
   
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers,cookies=cookies)
        #resp.raise_for_status()
    if resp.status_code != 200:
        print(f"[ERROR] Failed to fetch data from X: {resp.status_code}")
        return [],str(resp.status_code)
    if resp.status_code == 429:
        print(f"[ERROR] Failed to fetch data from X: {resp.status_code}")
        return [],str(resp.status_code)
    data_res = json.loads(resp.text)
    instructions = data_res['data']['search_by_raw_query']['search_timeline']['timeline']['instructions']
    entries = []
    for ins in instructions:
        if ins.get("type") == "TimelineAddEntries" and "entries" in ins:
            entries = ins["entries"]
            break

    if not entries:
        print("[ERROR] Không tìm thấy entries.")
        return [],str(resp.status_code)
    list_post_res = []
    for entry in entries:
        try:
                    # Bỏ qua nếu không có tweet
            if 'itemContent' not in entry.get('content', {}):
                continue
            item = handle_parse_data_x(entry, keyword)
            list_post_res.append(item)    
        except json.JSONDecodeError:
            continue
    

    if not list_post_res:
        return [],str(resp.status_code)
    return list_post_res,str(resp.status_code)

def decode_id_to_publishtime( video_id):
        try:
            timestamp = int(video_id) >> 32
            content_created = datetime.fromtimestamp(timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            return content_created
        except:
            return ""

async def get_request_data_tiktok( keyword: str )  -> list[CrawlerPostItem]:
    random_did = random.randint(1241242141211411412, 7465151651135121111)
    keyword_new = keyword.replace(" ", "+")
    search_id = str(uuid.uuid4()).replace("-", "").upper()
    url = "https://search22-normal-c-alisg.tiktokv.com/aweme/v1/search/item/?device_platform=android&channel=googleplay&aid=1180&app_name=trill&version_code=390804&device_type=SM-N976N&device_brand=samsung&os_version=12&sys_region=VN&app_language=vi&carrier_region=VN&device_id={}".format(random_did)
    payload = "keyword="+str(keyword_new)+"&offset=0&count=20&source=video_search&is_filter_search=1&sort_type=3&publish_time=1&query_correct_type=1&search_source=tab_search&enter_from=homepage_hot&hot_search=0&sug_generate_type=0&search_id={}".format(search_id)
    headers = {
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "User-Agent": "com.ss.android.ugc.trill/390804 (Linux; U; Android 12; vi_VN; SM-N976N; Build/QP1A.190711.020;tt-ok/3.12.13.20)",
                    "X-Ladon": "5WBiWQCbBW6x4cDqy+pTI9p5JlxI65YvPskne2P3ZJENTPih",
                    "X-Khronos": str(int(time.time())),
                    "X-Gorgon": "84047061000023d04c1888d38d41724be4134855fd9c8c8e67b0",
                    "X-Argus": "eiTARWbMVZ3y7pcESV5FnDpEsDug2ljii/GxXyTh+ty6d+84AVQexob+xVtOJee2ddS+mzP0wMUB5Aid1HN1pl0V645+o7ifjYGcIXYa2VdPg82apbtEKDtCeDKtK+jWjsPNwWDCSK0SJZaylI3X1zslAL3649O7FvUPNxTVuQyqp0719gohkq3ZwkRTNRpfNX4BRUX4ZuA2ZZfgM+CE81ej9AujdYIlJrWI3uUXtAAhqFphD3r0n6traNZYBNFkc33V9FYQJx6FKIVcBqGO5Fv5X0TbgrPuI53iUR542ojbxEgbUZ+rBddtWZui6Ikp3cowpxH4WHdNPsU5obNJ03rn0Yrx1AXk6onYNlnpNLsyIZpxsISLH4rAcEXJRCJd6WUPfLB061tb6LdSlhRuBqZf0wbDRcIUdKm+1us4J3GqZcMiqUfomXx+FCJMvbCsEyf87xu95BaLzPrx1Togf85zFrxM2bZCeQuVkmmTc+btzvml2B/B9NOz9GGNieCHD8Ig8c1VpuZXhyciC1F4Mjqs5agLc8XbUo2NtSIiYc/Er+3dl3La/htlGbgUIQx/YQcLDWU0l8HfwMs1j9EB7P3pHI6/zt2T7YgWBWlYJcEK3sC494LTMUTf1p97oNYlVLPlGptMyCxpDFA7QPCd3jApt5o35LN/RIB6YsBH0tP+jw==",
                    "sdk-version": "2",
                    "Accept-Encoding": "gzip",
                    "X-SS-TC": "0",
                    "X-SS-REQ-TICKET": str(int(time.time() * 1000)),
                    "X-Tt-Trace-Id": str(random.randint(1e18, 9e18)),
                }

    cookies = {
                    "store-idc": "alisg",
                    "odin_tt": "f9c2defc7a38cc5b30e04f847f77759333b13789b9e4ecd4542bd76fa766f00afe76dc8d1e05fcbe77e2cd201e5d235103a3c68ecae34d58421e60c4e3b941f39dcdd07f94d3d96c9edb673beb8ea3eb",
                    "store-country-sign": "MEIEDCzU6FlF0aQMHuIC3AQgfP5bv_JwgINkcRTqIFw7rhr7jgg7l_mvfa8Jba6kbdoEEAIzujdiiCiwPatClxwtdCs",
                    "install_id": "7503837284204119825",
                    "ttreq": "1$6d07694f4412bd6c4bc0af1fc5157ba9bacc355c",
                    "store-country-code": "-"
                }
   
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers,cookies=cookies, data=payload)
        #resp.raise_for_status()
    if resp.status_code != 200:
        print(f"[ERROR] Failed to fetch data from X: {resp.status_code}")
        return [],str(resp.status_code)
    aweme_ids = re.findall(r'"aweme_id":\s*"(\d+)"', resp.text)
    list_post_res = []
    created_at = int(datetime.now().timestamp())
    seen_post_ids = set()
    if aweme_ids:
        for video_id in aweme_ids:
            #print("[INFO] VIDEO ID: " + str(video_id))
            if video_id in seen_post_ids:
                continue
            seen_post_ids.add(video_id)
            content_created = decode_id_to_publishtime(video_id)
            async with httpx.AsyncClient() as client:
                url_detail=f'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@username/video/{video_id}'
                detail_post = await client.get(url_detail, headers=headers,cookies=cookies)
            if detail_post.status_code == 200:
                data_detail = json.loads(detail_post.text)
                item = CrawlerPostItem(
                    post_id=video_id,
                    post_type="tiktok",
                    post_keyword=keyword,
                    post_url="https://www.tiktok.com/@huongnoiivuive/video/" + video_id,
                    message=data_detail.get("title", ""),
                    type=0,
                    post_image= data_detail.get("thumbnail_url", ""),
                    post_created=content_created,
                    post_created_timestamp= int(video_id) >> 32,
                    post_raw="",
                    count_like=0,
                    count_share=0,
                    count_comments=0,
                    comments="",
                    brand_id="",
                    object_id="",
                    service_id="",
                    parent_post_id="",
                    parent_object_id="",
                    parent_service_id="",
                    page_id="",
                    page_name="",
                    author_id=data_detail.get("author_unique_id", ""),
                    author_name=data_detail.get("author_name", ""),
                    author_username=data_detail.get("author_url", "").replace("https://www.tiktok.com/@", ""),
                    author_image=data_detail.get("author_image", ""),
                    data_form_source=0,
                    )
                list_post_res.append(item)
    return list_post_res,str(resp.status_code)

def merge_text_and_first_image(content: list) -> tuple[str, str | None]:
    """
    - Gộp tất cả đoạn text từ content có type = 'text'
    - Trả về thêm một URL ảnh đầu tiên (nếu có type = 'image')
    """
    merged_text = []
    image_url = None

    for item in content:
        if item.get("type") == "text" and "text" in item:
            merged_text.append(item["text"])
        elif item.get("type") == "image" and not image_url:
            media_list = item.get("media", [])
            if media_list:
                # Ưu tiên ảnh lớn nhất (sắp xếp theo width giảm dần)
                sorted_media = sorted(media_list, key=lambda m: m.get("width", 0), reverse=True)
                image_url = sorted_media[0].get("url")

    full_text = "\n".join(merged_text).strip()
    return full_text, image_url

def get_data_post_search_tumblr(post,keyword):
    
    try:
        post_id = post["id"]
    except KeyError:
        post_id = "get_id_error"
    try:
        post_url = post["postUrl"]
    except KeyError:
        post_url = "get_url_error"
    try:
        message,post_image = merge_text_and_first_image(post["content"])
    except KeyError:
        message = "get_message_error"
        post_image = ""
    try:
        post_created_timestamp = post["timestamp"]
        post_created = datetime.fromtimestamp(post_created_timestamp).strftime(DATETIME_FORMAT)
    except:
        post_created = "get_created_error"
        post_created_timestamp = 0
    try:
        count_like = post["likeCount"]   
    except:
        count_like = 0
    try:
        count_share = post["noteCount"]   
    except:
        count_share = 0
    try:
        count_comments=post["replyCount"]   
    except:
        count_comments = 0
    item = CrawlerPostItem(
            post_id=post_id,
            post_type="tumblr",
            post_keyword=keyword,
            post_url=post_url,
            message=message,
            type=0,
            post_image= post_image,
            post_created=post_created,
            post_created_timestamp=post_created_timestamp,
            post_raw="",
            count_like=count_like,
            count_share=count_share,
            count_comments=count_comments,
            comments="",
            brand_id="",
            object_id="",
            service_id="",
            parent_post_id="",
            parent_object_id="",
            parent_service_id="",
            page_id="",
            page_name="",
            author_id='',
            author_name='',
            author_username='',
            author_image='',
            data_form_source=0,
        )
    return item

async def get_request_data_tumblr( keyword: str )  -> list[CrawlerPostItem]:
    """
    Fetch data from a given URL with optional parameters.
    
    :keyword: The keyword to fetch data from instagram.
    :return: Response object containing the fetched data.
    """
    keyword = unidecode(keyword).replace(" ", "").lower()
    user_agent = random.choice(USER_AGENTS)
    try:
        url = f'https://www.tumblr.com/api/v2/timeline/search?limit=20&days=0&query={keyword}&mode=recent&timeline_type=post&skip_component=blog_search&reblog_info=true&query_source=search_box_typed_query&post_role=any&fields%5Bblogs%5D=%3Fadvertiser_name%2C%3Favatar%2C%3Fblog_view_url%2C%3Fcan_be_booped%2C%3Fcan_be_followed%2C%3Fcan_show_badges%2C%3Fdescription_npf%2C%3Ffollowed%2C%3Fis_adult%2C%3Fis_member%2Cname%2C%3Fprimary%2C%3Ftheme%2C%3Ftitle%2C%3Ftumblrmart_accessories%2Curl%2C%3Fuuid%2C%3Fshare_following%2C%3Fshare_likes%2C%3Fask'

        headers = {
            "accept": "application/json;format=camelcase",
            "accept-language": "en-us",
            "authorization": "Bearer aIcXSOoTtqrzR8L8YEIOmBeW94c3FmbSNSWAUbxsny9KKx5VFh",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.tumblr.com/search/vietnam/recent?src=typed_query",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": user_agent,
            "x-ad-blocker-enabled": "0",
            "x-version": "redpop/3/0//redpop/"
        }

        cookies = {
            "tz": "Etc%2FGMT-7",
            "tmgioct": "fc573fbb7a05f52b6decce91",
            "snacc": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImI1MDljNTEzODc2OGY3Y2YyZTgyN2UwNGIyN2U3ZTRjYmM3YmI5MTkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDc0MTQ2MDM2MzAzLW04djEwZDF0ZGt2ZWxndjQybmpyczZwNmxjM3JrMnRjLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTA3NDE0NjAzNjMwMy1tOHYxMGQxdGRrdmVsZ3Y0Mm5qcnM2cDZsYzNyazJ0Yy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMDc2MjcwMjc1MjI3ODE0NzA5MiIsImVtYWlsIjoiaGlldW5rYmJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJnOVhVYm5zNGdxWnhRSmhaNVRWZGpBIiwiaWF0IjoxNzUzMDgxNzA2LCJleHAiOjE3NTMwODUzMDZ9.AAyFC8YDj8eTb2sPAEv0AHgxHo3svvnrziDaznA1VGGEkXofBmq4AaB4fcTDYVpJmKwKIzAr5jG2tc5tGEQDWd4bzQpNXtAKAf5FugrwvLcG2fdaCfYj5uDuH8ONYJkHdgof8Px0Z4lbJ2dfP1KvAyPJBjA3b6XbZzWkC5eyST4ah5H1E2Y3Id43xTF8vqQgrURbkPZak68dQwvgQ424afEll2SBH4u0FC0wP0h4jN5iarrqgGZ1iUjZUMC7S14xz0f1voRaj5D9riqXzIsVgP4CfUvHpetohcrP0VHjm2sP-4Q2zeeq6MSICGVtCJabwAXrDqmueuuB-D19Sl-RsQ",
            "devicePixelRatio": "1",
            "documentWidth": "1897",
            "sid": "aKxjoZcFy97YvW5Zz7FedhwpfKlcUo1TFTFrRASCjin7Ycvm7S.aeAXAtigoAOyOa8Wxbap8jMvE1xlNt7Q7ic1ZA6Tb638EA9Sc6",
            "pfu": "395805680",
            "logged_in": "1",
            "cl_pref": "block",
            "_li_dcdm_c": ".tumblr.com",
            "_lc2_fpi": "ed972f83c03d--01k0nx2g69ztgy5m599kd7jewh",
            "_lc2_fpi_meta": "%7B%22w%22%3A1753081790665%7D",
            "_pubcid": "66a92971-44a9-415d-8e3b-f637f6d5e021",
            "_pubcid_cst": "kSylLAssaw%3D%3D",
            "_lr_retry_request": "true",
            "_lr_env_src_ats": "false",
            "panoramaId_expiry": "1753686596469",
            "_cc_id": "7e7429cf933ecd7a1273dec4af9b513e",
            "panoramaId": "d4fee835470b32418d9701f738304945a7023063e32d3c2057e2c22d096d2b97",
            "pbjs-unifiedid": "%7B%22TDID%22%3A%2284d0f5da-7e3b-4473-92dc-0c53bf8d9dc0%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222025-06-21T07%3A09%3A56%22%7D",
            "pbjs-unifiedid_cst": "kSylLAssaw%3D%3D",
            "cto_bundle": "n8trA18lMkJOVElsa3lGMTdSdVJhVXI3eWNGUFhIbTBLZWQlMkZzVUc3TXhpR3VpTEJENk02WW0lMkZtJTJCczdvQng1VUhJWEFkQUZreG8wMmgwSGNxcGNaaGo3RE1GT1lKelclMkZyeWJGZmg5cXNyR3RjY3ZZb1l4MldZUTFVUnY1bmcxUXREWkRUNzZGWVp6U0hYb1ZvYVlDbTIwayUyRlh4bmclM0QlM0Q",
            "cto_bidid": "qgBrHF9LYnFybkRLTEY0VDlXTFNyNDVjVFVuakhhRUZ3T2xoaHJxRzNDSGt0c3c5d2FrVHZGUlNBRzI5SHBNTnZyJTJGZ24yJTJGVGo1N0tSbTJ6ZlRVc3BNOFFtSCUyQlJ6a2c5VzRCcVZlUmx5bEs4Vkk2dyUzRA",
            "cto_dna_bundle": "3oaWzl9KZHk5NnRxemlGVmZSaDU4c2g4eXdCdyUyQk9Tb29xN0dkUGx4WnNMMWRVbFo2QWQwZGNCc2ZIa0tLWGFQTEhPZ1VmOEIzT2xmQ0hiZ00xdXBsMjBNb2hBJTNEJTNE",
            "search-displayMode": "2",
            "__gads": "ID=9861e47007a9223e:T=1753081798:RT=1753082537:S=ALNI_MY_wqmATYw4j9reraxCtz0W2yfoLg",
            "__gpi": "UID=0000116b2e9c12d6:T=1753081798:RT=1753082537:S=ALNI_MZUOVnUHTfVN2ekRpZ5k2jZuJI3fg",
            "__eoi": "ID=b09c5137c3c1766d:T=1753081798:RT=1753082537:S=AA-Afjbjai6_xgdoTv6u9HxBERxI"
        }

        print(url)
        response = requests.get(url=url, headers=headers, cookies=cookies)
        if response.status_code != 200:  # Raise an error for bad responses
            print(f"[ERROR] Failed to fetch data from tumblr: {response.status_code}")
            return [],str(response.status_code)
        data_res = json.loads(response.text)
        #print(data_res)
        try:
            list_post=data_res['response']['timeline']['elements']
        except:
            list_post=[]
        if not list_post:
            return [],str(response.status_code)
        list_post_res = []
        for post in list_post:       
            item = get_data_post_search_tumblr(post,keyword)
            list_post_res.append(item)
        return list_post_res,str(response.status_code)
    except requests.RequestException as e:
        raise Exception(f"Error fetching data from instagram: {str(e)}")


def convert_id_to_timestamp( _id):
        bin_num = bin(int(_id))[2:]
        first_41_letters = bin_num[:41]
        decimal_num = int(first_41_letters, 2)
        return datetime.fromtimestamp(decimal_num/1000).strftime(DATETIME_FORMAT), int(decimal_num/1000)

def extract_largest_image_url_from_vectorImage(vector_image: dict) -> str:
    artifacts = vector_image.get("artifacts", [])
    root_url = vector_image.get("rootUrl", "")
    
    if not artifacts or not root_url:
        return ""

    # Chọn artifact có width lớn nhất
    largest_artifact = max(artifacts, key=lambda a: a.get("width", 0))
    path_segment = largest_artifact.get("fileIdentifyingUrlPathSegment", "")
    
    return root_url + path_segment if path_segment else ""

def get_data_post_search_linedin(post,keyword):
    metadata = post.get("metadata", {})
    try:
        post_url = metadata["backendUrn"]
        urn_split = post_url.split(":")
        post_id = urn_split[-1]
        post_created,post_created_timestamp = convert_id_to_timestamp(post_id)
    except:
        try:
            post_url = metadata["shareUrn"]
            urn_split = post_url.split(":")
            post_id = urn_split[-1]
            post_created,post_created_timestamp = convert_id_to_timestamp(post_id)
        except:
            post_id = "get_id_error"
            post_url = "get_url_error"
            post_created_timestamp = 0
            post_created = "get_created_error"
 
    try:
        message = post["commentary"]['text']['text']
    except KeyError:
        message = "get_message_error"
    try:
        post_image = extract_largest_image_url_from_vectorImage(post["content"]['articleComponent']['smallImage']['attributes'][0]['detailData']['vectorImage'])
    except:
        post_image = ""
    
    try:
        count_like = 0  
    except:
        count_like = 0
    try:
        count_share = 0  
    except:
        count_share = 0
    try:
        count_comments=0   
    except:
        count_comments = 0
    item = CrawlerPostItem(
            post_id=post_id,
            post_type="linkedin",
            post_keyword=keyword,
            post_url=post_url,
            message=message,
            type=0,
            post_image= post_image,
            post_created=post_created,
            post_created_timestamp=post_created_timestamp,
            post_raw="",
            count_like=count_like,
            count_share=count_share,
            count_comments=count_comments,
            comments="",
            brand_id="",
            object_id="",
            service_id="",
            parent_post_id="",
            parent_object_id="",
            parent_service_id="",
            page_id="",
            page_name="",
            author_id='',
            author_name='',
            author_username='',
            author_image='',
            data_form_source=0,
        )
    return item


async def get_request_data_linkedin( keyword: str )  -> list[CrawlerPostItem]:
    """
    Fetch data from a given URL with optional parameters.
    
    :keyword: The keyword to fetch data from instagram.
    :return: Response object containing the fetched data.
    """
    keyword = unidecode(keyword).replace(" ", "%20").lower()
    user_agent = random.choice(USER_AGENTS)
    try:
        count=30
        url = f'https://www.linkedin.com/voyager/api/graphql?variables=(start:6,origin:FACETED_SEARCH,query:(keywords:{keyword},flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:resultType,value:List(CONTENT)),(key:sortBy,value:List(date_posted)))),count:{count})&queryId=voyagerSearchDashClusters.5ba32757c00b31aea747c8bebb92855c'

        headers = {
            "accept": "application/vnd.linkedin.normalized+json+2.1",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "csrf-token": "ajax:6470660172063231795",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.linkedin.com/search/results/content/?keywords={keyword}&origin=FACETED_SEARCH&sid=Ps%2C&sortBy=%22date_posted%22",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": user_agent,
            "x-li-lang": "en_US",
            "x-li-page-instance": "urn:li:page:d_flagship3_search_srp_content;mslhcFPNSayE5APL8/urfQ==",
            "x-li-pem-metadata": "Voyager - Content SRP=search-results",
            "x-li-track": "{\"clientVersion\":\"1.13.37322\",\"mpVersion\":\"1.13.37322\",\"osName\":\"web\",\"timezoneOffset\":7,\"timezone\":\"Etc/GMT-7\",\"deviceFormFactor\":\"DESKTOP\",\"mpName\":\"voyager-web\",\"displayDensity\":1,\"displayWidth\":1920,\"displayHeight\":1080}",
            "x-restli-protocol-version": "2.0.0"
        }
        cookies = {
            "bcookie": "v=2&bd0728f1-dd60-4e37-8638-cd7d5b708d5f",
            "bscookie": "v=1&2025042103550172c8d890-9870-4c98-8b1e-042b1112af6fAQEksHT9RYVo6JwywvJ8x908bvYTPMNA",
            "li_sugr": "1c220d85-85de-4421-81f6-86781f50fcda",
            "liap": "true",
            "JSESSIONID": "ajax:6470660172063231795",
            "li_theme": "light",
            "li_theme_set": "app",
            "_guid": "7999cbe4-51a2-46cc-9c42-31d703a43154",
            "dfpfpt": "967e971e4393412bad26c260b3c81135",
            "li_alerts": "e30=",
            "VID": "V_2025_05_12_08_5384709",
            "gpv_pn": "www.linkedin.com%2Flegal%2Fl%2Fapi-terms-of-use",
            "s_tp": "27835",
            "s_tslv": "1747037027803",
            "s_ips": "1362",
            "_gcl_au": "1.1.2121256374.1746782782.1909983468.1749193405.1749193405",
            "li_at": "AQEDATTs4-UFaf-FAAABlrRd4p8AAAGYMXmx600Ar0oGeThxxEOCBVjun3JEDy4HgIz32pJQR9DpUGu-sWN53EzSsJ6SxiU0FhFPUO70zb-0_-dOmbFzi4uGF4GP2EOMe2MJldqIWhNXmqudlRZkd6aE",
            "lang": "v=2&lang=en-us",
            "timezone": "Etc/GMT-7",
            "AnalyticsSyncHistory": "AQILGifO-1pJPwAAAZgq8trCRP0moWBqcHswvcqB11sikurC6xNaeHprCxbQY-r9ZMgEEzSRsxnIasEVZyLuBw",
            "lms_ads": "AQFzvRNOgVPPCAAAAZgq8tvmkbYL4lOEfxsUGLKMP_VJAoHzHzsVHf4099UgpQ-_mUsmYlZqYJ8sJylxdJCF9YKQ5y7kimRV",
            "lms_analytics": "AQFzvRNOgVPPCAAAAZgq8tvmkbYL4lOEfxsUGLKMP_VJAoHzHzsVHf4099UgpQ-_mUsmYlZqYJ8sJylxdJCF9YKQ5y7kimRV",
            "AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg": "1",
            "aam_uuid": "32988820362534772503488696944483243602",
            "fptctx2": "taBcrIH61PuCVH7eNCyH0J9Fjk1kZEyRnBbpUW3FKs8BBmipgyeYbO6dxdCN0Ne68Fbly68T5Q2K78hp9IlXNXqNXt6i49xvCVarD2XVbqbzpucx79bTC9OuJ%252bxWUcRc14%252bW99shhXovzwB2%252bhDaP27XCnchqfCiDgDp3O1OovBMMNrnE5F2%252bcvLMTLn%252fxMTfhqsu1MoAvH3z9pZMrA2eB11e735PyZJPP%252fOJNsG%252f78X%252bh283es3K0VsMiFwsoIb%252bbrsxBCr2XDUO5tTNax2XgeecgpluXzHMsMiSA28AYq4fIVPrcG7nURulraJBbBFwXKJKW12CBywOC37UuVjeIoj79GGsPdXc3PPDZPZELA%253d",
            "AMCV_14215E3D5995C57C0A495C55%40AdobeOrg": "-637568504%7CMCIDTS%7C20291%7CMCMID%7C32450772095884805853505340237148120473%7CMCAAMLH-1753773175%7C3%7CMCAAMB-1753773175%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1753175575s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1843645645",
            "__cf_bm": "3.f7AbWSrSnvwjNfdEB.gMicSXsfuoxJvWtYv.kpSPI-1753169146-1.0.1.1-c5iBBk5M1cGsdsPPrgEZu0r3xpgGllWmxbGPi0ZhKFJKUGmqrAUl0OY6krnDY_5KC3t6WDmgQ.q2aXTl_uf20BinVQjt9ZuTsF50TnBUNJU", 
            "UserMatchHistory": "AQJbNuImErThqgAAAZgxB0G4hhxQb4iSLbY0IkNSAqQUXicHc4Mz6mwOPQ8QWS1V4xjPMnSpv1jFLyGggHhRN_aumeUUEIszcAO52OjR3MNB8YJJdUvKMmfEF5Rp1haHIgyVbYRV093YuSFUTQVjHcUX4R3_Owrf06pNAqMtdV2-6jZKWaYWWkXRU0UtPyezpAcAg015dA-aGa072cLudMmBp4X8HhLQn8-_lzjqubcU_1xB-o_N2p4AkvX8uGb9_LlbmB9jgNKoUzXc2QNriyRooX4SX7Om8sFnr1d0pEtlixe_p35VGDNNoBqI2GMn6IHyIsPClzKdHFJhbRnN3IOYvZcKmU9mGxQJ3QKOTJ8y3lwKdw",
            "lidc": "b=OB69:s=O:r=O:a=O:p=O:g=5020:u=262:x=1:i=1753169217:t=1753248584:v=2:sig=AQGB73fIut4ofHDgS21KQQN81nkvIOfh"
            }
        cookies={}
        response = requests.get(url=url, headers=headers, cookies=cookies)
        if response.status_code != 200:  # Raise an error for bad responses
            print(f"[ERROR] Failed to fetch data from Linkedin: {response.status_code}")
            return [],str(response.status_code)
        data_res = json.loads(response.text)
        #print(data_res)
        try:
            list_post=data_res['included']
        except:
            list_post=[]
        if not list_post:
            return [],str(response.status_code)
        list_post_res = []
        for post in list_post:   
            if post.get("metadata") is None:
                continue  

            item = get_data_post_search_linedin(post,keyword)
            list_post_res.append(item)
        return list_post_res,str(response.status_code)
    except requests.RequestException as e:
        raise Exception(f"Error fetching data from instagram: {str(e)}")

def url_encode(text: str) -> str:
    return urllib.parse.quote(text, safe='')



def get_data_post_search_watchfb(post,keyword):
    
    try:
        mess_data=post['rendering_strategy']['view_model']['video_metadata_model']

        post_id = mess_data['video']['id']
        post_url = "https://www.facebook.com/reel/" + post_id
        post_created=""
        post_created_timestamp= int(datetime.now().timestamp())
    except:
        post_id = "get_id_error"
        post_url = "get_url_error"
        post_created_timestamp = 0
        post_created = "get_created_error"
 
    try:
        durex=post['rendering_strategy']['view_model']['video_thumbnail_model']['video_duration_text']
        message = (
            "Thời lượng: " +durex + '\n' +
            mess_data['relative_time_string'] + '\n' +
            mess_data['title'] + '\n' +
            mess_data['save_description']
        )
    except KeyError:
        message = "get_message_error"
    try:
        post_image = post['rendering_strategy']['view_model']['video_thumbnail_model']['thumbnail_image']['uri']
    except:
        post_image = ""
    
    try:
        count_like = 0  
    except:
        count_like = 0
    try:
        count_share = 0  
    except:
        count_share = 0
    try:
        count_comments=0   
    except:
        count_comments = 0
    item = CrawlerPostItem(
            post_id=post_id,
            post_type="facebook",
            post_keyword=keyword,
            post_url=post_url,
            message=message,
            type=0,
            post_image= post_image,
            post_created=post_created,
            post_created_timestamp=post_created_timestamp,
            post_raw="",
            count_like=count_like,
            count_share=count_share,
            count_comments=count_comments,
            comments="",
            brand_id="",
            object_id="",
            service_id="",
            parent_post_id="",
            parent_object_id="",
            parent_service_id="",
            page_id="",
            page_name="",
            author_id='',
            author_name='',
            author_username='',
            author_image='',
            data_form_source=0,
        )
    return item
def generate_filters(start_date: datetime, end_date: datetime) -> str:
    """
    Trả về filters URL-encoded cho Facebook GraphQL dạng:
    "filters": ["{...}", "{...}"]
    """
    import json
    import urllib.parse
    from datetime import datetime, timedelta

    # filter sắp xếp
    sort_by = json.dumps({
        "name": "videos_sort_by",
        "args": "Most Recent"
    }, separators=(',', ':'))

    # filter theo thời gian
    creation_time = json.dumps({
        "name": "creation_time",
        "args": json.dumps({
            "start_year": str(start_date.year),
            "start_month": f"{start_date.year}-{start_date.month:02}",
            "start_day": f"{start_date.year}-{start_date.month:02}-{start_date.day:02}",
            "end_year": str(end_date.year),
            "end_month": f"{end_date.year}-{end_date.month:02}",
            "end_day": f"{end_date.year}-{end_date.month:02}-{end_date.day:02}",
        }, separators=(',', ':'))
    }, separators=(',', ':'))

    filters = [sort_by, creation_time]

    # Chuyển thành JSON rồi URL-encode
    filters_str = json.dumps(filters, separators=(',', ':'))
    return urllib.parse.quote(filters_str)

def generate_creation_time_filter(start_date: datetime, end_date: datetime) -> str:
    """
    Trả về filters URL-encoded đúng định dạng Facebook yêu cầu,
    với args trong creation_time là một chuỗi JSON đã escape.
    """
    # B1: Tạo chuỗi JSON cho phần args của creation_time
    args_obj = {
        "start_year": str(start_date.year),
        "start_month": f"{start_date.year}-{start_date.month:02}",
        "start_day": f"{start_date.year}-{start_date.month:02}-{start_date.day:02}",
        "end_year": str(end_date.year),
        "end_month": f"{end_date.year}-{end_date.month:02}",
        "end_day": f"{end_date.year}-{end_date.month:02}-{end_date.day:02}"
    }
    args_str = json.dumps(args_obj, separators=(',', ':'))  # encode 1 lần

    # B2: Tạo từng filter string (vẫn ở dạng string)
    sort_by = json.dumps({
        "name": "videos_sort_by",
        "args": "Most Recent"
    }, separators=(',', ':'))

    creation_time = json.dumps({
        "name": "creation_time",
        "args": args_str  # giữ nguyên string JSON
    }, separators=(',', ':'))

    # B3: Gộp lại thành mảng chuỗi JSON
    filters = [sort_by, creation_time]

    # B4: Dump mảng này thành JSON (list of strings)
    filters_json_array = json.dumps(filters, separators=(',', ':'))

    # B5: URL-encode để truyền qua network
    return urllib.parse.quote(filters_json_array)

async def get_request_data_watchfb( keyword: str )  -> list[CrawlerPostItem]:
    """
    Fetch data from a given URL with optional parameters.
    
    :keyword: The keyword to fetch data from instagram.
    :return: Response object containing the fetched data.
    """
    keyword_encoded = url_encode(keyword)
    now = datetime.now()
    start_day = now - timedelta(days=3)
    end_day = now +timedelta(days=3)
    filters_encoded = generate_creation_time_filter(start_day, end_day)
    print(filters_encoded)
    user_agent = random.choice(USER_AGENTS)
    try:
        count=30
        url = "https://www.facebook.com/api/graphql/"
        #  payload = f'av=0&__aaid=0&__user=0&__a=1&__req=a&__hs=20291.HYP%3Acomet_loggedout_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1025011720&__s=tuo5p9%3Au1n4cw%3Aqal427&__hsi=7529969641645841789&__dyn=7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W0qa0FE2awpUO0n24oaEd82lwv89k2C1Fwc60D85m1mzXwae4UaEW0LobrwmE2eUlwhE2FBwxw4BwqEGdw46wbS1LwTwNwLweq1Iwqo4eEgwro7SmEb8uwm85K0UE62&__csr=gqFr4WNnsLimKBOtfTahrQINYB5G8yaG9yV8Gm498O4oSiiFkcABK9CGaV8C58RwwAxqmiawkUohErxC1dAwBy8iwiqyqwhU5m26U98sx60jm8Bg6h01u67E06yi0adw1yW0c7w1MK0kuU03vkt08G04kE0AC09-w7uwrU1GA1Yo0HK04g80SS1KxNw20o0jAw5OAo0P-02Pz802Zu03Ly3Dhkl6w2eC0NE0gmw0yCw6tyo0aO8Bw2l81zUnpUG&__hsdp=hVhPZnsdNc5GDzbQ8wk6Gl8A-S7KeQl4gbAcvZk9y8eQdJXci6p84u1lwaacBy89E5q2C1Dw4fg59wLy83c82217w64w8u0yo0ym04O83fw2-U34wl83YwVwk82Iw3F81gU1Bo&__hblp=0uU2lwaW1eyUkV85i7o560zVU26wFwm40qe0-o1P827w8C6o0wK04O84e0yU0LK0Bk2S1kwfO36u58pxqawiE660_80yO1Wwbai48a8f8kwXwUw4ww&__sjsp=hVhPZnsdNcbiMwFUOZ2851GBi9fJxXzJ5h42V37_l1a3J15U9V82twaacBy89E1-41ioe83c82217w64w&__comet_req=15&lsd=AVq0e4Glnac&jazoest=2950&__spin_r=1025011720&__spin_b=trunk&__spin_t=1753207678&__crn=comet.fbweb.CometWatchSearchRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=SearchCometResultsPaginatedResultsQuery&'\
        # f'variables=%7B%22allow_streaming%22%3Afalse%2C%22args%22%3A%7B%22callsite%22%3A%22comet%3Awatch_search%22%2C%22config%22%3A%7B%22exact_match%22%3Afalse%2C%22high_confidence_config%22%3Anull%2C%22intercept_config%22%3Anull%2C%22sts_disambiguation%22%3Anull%2C%22watch_config%22%3Anull%7D%2C%22context%22%3A%7B%22bsid%22%3A%2294d4e363-7db4-44e6-af68-cce2ff5034bb%22%2C%22tsid%22%3Anull%7D%2C%22experience%22%3A%7B%22client_defined_experiences%22%3A%5B%22ADS_PARALLEL_FETCH%22%5D%2C%22encoded_server_defined_params%22%3Anull%2C%22fbid%22%3Anull%2C%22type%22%3A%22WATCH_TAB_GLOBAL%22%7D%2C' \
        # f'%22filters%22%3A%5B%22%7B%5C%22name%5C%22%3A%5C%22videos_sort_by%5C%22%2C%5C%22args%5C%22%3A%5C%22Most%20Recent%5C%22%7D%22%2C%22%7B%5C%22name%5C%22%3A%5C%22creation_time%5C%22%2C%5C%22args%5C%22%3A%5C%22%7B%5C%5C%5C%22start_year%5C%5C%5C%22%3A%5C%5C%5C%222025%5C%5C%5C%22%2C%5C%5C%5C%22start_month%5C%5C%5C%22%3A%5C%5C%5C%222025-07%5C%5C%5C%22%2C%5C%5C%5C%22end_year%5C%5C%5C%22%3A%5C%5C%5C%222025%5C%5C%5C%22%2C%5C%5C%5C%22end_month%5C%5C%5C%22%3A%5C%5C%5C%222025-07%5C%5C%5C%22%2C%5C%5C%5C%22start_day%5C%5C%5C%22%3A%5C%5C%5C%222025-07-{start_day}%5C%5C%5C%22%2C%5C%5C%5C%22end_day%5C%5C%5C%22%3A%5C%5C%5C%222025-07-{end_day}%5C%5C%5C%22%7D%5C%22%7D%22%5D%'\
        # f'%2C%22text%22%3A%22{keyword_encoded}%22%7D%2C%22count%22%3A5%2C%22cursor%22%3A%22AbrEic2g5fjI9wHwz6Mzve4uN4BGTw3gSapjPV_g9umdXT4wgKMeT4iwhSJiyZGinp7ZxglbqA2kmUJ_OhvYA4yr9BdFo9MW77hBOyQzpDaqVNshMUM05KV2vZoKkf22aQFECOQn-3TWlzOriuHMFXK3flUNVpj2DJl69_HNhEgbRkixC-uQ5CE9sVQbwka2EHZW5x3DNLp3WPfm-2OtzJqmOZZpUgDVoHRC66BNzpwy_zeltKKkgKIvGGUOwqGRrFvDbCDyWhYThy25twSGIkSWcM66xP-gpc7x-dccDDn5MIygBkI44ggPQBa5GQeBVEMNfRAWWjnz1RUP8XYaIoaTcxfk55Zv75RXkZRjkF7IflPk4B6p7j06TYpEM5DjnA_NxPpzQ7JKM-SbaET1Hz4R4Wh8Ha5EYrE3edUGGB0sc2EvHVFdk2tZZ7QbS40_BuappgfVKrj8GOo-P7Z_X5p3lBAGN19G55KtgOtuw_V0bekgwGv_sxPphRu771KqwIl8Xw5NR53xqncVgnYguCkiQb3ArFtaWQZygfnPLwqcmMbNoJQBCVQ6VsConHASP9-KrO1F3o7j7vILqFfrnGXHGNl9OFo_CjX8jJe5RM1YNFvn5ztMjdtwHK022ZiBvrFBjWjowXSNKTYI9uODsM14FlC8wP77prfQuW2h5QN9NANgQrQFeuKZXuukloBRTYuzdGGaOgqrHAoN14TLxN0Ak2x2NyhmqJ4hS4NYFB42YC2rxOh_tJ0Zf73xSSGIJIBw2GS-VqrCHGf25rpJ4QAPx02956716A6RNiA2sdZN3CKEy9VaIh8ilL5Rv2QZdL_1kWTsx3wUz5pdCWQV-xwCrFgN7hdKrBYPSfO4p3VEYx-p-cmTjK2TGOJJ1pvAWLJbuP6QxlyBBKqqkgM2QRKe0Swa6uH09L2p-7zBIN_7P7WcVM5hinGlWtJ7c9Vq_p-O8i_OLNLSeFOL62bWBjt4hlcU_44mIz1yYzYIGstLZ0_dmu_A0Qn9hpAbXbCRzcKmJYgDaTt9LvL8j_bQ9GjYjnnVHNZ22xpJv3W6LHAW7cBVFtN5P2g2Tjo1t6vovm3GgugdBckyMoiwtNxeQfUZlTrslT-urIto3NCLiD2P121zv0ZY-Rn-BqiHZvKv5r5HzqVppz9upWhSPtLUf0_hIw1yQlQI75xiBYnf4zojqg-gKy3A3rOo_sx62xpnZMx_nP2JoQSAe5dh0vBnncT-B-doXbgPwhIoo7CQtouMV1PimrjhlWHSsec9sThTBqqBke8Xg7ZRLOnKvuGXumzD1ScI0p67Of9dpcsKg7Xu4Pk5mppFy8P8vlhbCW4FN62f1K2qGjlOFjRYDaZ9iAfJ6UaMRPkKdeh-LjeK7trDE1Sh7VUcry2cAlIDo42Uec0AH49WeSL3d2TJ5d8M0-6fD0kLFpYDDRxyPTdxJJIBpmP1odN9ZC5LoL3jUWx5qsquo5PA21pu2FJvRS3f3iDthOljSEJQHmm12m6C8sbRqwcUYKKwB-qcIoeHCCGVHAMd5idV6IZNO0TYKm77n5CjHNioYlKppUCysPTku2TPjs5fxTEM8sEKlwezaACHOzQ%22%2C%22feedLocation%22%3A%22SEARCH%22%2C%22feedbackSource%22%3A23%2C%22fetch_filters%22%3Atrue%2C%22focusCommentID%22%3Anull%2C%22locale%22%3Anull%2C%22privacySelectorRenderLocation%22%3A%22COMET_STREAM%22%2C%22renderLocation%22%3A%22search_results_page%22%2C%22scale%22%3A1%2C%22stream_initial_count%22%3A0%2C%22useDefaultActor%22%3Afalse%2C%22__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__IsWorkUserrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider%22%3Afalse%2C%22__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider%22%3Afalse%2C%22__relay_internal__pv__IsMergQAPollsrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometUFIShareActionMigrationrelayprovider%22%3Atrue%2C%22__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider%22%3Afalse%7D&server_timestamps=true&doc_id=24030724856591072'
        
        #payload = f'av=0&__aaid=0&__user=0&__a=1&__req=a&__hs=20291.HYP%3Acomet_loggedout_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1025011720&__s=tuo5p9%3Au1n4cw%3Aqal427&__hsi=7529969641645841789&__dyn=7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W0qa0FE2awpUO0n24oaEd82lwv89k2C1Fwc60D85m1mzXwae4UaEW0LobrwmE2eUlwhE2FBwxw4BwqEGdw46wbS1LwTwNwLweq1Iwqo4eEgwro7SmEb8uwm85K0UE62&__csr=gqFr4WNnsLimKBOtfTahrQINYB5G8yaG9yV8Gm498O4oSiiFkcABK9CGaV8C58RwwAxqmiawkUohErxC1dAwBy8iwiqyqwhU5m26U98sx60jm8Bg6h01u67E06yi0adw1yW0c7w1MK0kuU03vkt08G04kE0AC09-w7uwrU1GA1Yo0HK04g80SS1KxNw20o0jAw5OAo0P-02Pz802Zu03Ly3Dhkl6w2eC0NE0gmw0yCw6tyo0aO8Bw2l81zUnpUG&__hsdp=hVhPZnsdNc5GDzbQ8wk6Gl8A-S7KeQl4gbAcvZk9y8eQdJXci6p84u1lwaacBy89E5q2C1Dw4fg59wLy83c82217w64w8u0yo0ym04O83fw2-U34wl83YwVwk82Iw3F81gU1Bo&__hblp=0uU2lwaW1eyUkV85i7o560zVU26wFwm40qe0-o1P827w8C6o0wK04O84e0yU0LK0Bk2S1kwfO36u58pxqawiE660_80yO1Wwbai48a8f8kwXwUw4ww&__sjsp=hVhPZnsdNcbiMwFUOZ2851GBi9fJxXzJ5h42V37_l1a3J15U9V82twaacBy89E1-41ioe83c82217w64w&__comet_req=15&lsd=AVq0e4Glnac&jazoest=2950&__spin_r=1025011720&__spin_b=trunk&__spin_t=1753207678&__crn=comet.fbweb.CometWatchSearchRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=SearchCometResultsPaginatedResultsQuery&variables=%7B%22allow_streaming%22%3Afalse%2C%22args%22%3A%7B%22callsite%22%3A%22comet%3Awatch_search%22%2C%22config%22%3A%7B%22exact_match%22%3Afalse%2C%22high_confidence_config%22%3Anull%2C%22intercept_config%22%3Anull%2C%22sts_disambiguation%22%3Anull%2C%22watch_config%22%3Anull%7D%2C%22context%22%3A%7B%22bsid%22%3A%2294d4e363-7db4-44e6-af68-cce2ff5034bb%22%2C%22tsid%22%3Anull%7D%2C%22experience%22%3A%7B%22client_defined_experiences%22%3A%5B%22ADS_PARALLEL_FETCH%22%5D%2C%22encoded_server_defined_params%22%3Anull%2C%22fbid%22%3Anull%2C%22type%22%3A%22WATCH_TAB_GLOBAL%22%7D%2C%22filters%22%3A{filters_encoded}%2C%22text%22%3A%22{keyword_encoded}%22%7D%2C%22count%22%3A5%2C%22cursor%22%3A%22AbrEic2g5fjI9wHwz6Mzve4uN4BGTw3gSapjPV_g9umdXT4wgKMeT4iwhSJiyZGinp7ZxglbqA2kmUJ_OhvYA4yr9BdFo9MW77hBOyQzpDaqVNshMUM05KV2vZoKkf22aQFECOQn-3TWlzOriuHMFXK3flUNVpj2DJl69_HNhEgbRkixC-uQ5CE9sVQbwka2EHZW5x3DNLp3WPfm-2OtzJqmOZZpUgDVoHRC66BNzpwy_zeltKKkgKIvGGUOwqGRrFvDbCDyWhYThy25twSGIkSWcM66xP-gpc7x-dccDDn5MIygBkI44ggPQBa5GQeBVEMNfRAWWjnz1RUP8XYaIoaTcxfk55Zv75RXkZRjkF7IflPk4B6p7j06TYpEM5DjnA_NxPpzQ7JKM-SbaET1Hz4R4Wh8Ha5EYrE3edUGGB0sc2EvHVFdk2tZZ7QbS40_BuappgfVKrj8GOo-P7Z_X5p3lBAGN19G55KtgOtuw_V0bekgwGv_sxPphRu771KqwIl8Xw5NR53xqncVgnYguCkiQb3ArFtaWQZygfnPLwqcmMbNoJQBCVQ6VsConHASP9-KrO1F3o7j7vILqFfrnGXHGNl9OFo_CjX8jJe5RM1YNFvn5ztMjdtwHK022ZiBvrFBjWjowXSNKTYI9uODsM14FlC8wP77prfQuW2h5QN9NANgQrQFeuKZXuukloBRTYuzdGGaOgqrHAoN14TLxN0Ak2x2NyhmqJ4hS4NYFB42YC2rxOh_tJ0Zf73xSSGIJIBw2GS-VqrCHGf25rpJ4QAPx02956716A6RNiA2sdZN3CKEy9VaIh8ilL5Rv2QZdL_1kWTsx3wUz5pdCWQV-xwCrFgN7hdKrBYPSfO4p3VEYx-p-cmTjK2TGOJJ1pvAWLJbuP6QxlyBBKqqkgM2QRKe0Swa6uH09L2p-7zBIN_7P7WcVM5hinGlWtJ7c9Vq_p-O8i_OLNLSeFOL62bWBjt4hlcU_44mIz1yYzYIGstLZ0_dmu_A0Qn9hpAbXbCRzcKmJYgDaTt9LvL8j_bQ9GjYjnnVHNZ22xpJv3W6LHAW7cBVFtN5P2g2Tjo1t6vovm3GgugdBckyMoiwtNxeQfUZlTrslT-urIto3NCLiD2P121zv0ZY-Rn-BqiHZvKv5r5HzqVppz9upWhSPtLUf0_hIw1yQlQI75xiBYnf4zojqg-gKy3A3rOo_sx62xpnZMx_nP2JoQSAe5dh0vBnncT-B-doXbgPwhIoo7CQtouMV1PimrjhlWHSsec9sThTBqqBke8Xg7ZRLOnKvuGXumzD1ScI0p67Of9dpcsKg7Xu4Pk5mppFy8P8vlhbCW4FN62f1K2qGjlOFjRYDaZ9iAfJ6UaMRPkKdeh-LjeK7trDE1Sh7VUcry2cAlIDo42Uec0AH49WeSL3d2TJ5d8M0-6fD0kLFpYDDRxyPTdxJJIBpmP1odN9ZC5LoL3jUWx5qsquo5PA21pu2FJvRS3f3iDthOljSEJQHmm12m6C8sbRqwcUYKKwB-qcIoeHCCGVHAMd5idV6IZNO0TYKm77n5CjHNioYlKppUCysPTku2TPjs5fxTEM8sEKlwezaACHOzQ%22%2C%22feedLocation%22%3A%22SEARCH%22%2C%22feedbackSource%22%3A23%2C%22fetch_filters%22%3Atrue%2C%22focusCommentID%22%3Anull%2C%22locale%22%3Anull%2C%22privacySelectorRenderLocation%22%3A%22COMET_STREAM%22%2C%22renderLocation%22%3A%22search_results_page%22%2C%22scale%22%3A1%2C%22stream_initial_count%22%3A0%2C%22useDefaultActor%22%3Afalse%2C%22__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__IsWorkUserrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider%22%3Afalse%2C%22__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider%22%3Afalse%2C%22__relay_internal__pv__IsMergQAPollsrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometUFIShareActionMigrationrelayprovider%22%3Atrue%2C%22__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider%22%3Afalse%7D&server_timestamps=true&doc_id=24030724856591072'
        payload = 'av=0&__aaid=0&__user=0&__a=1&fb_api_req_friendly_name=SearchCometResultsPaginatedResultsQuery&variables=%7B%22allow_streaming%22%3Afalse%2C%22args%22%3A%7B%22callsite%22%3A%22comet%3Awatch_search%22%2C%22config%22%3A%7B%22exact_match%22%3Afalse%2C%22high_confidence_config%22%3Anull%2C%22intercept_config%22%3Anull%2C%22sts_disambiguation%22%3Anull%2C%22watch_config%22%3Anull%7D%2C%22context%22%3A%7B%22bsid%22%3A%2298bff3d0-ce63-4197-bccb-ef9b2efdc2a7%22%2C%22tsid%22%3Anull%7D%2C%22experience%22%3A%7B%22client_defined_experiences%22%3A%5B%22ADS_PARALLEL_FETCH%22%5D%2C%22encoded_server_defined_params%22%3Anull%2C%22fbid%22%3Anull%2C%22type%22%3A%22WATCH_TAB_GLOBAL%22%7D%2C%22filters%22%3A' +filters_encoded + \
        '%2C%22text%22%3A%22v%C5%A9%20tr%E1%BB%A5%20%C4%91%C6%B0a%20tin%22%7D%2C%22count%22%3A5%2C%22cursor%22%3A%22AbrNCL6qRdewSfExHNnWMH4EP4LNDpWwCROV6kQsqmSuxR-F6zWNN2BCYpWpTiXocKOwJx2qHcVSfu9Hci609zoAfDtFjDEGUhYuRd8D6PCHIe0N4O64MlJwR-rZSI4ii4vYnxVcq6Gr5P2iw0cOsIYt0XbvWlMdoNAsygaOqNdvw0d0hUl3AX6iVboUnBwKw4Tn_Q9uYWOZ5cjafstXP9pjaffMKC8Jp5WqnePRklMyxOP-yOXa-jY8gOaES0G0gheG0hkHEf_eCFD7BdfFpgOPuZ_gNLqeGQiFsUlwp8o_-9uUH6_x1IUZHGppC2QXZlubydXEXpOvXPWziYkIMqHhyMfO3urhXK_dhqNtc74yxp6NcemxvcwrN4CjPIDj61MGmW5rZNv0dMwbqd_WqCQL6LWCXkg9JHMuVNUsly-_DW2GfpJEr-oO7vegATbPtBUMYH-fe6oDT6Ym58kZJX45gFnOgqiLZG-Nxj8RQs6sxFA4OXX2pzh4TPyXy2bEXg7pFEhL-d-nw6FkslB0ZtAaAybuf7hx7Z46mBsFSFyBwFdE9uYYlfCx3OlvB-fLihjIH8k5Hzcm52R1jOcmHCiQnaN4e0TNNBzRwsGkRSTKbCXkumcDryOJwR1SUP3nQ5PghFd7T4s3MidbF1_bUOUf77ErAUD-TFEAYLKT81Nsfg9Voqns4eBGyxL1frjmuVuAocbPPQ_UPMvXajt5wVTYXAj0UdINZVtK58ZwqqOl74s39z_loYWfzkFkPKqfO_pphT8pX_XbSVsf-CPwz6Q4SQSXmDD4uwKcQ7EHv4TW4KKVO1LM7Jj4d9_AgHOwBiXn6d-2Bo-EEgK_ZFPriCqSwpwEHuRoY0xtepiNPkR2Gkja9bgt7VjW0sUT4ndbyDbdr13NDeIdPxBbM6U-9MA37t4TEhs_4WZUHtyUF5NzimOX-87_GlZtgSvme-Amm3smrTtaxrcCm4P5V5sCXO7nzOc0oTTFTthrKAs9xKSntNohhZw4i5b84eN1mZVb2TsYzNyycxFTIcAlvOlbbpQeTAQh22I4y2R83ehVRKcEfUjpvpE4dEEkidL6FTgb76D5lLD23h1TWgs-4n2JgD8MWbbf1OmBJhy4hJrnLKKuYoqhtyWIB2EpvicyneeIx38iY0-UC7MNukcX5tj8GiNMdg9KXHLGa0G_Q7uLSFsvA7Bic2ziTKt2BG4YP12zMGl1Ajf3_edPTdKdlo56SJh96UDmQ7QSCbGs821ajl8-pofZLm40gfI8rugNZjjcLTYNC-3KkoEuYYz2SG8Be-9GIH8nOmz9jQxdulYXSGLfHzMo0B479sSc0SduD-Grna31hHsxYYclYW1ufWlHsMB4WZDhpnSSkKslFxJV1TVvyvqcacfzGmHizzVD2HBkAhUUrusf_TFtZJ1eh3hZIbBnT0Qpdu7duQxBqjAbBbY8nO591rJYoNsPqPiFyWTANJWkgkgyppE2ZpaWOCoxtv6RjM2xzPrKWl5N91Ma0mC2fGzRTizY4oT6ohpB89YTMmsa35BfwSUcx9_YgCzreLGI88pNWSNqOY33U7x0gLAq8SfaiZ9oHIFmoyQwqCiBkHY%22%2C%22feedLocation%22%3A%22SEARCH%22%2C%22feedbackSource%22%3A23%2C%22fetch_filters%22%3Atrue%2C%22focusCommentID%22%3Anull%2C%22locale%22%3Anull%2C%22privacySelectorRenderLocation%22%3A%22COMET_STREAM%22%2C%22renderLocation%22%3A%22search_results_page%22%2C%22scale%22%3A1%2C%22stream_initial_count%22%3A0%2C%22useDefaultActor%22%3Afalse%2C%22__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__IsWorkUserrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider%22%3Afalse%2C%22__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider%22%3Afalse%2C%22__relay_internal__pv__IsMergQAPollsrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider%22%3Afalse%2C%22__relay_internal__pv__CometUFIShareActionMigrationrelayprovider%22%3Atrue%2C%22__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider%22%3Afalse%2C%22__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider%22%3Afalse%7D&doc_id=24030724856591072'
        headers = {
        'accept': '*/*',
        'accept-language': 'vi',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': f'https://www.facebook.com/watch/search?q={keyword_encoded}&filters=eyJ2aWRlb3Nfc29ydF9ieTowIjoie1wibmFtZVwiOlwidmlkZW9zX3NvcnRfYnlcIixcImFyZ3NcIjpcIk1vc3QgUmVjZW50XCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyNVxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyNS0wN1xcXCIsXFxcImVuZF95ZWFyXFxcIjpcXFwiMjAyNVxcXCIsXFxcImVuZF9tb250aFxcXCI6XFxcIjIwMjUtMDdcXFwiLFxcXCJzdGFydF9kYXlcXFwiOlxcXCIyMDI1LTA3LTIyXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjUtMDctMjJcXFwifVwifSJ9',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.158", "Microsoft Edge";v="138.0.3351.95"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user_agent,
        'x-asbd-id': '359341',
        'x-fb-friendly-name': 'SearchCometResultsPaginatedResultsQuery',
        'x-fb-lsd': 'AVq0e4Glnac',
        'Cookie': 'datr=sv-BaA0_-TySrWP5zX-6LmXL; sb=sv-BaCIBDhgYr9BRryLqZ7iz; fr=0oKSN20zHA5Xk5Pw9..Bogf-y..AAA.0.0.Bogf-5.AWc85SdtsqXirkkvCrddMeR64pc; ps_l=1; ps_n=1; wd=1060x927'
        }
        #print(payload)
        response = requests.post(url=url, headers=headers, data=payload)
        if response.status_code != 200:  # Raise an error for bad responses
            print(f"[ERROR] Failed to fetch data from fbwatch: {response.status_code}")
            return [],str(response.status_code)
        data_res = json.loads(response.text)
        #print(data_res)
        try:
            list_post=data_res['data']['serpResponse']['results']['edges']
        except:
            list_post=[]
        if not list_post:
            return [],str(response.status_code)
        list_post_res = []
        for post in list_post:   


            item = get_data_post_search_watchfb(post,keyword)
            list_post_res.append(item)
        return list_post_res,str(response.status_code)
    except requests.RequestException as e:
        raise Exception(f"Error fetching data from instagram: {str(e)}")
