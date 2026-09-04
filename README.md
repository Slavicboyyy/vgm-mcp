# VGM MCP

Serwer MCP do TradingView. Czyta rynek bez logowania i bez otwartej przeglądarki.

Czterdzieści trzy narzędzia plus polecenie w terminalu. Dziewięćdziesiąt jeden pól danych. Sześć przedziałów czasowych
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
| `vgm_wykres_przelacz` | zmiana instrumentu Z WERYFIKACJĄ danych | EURUSD i złoto, ceny zgodne |
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
| `vgm_sygnal_czy_trend` | czy warunek wnosi coś ponad sam trend | złoto, ropa, srebro |
| `vgm_odniesienie_trzymanie` | ile daje samo trzymanie bez sygnału | 265 wejść |
| `vgm_jak_dlugo_trzymac` | po ilu świecach sygnał daje najwięcej | złoto i ropa, 5 długości |
| `vgm_koszt_a_przewaga` | przy jakim koszcie sygnał traci sens | złoto i ropa, 6 poziomów |

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

### Pierwszy warunek, który przeszedł

Pomiar na złocie, cztery przedziały czasu, dane zweryfikowane:

```
COMEX:GC1!, warunek: położenie powyżej 90% kanału Bollingera

15 min    41 wejść    +0,1964%   58,5% trafień   przewaga 0,1651%   przeszedł
60 min    34 wejścia  +0,3421%   73,5% trafień   przewaga 0,4213%   przeszedł
240 min   37 wejść    +0,2618%   54,1% trafień   przewaga -0,018%   odpadł
dzienny   54 wejścia  +2,0130%   59,3% trafień   przewaga 1,0435%   przeszedł

Na EURUSD i bitcoinie ten sam warunek nie przeszedł.
```

Ten sam warunek na czterech surowcach, przedział dzienny:

```
złoto    54 wejścia  +2,0113%   59,3% trafień   przewaga +0,618    przeszedł
srebro   67 wejść    +1,9925%   67,2% trafień   przewaga -1,1417   odpadł
miedź    56 wejść    +0,4569%   58,9% trafień   przewaga -1,2906   odpadł
ropa     34 wejścia  +3,1606%   55,9% trafień   przewaga +1,2515   przeszedł
```

Srebro warto obejrzeć uważnie. Ma najwyższy odsetek trafień w całym zestawieniu,
67,2 procent, i prawie dwa procent zwrotu. A mimo to odpada, bo w badanym okresie
rosło tak mocno, że losowe wejście dawało jeszcze więcej. Sygnał nie dodawał nic
ponad samo bycie na rynku.

Bez porównania z losowym wejściem srebro wyglądałoby na najlepszy wiersz tabeli.
Tak właśnie powstają strategie, które świetnie wyglądają w hossie.

Podsumowując: dwa surowce z czterech, trzy przedziały z czterech. Warunek nie jest
uniwersalny i nie ma tu dowodu na przewagę, bo trzysta świec to mało, nie było
sprawdzenia poza próbą, a poślizg nie wchodzi do rachunku. Jest to natomiast
pierwszy kandydat, który przetrwał wszystkie cztery bariery na kilku instrumentach
i przedziałach naraz.

### Sygnał czy sam trend

Placebo losowe ma słabość: sygnał może je bić, a mimo to przegrywać
z nicnierobieniem. Dlatego `vgm_sygnal_czy_trend` porównuje cztery liczby
naraz — warunek, warunek odwrotny, samo trzymanie i losowe wejście.

Prawdziwy sygnał bije trzymanie, a jego odwrotność wypada gorzej. Sam trend
daje podobny wynik niezależnie od warunku.

Zmierzone na przedziale dziennym, warunek: powyżej 90% kanału Bollingera:

```
złoto    warunek 2,0118%   odwrotny 0,6022%    trzymanie 1,1922%
         bije trzymanie o 0,82 pp, odwrotność gorsza o 1,41 pp -> sygnał

ropa     warunek 3,1606%   odwrotny -0,0362%   trzymanie 1,6629%
         bije trzymanie o 1,50 pp, odwrotność gorsza o 3,20 pp -> sygnał

srebro   warunek 1,9928%   odwrotny -0,8155%   trzymanie 2,8028%
         trzymanie BIJE warunek -> sygnał nie wnosi nic
```

Srebro pokazuje, po co to kryterium istnieje. Warunek dawał tam prawie dwa
procent i sześćdziesiąt siedem procent trafień, ale samo trzymanie dawało
dwa i osiem dziesiątych procent. Aktywne handlowanie wypadało gorzej niż
nierobienie niczego.

Próg kanału ma znaczenie tylko na ropie. Na złocie zwrot jest niemal płaski
między progiem 70 a 95 (od 2,04 do 2,20 procent), więc sam próg niewiele wnosi.
Na ropie zwrot rośnie do progu 80 i znika przy 95, gdzie zostaje dwadzieścia
siedem wejść i zwrot 0,23 procent.

### Jak długo trzymać

Ten sam warunek potrafi działać odwrotnie na krótkim terminie i dobrze
na długim. Zmierzone na przedziale dziennym:

```
ZŁOTO   świec    warunek   odwrotny   trzymanie   rozstęp
            5     0,4694     1,0684      0,5304    -0,599   dół bije górę
           10     2,0092     0,6022      1,1917     1,407
           20     4,1933     0,0189      2,4532     4,174
           40     6,8633    -0,6285      3,8912     7,492

ROPA        5     2,2618     0,1174      0,8410     2,144
           40    27,3414     3,7692      7,1263    23,572
```

Na złocie warunek nie działa przy trzech i pięciu świecach, a przy pięciu
działa wręcz odwrotnie: dół kanału daje więcej niż góra. Zaczyna działać
od dziesięciu świec i rośnie dalej.

Rosnący zwrot sam w sobie niczego nie dowodzi, bo przy dłuższym trzymaniu
rośnie wszystko, także zwykłe trzymanie. Rozstrzyga to, że warunek odwrotny
zostaje płaski albo schodzi pod zero, gdy trzymanie daje prawie cztery procent.
Sam trend podnosiłby obie strony.

### Nakładanie pozycji, czyli jak sam się oszukałem

Wszystkie liczby wyżej mówią, co dzieje się średnio po sygnale. To poprawne
pytanie, ale nie odpowiada na inne: ile da się na tym zarobić naprawdę.

Przy trzymaniu przez czterdzieści świec wejścia z sąsiednich dni to niemal
ta sama pozycja. Sumowanie ich jak niezależnych transakcji zawyża wynik
kilkukrotnie. Zmierzone: sumowanie z nakładaniem dawało 322 procent na złocie
przy trzydziestu procentach z kupna i trzymania. Ta liczba powinna była od razu
zapalić lampkę.

Po policzeniu transakcji bez nakładania, czyli jedna pozycja naraz:

```
ZŁOTO   4 transakcje (22 wejścia pominięte, bo pozycja była otwarta)
        sygnał 30,36%   kupno i trzymanie 30,29%
        przewaga znika przy koszcie 0,1% na transakcję

ROPA    3 transakcje (22 pominięte)
        sygnał 32,48%   kupno i trzymanie 37,13%
        przegrywa nawet przy koszcie bliskim zeru
```

Cztery transakcje to poniżej progu dwudziestu wejść, który sam sobie
postawiłem. Wniosek jest więc taki: **na tych danych sygnał nie daje przewagi
możliwej do wykorzystania**. Wcześniejsze 2,97 i 20,21 punktu procentowego
brały się z liczenia tej samej pozycji wiele razy.

Pomiar średniego zwrotu po sygnale zostaje poprawny i przydatny. Zmienia się
tylko to, jak go czytać: mówi o zachowaniu rynku po warunku, nie o zysku
z handlu.
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

Warstwa wykresu działa bez logowania, gdy chodzi o odczyt i sterowanie. Zapisywanie
skryptów, alerty i listy obserwowanych wymagają zalogowanej sesji.

Te rzeczy są zaplanowane, ale żadnej nie ma w kodzie. Nie chcę, żeby ktoś liczył
na coś, czego nie zbudowałem.

---

## Co trzeba wiedzieć, zanim się użyje

🔴 **Pułapka, na którą trzeba uważać.** Zmiana instrumentu przez
`vgm_wykres_symbol` zmienia nazwę natychmiast, ale seria świec potrafi
zostać przy poprzednim instrumencie. Wykres pokazuje wtedy jedną nazwę,
a zwraca ceny innego waloru, przy czym nic tego nie sygnalizuje.

Zmierzone: po przełączeniu na bitcoina wykres deklarował `COINBASE:BTCUSD`,
a ostatnia świeca miała 1,35206, czyli cenę funta. Statystyka policzona na
takich danych jest bezwartościowa i wygląda dokładnie tak samo jak prawdziwa.

Dlatego przed czytaniem świec używaj `vgm_wykres_przelacz`. Sprawdza
on cenę krzyżowo z publicznym punktem TradingView i, gdy trzeba, przeładowuje
stronę z symbolem wpisanym w adres.

🔴 **Druga pułapka, tego samego rodzaju.** Zmiana przedziału czasu przez
`vgm_wykres_interwal` też zmienia samą nazwę. Zmierzone: wykres pokazywał
"1D", a odstęp między świecami wynosił godzinę. Cztery różne przedziały dawały
wtedy identyczne wyniki pomiaru.

`vgm_wykres_przelacz` sprawdza więc dwie rzeczy naraz: czy cena zgadza się
z publicznym punktem i czy **odstęp między świecami odpowiada przedziałowi**.
Sama nazwa nie wystarcza w żadnym z tych dwóch przypadków.



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
