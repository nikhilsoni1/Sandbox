from bs4 import BeautifulSoup
import urllib3
import certifi


def response(url, request='GET', header=None, auth=None):

    '''
    Sends the request to a server and receives the response

    Args:
        url (str): URL
        request (str): 'GET' or 'POST'
        header (str): Header String
        auth (str): Signed Query

    Returns:
        urllib3.response.HTTPResponse: Response

    '''

    if request.lower() == 'get':
        try:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            resp = http.request(request, url)
        except (urllib3.exceptions.MaxRetryError, ValueError) as error:
            resp = error
        return resp
    elif request.lower() == 'post':
        try:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            resp = http.request(request, url + auth, headers=header)
        except (urllib3.exceptions.MaxRetryError, ValueError) as error:
            resp = error
        return resp
    else:
        return 'Bad Request'


url0 = "wikipedia.com"
url = "https://www.imdb.com/streaming/canceled-renewed/ls063853872/mediaviewer/rm2481878528?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3d30d071-3fb0-4daa-8891-f770a4cb7278&pf_rd_r=ENAHRJQQRT2BSBDGA779&pf_rd_s=center-3&pf_rd_t=15061&pf_rd_i=homepage&ref_=hm_str_can_ren_i_1"
url2 = "https://www.imdb.com/streaming/canceled-renewed/ls063853872/mediaviewer/rm2481878528?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3d30d071-3fb0-4daa-8891-f770a4cb7278&pf_rd_r=ENAHRJQQRT2BSBDGA779&pf_rd_s=center-3&pf_rd_t=15061&pf_rd_i=homepage&ref_=hm_str_can_ren_i_1"
url3 = "https://www.twitch.tv"
url4 = "https://www.amazon.com.br/gp/cart/view.html?ref=nav_cart"
url5 = "https://www.adobe.com/lv/analytics/audience-manager.html?promoid=ZSV7F89Y&mv=other"
url6 = "https://www.imdb.com/title/tt0944947/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3b9ae4b1-1c64-4090-8faa-94bc8ca3099d&pf_rd_r=6H1KHMPXSTCYQ9DSVHJ9&pf_rd_s=center-3&pf_rd_t=60601&pf_rd_i=toronto&ref_=fea_tor_tor_studio_lk3"
resp = response(url6)
print(resp.status)
soup = BeautifulSoup(resp.data, "html.parser")
print(soup)
target = soup.find_all("a")
print(len(target))
print(target)
