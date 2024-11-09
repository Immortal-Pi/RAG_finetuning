import asyncio
from crawl4ai import AsyncWebCrawler
import nest_asyncio
nest_asyncio.apply()
async def main(url):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        # print(result.markdown)
        return result.markdown

def crawl_4ai(url):
    return asyncio.run(main(url))

data=crawl_4ai(url="https://www.nbcnews.com/business")
print(data)

# if __name__ == "__main__":
#     data=crawl_4ai(url="https://www.nbcnews.com/business")
#     print(data)