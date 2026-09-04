#!/usr/bin/env python3
"""VGM MCP — serwer Model Context Protocol do TradingView.

Zasada, według której powstał: **w serwerze są wyłącznie narzędzia, które
zostały uruchomione na żywym rynku i zwróciły prawdziwe dane.** Nic „na zapas",
nic „powinno działać". Czego nie sprawdziłem, tego tu nie ma — plan reszty
jest w README, jawnie oznaczony jako niezbudowany.

Wszystkie narzędzia działają bez logowania do TradingView i bez otwartej
przeglądarki. Korzystają z publicznego punktu `scanner.tradingview.com`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dane  # noqa: E402

from mcp.server import Server  # noqa: E402
from mcp.server.stdio import stdio_server  # noqa: E402
from mcp.types import TextContent, Tool  # noqa: E402

serwer = Server("vgm-mcp")

OSTRZEZENIE_DANE = (
    "Dane pochodzą z publicznego punktu TradingView i są liczone po ich stronie. "
    "Nie są kwotowaniem brokera — do handlu użyj ceny od swojego brokera."
)


@serwer.list_tools()
async def lista_narzedzi() -> list[Tool]:
    return [
        Tool(
            name="vgm_odczyt",
            description=(
                "Bieżące wartości dla jednego instrumentu: cena, zmiana, wolumen "
                "i wskaźniki policzone przez TradingView (RSI, ADX, MACD, ATR, "
                "średnie, wstęgi Bollingera, punkty zwrotne). Bez logowania, "
                "bez przeglądarki. " + OSTRZEZENIE_DANE
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Nazwa z giełdą, np. FX:EURUSD, NASDAQ:NVDA, COINBASE:BTCUSD",
                    },
                    "pola": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Nazwy pól TradingView. Pominięte = zestaw domyślny.",
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="vgm_wiele",
            description=(
                "To samo dla wielu instrumentów w JEDNYM zapytaniu, zamiast kilku "
                "osobnych. Używaj, gdy porównujesz pary. " + OSTRZEZENIE_DANE
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "symbole": {"type": "array", "items": {"type": "string"}},
                    "pola": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["symbole"],
            },
        ),
        Tool(
            name="vgm_przeglad",
            description=(
                "Przegląd rynku z filtrem — np. wszystkie pary z RSI poniżej 30. "
                "Zwraca listę posortowaną po zmianie. " + OSTRZEZENIE_DANE
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "rynek": {
                        "type": "string",
                        "description": "forex, crypto, america, poland…",
                        "default": "forex",
                    },
                    "warunki": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": 'Filtr TradingView, np. [{"left":"RSI","operation":"less","right":30}]',
                    },
                    "ile": {"type": "integer", "default": 30},
                },
            },
        ),
        Tool(
            name="vgm_mtf",
            description=(
                "Ten sam wskaźnik na kilku interwałach naraz, jednym zapytaniem. "
                "Zmierzone działające interwały: 1, 5, 15, 60, 240, 1W. "
                "Interwał 1D bywa zwracany jako pusty — to zachowanie TradingView, "
                "nie błąd tego narzędzia. " + OSTRZEZENIE_DANE
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "wskazniki": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "np. RSI, ADX, Recommend.All",
                    },
                    "interwaly": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "np. 5, 15, 60, 240",
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="vgm_zgodnosc",
            description=(
                "Ile interwałów wskazuje w tę samą stronę. Zwraca surowe zliczenie: "
                "które interwały są powyżej progu kupna, które poniżej progu sprzedaży. "
                "CELOWO nie podejmuje decyzji handlowej — próg i sposób łączenia "
                "należą do strategii i wymagają własnego pomiaru. " + OSTRZEZENIE_DANE
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interwaly": {"type": "array", "items": {"type": "string"}},
                    "prog_kupno": {"type": "number", "default": 55},
                    "prog_sprzedaz": {"type": "number", "default": 45},
                },
                "required": ["symbol"],
            },
        ),
    ]


@serwer.call_tool()
async def wywolaj(nazwa: str, argumenty: dict) -> list[TextContent]:
    def odpowiedz(obiekt) -> list[TextContent]:
        return [TextContent(type="text",
                            text=json.dumps(obiekt, ensure_ascii=False, indent=1))]

    try:
        if nazwa == "vgm_odczyt":
            return odpowiedz(dane.odczyt(argumenty["symbol"], argumenty.get("pola")))
        if nazwa == "vgm_wiele":
            return odpowiedz(dane.wiele(argumenty["symbole"], argumenty.get("pola")))
        if nazwa == "vgm_przeglad":
            return odpowiedz(dane.przeglad(
                argumenty.get("rynek", "forex"),
                argumenty.get("warunki"),
                None,
                argumenty.get("ile", 30),
            ))
        if nazwa == "vgm_mtf":
            return odpowiedz(dane.mtf(
                argumenty["symbol"],
                argumenty.get("wskazniki"),
                argumenty.get("interwaly"),
            ))
        if nazwa == "vgm_zgodnosc":
            return odpowiedz(dane.zgodnosc(
                argumenty["symbol"],
                argumenty.get("interwaly"),
                argumenty.get("prog_kupno", 55),
                argumenty.get("prog_sprzedaz", 45),
            ))
        return odpowiedz({"blad": f"nieznane narzędzie: {nazwa}"})

    except dane.BladTV as e:
        # Błąd TradingView oddajemy w całości — wywołujący ma wiedzieć, co się stało,
        # a nie dostać pustą odpowiedź do interpretacji.
        return odpowiedz({"blad": str(e), "narzedzie": nazwa})
    except KeyError as e:
        return odpowiedz({"blad": f"brakuje wymaganego pola: {e}", "narzedzie": nazwa})


async def main():
    async with stdio_server() as (we, wy):
        await serwer.run(we, wy, serwer.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
