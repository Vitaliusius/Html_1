import datetime
import collections
import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_an_age(year_of_creation):
    this_year = datetime.date.today()
    age_winery = this_year.year - year_of_creation

    return age_winery


def get_category_titles(sorted_categories):
    titles = [ drink for drink in sorted_categories]

    return titles


def get_sorting_categories(all_drinks):
    sorted_categories = collections.defaultdict(list)
    for drinks in all_drinks:
        sorted_categories[drinks['Категория']].append(drinks)

    return sorted_categories


def get_age_label(year):
    if year % 10 == 0 or year < 20 and year > 15:
        word = 'лет'
    elif year % 10 == 1:
        word = 'год'
    elif year % 10 == 2:
        word = 'года'
    else:
        word = 'лет'

    return f'{year} {word}'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    year_of_creation = 1920
    drinks_in_excel = pandas.read_excel('drinks.xlsx', keep_default_na=False)
    all_drinks = drinks_in_excel.to_dict(orient='records')
    sorted_categories = get_sorting_categories(all_drinks)
    rendered_page = template.render(
        old=get_age_label(get_an_age(year_of_creation)),
        sorted_categories=sorted_categories,
        titles_drinks=get_category_titles(sorted_categories)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()

