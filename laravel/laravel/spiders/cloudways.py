"""
Demonstrates the usage of scrapy.FormRequest to load additional data 
for list pages and how to pass arguments to the spider.
"""

import re

import scrapy
from scrapy import Selector


class CloudwaysSpider(scrapy.Spider):
    """
    Sample spider to crawl through the below mentioned blogging site.
    """

    name = "cloudways"
    allowed_domains = ["www.cloudways.com"]
    start_urls = [
        "https://www.cloudways.com/blog/laravel/",
    ]

    def __init__(self, *args, max_page_num=2, **kwargs):
        """
        Initializes the CloudwaysSpider instance.
        """
        super(CloudwaysSpider, self).__init__(*args, **kwargs)
        self.max_page_num = int(max_page_num)

    def parse(self, response, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Crawls through the list page of the blog site
        """
        blogs = response.css(
            "section#blg-catg-sec div.cw-cat-wrap div.container div.hm-catg-post-box div.hm-catg-post-txt"
        )
        blog_tag = "Laravel"
        yield from self.parse_blog_list(response, blogs)
        show_posts = 2024 if blog_tag == "Laravel" else 1477
        for page_number in range(2, self.max_page_num + 1):
            yield self.fetch_page_wise_blogs(response, page_number, show_posts)

    def parse_blog_detail(self, response, blog_details):
        """
        Crawls through the detailed page of the blog site
        """
        published_at_element = (
            response.css(
                "div#cw_postBlog_ttlWrap div.cw-inr-bnr-auth-wrap div.cwBlg_rtimeBox p span::text"
            )
            .get()
            .strip()
        )
        published_at_string = re.search(
            r"(\w+ \d{1,2}, \d{4})", published_at_element
        ).group(1)
        yield {
            **blog_details,
            "title": response.css("h1.post_title::text").get().strip(),
            "published_at": published_at_string,
        }

    def fetch_page_wise_blogs(self, response, page_number, show_posts):
        """
        Handles the `load more` option to load the additional data.
        """
        return scrapy.FormRequest.from_response(
            response,
            url="https://www.cloudways.com/blog/wp-admin/admin-ajax.php",
            formdata={
                "show_posts": str(show_posts),
                "search_keyword": "undefined",
                "author_id": "undefined",
                "tag_keyword": "undefined",
                "pageNumber": str(page_number),
                "action": "more_post_ajax",
            },
            method="POST",
            callback=self.parse_load_more_blogs,
        )

    def parse_load_more_blogs(self, response):
        """
        Handles the redirection of request to scrape the additional data.
        """
        response_body_string = response.body.decode("utf-8")
        response_body = Selector(text=response_body_string)
        blogs = response_body.css("div.hm-catg-post-txt")
        yield from self.parse_blog_list(response, blogs)

    def parse_blog_list(self, response, blogs):
        """
        Crawls through the list page.
        """
        for blog in blogs:
            blog_url = blog.css("h3.catg-post-title a::attr(href)").get()
            blog_tag = blog.css("a.post-catg-tag::text").get()
            blog_details = {
                "short_description": blog.css("p.catg-post-discBox::text").get(),
                "url": blog_url,
                "site": 1,
                "tags": [blog_tag],
                "author": (
                    blog.css("ul.catg-post-addnl-info a.post-author-name::text")
                    .get()
                    .strip()
                ),
                "author_url": blog.css(
                    "ul.catg-post-addnl-info a.post-author-name::attr(href)"
                ).get(),
            }
            yield response.follow(
                blog_url,
                self.parse_blog_detail,
                cb_kwargs={"blog_details": blog_details},
            )
