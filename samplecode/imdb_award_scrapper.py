'''
This python script is a specific script written to scrape award list of
actor Jackie Chan from imdb webpage.
'''

from lxml import html
import requests
import json


def scrape_award_list(html_page):

    awards_list = []

    page = requests.get(html_page)
    webpage = html.fromstring(page.content)
    awards_name = webpage.xpath('//div[@class="article listo"]/h3/text()')

    for each_name in awards_name:
        awards_dict = {}
        awards_dict['award_name'] = each_name
        awards_dict['award_description'] = []
        awards_list.append(awards_dict)
    awards_desc = webpage.xpath(
        '//div[@class="article listo"]/table[@class="awards"]')
    for ind_desc, item_desc in enumerate(awards_desc):
        tr = item_desc.xpath('./tr')
        for index, item in enumerate(tr):
            new_dict = {}
            year = item.xpath(
                './td[@class="award_year"]/a/text()')
            result_outcome = item.xpath(
                './td[@class="award_outcome"]/b/text()')
            desc_outcome = item.xpath(
                './td[@class="award_outcome"]/span/text()')
            description = item.xpath(
                './td[@class="award_description"]')[0].text_content()
            description = description.replace('\n', ' ').strip()
            description = " ".join(description.split())
            desc_note = item.xpath(
                './td[@class="award_description"]/' +
                'div/p[@class="full-note"]/text()')
            if len(year) != 0:
                new_dict['award_year'] = year[0]
            if len(result_outcome) != 0:
                new_dict['result_outcome'] = result_outcome[0]
            if len(desc_outcome) != 0:
                new_dict['desc_outcome'] = desc_outcome[0]
            if len(desc_note) != 0:
                new_dict['description'] = desc_note[0]
            new_dict['description'] = description
            awards_list[ind_desc]['award_description'].append(new_dict)

    with open('jsonfile', 'w') as outfile:
        json.dump(awards_list, outfile)

html_page = 'http://www.imdb.com/name/nm0000329/awards?ref_=nm_awd'
scrape_award_list(html_page)
