# mozilla-blog-translate

## Dependencies
- Flask
- google-cloud-translate
- beautifulsoup4
- gunicorn (optional to deploy)

## Requirements
- a api-key of google translate api

## Test on development
1) declares an environment variable with the path to the .json file of the Google translate api-key
2) Execute `python app.py`
3) Open a web browser and go to http://127.0.0.1:5000

## Deploy
1) declares an environment variable with the path to the .json file of the Google translate api-key
2) Execute "gunicorn -b 0.0.0.0:8000 app:app"

