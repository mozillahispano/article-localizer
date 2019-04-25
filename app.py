'''
Written originally by @kirbylife
This is a program to translate the articles of the english Mozilla blog to spanish.
Original repo:
https://gitlab.com/kirbylife/
'''

import re
from urllib.parse import quote

from bs4 import BeautifulSoup, NavigableString, Tag
from flask import Flask, render_template, request
from requests import get, post


def _translate(text):
    '''
    Use the free API endpoint of Google translate to translate (Daahhh)
    if the answer is not a json it means that the IP is sending many requests and it does not work
    '''
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q="
    text = quote(text)
    response = get(url + text)
    try:
        response = response.json()
    except:
        return "Servicio no disponible por el momento :c intenta mas tarde"

    return "".join([i[0] for i in response[0]])


def translate(html_element):
    '''
    Split the full article into the child elements because the free google translate api has a character limit.
    '''
    childs = html_element.children
    for child in childs:
        if not isinstance(child, NavigableString):
            child_text = child.text
            text_translated = _translate(child_text)
            child_text = str(child).replace(child_text, text_translated)
            child.replace_with(child_text)

    text_translated = str(html_element)

    # Replace the "<Space>." and "<Space>," with only the punctuation sign
    text_translated = re.sub(r"\s(,|\.)", "\g<1>", text_translated)

    # Replace the "usted" for "tú"
    text_translated = re.sub(r".sted", "tu", text_translated, re.IGNORECASE)
    text_translated = text_translated.replace("&lt;", "<")
    text_translated = text_translated.replace("&gt;", ">")
    return text_translated


def get_article(url):
    '''
    receives url of the article and translates it
    '''
    response = get(url).text
    page = BeautifulSoup(response)
    article = page.find("div", attrs={"class": "entry-content"})
    if not article:
        return "Por favor, introduce una URL de un articulo de el blog de Firefox en inglés"
    article_translated = translate(article)
    author = page.address
    if author:
        author = author.text.strip()
        author_quote = f'''<p>Esta es una traducción del <a href="{url}">artículo original</a> realizado por {author}</p>'''
        article_translated = author_quote + "\n" + article_translated
    return article_translated


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        url = request.form.get("url")
        if not url:
            return "Por favor, ingresa una URL"
        translation = get_article(url)
        return translation


if __name__ == "__main__":
    app.run(debug=True, port=5000)
