import json
import random
import string
import time

import httpx
from django.http import HttpRequest, JsonResponse
from django.urls import path

ALPHAVANTAGE_API_KEY: str = "N57CVYU83F19L5UR"
last_api_call_time = 0.0
cached_rate = None


def create_random_string(size: int) -> str:
    return "".join([random.choice(string.ascii_letters) for _ in range(size)])


def generate_article(request: HttpRequest):
    return JsonResponse(
        {
            "title": create_random_string(size=10),
            "description": create_random_string(size=20),
        }
    )


async def get_current_market_state(request: HttpRequest):
    global last_api_call_time, cached_rate

    if time.time() - last_api_call_time < 10 and cached_rate:
        return JsonResponse({"rate": cached_rate})

    elif request.method == "GET":
        return JsonResponse({"message": "Endpoint only accepts POST requests"})

    elif request.method == "POST":
        data = json.loads(request.body)
        from_currency = data.get("from_currency")
        to_currency = data.get("to_currency")
        url = (
            f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&"
            f"from_currency={from_currency}&to_currency={to_currency}&"
            f"apikey={ALPHAVANTAGE_API_KEY}"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        rate = response.json()["Realtime Currency Exchange Rate"][
            "5. Exchange Rate"
        ]

        cached_rate = rate
        last_api_call_time = time.time()

        return JsonResponse({"rate": rate})


urlpatterns = [
    path("exchange-rates", get_current_market_state),  # type: ignore
    path("generate-article", generate_article),
]
