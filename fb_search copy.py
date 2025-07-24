import requests
import json
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
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
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
keyword_encode ="Quỳnh anh"
body = 'av=17841458334146092&__d=www&__user=0&__a=1&__req=13&__hs=20279.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1024608489&__s=al53u2%3Avem5lm%3A6p3xd2&__hsi=7525342165906477118&__dyn=7xeUjG1mxu1syUbFp41twWwIxu13wvoKewSAwHwNw9G2S7o2vwpUe8hw2nVE4W0qa0FE2awgo9oO0n24oaEnxO1ywOwv89k2C1Fwc60AEC1TwQzXwae4UaEW2G0AEco5G1Wxfxm16wUwtE1wEbUGdG1QwTU9UaQ0z8c86-3u2WE5B08-269wr86C1mgcEed6goK2O4Xxui2qi7E5y4UrwHwGwa6byohw4rxO7EG3a&__csr=iMoWn2IpMRqMh5RbsBmj6cZeViYWBQGy4WFpOK8Gv8dl2nlmilfyJeVaAHCFvSturiWmEx24XgCRCo_BKmjHQWDiF5ChutF2q-4FUOaDxh2Q4Ehjx68BAGAurGiiTRhaAAzoy49fKeLDuiUV4zUrVApe4p8B3pBBUiz9VUtAx54xaqt5DCHngy00lkOXwtStwbkwfy0qo1uU45wj88E4upa0oy42K8gG0J20OwcG0TE0TK1Aw1NA8wxU4Cu1Uw58ws4m8Bsw3jwPwBA9849U6Ol1502ZEx2Fm1Gxa0qqp015S00wxE0RC02WC&__hsdp=gePX95TT2D36PaALqkbxvLH8D4h2E2j2Dshd4EMxAkx2eimAgjKgOAhpPsB5wmm7ln6xaeyUrzkfIkEroVx3wmEG22R8dzEaoRFe8Dwru6bwn8AiUeo8U4a2Gu7rw-yUB6UfEcUkwfiu0wo1yU3rw5Zxe0FU8E9o9U3ywkoa8461Pwba0GP0_g2wg8o621Yw-wfy2e1HUwS2W&__hblp=0kpEW2C1hxq7XAQ68O1MyUhyV8oxG0DEd8tGcLxnxKXyQ7odk5p9EGucCzomhV8jzpoiAKAUNbDAx62WcUoKcyF43WUvDwxWxqvwPKWLAwyiAK6rDwIVVF8CuawRx916dxi0xEcoa8iDxG10wBw45yE7G0LotwlonG0w87N4hUjw9a58W4U9p88E9UO0HodUpwEwYAwsU2ewzwiEG1lc227A1uwg7xOErwh4789EdVUdEkgnwyxe7t0seexi2l0CgOfUwSE99Eiw&__sjsp=gePX95-T2D36PaALqkbxvLH8D4h2E2j2DshdPEMxAkx229qh4iUlwzwukr5xa3qdg-NixJwaGQ&__comet_req=7&fb_dtsg=NAft7f1PKnxMVSUcCPmJz3WqD8k24SapIWCdPnISYWNbnuv0I3jMCBQ%3A17843676607167008%3A1747877953&jazoest=26196&lsd=B8K0DxfdDOgtIkJ5oWgCmY&__spin_r=1024608489&__spin_b=trunk&__spin_t=1752130260&__crn=comet.igweb.PolarisFeedRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisSearchBoxRefetchableQuery&variables=%7B%22data%22%3A%7B%22context%22%3A%22blended%22%2C%22include_reel%22%3A%22true%22%2C%22query%22%3A%22'+keyword_encode+'%22%2C%22rank_token%22%3A%22%22%2C%22search_session_id%22%3A%229e9878b4-f0f1-4f3a-ac99-7816ae24bbe5%22%2C%22search_surface%22%3A%22user%22%7D%2C%22hasQuery%22%3Atrue%7D&server_timestamps=false&doc_id=9523870587735596'

response = requests.request("POST", url, headers=headers, cookies=cookies,data=body)
# json_data = json.loads(response.text)
# with open("response.json", "w", encoding="utf-8") as f:
#     json.dump(json_data, f, ensure_ascii=False, indent=2)
       
print(response.text)
