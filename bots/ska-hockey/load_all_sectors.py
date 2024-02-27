from user import User
from tickets import Tickets
from main import Main
import asyncio

# async def main():
#     acc = {
#             "login": "mikheyev98@gmail.com",
#             "password": "Ai5F,;baB:rVf!8"
#         }
#     user_3 = User(proxy="77.83.149.10:3000@2Xf9Go:5oVzj0pUFD", account=acc)
#     x = await user_3.make_session()
#     print(x)
async def main():
    worker = Main('https://tickets.ska.ru/view-available-zones/2025')
    res = await worker.main()

asyncio.run(main())