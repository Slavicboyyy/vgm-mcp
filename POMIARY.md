# Badanie jednego sygnału

> Zapis tego, co wyszło przy sprawdzaniu warunku „cena powyżej 90 procent
> kanału Bollingera" na surowcach. Razem z trzema błędami, które warstwa
> pomiaru wykryła w moich własnych obliczeniach.

Wniosek jest odmowny: **na tych danych sygnał nie daje przewagi możliwej
do wykorzystania**. Wart uwagi jest natomiast sposób, w jaki to wyszło —
trzy razy wynik wyglądał świetnie i trzy razy okazał się artefaktem.

---
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

---

## Koniec badania: sygnał nie działa

Ostatni pomiar zamyka sprawę. Transakcje bez nakładania, jedna pozycja naraz,
koszt 0,05 procent, przedział dzienny:

```
ZŁOTO   świec   transakcji    sygnał   trzymanie
            3           24     6,05%      30,33%
            5           17    17,83%      30,33%
           10           12    25,53%      30,33%
           20            8    26,25%      30,33%

ROPA        3           17    21,65%      37,41%
            5           12    17,23%      37,41%
           10            8     6,56%      37,41%
           20            5    43,86%      37,41%   (za mało transakcji)
```

Przy trzech świecach na złocie mamy dwadzieścia cztery transakcje, czyli powyżej
progu, który sam sobie postawiłem. Sygnał daje tam sześć procent, a zwykłe
kupno z trzymaniem trzydzieści. Próbka wystarczająca, wynik jednoznaczny.

Jedyny wiersz, w którym sygnał wygrywa, to ropa przy dwudziestu świecach —
pięć transakcji. Za mało, żeby cokolwiek z tego wnioskować.

## Czego nauczyło to narzędzie

Badanie skończyło się odmownie, ale po drodze warstwa pomiaru wykryła trzy
błędy w moich własnych obliczeniach. Każdy z nich wyglądał na sukces:

**Świece z innego instrumentu.** Wykres pokazywał BTCUSD i zwracał ceny funta.
Objaw: cztery różne instrumenty dały identyczne liczby.

**Przedział czasu, który kłamie.** Wykres pokazywał dniówkę, a odstęp między
świecami wynosił godzinę. Objaw: cztery różne przedziały dały identyczne liczby.

**Nakładające się pozycje.** Czterdzieści siedem wejść w miejscu czterech
prawdziwych transakcji. Objaw: suma 322 procent przy trzydziestu z trzymania.

Za każdym razem objawem była liczba zbyt dobra, żeby była prawdziwa. Bez tych
sprawdzeń mielibyśmy dziś „działającą strategię na złocie" opartą na czterech
transakcjach i pomyłce w liczeniu.

Sygnał odpadł. Narzędzie, które go odsiało, zostaje.

---

## Drugi przegląd: sześć kolejnych błędów, tym razem cudzym okiem

Po zamknięciu badania dałem kod pomiaru do przeglądu innemu modelowi (GLM 5.3)
z pytaniem, czego nie zauważyłem. Znalazł dziesięć rzeczy. Sześć zweryfikowałem
pomiarem i naprawiłem; każdy z nich zmieniał liczby, nie tylko styl.

**Wejście po zamknięciu świecy sygnału.** Sygnał liczę z zamknięcia świecy i,
a wchodziłem po tym samym zamknięciu. Realnie da się wejść dopiero na otwarciu
i+1. Zmierzone na RSI<30, złoto: 3,1213% wobec 2,7368%, czyli **0,38 pp zawyżenia**
— bo dla powrotu do średniej to zamknięcie jest lokalnym dołkiem, którego nikt
nie łapie.

**ADX bez wygładzania Wildera.** Sumy proste dawały **48,89 tam, gdzie TradingView
pokazywał 25,71** — 23 punkty różnicy. Każdy pomiar na progach ADX 30 i 15 był
na wartościach, które nie miały nic wspólnego z tym, co widać na wykresie.
Po przepisaniu na Wildera: 25,71 wobec 25,71, różnica 0,00.

**Nakładające się wejścia w samym pomiarze.** Naprawiłem to wcześniej w liczeniu
kosztu, ale nie w `zmierz` — tam próg dwudziestu wejść nadal przechodził na
powtórkach tej samej pozycji. Po policzeniu epizodów: Bollinger>90 z 54 wejść
spadł do 10, ADX>30 ze 137 do 13.

**Placebo bez ziarna.** Dwa uruchomienia dawały różne losowania i różne wnioski.
Teraz ziarno jest jawnym parametrem, a losowań 50 zamiast 20.

**Połówki bez minimalnej próby.** Zgodność połów liczyła się nawet przy jednym
wejściu w połowie. Teraz poniżej ośmiu narzędzie mówi wprost, że to za mało.

**Trzymanie mylone ze średnią per okno.** `odniesienie_trzymanie` liczyło średnią
z każdego okna, nie kupno raz i trzymanie do końca. Właściwy wzorzec jest w
`koszt_a_przewaga`; tamta funkcja zostaje jako „bezwarunkowa średnia per okno"
i tak jest opisana.

Po tych sześciu poprawkach przegląd siedmiu warunków na złocie dziennym dał
ten sam wniosek co wcześniej, tylko na poprawnych liczbach: żaden nie przeszedł.

Cztery pozostałe uwagi z przeglądu (miara niepewności placebo, placebo blokowe
względem reżimu zmienności, test trwałości przewagi zamiast zyskowności w połówkach,
brak sprawdzenia poza próbą) są zapisane, ale niezrobione. To wciąż pomiar
w próbie, nie poza nią.

---

## Trzeci przegląd: dziesięć lat historii i z-score

Dwie rzeczy naraz. Po pierwsze, wykres miał wczytane 2518 świec dziennych,
a każdy pomiar brał ostatnie 300 — bo tyle wpisałem jako domyślne. Po drugie,
z przeglądu GLM doszła miara niepewności: odchylenie losowań placebo, z-score
prawdziwego wyniku wobec nich i percentyl.

Siedem warunków, złoto dzienne, 2500 świec, wejście na otwarciu następnej
świecy, epizody bez nakładania, 50 losowań z jawnym ziarnem:

```
warunek                epiz   zwrot%  placebo   odch     z    pctl
RSI poniżej 30           16    0,820    0,651  0,887  0,19   62   za mało
RSI powyżej 70           43    0,497    0,581  0,529 -0,16   42   nie bije
Bollinger poniżej 10     62    0,256    0,605  0,434 -0,80   20   nie bije
Bollinger powyżej 90     92    0,333    0,551  0,314 -0,69   24   nie bije
ADX powyżej 30           87    0,636    0,552  0,355  0,24   64   szum
ADX poniżej 15           41    0,006    0,590  0,516 -1,13   14   nie bije
ATR powyżej 0,15        224    0,585    0,574  0,198  0,05   54   szum
```

Bollinger powyżej 90, który na trzystu świecach wyglądał na sygnał, na dziesięciu
latach ma 92 epizody, z-score −0,69 i 24. percentyl: **gorzej niż losowe wejście**.
Dwa warunki z dodatnią różnicą (ADX>30, ATR) mieszczą się w rozrzucie placebo
z zapasem, z-score 0,24 i 0,05.

Odchylenie losowań (0,20–0,89 punktu procentowego) jest w każdym wierszu większe
od różnicy między sygnałem a placebo. To jest właściwy powód, dla którego
wcześniejsze „przewagi" rzędu 0,1–0,4 pp nic nie znaczyły: mieściły się
w szumie, którego wtedy nie mierzyłem.

Od teraz pomiar bierze domyślnie całą dostępną historię, a wniosek wymaga
pięciu rzeczy naraz: dodatni zwrot po koszcie, przewaga nad placebo, |z| ≥ 1,
zgodność obu połów, co najmniej dwadzieścia epizodów.
