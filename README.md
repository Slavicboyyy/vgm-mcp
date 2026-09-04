# VGM MCP

**Velarion Growth Matrix** — serwer MCP do TradingView. Odczyt wskaźników i przegląd
rynku **bez logowania i bez otwartej przeglądarki**.

Powstał przez przejrzenie 17 istniejących serwerów MCP do TradingView i wzięcie z nich
tego, co działa, bez wad każdego z osobna.

## Co działa dzisiaj

Pięć narzędzi. Każde uruchomione na żywym rynku przed umieszczeniem tutaj.

| narzędzie | co robi |
|---|---|
| `vgm_odczyt` | cena, zmiana, wolumen i wskaźniki dla jednego instrumentu |
| `vgm_wiele` | to samo dla wielu instrumentów w jednym zapytaniu |
| `vgm_przeglad` | przegląd rynku z filtrem, np. wszystko z RSI poniżej 30 |
| `vgm_mtf` | ten sam wskaźnik na kilku interwałach naraz |
| `vgm_zgodnosc` | ile interwałów wskazuje w tę samą stronę |

Dostępne wskaźniki: RSI, ADX, MACD, ATR, CCI, Momentum, Stochastic, Awesome Oscillator,
średnie SMA i EMA (5–200), VWMA, Hull, wstęgi Bollingera, punkty zwrotne oraz zbiorcza
ocena TradingView.

Zmierzone działające interwały: `1`, `5`, `15`, `60`, `240`, `1W`.

## Przykład

```python
from src import dane

dane.odczyt("FX:EURUSD", ["close", "RSI", "SMA50", "ATR"])
# {'close': 1.1619, 'RSI': 56.09, 'SMA50': 1.15077, 'ATR': 0.0046}

dane.mtf("FX:EURUSD", ["RSI"], ["5", "15", "60", "240"])
# {'RSI': {'5': 41.8, '15': 38.6, '60': 48.8, '240': 53.3}}

dane.przeglad("forex", [{"left": "RSI", "operation": "less", "right": 30}])
# pary wyprzedane, posortowane po zmianie
```

## Instalacja

Wymaga Pythona 3.10 lub nowszego i pakietu `mcp`.

```bash
pip install mcp
```

W konfiguracji klienta MCP:

```json
{
  "mcpServers": {
    "vgm": {
      "command": "python3",
      "args": ["/ścieżka/do/vgm-mcp/src/serwer.py"]
    }
  }
}
```

Sprawdzenie warstwy danych bez klienta MCP:

```bash
python3 src/dane.py
```

## Czego tu NIE ma

Uczciwa lista. Te rzeczy są zaplanowane, ale **niezbudowane i niesprawdzone** —
nie ma ich w serwerze, żeby nikt nie liczył na coś, co nie istnieje.

| brakuje | dlaczego jeszcze nie |
|---|---|
| sterowanie wykresem | wymaga przeglądarki — kolejny krok |
| Pine Script: pisanie i sprawdzanie | wymaga przeglądarki i konta |
| Strategy Tester | wymaga przeglądarki, a jego wyniki i tak są tylko poglądowe |
| świece historyczne | inny punkt dostępu, jeszcze niesprawdzony |
| zrzuty wykresu | wymaga przeglądarki |

## Ograniczenia, o których trzeba wiedzieć

**To nie są kwotowania brokera.** Dane pochodzą z publicznego punktu TradingView
i są liczone po ich stronie. Do handlu używaj ceny od swojego brokera — różnice
w cenie i spreadzie są normalne.

**Interwał `1D` bywa pusty.** Tak zachowuje się TradingView, nie jest to błąd serwera.
Narzędzie zwraca wtedy wartość pustą, a `vgm_zgodnosc` wypisuje taki interwał
osobno w polu `bez_danych`.

**`vgm_zgodnosc` celowo nie podejmuje decyzji handlowej.** Zwraca surowe zliczenie:
które interwały są powyżej progu kupna, które poniżej progu sprzedaży. Próg i sposób
łączenia należą do strategii i wymagają własnego pomiaru — wpisanie ich tutaj
sugerowałoby przewagę, której nikt nie zmierzył.

**Odstęp między zapytaniami: 1,2 sekundy.** Wymuszony w kodzie. Przy odpowiedzi
403 albo 429 serwer **zatrzymuje się i nie ponawia** — ponawianie przy tych kodach
prowadzi do blokady adresu.

## Skąd to się wzięło

Przejrzane projekty i ich narzędzia: [`inwentarz.md`](inwentarz.md).

Z 17 projektów tylko 8 ma licencję MIT. Pozostałe nie mają jasnej licencji, więc
**nie użyto z nich ani linijki kodu** — posłużyły wyłącznie jako podpowiedź, jak
nazywać polecenia.

## Licencja

MIT.
