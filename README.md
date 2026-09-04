# VGM MCP

Serwer MCP do TradingView. Czyta rynek bez logowania i bez otwartej przeglądarki.

Trzydzieści siedem narzędzi plus polecenie w terminalu. Dziewięćdziesiąt jeden pól danych. Sześć przedziałów czasowych
naraz, jednym zapytaniem.

Większość działa bez logowania i bez przeglądarki. Reszta steruje otwartą kartą
z wykresem.

---

## Dlaczego powstał

Większość narzędzi tego typu wymaga uruchomionej aplikacji TradingView albo własnego
okna przeglądarki. Nie ruszą więc na serwerze ani w tle, a już na pewno nie bez
człowieka przy monitorze.

Drugi problem jest cichszy: sięgają po garść pól, zwykle sześć albo dwanaście.
TradingView udostępnia publicznie znacznie więcej. Przy sprawdzeniu okazało się,
że działa sześćdziesiąt dwa.

VGM bierze wszystkie i nie potrzebuje do tego okna.

---

## Co potrafi

### Odczyt

| narzędzie | do czego | sprawdzone na |
|---|---|---|
| `vgm_odczyt` | wybrane pola dla instrumentu | FX:EURUSD, 91 pól |
| `vgm_obraz` | wszystkie 91 pól naraz, w dziewięciu grupach | FX:EURUSD |
| `vgm_pola` | spis dostępnych pól, do sprawdzenia przed zgadywaniem nazwy | tylko wywołanie |
| `vgm_rynki` | spis dziesięciu sprawdzonych rynków | tylko wywołanie |
| `vgm_obraz_pelny` | wszystko o instrumencie jednym wywołaniem | FX:EURUSD, 6 sekcji |

### Położenie ceny

| narzędzie | do czego | sprawdzone na |
|---|---|---|
| `vgm_polozenie` | miejsce ceny w kanale Bollingera, w rozpiętości rocznej, względem średnich | FX:EURUSD |
| `vgm_srednie` | układ sześciu średnich wykładniczych od 5 do 200 | FX:EURUSD |

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

### Wykres

Ta grupa wymaga otwartej karty z TradingView. Port podajesz w `VGM_CDP_PORT`.

| narzędzie | do czego | sprawdzone na |
|---|---|---|
| `vgm_wykres_zdrowie` | czy da się sterować, sprawdź przed resztą | karta z wykresem |
| `vgm_wykres_stan` | instrument, przedział, typ, wskaźniki, rysunki | BATS:AAPL, FX:GBPUSD |
| `vgm_wykres_wartosci` | bieżące wartości wskaźników z wykresu | RSI 53,16 i Volume |
| `vgm_wykres_symbol` | zmiana instrumentu | AAPL na EURUSD, potwierdzone odczytem |
| `vgm_wykres_interwal` | zmiana przedziału czasu | D na 60, potwierdzone odczytem |
| `vgm_wykres_typ` | świece, słupki, linia, Heikin Ashi | wywołanie przechodzi |
| `vgm_wskaznik_dodaj` | dodanie wskaźnika po nazwie | RSI dodany i widoczny |
| `vgm_wskaznik_usun` | usunięcie po identyfikatorze | RSI usunięty |
| `vgm_wykres_swiece` | świece historyczne z pełnym OHLCV | 300 świec GBPUSD 1h |
| `vgm_wykres_zrzut` | obraz wykresu do pliku PNG | 84 KB, wykres widoczny |
| `vgm_swiece_statystyka` | rozpiętość, zasięg świec, udział wzrostowych, luki | 200 świec GBPUSD |
| `vgm_swiece_zmiennosc` | zmienność w dwóch oknach i ich stosunek | 2 okna po 20 świec |
| `vgm_swiece_przedzialy` | statystyka świec z kilku przedziałów naraz | 15, 60 i 240 minut |

`vgm_wykres_wartosci` czyta również wskaźniki własne, napisane w Pine. Publiczne
dane ich nie znają, bo istnieją tylko na Twoim wykresie.

`vgm_wykres_swiece` bierze historię z serii, którą wykres i tak ma wczytaną. Zwykle
dostępnych jest kilkaset świec z czasem, otwarciem, szczytem, dołkiem, zamknięciem
i wolumenem. Żadne osobne źródło danych nie jest potrzebne.

`vgm_wykres_zrzut` zapisuje obraz wykresu do pliku. Model może dzięki temu wykres
obejrzeć, a nie tylko odczytać z niego liczby.

### Pine Script

Bez przeglądarki i bez konta.

| narzędzie | do czego | sprawdzone na |
|---|---|---|
| `vgm_pine_sprawdz` | kompilacja z dokładną linią i kolumną błędu | kod poprawny, jeden błąd, dwa błędy |
| `vgm_pine_sprawdz_plik` | to samo, z pliku na dysku | tylko wywołanie |
| `vgm_pine_szkielet` | gotowy punkt wyjścia, sam się kompiluje | kompiluje się bez błędu |

Sprawdzenie trwa około sekundy i wygląda tak:

```
   3 | plot(ta.sma(clse, 20))
     |             ^-- Undeclared identifier 'clse'
```

Kolumna po prawej mówi, na czym dane narzędzie zostało uruchomione. Puste pole
znaczy, że sprawdziłem tylko, czy się wywołuje.

---

### Pomiar

Ta grupa nie liczy sygnału. Sprawdza, czy sygnał jest cokolwiek wart.

| narzędzie | do czego | sprawdzone na |
|---|---|---|
| `vgm_zmierz_prog` | czy przekroczenie progu cokolwiek zapowiada | RSI 30, 300 świec |
| `vgm_porownaj_progi` | ten sam pomiar na kilku progach naraz | pięć progów RSI |
| `vgm_zmierz` | to samo dla czterech wskaźników | RSI, Bollinger, ADX, ATR |
| `vgm_przeglad_wskaznikow` | siedem warunków jednym przebiegiem | GBPUSD 1h, 300 świec |

Cztery warunki, wszystkie muszą być spełnione naraz:

**Dodatni zwrot po spreadzie.** Koszt wejścia wchodzi do rachunku.

**Przewaga nad sygnałem losowym.** Ten sam pomiar na losowych wejściach
o tej samej częstości. Placebo bywa gorsze od stratnego sygnału, więc samo
pobicie go nie wystarcza.

**Zgodność obu połów okresu.** Wynik z jednej połowy nic nie znaczy, dopóki
nie powtórzy się w drugiej.

**Co najmniej dwadzieścia wejść.** Trzy trafienia na trzy próby to przypadek.

Przegląd siedmiu warunków na czterech wskaźnikach dał wynik odmowny w całości:

```
ADX poniżej 15:   +0,1687%   85,7% trafień   ale 7 wejść
RSI poniżej 30:   +0,0416%   76,5% trafień   ale 17 wejść
ADX powyżej 30:   -0,0260%   40,1% trafień   137 wejść, zwrot ujemny
```

Dwa pierwsze wyglądają świetnie i oba odpadają na liczbie wejść. Trzeci ma dość
wejść, ale traci po spreadzie. Narzędzie mówi to wprost, zamiast wybierać
najładniejszy wiersz.
---

## Dane, do których sięga

Sześćdziesiąt dwa pola, wszystkie sprawdzone na żywym rynku:

**Cena.** Otwarcie, zamknięcie, szczyt, dołek, luka, zmiana, VWAP
**Wolumen.** Bieżący, średnia dziesięciodniowa, stosunek jednego do drugiego
**Pęd.** RSI, RSI7, Stochastic K i D, Stochastic RSI K i D, CCI, Momentum, Awesome, ROC, Ultimate, Williams, przepływ pieniądza, przepływ Chaikina
**Trend.** ADX z obiema składowymi kierunkowymi, MACD z linią i histogramem, Parabolic SAR, Aroon w górę i w dół, pełny Ichimoku (bazowa, konwersji, obie wyprzedzające)
**Średnie.** SMA i EMA po siedem każda, od 5 do 200, plus VWMA i Hull
**Zmienność.** ATR, wstęgi Bollingera, siła wstęg, zmienność dzienna, tygodniowa i miesięczna, kanały Donchiana i Keltnera
**Poziomy.** Pięć systemów punktów zwrotnych (klasyczny, Fibonacciego, Woodiego, Camarilli, DeMarka) oraz szczyt i dołek z roku
**Wyniki.** Tydzień, miesiąc, trzy i sześć miesięcy, od początku roku, rok, pięć lat
**Ocena.** Zbiorcza TradingView, osobno dla średnich i oscylatorów, plus ocena siedmiu pojedynczych wskaźników

Każde z tych pól przyjmuje przyrostek z przedziałem czasu. `RSI|240` daje RSI z czterech godzin. Zmierzone przedziały: 1, 5, 15, 60, 240 minut oraz tydzień.

Dziewięćdziesiąt jeden pól razy sześć przedziałów to 546 wartości. Jedno zapytanie.

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
python3 test_vgm.py      # sprawdza wszystko: pola, rynki, Pine, wykres
python3 src/dane.py      # warstwa danych
python3 src/analiza.py   # warstwa analizy
python3 src/pola.py      # sprawdza, czy wszystkie 91 pól nadal działają
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


## Rynki

Sprawdzone, wszystkie zwracają wyniki:

| nazwa | co obejmuje |
|---|---|
| `forex` | pary walutowe |
| `crypto`, `coin` | kryptowaluty, dwa różne zestawy |
| `america` | akcje amerykańskie |
| `poland` | GPW i NewConnect |
| `germany`, `uk`, `japan` | akcje z tych giełd |
| `futures` | kontrakty terminowe |
| `cfd` | kontrakty na różnicę |

Wszystkie 91 pól działa na każdym z tych rynków. Sprawdzone na kryptowalutach,
akcjach amerykańskich, GPW i kontraktach na złoto: za każdym razem 91 z 91.

---

## Z terminala

Te same narzędzia bez klienta MCP:

```bash
vgm odczyt FX:EURUSD              cena i wskaźniki
vgm obraz FX:EURUSD               wszystkie 91 pól
vgm polozenie FX:EURUSD           miejsce ceny względem odniesień
vgm mtf FX:EURUSD                 wskaźnik na kilku przedziałach
vgm zgodnosc FX:EURUSD            ile przedziałów mówi to samo
vgm porownaj FX:EURUSD FX:GBPUSD  instrumenty obok siebie
vgm skan trend                    przegląd rynku
vgm pine moj-wskaznik.pine        sprawdzenie kodu
vgm wykres stan                   co jest na wykresie
vgm wykres zrzut obraz.png        zapis wykresu
vgm swiece 200 --statystyka       liczby ze świec
vgm wszystko FX:EURUSD            pełny obraz jednym poleceniem
```

Każde polecenie przyjmuje `--json`, gdy wynik ma iść dalej do skryptu.

---

## Czego tu nie ma

Lista jawna. Lepiej wiedzieć z góry, niż odkryć w trakcie.

| brakuje | powód |
|---|---|
| wstawianie Pine na wykres | wymaga zalogowanego edytora |
| alerty | wymagają konta |
| rysowanie na wykresie | sprawdzone: wywołanie przechodzi, ale nic się nie pojawia bez sesji |
| Strategy Tester | wyniki są i tak tylko poglądowe, więc niski priorytet |

Warstwa wykresu działa bez logowania w zakresie odczytu i sterowania, natomiast zapisywanie
skryptów, alerty i listy obserwowanych wymagają zalogowanej sesji.

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
albo 429 serwer staje i nie ponawia. Ponawianie przy tych kodach kończy się blokadą adresu, o czym przekonaliśmy się
na własnej skórze.

---

## Licencja

MIT. Rób, co chcesz.
