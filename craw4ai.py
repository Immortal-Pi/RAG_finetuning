import asyncio
from crawl4ai import AsyncWebCrawler
import sys

async def crawl_url(crawler, url):
    result = await crawler.arun(
        url=url,
        #word_count_threshold=10,
        excluded_tags=['form', 'header'],
        exclude_external_links=True,
        process_iframes=True,
        remove_overlay_elements=True,
        bypass_cache=False,
        
        word_count_threshold=10,
        exclude_external_images=True
        
    )

    if result.success:
        content = f"URL: {url}\n"
        content += f"Content:\n{result.markdown}\n"
        content += "Internal Links:\n" + "\n".join(link['href'] for link in result.links["internal"]) + "\n"
        content += f"Metadata:\n{result.metadata}\n"
        return content
    else:
        return f"Failed to crawl {url}\n"

async def main(url):
    initial_url = url
    all_content = ""

    async with AsyncWebCrawler(verbose=True) as crawler:
        # Crawl the initial URL
        initial_result = await crawl_url(crawler, initial_url)
        all_content += initial_result

        # Extract internal links from the initial crawl
        result = await crawler.arun(url=initial_url)
        if result.success:
            internal_links = [link['href'] for link in result.links["internal"]]

            # Crawl internal links
            for link in internal_links:
                link_result = await crawl_url(crawler, link)
                all_content += link_result

        # Print the combined content
        print(all_content)

        # Optionally, save to a file
        with open("data/crawled_data.txt", "w", encoding="utf-8") as f:
            f.write(all_content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(url)
        asyncio.run(main(url))

    else:
        print("No URL provided.")