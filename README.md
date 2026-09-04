# VGM MCP

Serwer MCP do TradingView. Czyta rynek bez logowania i bez otwartej przeglądarki.

Piętnaście narzędzi. Sześćdziesiąt dwa pola danych. Sześć przedziałów czasowych naraz,
jednym zapytaniem.

---

## Dlaczego powstał

Na GitHubie leży 410 projektów z „tradingview mcp" w nazwie. Sklonowałem czternaście
największych i policzyłem, co naprawdę mają w kodzie, a nie w opisie, bo opisy potrafią kłamać.
Wyszło 598 narzędzi, z czego 246 to osobne nazwy. Reszta to kopie i widełki tego samego.

Wnioski z tego liczenia były trzy.

Po pierwsze, prawie wszystkie wymagają aplikacji TradingView Desktop albo własnego okna
przeglądarki. Czyli nie ruszą na serwerze ani w tle, a już na pewno nie bez człowieka przy monitorze.

Po drugie, żaden nie sięga po pełen zestaw pól, który TradingView udostępnia publicznie.
Biorą sześć, czasem dwanaście, a przy sprawdzeniu okazało się, że działa sześćdziesiąt dwa.

Po trzecie, licencje. Z siedemnastu przejrzanych repozytoriów tylko osiem ma MIT, a pozostałe
nie mają żadnej, więc formalnie nikt nie ma prawa użyć ich kodu. Z tych nie wziąłem
ani linijki. Posłużyły za podpowiedź, jak nazywać polecenia, i tyle.

---

## Co potrafi

### Odczyt

| narzędzie | do czego |
|---|---|
| `vgm_odczyt` | wybrane pola dla instrumentu |
| `vgm_obraz` | wszystkie 62 pola naraz, w dziewięciu grupach |
| `vgm_pola` | spis dostępnych pól, do sprawdzenia przed zgadywaniem nazwy |

### Położenie ceny

| narzędzie | do czego |
|---|---|
| `vgm_polozenie` | gdzie stoi cena w kanale Bollingera, w rozpiętości rocznej, względem średnich |
| `vgm_srednie` | układ sześciu średnich wykładniczych od 5 do 200 |

### Wiele przedziałów czasu

| narzędzie | do czego |
|---|---|
| `vgm_mtf` | ten sam wskaźnik na kilku przedziałach, jednym zapytaniem |
| `vgm_zgodnosc` | ile przedziałów wskazuje w tę samą stronę |
| `vgm_zgodnosc_pelna` | tabela wielu wskaźników na wielu przedziałach |

### Porównania i skany

| narzędzie | do czego |
|---|---|
| `vgm_wiele` | kilka instrumentów w jednym zapytaniu |
| `vgm_porownaj` | instrumenty obok siebie, po sile ruchu |
| `vgm_skan_wyprzedane` | RSI poniżej progu |
| `vgm_skan_wykupione` | RSI powyżej progu |
| `vgm_skan_trend` | ADX powyżej progu, z kierunkiem |
| `vgm_skan_wolumen` | wolumen ponad wielokrotność średniej z dziesięciu dni |
| `vgm_skan` | dowolny filtr TradingView |

---

## Dane, do których sięga

Sześćdziesiąt dwa pola, wszystkie sprawdzone na żywym rynku:

**Cena.** Otwarcie, zamknięcie, szczyt, dołek, luka, zmiana, VWAP
**Wolumen.** Bieżący, średnia dziesięciodniowa, stosunek jednego do drugiego
**Pęd.** RSI, RSI7, Stochastic K i D, Stochastic RSI, CCI, Momentum, Awesome, ROC, Ultimate, Williams
**Trend.** ADX z obiema składowymi kierunkowymi, MACD z linią i histogramem, Parabolic SAR, Ichimoku
**Średnie.** SMA i EMA po sześć każda, od 5 do 200, plus VWMA i Hull
**Zmienność.** ATR, wstęgi Bollingera, siła wstęg, zmienność dzienna i tygodniowa
**Poziomy.** Punkty zwrotne klasyczne i Fibonacciego, szczyt i dołek z roku
**Wyniki.** Tydzień, miesiąc, od początku roku
**Ocena.** Zbiorcza TradingView, osobno dla średnich i oscylatorów

Każde z tych pól przyjmuje przyrostek z przedziałem czasu. `RSI|240` daje RSI z czterech godzin. Zmierzone przedziały: 1, 5, 15, 60, 240 minut oraz tydzień.

Sześćdziesiąt dwa pola razy sześć przedziałów to 372 wartości. Jedno zapytanie.

---

## Jak zacząć

```bash
pip install mcp
```

W ustawieniach klienta MCP:

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

Sprawdzenie bez klienta MCP:

```bash
python3 src/dane.py      # warstwa danych
python3 src/analiza.py   # warstwa analizy
python3 src/pola.py      # sprawdza, czy wszystkie 62 pola nadal działają
```

Ostatnie polecenie warto puścić, kiedy coś zacznie zwracać puste wartości. Powie,
która grupa pól przestała odpowiadać.

---

## Z kodu, nie z opisu

```python
from src import analiza

analiza.polozenie("FX:EURUSD")
# cena 1.16211
# w kanale Bollingera: 56.7%
# w rozpiętości rocznej: 39.1%
# nad EMA200: +0.47%
# szerokość kanału: 1.79% ceny
# ATR: 0.395% ceny

analiza.zgodnosc_pelna("FX:EURUSD")
# RSI       1min 54.4 | 5min 51.8 | 15min 45.3 | 60min 51.3
# ADX       1min 29.3 | 5min 23.6 | 15min 21.7 | 60min 26.3
# MACD.hist 1min -0.0 | 5min  0.0 | 15min -0.0 | 60min -0.0

analiza.skan_silny_trend("forex", prog_adx=30)
# instrumenty z ADX ponad 30, z kierunkiem
```

---

## Czego tu nie ma

Lista jawna. Lepiej wiedzieć z góry, niż odkryć w trakcie.

| brakuje | powód |
|---|---|
| sterowanie wykresem | potrzebna przeglądarka, następny krok |
| Pine Script | potrzebna przeglądarka i konto |
| Strategy Tester | potrzebna przeglądarka, a wyniki i tak tylko poglądowe |
| świece historyczne | inne źródło, jeszcze niesprawdzone |
| zrzuty wykresu | potrzebna przeglądarka |

Te rzeczy są zaplanowane, ale żadnej nie ma w kodzie. Nie chcę, żeby ktoś liczył
na coś, czego nie zbudowałem.

---

## Co trzeba wiedzieć, zanim się użyje

**To nie są ceny brokera.** Dane idą z publicznego punktu TradingView i są liczone
po ich stronie. Twój broker pokaże inną cenę i inny spread. Do handlu bierz jego.

**Przedział dzienny bywa pusty.** Tak zachowuje się TradingView. Narzędzie zwraca
wtedy wartość pustą i wypisuje taki przedział osobno, w polu `bez_danych`.

**`vgm_zgodnosc` nie mówi „kupuj".** Zwraca liczby: tyle przedziałów powyżej progu,
tyle poniżej. Próg jest w parametrze, bo należy do strategii. Wpisanie go na sztywno
sugerowałoby przewagę, której nikt nie zmierzył. To najdroższy rodzaj kłamstwa w handlu.

**Odstęp między zapytaniami: 1,2 sekundy.** Wymuszony w kodzie. Przy odpowiedzi 403
albo 429 serwer staje i nie ponawia. Ponawianie przy tych kodach kończy się blokadą adresu.
Sprawdzone drogą doświadczenia.

---

## Skąd wzięte

Pełna lista przejrzanych projektów wraz z tym, co każdy ma w kodzie: [`inwentarz.md`](inwentarz.md).

---

## Licencja

MIT. Rób, co chcesz.
