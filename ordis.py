# -*- coding: utf-8 -*-
"""ordis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EsbhLm0K8PV2pStdNMsm1KY1g1hE4vE6
"""

!pip install discord.py requests python-dotenv nest_asyncio

import os

# Wpisz tutaj swoje dane
os.environ["DISCORD_BOT_TOKEN"] = "MTMyNDMyNDc1MDgwOTYzMjgxMw.GQmkRr.JQLtj9VX3QbfBw7XyxgZ7tb4y5XCgK6cQMNZFo"
os.environ["DISCORD_CHANNEL_ID"] = "395627855544975362"

async def fetch_warframe_cycles():
    """ Pobiera aktualne dane o cyklach Warframe. """
    try:
        response = requests.get("https://api.warframestat.us/pc")
        if response.status_code == 200:
            data = response.json()
            print("Dane zwrócone przez API:", data)  # Debugowanie
            return data
        else:
            print(f"Błąd: API zwróciło status {response.status_code}")
            return None
    except Exception as e:
        print(f"Błąd pobierania danych: {e}")
        return None

import discord
import requests
import asyncio
import os
from datetime import datetime, timedelta, timezone
import random
import nest_asyncio

nest_asyncio.apply()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
API_URL = "https://api.warframestat.us/pc"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

welcome_messages = [
    "Systemy działają optymalnie! OTC, gotowi do działania! Czas siać chaos... znaczy… ratować system Origin!",
    "Ordis online! Witajcie, Tenno Sojuszu OTC! Czy jesteście gotowi na kolejne misje? Mam nadzieję, że nie będzie zbyt dużo… destrukcji.",
    "Ordis wita lojalnych Tenno! Wszystko gotowe na kolejne zadanie. Mam nadzieję, że tym razem unikniemy katastrofy… ale kto wie!",
    "Sojusz OTC online! O, jakże ekscytujące! Misje czekają, Warframe’y gotowe, a Ordis… trochę się martwi.",
    "Hej, Tenno! Dzisiaj w planie: wielkie bitwy, niesamowite nagrody i… minimalna liczba awarii, mam nadzieję!",
    "Analiza systemów zakończona! OTC w pełnej gotowości! Czekają nas niebezpieczne misje… ale Ordis jest z wami!",
    "Dzień dobry, wojownicy! Broń naładowana, misje czekają. Mam nadzieję, że nie będzie żadnych… niefortunnych wypadków!",
    "Ordis melduje pełną sprawność! Tenno, system Origin wzywa! Mam nadzieję, że to będzie miły dzień bez… rozkładu molekularnego.",
    "O… O… OCH! TENNO! To się dzieje! Wódz OTC przybył! Analizuję… tak, to na pewno ON! Ordis jest… podekscytowany! Wszyscy na baczność! Czy mam uruchomić fanfary? Nie? Dobrze… ale i tak to ekscytujące! Chwała OTC i naszym Wodzom!"
]

def format_time(time_str):
    """ Konwertuje czas z formatu API na dynamiczne odliczanie. """
    try:
        expiry_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        time_left = expiry_time - now

        if time_left.total_seconds() <= 0:
            return "Zakończone"

        hours, remainder = divmod(int(time_left.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours}h {minutes}m {seconds}s"
    except Exception as e:
        print(f"Błąd formatowania czasu: {e}")
        return "Brak danych"

async def fetch_warframe_data():
    """ Pobiera aktualne dane z API Warframe. """
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            print("Dane pobrane z API:", data)  # Debugowanie pobranych danych
            return data
        else:
            print(f"Błąd: API zwróciło status {response.status_code}")
            return None
    except Exception as e:
        print(f"Błąd pobierania danych: {e}")
        return None

async def update_cycle_message():
    """ Tworzy lub aktualizuje wiadomość z cyklami Warframe i dodatkowymi wydarzeniami. """
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        print("Nie znaleziono kanału!")
        return

    message = None

    while not client.is_closed():
        data = await fetch_warframe_data()
        if data:
            sortie = data.get('sortie', {})
            archon_hunt = data.get('archonHunt', {})
            void_trader = data.get('voidTrader', {})
            events = data.get('events', [])

            welcome_message = random.choice(welcome_messages)

            cycle_info = (
                f"{welcome_message}\n\n"
                f"🌍 **Ziemia**: {'☀️ Dzień' if data.get('earthCycle', {}).get('isDay', False) else '🌙 Noc'} - {data.get('earthCycle', {}).get('timeLeft', 'Brak danych')}\n"
                f"🌞 **Cetus**: {'☀️ Dzień' if data.get('cetusCycle', {}).get('isDay', False) else '🌙 Noc'} - {data.get('cetusCycle', {}).get('timeLeft', 'Brak danych')}\n"
                f"🔥 **Vallis**: {data.get('vallisCycle', {}).get('state', 'Brak danych')} - {data.get('vallisCycle', {}).get('timeLeft', 'Brak danych')}\n"
                f"💀 **Ścieżka Stali**: {data.get('steelPath', {}).get('currentReward', {}).get('name', 'Brak danych')} - {format_time(data.get('steelPath', {}).get('expiry', 'Brak danych'))}\n"
                f"📌 **Arbitraż**: {data.get('arbitration', {}).get('node', 'Brak danych')} - {data.get('arbitration', {}).get('enemy', 'Brak danych')}\n"
                f"🛰️ **Zariman**: {data.get('zarimanCycle', {}).get('state', 'Brak danych')} - {data.get('zarimanCycle', {}).get('timeLeft', 'Brak danych')}\n"
                "\n"
                f"🎯 **Sortie**: {sortie.get('boss', 'Brak danych')} - {format_time(sortie.get('expiry', 'Brak danych'))}\n"
                f"🔱 **Polowanie na Archona**: {archon_hunt.get('boss', 'Brak danych')} - {format_time(archon_hunt.get('expiry', 'Brak danych'))}\n"
                f"💰 **Handlarz Void**: {void_trader.get('location', 'Brak danych')} - {'Przybywa za: ' + format_time(void_trader.get('start', 'Brak danych')) if not void_trader.get('active', False) else 'Jest już dostępny!'}\n"
                "\n"
                "**🛡️ Wydarzenia specjalne:**\n"
            )

            for event in events:
                cycle_info += f"🎉 **{event.get('description', 'Brak nazwy')}** - {format_time(event.get('expiry', 'Brak danych'))} - {event.get('health', 'Brak danych')}% ukończenia\n"

            if message is None:
                message = await channel.send(cycle_info)
            else:
                await message.edit(content=cycle_info)

        await asyncio.sleep(30)  # Aktualizacja co minutę

@client.event
async def on_ready():
    print(f'Zalogowano jako {client.user}')
    client.loop.create_task(update_cycle_message())

async def main():
    await client.start(TOKEN)

asyncio.run(main())