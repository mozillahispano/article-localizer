'''
Written originally by @kirbylife
This is a program to translate the articles of the english Mozilla blog to spanish.
Original repo:
https://gitlab.com/kirbylife/
'''

import re
from urllib.parse import quote

from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from google.cloud import translate
from requests import get, post

client = translate.Client(target_language="es")


def translate(html_element):
    '''
    Split the full article into the child elements because the free google translate api has a character limit.
    '''
    response = client.translate(
        str(html_element), source_language="en", format_="html")
    text_translated = response["translatedText"]

    # Replace the "<Space>." and "<Space>," with only the punctuation sign
    text_translated = re.sub(r"\s(,|\.)", "\g<1>", text_translated)

    # Replace the "usted" for "tú"
    text_translated = re.sub(r".sted", "tu", text_translated, re.IGNORECASE)

    #Remove the whitespaces befora and after a slash
    text_translated = re.sub(r"\s?(/)", "\g<1>", text_translated)
    text_translated = re.sub(r"(/)\s?", "\g<1>", text_translated)

    text_translated = text_translated.replace("https//", "https://")
    text_translated = text_translated.replace(" = ", "=")

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
