"""
This spider implements a basic scraping of an blog application and,
crawls through both list and detail pages.
"""

import scrapy


class LaravelNewsSpider(scrapy.Spider):
    """
    This spider is responseible for scraping through the Laravel Site.
    """

    name = "laravel_news"
    allowed_domains = ["laravel-news.com"]
    start_urls = ["https://laravel-news.com/blog"]

    def parse(self, response, *args, **kwargs): # pylint: disable=unused-argument
        """
        This will parse from the start_urls and crawls through next page, if there is any.
        Also initiates a function to crawl the detail pages.
        """
        articles = response.css("section.py-20 div.group.relative")
        for article in articles:
            article_url = article.css("div a::attr(href)").get()
            article_details = {
                "title": article.css("h3::text").get(),
                "image_url": article.css("div img::attr(src)").get(),
                "image_alt": article.css("div img::attr(alt)").get(),
                "article_url": article_url,
                "summary": article.css("div p::text").get(),
            }
            yield response.follow(
                article_url,
                self.parse_article,
                cb_kwargs={"article_details": article_details},
            )

        next_page = response.css("button:contains('Next')").get()
        if next_page:
            try:
                page_num = int(response.url.split("=")[-1])
            except ValueError:
                page_num = 1
            next_page_url = response.urljoin(f"?page={page_num + 1}")
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response, article_details):
        """
        This crawls the blog and scraps the details regarding the author and the article.
        """
        article_author = response.css("p[itemprop='author'] a::text").get()
        author_intro = response.css("article div.prose.prose-sm p::text").get()
        article_tags = []
        for tags in response.css("article div.mt-6.flex div a::text"):
            article_tags.append(tags.get())
        author_socials = {}
        for social in response.css("article div.mt-4.flex a"):
            author_socials[social.css("img::attr(alt)").get()] = social.css(
                "a::attr(href)"
            ).get()

        yield article_details | {
            "article_author": article_author,
            "author_intro": author_intro,
            "article_tags": article_tags,
            "author_socials": author_socials,
        }
