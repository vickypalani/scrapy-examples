# Scrapy Examples

This project shows how to use Scrapy, a Python framework for web crawling and scraping, to extract data from a website that has pagination and forms. This project serves as example for various Scrapy concepts.

### Basic scraping of list and detail pages

Site link: https://laravel-news.com/blog <br />
Spider reference: https://github.com/vickypalani/scrapy-examples/blob/main/laravel/laravel/spiders/laravel_news.py <br />
Description: This spider crawls through the list and detail pages of the Laravel News blog. 

The spider uses the `parse` method to scrape the list page, and the `parse_article` method to scrape the detail page. 

To run the spider: `scrapy crawl laravel_news`

Sample Output: https://github.com/vickypalani/scrapy-examples/blob/main/laravel/laravel_new.json

### Scraping sites with form submission and starting the spider with additional arguments

Site link: https://www.cloudways.com/blog/laravel/ <br />
Spider reference: https://github.com/vickypalani/scrapy-examples/blob/main/laravel/laravel/spiders/cloudways.py <br />
Description: This spider scrapes the Cloudways blog, which has a form that allows the user to filter the posts by category and page number. The spider submits the form with the desired category and page number. This spider implements the following concepts
- `FormRequest()` method is used to load additional data. (This allows us to submit a form through scrapy)
- This also serves as a reference for accepting input arguments from the client: max_page_num, which defaults to 2.

To run the spider: `scrapy crawl cloudways -a max_page_num=<any number>` 

Sample Output: https://github.com/vickypalani/scrapy-examples/blob/main/laravel/cloudways.json
