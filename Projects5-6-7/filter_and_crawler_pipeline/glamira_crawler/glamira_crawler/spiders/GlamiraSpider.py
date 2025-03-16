import scrapy
from glamira_crawler.mongo_db import MongoDB


class GlamiraSpider(scrapy.Spider):
    name = "glamira"

    def start_requests(self):
        cursor = MongoDB().filter_data()
        for doc in cursor:
            product_id = doc["product_id"]
            current_url = doc["current_url"]
            if not product_id or not current_url:
                continue
            headers = {
                ":authority": "www.google.com",
                ":method": "GET",
                ":path": "/recaptcha/api2/anchor?ar=1&k=6LfjIBoTAAAAAHKfkXDTMLaAlKKEzCFDuaUUbcQ1&co=aHR0cHM6Ly93d3cuZ2xhbWlyYS5jb20uYXU6NDQz&hl=en&v=IyZ984yGrXrBd6ihLOYGwy9X&theme=light&size=normal&cb=w5l5vxitf0pm",
                ":scheme": "https",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.9,vi;q=0.8",
                "cookie": "__Secure-3PAPISID=uVM4k_JEgFEjRBlk/AwfnwBVxARMzNMTuP; __Secure-3PSID=g.a000rgie7Slz2FWJylBQ_kYrhUgVXqRvtBi8hoAgqM24zwUCuRmMxYZPbc43d3HrM_9B2ahH-AACgYKAakSARYSFQHGX2Mi5GG1ZR7l5XSxeJEiXbwB2RoVAUF8yKqLWOABtOiDo456oOBKAYsW0076; __Secure-3PSIDTS=sidts-CjEB7wV3sR90CKWduRUNb7ceGxzeT4vXmCNTC1jwogpFY1p2nD6IOYXMqVgjDd_ajAjzEAA; NID=520=jBxpeDzIWgQV7r1crOnakAdS1xZzwRLS4Awq8hMd9HrQs4k5u_736jqppT4Wpgju_1dhjqsHC89H6iE5OvbDA7sy36UJ9qAW3YsQZetNigeBLmdUTwugc4BBe4r8oEiIDNdrydER7OyIqFiRmYicRw5GQ4NPRWfiMAHeyAVWi_ftbD9rhGzJQDqn0YBc6dGxQPL3n4jZJe1zg51OSpe1Mw7cIqinMQUYqn4fCqlJgyAgd4ofkC7HbauUwlTgSrMhiGVy6ImHxkGarN-DaZVJrWMeEH_UiAJD5Q6s8ieg5QxuNTaOdLt3akRmyiiE-OhQRAKdyK79n744RUOLTRIb3Jbk1acA7C6MS60RVd1Irnz4xKukO0HxGbwTpq6tlODptu9_8e7qTWXe8PJPVfU8Z9hqecNUZQlzScg; __Secure-3PSIDCC=AKEyXzUU-Rdh-Pv4L3R59k4O7RxUINHtY2YLvUoD1LFcSaWanzGUqBTgedJ4z8a-btdK1Q9sAA",
                "priority": "u=0, i",
                "referer": "https://www.glamira.com.au/",
                "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "iframe",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "sec-fetch-storage-access": "active",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
            }

            cookies = {
                "__Secure-3PAPISID": "uVM4k_JEgFEjRBlk/AwfnwBVxARMzNMTuP",
                "__Secure-3PSID": "g.a000rgie7Slz2FWJylBQ_kYrhUgVXqRvtBi8hoAgqM24zwUCuRmMxYZPbc43d3HrM_9B2ahH-AACgYKAakSARYSFQHGX2Mi5GG1ZR7l5XSxeJEiXbwB2RoVAUF8yKqLWOABtOiDo456oOBKAYsW0076",
                "__Secure-3PSIDTS": "sidts-CjEB7wV3sR90CKWduRUNb7ceGxzeT4vXmCNTC1jwogpFY1p2nD6IOYXMqVgjDd_ajAjzEAA",
                "NID": "520=jBxpeDzIWgQV7r1crOnakAdS1xZzwRLS4Awq8hMd9HrQs4k5u_736jqppT4Wpgju_1dhjqsHC89H6iE5OvbDA7sy36UJ9qAW3YsQZetNigeBLmdUTwugc4BBe4r8oEiIDNdrydER7OyIqFiRmYicRw5GQ4NPRWfiMAHeyAVWi_ftbD9rhGzJQDqn0YBc6dGxQPL3n4jZJe1zg51OSpe1Mw7cIqinMQUYqn4fCqlJgyAgd4ofkC7HbauUwlTgSrMhiGVy6ImHxkGarN-DaZVJrWMeEH_UiAJD5Q6s8ieg5QxuNTaOdLt3akRmyiiE-OhQRAKdyK79n744RUOLTRIb3Jbk1acA7C6MS60RVd1Irnz4xKukO0HxGbwTpq6tlODptu9_8e7qTWXe8PJPVfU8Z9hqecNUZQlzScg",
                "__Secure-3PSIDCC": "AKEyXzVabhpmj73c6D3LuaQO8AXAj3AYK_Y3h2amm3VyuZML4blSDB73xhIH5yoHV80g9cGfVw",
            }
            yield scrapy.Request(
                url=current_url,
                headers=headers,
                cookies=cookies,
                callback=self.parse,
                meta={"product_id": product_id},
            )

    def parse(self, response):
        product_id = response.meta["product_id"]
        product_name = response.xpath(
            '//*[@id="maincontent"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/h1/span/text()'
        ).get()
        yield {"product_id": product_id, "product_name": product_name}
