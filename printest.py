import requests
import json
url = 'https://www.threads.com/graphql/query'

headers = {
    "accept": "*/*",
    "accept-language": "vi,en-US;q=0.9,en;q=0.8,fr-FR;q=0.7,fr;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.threads.com",
    "priority": "u=1, i",
    "referer": "https://www.threads.com/search?q=quockhanh&serp_type=default&filter=recent",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-full-version-list": "\"Google Chrome\";v=\"137.0.7151.124\", \"Chromium\";v=\"137.0.7151.124\", \"Not/A)Brand\";v=\"24.0.0.0\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"10.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "x-asbd-id": "359341",
    "x-bloks-version-id": "fe8bb1f2a0dd0a9a586850e809842e362c9a073430f63478a25155397dcd157b",
    "x-csrftoken": "3A2pS7UKPFP4WjL_Ef-m9I",
    "x-fb-friendly-name": "BarcelonaSearchResultsQuery",
    "x-fb-lsd": "vxK12nVGtt2_rHGgQv9dfU",
    "x-ig-app-id": "238260118697367",
    "x-root-field-name": "xdt_api__v1__text_feed__search_results__connection_v2"
}
cookies = {
    "ig_did": "F8BF3F5A-57DF-46F3-A80F-29BE23BEFC70",
    "mid": "aCF3cgALAAG32FgKlTRckAM9GVQv",
    "csrftoken": "3A2pS7UKPFP4WjL_Ef-m9I",
    "ds_user_id": "74512069398",
    "ps_l": "1",
    "ps_n": "1",
    #"sessionid": "74512069398:NNXtmduXUA6nlk:19:AYcymoqg6OKVM1267ISqq4NGSsaWY63pgsKOgKJXhvI",
    "rur": 'HIL,74512069398,1784693670:01fe85ded700a99ac0529741410d949589a30155c0e45585933c4977289a3f629fcc32fb'
}
body = 'av=17841474561954008&__user=0&__a=1&__req=k&__hs=20291.HYP%3Abarcelona_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1024994026&__s=vcu3y7%3Accejzs%3Alr8kpr&__hsi=7529754831700334865&__dyn=7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo1nEhw2nVE4W0qa0FE2awgo9oO0n24oaEd82lwv89k2C1Fwc60D85m1mzXwae4UaEW0Loco5G0zK5o4q0HU1IEGdwtU2ewbS1LwTwKG0hq1Iwqo9EpwUwiQ1mwLwHxW17y9UjgbVE-19w9y1swnrwu8&__csr=gjjkhijsDaxiRt9O5bHmZjJtWAmRjGszyECnUkxl16axO5EhKucDKh15w05POhUB2Uy0hV1K4E0iWwpkEkgn609N1y41Shs9160zCEkkjygM0XE2nwEzk0dxwgbw2-oB5xu6qgC0O8iK1-g3Hxm0aywhE11EeE2-5yl2ywyyk2Wfa1Fw-gjy581Zg1cU620ohw4ZgeayUqwiErwieks3264WG1hB9gC2S4CEkogB5w4Yw18y9w9yzPwccM02gnxicypA&__hsdp=gacItY960hBagwgqaohawGsu2fgMiWp4yY872h5b3xxUE5RA9Ap0H8lG44p1oks6Aggy8ONb8y62gamQQa87Eiq1sBIWCjwU6wgECqt0QwXw8a3K0x8b9S1FxK5U6Twro986q3x0o84e2S2lyXwgE0wW&__hblp=4g7p0cu798iwyoOp3EdQ10U2twjVqG9yEqG2Cq15wPixi14wIxC9GcwkUmBwpE3swIw4lU52Ey48y6-FUf8pzoKcxh0QUuyEHwSwJxe7aK10U0wW&__sjsp=g9_8xTMAoiAc40komobx0xxBUbt14zFAigMx4s94hp8nx10jEw-dBo2cDulIw3bw&__comet_req=29&fb_dtsg=NAfuBnj0r5N-bWoLkwW2pK16PKqumsrPG9gdtOabWCj9Is7XX5y5uTQ%3A17843683195144578%3A1747195941&jazoest=26320&lsd=vxK12nVGtt2_rHGgQv9dfU&__spin_r=1024994026&__spin_b=trunk&__spin_t=1753157664&__jssesw=2&__crn=comet.threads.BarcelonaSearchResultsColumnRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=BarcelonaSearchResultsQuery&variables=%7B%22meta_place_id%22%3Anull%2C%22power_search_info%22%3Anull%2C%22query%22%3A%22vietnam%22%2C%22recent%22%3A1%2C%22search_surface%22%3A%22default%22%2C%22tagID%22%3Anull%2C%22trend_fbid%22%3Anull%2C%22__relay_internal__pv__BarcelonaHasSERPHeaderrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsLoggedInrelayprovider%22%3Atrue%2C%22__relay_internal__pv__BarcelonaHasSelfReplyContextrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaHasInlineReplyComposerrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaHasEventBadgerelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsSearchDiscoveryEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaSnippetConsumptionEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__IsTagIndicatorEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaOptionalCookiesEnabledrelayprovider%22%3Atrue%2C%22__relay_internal__pv__BarcelonaHasSpoilerStylingInforelayprovider%22%3Atrue%2C%22__relay_internal__pv__BarcelonaHasDeepDiverelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaQuotedPostUFIEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsCrawlerrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaHasDisplayNamesrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaCanSeeSponsoredContentrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaShouldShowFediverseM075Featuresrelayprovider%22%3Atrue%2C%22__relay_internal__pv__BarcelonaImplicitTrendsGKrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsInternalUserrelayprovider%22%3Afalse%7D&server_timestamps=true&doc_id=24575927222043613'
body='av=17841474561954008&__user=0&__a=1&__req=1y&__hs=20291.HYP%3Abarcelona_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1024994026&__s=1y27mq%3Accejzs%3Abnfb5k&__hsi=7529760042195798353&__dyn=7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo1nEhw2nVE4W0qa0FE2awgo9oO0n24oaEd82lwv89k2C1Fwc60D85m1mzXwae4UaEW0Loco5G0zK5o4q0HU1IEGdwtU2ewbS1LwTwKG0hq1Iwqo9EpwUwiQ1mwLwHxW17y9UjgbVE-19xW1Vwn85SU7y&__csr=gjjkhijsDaxiRt9O5bH8ZjJtWAaBnSHdyEB4-Ve9igggyRQ9KfWixq4rhEOuV44m00nf97ykby817A6Uiw19bU8U6la545Nw2shUgx0tAn2ghw8VG554UAc0eW0ze8wEzk0dxwgbw2-oB5xu6qgC0O8iK1-g3Hxm0aywhE11EeE2-5yl2ywyyk2Wfa1Fw-gjy581Zg1cU620ohw4ZgeayUqwiErwieks3264WG1hB9gC2S4CEkogB5w4Yw18y9w9yzPwv84oM02gnxicypA&__hsdp=gacItY960hBagwgqaohawGixYejkc4Cp4yY872h5b3xxUE5RA9Pl2Ix0JhA5xhMqh12bjrcvExwA2BJd2y1W4Cwn95eFAUe1E4a9CDgd8eU22wXw8i2Otwqorxu3C6UnU6S2i1CwUg6213wJwBo-12xG0ve&__hblp=4g7p0cu798iwyoOp3EdQ10U2twjVqG9yEqG2Cq15wPixi8x-6Ub8pyqz8pwVxqm1Cw921bwIwoU5G1mUlwWG8x28x2aWDwYxCdyUO54i2_xWayK7EnwJxe6qGU43xB07Pw&__sjsp=g9_8xTMAo14niA846yC4iFgAiyDsejk4i6p4yY872h4ygRC7whOFhwSgQvhA5xgfz17KcU5ab80wE&__comet_req=29&fb_dtsg=NAfuFZn4p3F_OY1XqrzLH6jQRU1EdLcRjPOfa3Fpl0kM-GcLQAZp_oA%3A17843683195144578%3A1747195941&jazoest=26188&lsd=BbQ6GYFhxuxQ0F0NVJiUl5&__spin_r=1024994026&__spin_b=trunk&__spin_t=1753158877&__crn=comet.threads.BarcelonaSearchResultsColumnRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=BarcelonaSearchResultsRefetchableQuery&variables=%7B%22after%22%3A%22bdf333e076f7478d875c62d2142e03cf%3A1%22%2C%22before%22%3Anull%2C%22first%22%3A20%2C%22has_serp_header%22%3Afalse%2C%22last%22%3Anull%2C%22meta_place_id%22%3Anull%2C%22pinned_ids%22%3Anull%2C%22power_search_info%22%3Anull%2C%22query%22%3A%22quockhanh%22%2C%22recent%22%3A1%2C%22search_surface%22%3A%22default%22%2C%22tagID%22%3Anull%2C%22trend_fbid%22%3Anull%2C%22__relay_internal__pv__BarcelonaHasSERPHeaderrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsLoggedInrelayprovider%22%3Atrue%2C%22__relay_internal__pv__BarcelonaHasSelfReplyContextrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaHasInlineReplyComposerrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaHasEventBadgerelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsSearchDiscoveryEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaSnippetConsumptionEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__IsTagIndicatorEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaOptionalCookiesEnabledrelayprovider%22%3Atrue%2C%22__relay_internal__pv__BarcelonaHasSpoilerStylingInforelayprovider%22%3Atrue%2C%22__relay_internal__pv__BarcelonaHasDeepDiverelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaQuotedPostUFIEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsCrawlerrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaHasDisplayNamesrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaCanSeeSponsoredContentrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaShouldShowFediverseM075Featuresrelayprovider%22%3Atrue%2C%22__relay_internal__pv__BarcelonaImplicitTrendsGKrelayprovider%22%3Afalse%2C%22__relay_internal__pv__BarcelonaIsInternalUserrelayprovider%22%3Afalse%7D&server_timestamps=true&doc_id=9934413276681366'
# proxies = {
#     "http": "http://sun3336076:G63D8mDjPbiQ@rotate131.psun.io.vn:36076",
#     "https": "http://sun3336076:G63D8mDjPbiQ@rotate131.psun.io.vn:36076"
# }

for i in range(1):
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=body)
        if response.status_code == 200:
            print("✅ Đã gửi request thành công! "+ str(i+1))
            json_data = json.loads(response.text)

            print(response.text[:1000])  # In ra 1000 ký tự đầu tiên của response
            with open("response.json", "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
        else:
            print(f"❌ Lỗi: Status code {response.status_code} khi gửi request lần {i+1}")
            break
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi gửi request: {e}")
# response = requests.request("get", url, headers=headers)
# print("✅ Đã gửi request thành công!")
# print(f"🔍 Status code: {response.status_code}")

# # Ghi ra file


# print("✅ Đã ghi response ra file response.json")



