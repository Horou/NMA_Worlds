import json
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..items import Chapter, Manga


class AsuraScansSpider(scrapy.Spider):
    name = "AsuraScans"
    start_urls = [
        'file:///C:/Users/Horous/Downloads/Manga%20-%20Asura%20Scans.htm',
    ]

    def parse(self, response, **kwargs):
        for manga in response.css('div.bs div.bsx a'):
            yield {
                'url': manga.css('a::attr("href")').get(),
                'title': manga.css('div.tt::text').get().strip(),
                'last_chapter': float(manga.css('div.epxs::text').get().replace("Chapter ", "")),
            }

        next_page = response.css('div.hpage a.r::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


class AsuraScansMangaSpider(scrapy.Spider):
    name = 'AsuraScansManga'
    start_urls = [
        'file:///C:/Users/Horous/Downloads/My%20School%20Life%20Pretending%20To%20Be%20a%20Worthless%20Person%20-%20Asura%20Scans.htm',
    ]

    def start_requests(self):
        with open("Manga/AsuraScans.json", 'r') as json_file:
            mangas = json.load(json_file)
        for manga in mangas:
            yield SeleniumRequest(url=manga['url'],
                                  callback=self.parse,
                                  wait_time=10,
                                  wait_until=EC.visibility_of_element_located((By.XPATH, 'readerarea')))

    def parse(self, response, **kwargs):
        item = Manga()
        manga = response.css("div.bigcontent")
        info = manga.css("div.fmed span::text").getall()
        item['url'] = response.url
        item['image_urls'] = [manga.css('img::attr("src")').get()]
        item['rating'] = float(manga.css("div.rating div.num::text").get())
        item['status'] = manga.css("div.tsinfo i::text").get()
        item['type'] = manga.css("div.tsinfo a::text").get()
        item['title'] = manga.css("h1.entry-title::text").get()
        item['description'] = manga.css("div.entry-content p::text").getall()
        item['author'] = info[1].strip()
        item['artist'] = info[2].strip()
        item['released'] = manga.css("div.fmed time[itemprop='datePublished']::attr(datetime)']").get()
        item['updated'] = manga.css("div.fmed time[itemprop='dateModified']::attr(datetime)").get()
        item['genres'] = manga.css("div.wd-full span.mgen a::text").getall()
        item['chapters'] = [
            {
                'url': chapter.css('a::attr("href")').get(),
                'number': float(chapter.css('span.chapternum::text').get().replace("Chapter ", "")),
                'date': chapter.css('span.chapterdate::text').get(),
            }
            for chapter in response.css('div.chbox div.eph-num a')
        ]
        return item


class AsuraScansChapterSpider(scrapy.Spider):
    name = "AsuraScansChapter"
    start_urls = [
        'file:///C:/Users/Horous/Downloads/My%20School%20Life%20Pretending%20To%20Be%20a%20Worthless%20Person%20Chapter%2022%20-%20Asura%20Scans.htm',
    ]

    def start_requests(self):
        with open("Manga/AsuraScansManga.json", 'r') as json_file:
            mangas = json.load(json_file)
        for manga in mangas:
            for chapter in manga['chapters']:
                yield SeleniumRequest(url=chapter['url'],
                                     callback=self.parse,
                                     wait_time=10,
                                     wait_until=EC.visibility_of_element_located((By.ID, 'readerarea')))

    def parse(self, response, **kwargs):
        item = Chapter()
        name, file_name, chapter_number = self.parse_name(response)
        chapter = {
            image.get(): (file_name, chapter_number, index)
            for index, image in enumerate(response.css('div#readerarea p img::attr("src")'))
            if "ENDING-PAGE" not in image.get()
        }
        item['url'] = response.url
        item['title'] = name
        item['number'] = chapter_number
        item['date'] = response.css('div.chaptertags time.entry-date::attr("datetime")').get()
        item['author'] = response.css("div.chaptertags span[itemprop='author']::text").get()
        item['image_urls'] = list(chapter.keys())
        item['image_names'] = chapter
        return item

    def parse_name(self, response):
        full_name = response.css('h1.entry-title::text').get()
        split_title = full_name.split(" Chapter ")
        chapter_number = split_title[-1]
        name = full_name.replace(" Chapter %s" % chapter_number, "")
        return name, name.lower().replace(" ", "_").replace("'", "_"), float(chapter_number)
