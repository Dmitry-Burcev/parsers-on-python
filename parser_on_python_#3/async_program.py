# было синхронно

# import time

# def load_data_sync(name, delay):
#     """Синхронно загружает данные (имитация запроса к серверу)"""
#     print(f"🟡 Начинаю загрузку: {name}")
#     time.sleep(delay)  # Имитация долгой операции
#     print(f"🟢 Загрузка завершена: {name}")
#     return f"Данные от {name} (заняло {delay} сек)"


# стало асинхронно
import asyncio

async def load_data_async(delay, name):
    print(f"🟡 Начинаю загрузку: {name}")   
    await asyncio.sleep(delay)
    print(f"🟢 Загрузка завершена: {name}")
    return f"Данные от {name} (заняло {delay} сек)" 

async def main():
    await asyncio.gather(load_data_async(2, "site_1"), load_data_async(1, "site_2"), load_data_async(3, "site_3")) 

if __name__ == "__main__":
    asyncio.run(main())