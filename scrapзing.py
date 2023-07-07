import re
import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_headers():

    return Headers(browser='chrome', os='win').generate()


def get_parametres():

    return {
        "text": 'python'+'django'+'flask',
        "area": ['1', '2'],
        "search_field": ["name", "company_name", "description"],
        "items_on_page": "20",
        "page": 0
    }


def get_requests(url):

    return requests.get(url, params=get_parametres(), headers=get_headers()).text


def parce_text():

    vacancies = BeautifulSoup(get_requests(url), features="html.parser").find_all("div", class_="serp-item")

    parsed_data_vacancy = []

    for vacancy in vacancies:
        vacancy_name = vacancy.find("a", class_="serp-item__title")
        vacancy_href = vacancy_name["href"]

        salary = vacancy.find("span", class_="bloko-header-section-3")
        if salary != None:
            salary_try = salary.text
        else:
            salary_try = "Заработная плата не указана"

        employer = vacancy.find("a", class_="bloko-link bloko-link_kind-tertiary").text

        city = vacancy.find("div", {"data-qa":"vacancy-serp__vacancy-address"}).text

        general_information = {
            "Вакансия": vacancy_name.text,
            "Ссылка": vacancy_href,
            "Заработная плата": re.sub(r'\u202f', ' ', salary_try),
            "Работодатель": re.sub(r'(\xa0)', ' ', employer),
            "Город": re.sub(r'(\xa01\xa0)', ' ', city)
        }

        parsed_data_vacancy.append(general_information)

    return parsed_data_vacancy


def write_json():
    with open("vacancies.json", "w", encoding='utf8') as f:
        datadump = json.dump(parce_text(), f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    host = 'https://hh.ru/'
    url = f'{host}/search/vacancy'
    get_requests(url)
    parce_text()
    write_json()