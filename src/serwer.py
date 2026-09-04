#!/usr/bin/env python3
"""VGM MCP — serwer Model Context Protocol do TradingView.

Zasada: **w serwerze są wyłącznie narzędzia uruchomione na żywym rynku.**
Nic „na zapas", nic „powinno działać". Czego nie sprawdziłem, tego tu nie ma —
lista brakujących rzeczy stoi otwarcie w README.

Wszystko działa bez logowania do TradingView i bez otwartej przeglądarki.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analiza  # noqa: E402
import dane  # noqa: E402
import pola  # noqa: E402

from mcp.server import Server  # noqa: E402
from mcp.server.stdio import stdio_server  # noqa: E402
from mcp.types import TextContent, Tool  # noqa: E402

serwer = Server("vgm-mcp")

UWAGA = ("Dane z publicznego punktu TradingView, liczone po ich stronie. "
         "To nie są kwotowania brokera — do handlu użyj ceny od swojego brokera.")

S = {"type": "string"}
L = {"type": "array", "items": {"type": "string"}}


def _n(nazwa, opis, wlasciwosci=None, wymagane=None):
    return Tool(
        name=nazwa,
        description=opis + " " + UWAGA,
        inputSchema={
            "type": "object",
            "properties": wlasciwosci or {},
            "required": wymagane or [],
        },
    )


@serwer.list_tools()
async def lista_narzedzi() -> list[Tool]:
    sym = {"symbol": dict(S, description="Nazwa z giełdą: FX:EURUSD, NASDAQ:NVDA, COINBASE:BTCUSD")}
    interw = {"interwal": dict(S, description="1, 5, 15, 60, 240, 1W. Pominięty = bieżący")}
    rynek = {"rynek": dict(S, description="forex, crypto, america, poland…", default="forex")}
    ile = {"ile": {"type": "integer", "default": 20}}

    return [
        # ── odczyt ──────────────────────────────────────────────────────
        _n("vgm_odczyt",
           "Wartości wybranych pól dla instrumentu. 62 dostępne pola: cena, wolumen, "
           "oscylatory pędu, wskaźniki trendu, średnie, zmienność, poziomy, wyniki, ocena.",
           {**sym, "pola": dict(L, description="Nazwy pól. Pominięte = zestaw domyślny")},
           ["symbol"]),

        _n("vgm_obraz",
           "PEŁNY obraz instrumentu: wszystkie 62 pola pogrupowane w dziewięć kategorii, "
           "jednym zapytaniem. Używaj, gdy chcesz zobaczyć całość naraz.",
           {**sym, **interw}, ["symbol"]),

        _n("vgm_pola",
           "Spis dostępnych pól z podziałem na grupy — sprawdź tu, zanim zgadniesz nazwę."),

        # ── położenie i układ ───────────────────────────────────────────
        _n("vgm_polozenie",
           "Gdzie stoi cena względem swoich odniesień, w procentach: miejsce w kanale "
           "Bollingera, miejsce w zakresie rocznym, odchylenie od średnich 20/50/200, "
           "szerokość kanału, zmienność ATR jako procent ceny.",
           {**sym, **interw}, ["symbol"]),

        _n("vgm_srednie",
           "Układ sześciu średnich wykładniczych (5 do 200): ile par stoi w kolejności "
           "rosnącej, ile w malejącej. Zwraca surowy fakt, nie nazywa go trendem.",
           {**sym, **interw}, ["symbol"]),

        # ── wiele interwałów ────────────────────────────────────────────
        _n("vgm_mtf",
           "Ten sam wskaźnik na kilku interwałach naraz, jednym zapytaniem. "
           "Zmierzone interwały: 1, 5, 15, 60, 240, 1W.",
           {**sym,
            "wskazniki": dict(L, description="np. RSI, ADX, Recommend.All"),
            "interwaly": L}, ["symbol"]),

        _n("vgm_zgodnosc",
           "Ile interwałów wskazuje w tę samą stronę. Zwraca zliczenie: które powyżej "
           "progu kupna, które poniżej progu sprzedaży. CELOWO nie podejmuje decyzji "
           "handlowej — próg należy do strategii i wymaga własnego pomiaru.",
           {**sym, "interwaly": L,
            "prog_kupno": {"type": "number", "default": 55},
            "prog_sprzedaz": {"type": "number", "default": 45}}, ["symbol"]),

        _n("vgm_zgodnosc_pelna",
           "Tabela wielu wskaźników na wielu interwałach naraz — rozszerzenie vgm_zgodnosc "
           "na dowolny zestaw. Zwraca wartości i listę brakujących.",
           {**sym, "wskazniki": L, "interwaly": L}, ["symbol"]),

        # ── porównania ──────────────────────────────────────────────────
        _n("vgm_wiele",
           "Kilka instrumentów w JEDNYM zapytaniu zamiast kilku osobnych.",
           {"symbole": L, "pola": L}, ["symbole"]),

        _n("vgm_porownaj",
           "Instrumenty obok siebie, posortowane po sile ruchu.",
           {"symbole": L, "pola": L}, ["symbole"]),

        # ── skany rynku ─────────────────────────────────────────────────
        _n("vgm_skan_wyprzedane",
           "Instrumenty z RSI poniżej progu.",
           {**rynek, "prog": {"type": "number", "default": 30}, **ile}),

        _n("vgm_skan_wykupione",
           "Instrumenty z RSI powyżej progu.",
           {**rynek, "prog": {"type": "number", "default": 70}, **ile}),

        _n("vgm_skan_trend",
           "Instrumenty z ADX powyżej progu — silny ruch kierunkowy. "
           "Zwraca też ADX+DI i ADX-DI, żeby było widać stronę.",
           {**rynek, "prog_adx": {"type": "number", "default": 30}, **ile}),

        _n("vgm_skan_wolumen",
           "Instrumenty z wolumenem powyżej wielokrotności średniej z dziesięciu dni.",
           {**rynek, "krotnosc": {"type": "number", "default": 2.0}, **ile}),

        _n("vgm_skan",
           "Dowolny filtr TradingView — pełna swoboda. Warunki w formacie "
           '[{"left":"RSI","operation":"less","right":30}]. '
           "Operacje: less, greater, equal, in_range, above_pct, below_pct.",
           {**rynek,
            "warunki": {"type": "array", "items": {"type": "object"}},
            "pola": L, **ile}, ["rynek", "warunki"]),
    ]


@serwer.call_tool()
async def wywolaj(nazwa: str, a: dict) -> list[TextContent]:
    def ok(x):
        return [TextContent(type="text", text=json.dumps(x, ensure_ascii=False, indent=1))]

    try:
        if nazwa == "vgm_odczyt":
            return ok(dane.odczyt(a["symbol"], a.get("pola")))
        if nazwa == "vgm_obraz":
            return ok(analiza.obraz(a["symbol"], a.get("interwal")))
        if nazwa == "vgm_pola":
            return ok({g: lista for g, lista in pola.GRUPY.items()}
                      | {"interwaly_zmierzone": pola.INTERWALY_PEWNE})
        if nazwa == "vgm_polozenie":
            return ok(analiza.polozenie(a["symbol"], a.get("interwal")))
        if nazwa == "vgm_srednie":
            return ok(analiza.uklad_srednich(a["symbol"], a.get("interwal")))
        if nazwa == "vgm_mtf":
            return ok(dane.mtf(a["symbol"], a.get("wskazniki"), a.get("interwaly")))
        if nazwa == "vgm_zgodnosc":
            return ok(dane.zgodnosc(a["symbol"], a.get("interwaly"),
                                    a.get("prog_kupno", 55), a.get("prog_sprzedaz", 45)))
        if nazwa == "vgm_zgodnosc_pelna":
            return ok(analiza.zgodnosc_pelna(a["symbol"], a.get("wskazniki"),
                                             a.get("interwaly")))
        if nazwa == "vgm_wiele":
            return ok(dane.wiele(a["symbole"], a.get("pola")))
        if nazwa == "vgm_porownaj":
            return ok(analiza.porownaj(a["symbole"], a.get("pola")))
        if nazwa == "vgm_skan_wyprzedane":
            return ok(analiza.skan_wyprzedane(a.get("rynek", "forex"),
                                              a.get("prog", 30), a.get("ile", 20)))
        if nazwa == "vgm_skan_wykupione":
            return ok(analiza.skan_wykupione(a.get("rynek", "forex"),
                                             a.get("prog", 70), a.get("ile", 20)))
        if nazwa == "vgm_skan_trend":
            return ok(analiza.skan_silny_trend(a.get("rynek", "forex"),
                                               a.get("prog_adx", 30), a.get("ile", 20)))
        if nazwa == "vgm_skan_wolumen":
            return ok(analiza.skan_wolumen(a.get("rynek", "forex"),
                                           a.get("krotnosc", 2.0), a.get("ile", 20)))
        if nazwa == "vgm_skan":
            return ok(analiza.skan_wlasny(a["rynek"], a["warunki"],
                                          a.get("pola"), a.get("ile", 30)))
        return ok({"blad": f"nieznane narzędzie: {nazwa}"})

    except dane.BladTV as e:
        return ok({"blad": str(e), "narzedzie": nazwa})
    except KeyError as e:
        return ok({"blad": f"brakuje wymaganego pola: {e}", "narzedzie": nazwa})


async def main():
    async with stdio_server() as (we, wy):
        await serwer.run(we, wy, serwer.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
