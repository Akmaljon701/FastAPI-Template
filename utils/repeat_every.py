from main import app
from fastapi_utils.tasks import repeat_every
import aiohttp


@app.on_event('startup')
@repeat_every(seconds=5, wait_first=False)
async def hi():
    async def fetch_url():
        print("aaaa")
        token = "Bot token"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        user_id = "user id"
        data = {
            'chat_id': user_id,
            'text': "Sent successfully"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.text()

        # api_url = "https://post_url/"
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(api_url) as response:
        #         await response.text()

    await fetch_url()
