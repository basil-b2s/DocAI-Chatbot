# # 2b714a1d073743a48cbd5a267cc846f3

# import requests

# api_key = "2b714a1d073743a48cbd5a267cc846f3"
# url = f"https://newsapi.org/v2/everything?q=health&language=en&apiKey={api_key}"
# response = requests.get(url)
# try:
#     response = requests.get(url)
#     news_data = response.json()

#     articles = news_data["articles"]

#     if articles:
#         for news_item in articles:
#             title = news_item["title"]
#             description = news_item["description"]
#             news_url = news_item["url"]

#             message = f"{title}\n\n{description}\n\nRead more: {news_url}"
#             print(message)
#     else:
#         print(text="No health news found at the moment. Please try again later.")

# except Exception as e:
#     print(text="Apologies, I couldn't fetch the health news at the moment. Please try again later.")

import os
print(os.getcwd()+"\\appointment.pdf")