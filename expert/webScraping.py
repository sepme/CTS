import requests, urllib, io
from bs4 import BeautifulSoup as bs
from requests import Session

def sendAjaxrequest(head, url, data):

    session = Session()
    session.head(head)
    response = session.post(url=url,
                            data=data,
                            headers={ 'Referer': head }
                        )
    return response

def getKeywords(head, personId):
    url="https://isid.research.ac.ir/Ajax.php?call=AjaxWordCloud"
    data={
        "entityType":"0",
        'entityId': str(personId),
        'mode': '0'
    }
    response = sendAjaxrequest(head=head, url=url, data=data)
    return [item['key'] for item in response.json()]

def getPapersInfo(head, personId):
    url="https://isid.research.ac.ir/search"
    data={
            'crawl_type':"1",
            "person_ids":str(personId),
            "per_page":'12',
            "sort[by]":"citation",
            "sort[order]":"desc",
            "page":"1",
            'aui':"0",
            'backendModule': '3',
            "posted":"1600453827807"
        }
    
    response = sendAjaxrequest(head=head, url=url, data=data)
    papers = response.json()['items']
    papersInfo = []
    for paper in papers:
        papersInfo.append({
            "title"         : paper['title'],
            "source"        : paper['source_title'],
            "impact_factor" : paper['source_rsf_cs'],
            "publish_year"  : paper['published_year'],
            "citation"      : paper['citation'],
        })
    return papersInfo

def webScraping(url):
    bsContainer = bs((requests.get(url=url).content), "html.parser")    
    personId = bsContainer.find('input', id="person_id").get("value")
    informationDiv = list(bsContainer.find('div', class_="person-details clearfix").children)[1]
    informations = []
    for info in informationDiv.find_all('div'):
        informations.append(info.get_text().strip().replace("\u200c", ""))

    keywords = getKeywords(url, personId)

    papers = getPapersInfo(url, personId)

    src = bsContainer.find("img", class_="image").get("src")
    photo_in_byte = urllib.request.urlopen("https://isid.research.ac.ir" + src).read()
    photo = io.BytesIO(photo_in_byte)

    result = {
        "fullname"    : informations[0],
        "keywords"    : keywords,
        "photo"       : photo,
        "information" : informations[1:],
        "papers_information" : papers,
    }
    return result
