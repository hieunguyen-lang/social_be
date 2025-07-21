import requests
import time
import random
import uuid
import re
import json
import httpx
from datetime import datetime,timedelta
from unidecode import unidecode
from parsel import Selector
from urllib.parse import urlparse, urlunparse
from ..schemas.search_schemas import CrawlerPostItem
print(httpx.__version__)
print(httpx.__file__)
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
            author_id=data['owner']['id']
        except:
            author_id=''
        try:
            full_name=data['caption']['user']['full_name']
        except:
            full_name=''
        try:
            author_username=data['caption']['user']['username']
        except:
            author_username=''
        try:
            author_image=data['caption']['user']['profile_pic_url']
        except:
            author_image=''
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
            author_name=full_name,
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
            'accept': '*/*',
            'accept-language': 'vi,en-US;q=0.9,en;q=0.8,fr-FR;q=0.7,fr;q=0.6',
            'priority': 'u=1, i',
            'referer': 'https://www.instagram.com/explore/search/keyword/?q={keyword}',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="137.0.7151.124", "Chromium";v="137.0.7151.124", "Not/A)Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user_agent,
            'x-asbd-id': '359341',
            'x-csrftoken': 'M5MexFCAmVtzWC8o5JMzgRbNHISu6F1M',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR2FSYbLkevUBDCqMQn-xnlIjZst3cTUXSMNMmxhp-LuyH66',
            'x-requested-with': 'XMLHttpRequest',
            'x-web-session-id': 'wyh59a:g0lokc:09aoyj',
    
        }
        cookies = {
            "datr": "FH0uaE9jzr2zLPSntS6XVb6y",
            "ig_did": "009BE4D0-E24E-4C38-B68C-D4130764E64B",
            "mid": "aAhXYQALAAFFk406Xx_Zu60Pk67y",
            "ig_nrcb": "1",
            "fbm_124024574287414": "base_domain=.instagram.com",
            "csrftoken": "M5MexFCAmVtzWC8o5JMzgRbNHISu6F1M",
            "ds_user_id": "74091417494",
            "ig_direct_region_hint": "\"ASH\\05458448736471\\0541779954390:01f756ac5f88a79ac1f70c32b2ce99c3895da8b76658d17d6b71cb9015d3c63ccfb638f0\"",
            "ps_l": "1",
            "ps_n": "1",
            "wd": "1260x932",
            "sessionid": "58448736471%3Aksyf2QvaN1dNZz%3A8%3AAYfFKMJGYML-_F8OyO7NMF1Jtw7EzfVCOG6cjqCYpA",
            "rur": "VLL\\05474091417494\\0541784366622:01fe75b8de6615d5f1f1b19bdaede61f9a34a6bae4f78ba4ca404410668abdd30e22f1bb"
        }
        url_rq =f"https://www.instagram.com/graphql/query/?query_hash=9b498c08113f1e09617a1703c22b2f32&variables=%7B%22tag_name%22%3A%22{keyword}%22%2C%22first%22%3A24%2C%22after%22%3Anull%7D"
        print(url_rq)
        response = requests.get(url=url_rq, headers=headers, cookies=cookies)
        if response.status_code != 200:  # Raise an error for bad responses
            print(f"[ERROR] Failed to fetch data from Instagram: {response.status_code}")
            return []
        data_res = json.loads(response.text)
        #print(data_res)
        try:
            list_post=data_res['data']['hashtag']['edge_hashtag_to_media']['edges']
        except:
            list_post=[]
        if not list_post:
            return []
        list_post_res = []
        for post in list_post:       
            item = get_data_post_hastag_ig_recent(post,keyword)
            list_post_res.append(item)
        return list_post_res
    except requests.RequestException as e:
        raise Exception(f"Error fetching data from instagram: {str(e)}")
    
def handle_parse_data_threads(item_post,keyword):
    content_created = datetime.fromtimestamp(item_post["taken_at"]).strftime(
                                DATETIME_FORMAT)
    try:
        message = item_post["caption"]["text"]
    except KeyError:
        message = ""
    try:
        post_image = item_post["media"]["image_versions2"]["candidates"][0]["url"]
    except KeyError:
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
            author_name=item_post["user"]["username"] if "user" in item_post else "",
            author_username=item_post["user"]["username"] if "user" in item_post else "",
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
    print("httpx version:", httpx.__version__)
    print("httpx file:", httpx.__file__)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, cookies=cookies)
        #resp.raise_for_status()
    if resp.status_code != 200:
        print(f"[ERROR] Failed to fetch data from Threads: {resp.status_code}")
        return []
    sel = Selector(text=resp.text)
    data_threads = sel.xpath(".//script[@type='application/json']/text()").getall()
    list_post_res = []
    for data in data_threads:
        try:
            if "searchResults" in data and "thread_items" in data:
                data_json = json.loads(data)
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
        return []
    return list_post_res


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
    created_at = legacy.get('created_at', '')

    author_username = user_info.get('screen_name', '')
    author_name = user_info.get('name', '')
    author_id = user_data.get('rest_id', '')
    profile_image = user_data.get('avatar', {}).get('image_url', '')
    try:
        post_image = entry['media']['media_url_https']
    except KeyError:
        post_image = ''
    # Convert thời gian
    try:
        timeFormat = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        timeFormat = datetime.now()  # Nếu không parse được, dùng thời gian hiện tại
    timeFormatStr = (timeFormat + timedelta(hours=7)).strftime(DATETIME_FORMAT)
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
        return []
    if resp.status_code == 429:
        print(f"[ERROR] Failed to fetch data from X: {resp.status_code}")
        return []
    data_res = json.loads(resp.text)
    instructions = data_res['data']['search_by_raw_query']['search_timeline']['timeline']['instructions']
    entries = []
    for ins in instructions:
        if ins.get("type") == "TimelineAddEntries" and "entries" in ins:
            entries = ins["entries"]
            break

    if not entries:
        print("[ERROR] Không tìm thấy entries.")
        return
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
        return []
    return list_post_res

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
        return []
    aweme_ids = re.findall(r'"aweme_id":\s*"(\d+)"', resp.text)
    list_post_res = []
    created_at = int(datetime.now().timestamp())

    if aweme_ids:
        for video_id in aweme_ids:
            #print("[INFO] VIDEO ID: " + str(video_id))

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
    return list_post_res
