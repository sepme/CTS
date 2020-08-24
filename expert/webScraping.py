from selenium import webdriver
import pickle
import os, time
import io, urllib.request
from django.core.files import File
from ChamranTeamSite import settings


def webScraping(link):
    driver = webdriver.Firefox(executable_path=settings.BASE_DIR + '/expert/geckodriver')
    driver.get(link)
    driver.execute_script("IRIS.searchPaper({sort_by: 'citation'}, event)")
    time.sleep(1.5)

    person_id = driver.find_element_by_id("person_id").get_attribute("value")
    author = driver.find_elements_by_xpath('//span[@data-paper-person="{id}"]'.format(id=person_id))
    
    counter = 0
    div_result = driver.find_element_by_class_name("result-body-paper")
    papers = div_result.find_elements_by_tag_name("tr")
    papers_information = []
    for paper in papers:
        data = paper.find_elements_by_tag_name("td")
        result_title = data[1].text

        try:
            first_author = author[counter].find_element_by_tag_name("i").get_attribute("class")
        except:
            first_author = ""
        author_condition = "همکار"
        counter += 1
        if first_author != "":
            if "pencil" in first_author:
                author_condition = "نویسنده اول"
            if "asterisk" in first_author:
                author_condition = "نویسنده مسئول"
            if "star" in first_author:
                author_condition == "مسئول اجرا"
        if len(data[3].text.split("\n")) > 1:
            result_source = data[3].text.split("\n")[0] + " (" + data[3].text.split("\n")[1] + ")"
        else:
            result_source = data[3].text.split("\n")[0]
        result_source_sc = data[4].text.split("\n")[0]
        result_publish_year = data[5].text
        result_citation = data[6].text
        paper_information = {
            "title"         : result_title,
            "source"        : result_source,
            "impact_factor" : result_source_sc,
            "publish_year"  : result_publish_year,
            "citation"      : result_citation,
            "author_condition" : author_condition,
        }
        # [result_title, author_condition, result_source, result_source_sc, result_publish_year, result_citation]
        papers_information.append(paper_information)

    div_keywords = driver.find_element_by_id("vis-paper")
    keywords = div_keywords.find_elements_by_tag_name("text")
    keyword_list = []
    for keyword in keywords:
        keyword_list.append(keyword.text)
    div_information = driver.find_element_by_class_name("information")
    informations = div_information.find_elements_by_class_name("zar")
    information_list = []
    for information in informations:
        information_list.append(information.text)

    fullname = driver.find_element_by_class_name("TitrHuge").text

    img = driver.find_element_by_class_name("image")
    src = img.get_attribute('src')
    photo_in_byte = urllib.request.urlopen(src).read()
    photo = io.BytesIO(photo_in_byte)
    driver.close()

    result = {
        "fullname"    : fullname,
        "keywords"    : keyword_list,
        "photo"       : photo,
        "information" : information_list,
        "papers_information" : papers_information,
    }    
    return result
