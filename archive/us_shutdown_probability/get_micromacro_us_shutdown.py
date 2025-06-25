import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        # go to the macromicro page
        await page.goto("https://en.macromicro.me/series/46814/us-chance-that-us-government-shutdown-in-2025")
        await page.wait_for_timeout(5000)  # wait for js to load

        # click data download
        await page.click("text=Data Download")
        await page.click("input[type='checkbox']")
        await page.click("text=Download")

        # download the file
        download = await page.wait_for_event('download')
        path = await download.path()
        dest = os.path.join(os.getcwd(), download.suggested_filename)
        await download.save_as(dest)
        print(f"Downloaded to {dest}")

        await browser.close()

asyncio.run(run())
