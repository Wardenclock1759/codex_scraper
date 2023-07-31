# Codex Scraper
This code collects text of all codexes from this [digital collection](https://rulaws.ru/).
## Spiders
### codex_parser
Simple spider that collects meta info that contains the title and href attribute from the main page. Then it stores results in urls.json. Below is the example of this file.
```
[
    {"title": "Арбитражный процессуальный кодекс РФ", "href": "/apk/"},
    {"title": "Бюджетный кодекс РФ", "href": "/bk/"},
    {"title": "Водный кодекс Российской Федерации РФ", "href": "/Vodnyy-kodeks/"},
    {"title": "Воздушный кодекс Российской Федерации РФ", "href": "/Vozdushnyy-kodeks/"},
    {"title": "Градостроительный кодекс Российской Федерации РФ", "href": "/Gradostroitelnyy-kodeks/"},
    {"title": "Гражданский кодекс РФ", "href": "/gk-rf/"},
```
### codex_collector
This is more complex spider. It iterates over above-mentioned list of URLs and collects data in the format as they appear on the page and saves it to separate file.  
Tree structure ensures that any inconsistency in tables of contents between codexes displays properly. Below is the example of on of the files.
![image](https://github.com/Wardenclock1759/codex_scraper/assets/65669569/d7aca722-4a0a-432a-980b-22c79bb418ba)
## How to run
To run this code make sure you have installed [scrapy](https://docs.scrapy.org/en/latest/intro/install.html#intro-install).  
Then follow this steps:
1. Run first spider that collects URLs
```
scrapy crawl codex_parser
```
2. Then run second spider. This process takes long time. To make it more managable remove some of the contents from URLs file.
```
scrapy crawl codex_collector
```
As it with scraping, I cant make sure that this code will work in the future as the site may change its structure. 
