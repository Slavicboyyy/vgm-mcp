#!/usr/bin/env python3
"""VGM MCP — pomiar. Sprawdza, czy sygnał cokolwiek przewiduje.

Narzędzie, którego nie ma żaden inny serwer MCP do TradingView. Reszta pozwala
sygnał policzyć. To pozwala sprawdzić, czy jest cokolwiek wart.

Cztery zasady, każda po to, żeby nie oszukać samego siebie:

1. **Placebo.** Ten sam pomiar na sygnale losowym, o tej samej częstości.
   Jeśli prawdziwy nie bije placebo, nie ma przewagi.
2. **Podział na dwie połowy.** Wynik z jednego okresu nic nie znaczy, dopóki
   nie powtórzy się w drugim.
3. **Koszt odjęty.** Spread wchodzi do rachunku. Sygnał zarabiający mniej niż
   koszt wejścia jest stratny.
4. **Licznik wejść.** Trzy trafienia na trzy próby to nie przewaga, to przypadek.

Liczy na świecach z wykresu, więc działa na dowolnym instrumencie i przedziale,
który wykres ma wczytany.
"""
from __future__ import annotations

import random
import statistics
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


class BladPomiaru(Exception):
    """Za mało danych albo błędne ustawienia pomiaru."""


def _wynik_po(swiece: list, wejscia: list[int], po_ilu: int,
              spread_proc: float) -> dict:
    """Co się działo po każdym wejściu, licząc w procentach ceny wejścia."""
    zwroty = []
    for i in wejscia:
        if i + po_ilu >= len(swiece):
            continue
        wejscie = swiece[i]["zamkniecie"]
        wyjscie = swiece[i + po_ilu]["zamkniecie"]
        if not wejscie:
            continue
        zwrot = (wyjscie - wejscie) / wejscie * 100 - spread_proc
        zwroty.append(zwrot)

    if not zwroty:
        return {"wejsc": 0}

    dodatnie = sum(1 for z in zwroty if z > 0)
    return {
        "wejsc": len(zwroty),
        "sredni_zwrot_proc": round(statistics.mean(zwroty), 4),
        "mediana_proc": round(statistics.median(zwroty), 4),
        "trafien_proc": round(dodatnie / len(zwroty) * 100, 1),
        "najlepsze": round(max(zwroty), 4),
        "najgorsze": round(min(zwroty), 4),
        "odchylenie": round(statistics.pstdev(zwroty), 4) if len(zwroty) > 1 else 0,
    }


def zmierz_prog(pole: str = "RSI", prog: float = 30, kierunek: str = "ponizej",
                po_ilu: int = 10, ile_swiec: int = 300,
                spread_proc: float = 0.02, losowan: int = 20) -> dict:
    """Czy przekroczenie progu przez wskaźnik cokolwiek zapowiada.

    pole:        na razie tylko "RSI" — liczony na świecach z wykresu
    prog:        wartość graniczna
    kierunek:    "ponizej" albo "powyzej"
    po_ilu:      ile świec po wejściu sprawdzamy wynik
    spread_proc: koszt wejścia w procentach ceny
    losowan:     ile powtórzeń placebo
    """
    import analiza

    swiece = analiza._swiece_z_wykresu(ile_swiec)
    if len(swiece) < 60:
        raise BladPomiaru(f"za mało świec: {len(swiece)}, potrzeba co najmniej 60")

    zamkniecia = [s["zamkniecie"] for s in swiece]
    rsi = _rsi(zamkniecia, 14)

    wejscia = []
    for i in range(15, len(swiece) - po_ilu):
        w = rsi[i]
        if w is None:
            continue
        if (kierunek == "ponizej" and w < prog) or (kierunek == "powyzej" and w > prog):
            wejscia.append(i)

    if not wejscia:
        return {"wejsc": 0,
                "uwaga": f"warunek {pole} {kierunek} {prog} nie wystąpił ani razu"}

    polowa = len(swiece) // 2
    pierwsza = [i for i in wejscia if i < polowa]
    druga = [i for i in wejscia if i >= polowa]

    prawdziwy = _wynik_po(swiece, wejscia, po_ilu, spread_proc)

    # placebo: tyle samo wejść, ale w losowych miejscach
    losowe = []
    for _ in range(losowan):
        prob = random.sample(range(15, len(swiece) - po_ilu),
                             min(len(wejscia), len(swiece) - po_ilu - 16))
        w = _wynik_po(swiece, prob, po_ilu, spread_proc)
        if w.get("wejsc"):
            losowe.append(w["sredni_zwrot_proc"])

    placebo = round(statistics.mean(losowe), 4) if losowe else None
    przewaga = (round(prawdziwy["sredni_zwrot_proc"] - placebo, 4)
                if placebo is not None and prawdziwy.get("wejsc") else None)

    return {
        "warunek": f"{pole} {kierunek} {prog}",
        "swiec": len(swiece),
        "sprawdzane_po": f"{po_ilu} świecach",
        "spread_odjety_proc": spread_proc,
        "caly_okres": prawdziwy,
        "pierwsza_polowa": _wynik_po(swiece, pierwsza, po_ilu, spread_proc),
        "druga_polowa": _wynik_po(swiece, druga, po_ilu, spread_proc),
        "placebo_sredni_zwrot": placebo,
        "przewaga_nad_placebo": przewaga,
        "wniosek": _wniosek(prawdziwy, placebo, przewaga,
                            _wynik_po(swiece, pierwsza, po_ilu, spread_proc),
                            _wynik_po(swiece, druga, po_ilu, spread_proc)),
    }


def _wniosek(prawdziwy, placebo, przewaga, pierwsza, druga) -> str:
    """Jedno zdanie o tym, co z pomiaru wynika. Bez upiększania."""
    if not prawdziwy.get("wejsc"):
        return "brak wejść — nie ma czego mierzyć"
    if prawdziwy["wejsc"] < 20:
        return (f"tylko {prawdziwy['wejsc']} wejść — za mało, żeby cokolwiek "
                "twierdzić; potrzeba co najmniej dwudziestu")
    if przewaga is None:
        return "placebo nie policzone — wynik nieporównywalny"
    if przewaga <= 0:
        return (f"sygnał NIE bije losowego wejścia (różnica {przewaga}%) — "
                "nie ma przewagi")
    if prawdziwy["sredni_zwrot_proc"] <= 0:
        # bicie placebo nie wystarcza: placebo bywa jeszcze gorsze, a stratny
        # sygnał zostaje stratny niezależnie od tego, z czym go porównamy
        return (f"sygnał bije placebo o {przewaga}%, ale sam traci "
                f"{prawdziwy['sredni_zwrot_proc']}% po spreadzie — bez wartości")

    a = pierwsza.get("sredni_zwrot_proc")
    b = druga.get("sredni_zwrot_proc")
    if a is None or b is None:
        return f"przewaga {przewaga}%, ale jedna połowa okresu bez wejść — niepewne"
    if (a > 0) != (b > 0):
        return (f"przewaga {przewaga}%, ale połowy okresu przeczą sobie "
                f"({a}% i {b}%) — wynik niestabilny")
    return (f"przewaga {przewaga}% nad losowym wejściem, zgodna w obu połowach "
            f"({a}% i {b}%) przy {prawdziwy['wejsc']} wejściach")


def _rsi(ceny: list[float], okres: int = 14) -> list[float | None]:
    """RSI liczony u nas, żeby dało się go policzyć dla każdej świecy wstecz."""
    wynik: list[float | None] = [None] * len(ceny)
    if len(ceny) < okres + 1:
        return wynik

    zyski, straty = [], []
    for i in range(1, len(ceny)):
        r = ceny[i] - ceny[i - 1]
        zyski.append(max(r, 0))
        straty.append(max(-r, 0))

    sz = sum(zyski[:okres]) / okres
    ss = sum(straty[:okres]) / okres
    for i in range(okres, len(ceny)):
        if i > okres:
            sz = (sz * (okres - 1) + zyski[i - 1]) / okres
            ss = (ss * (okres - 1) + straty[i - 1]) / okres
        wynik[i] = 100.0 if ss == 0 else 100 - 100 / (1 + sz / ss)
    return wynik


def porownaj_progi(progi: list[float] | None = None, kierunek: str = "ponizej",
                   po_ilu: int = 10, ile_swiec: int = 300,
                   spread_proc: float = 0.02) -> dict:
    """Ten sam pomiar na kilku progach naraz — który daje dość wejść i przewagę.

    Luźniejszy próg daje więcej wejść, ale słabszy sygnał. Ostrzejszy odwrotnie.
    To zestawienie pokazuje, gdzie leży granica, zamiast zgadywać.
    """
    progi = progi or [25, 30, 35, 40]
    wiersze = []
    for prog in progi:
        try:
            w = zmierz_prog("RSI", prog, kierunek, po_ilu, ile_swiec, spread_proc)
            c = w.get("caly_okres", {})
            a = w.get("pierwsza_polowa", {}).get("sredni_zwrot_proc")
            b = w.get("druga_polowa", {}).get("sredni_zwrot_proc")
            wiersze.append({
                "prog": prog,
                "wejsc": c.get("wejsc", 0),
                "sredni_zwrot_proc": c.get("sredni_zwrot_proc"),
                "trafien_proc": c.get("trafien_proc"),
                "przewaga_nad_placebo": w.get("przewaga_nad_placebo"),
                "polowy_zgodne": (a is not None and b is not None and (a > 0) == (b > 0)),
                "dosc_wejsc": c.get("wejsc", 0) >= 20,
            })
        except Exception as e:
            wiersze.append({"prog": prog, "blad": str(e)[:60]})

    uzyteczne = [w for w in wiersze
                 if w.get("dosc_wejsc") and w.get("polowy_zgodne")
                 and (w.get("przewaga_nad_placebo") or 0) > 0
                 # sam zwrot musi być dodatni — bicie placebo nie wystarcza,
                 # bo placebo bywa jeszcze gorsze od stratnego sygnału
                 and (w.get("sredni_zwrot_proc") or 0) > 0]

    return {
        "kierunek": kierunek,
        "sprawdzane_po": f"{po_ilu} świecach",
        "progi": wiersze,
        "przechodzi_wszystkie_warunki": [w["prog"] for w in uzyteczne],
        "wniosek": (
            f"progi z dodatnim zwrotem, przewagą nad placebo, zgodnymi połowami "
            f"i co najmniej 20 wejściami: {[w['prog'] for w in uzyteczne]}"
            if uzyteczne else
            "żaden próg nie przeszedł wszystkich czterech warunków"
        ),
    }


# ── wskaźniki liczone u nas, żeby dało się je policzyć dla każdej świecy ──
def _sma(ceny, okres):
    w = [None] * len(ceny)
    for i in range(okres - 1, len(ceny)):
        w[i] = sum(ceny[i - okres + 1:i + 1]) / okres
    return w


def _atr(swiece, okres=14):
    """Średni zasięg z uwzględnieniem luk między świecami."""
    zasiegi = []
    for i, s in enumerate(swiece):
        if i == 0:
            zasiegi.append(s["szczyt"] - s["dolek"])
            continue
        poprz = swiece[i - 1]["zamkniecie"]
        zasiegi.append(max(s["szczyt"] - s["dolek"],
                           abs(s["szczyt"] - poprz),
                           abs(s["dolek"] - poprz)))
    return _sma(zasiegi, okres)


def _bollinger(ceny, okres=20, odchylen=2.0):
    """Zwraca położenie ceny w kanale: 0 to dolna wstęga, 100 to górna."""
    srodek = _sma(ceny, okres)
    w = [None] * len(ceny)
    for i in range(okres - 1, len(ceny)):
        wycinek = ceny[i - okres + 1:i + 1]
        sr = srodek[i]
        odch = (sum((x - sr) ** 2 for x in wycinek) / okres) ** 0.5
        gora, dol = sr + odchylen * odch, sr - odchylen * odch
        w[i] = None if gora == dol else (ceny[i] - dol) / (gora - dol) * 100
    return w


def _adx(swiece, okres=14):
    """Siła ruchu kierunkowego. Wysoka wartość to trend, niska to zakres."""
    if len(swiece) < okres * 2:
        return [None] * len(swiece)

    plus, minus, tr = [], [], []
    for i in range(1, len(swiece)):
        gora = swiece[i]["szczyt"] - swiece[i - 1]["szczyt"]
        dol = swiece[i - 1]["dolek"] - swiece[i]["dolek"]
        plus.append(gora if gora > dol and gora > 0 else 0)
        minus.append(dol if dol > gora and dol > 0 else 0)
        poprz = swiece[i - 1]["zamkniecie"]
        tr.append(max(swiece[i]["szczyt"] - swiece[i]["dolek"],
                      abs(swiece[i]["szczyt"] - poprz),
                      abs(swiece[i]["dolek"] - poprz)))

    w = [None] * len(swiece)
    dx = []
    for i in range(okres, len(tr)):
        str_ = sum(tr[i - okres:i])
        if not str_:
            dx.append(0)
            continue
        dp = sum(plus[i - okres:i]) / str_ * 100
        dm = sum(minus[i - okres:i]) / str_ * 100
        dx.append(0 if dp + dm == 0 else abs(dp - dm) / (dp + dm) * 100)

    for i, wart in enumerate(dx):
        poz = i + okres + 1
        if poz < len(w) and i >= okres:
            w[poz] = sum(dx[i - okres:i]) / okres
    return w


WSKAZNIKI = {
    "RSI": "siła względna, 0 do 100",
    "Bollinger": "położenie w kanale, 0 to dolna wstęga, 100 to górna",
    "ADX": "siła ruchu kierunkowego",
    "ATR_proc": "zasięg świecy jako procent ceny",
}


def _policz(nazwa: str, swiece: list) -> list:
    zamkniecia = [s["zamkniecie"] for s in swiece]
    if nazwa == "RSI":
        return _rsi(zamkniecia, 14)
    if nazwa == "Bollinger":
        return _bollinger(zamkniecia, 20, 2.0)
    if nazwa == "ADX":
        return _adx(swiece, 14)
    if nazwa == "ATR_proc":
        atr = _atr(swiece, 14)
        return [None if a is None or not c else a / c * 100
                for a, c in zip(atr, zamkniecia)]
    raise BladPomiaru(f"nieznany wskaźnik: {nazwa}. Dostępne: {list(WSKAZNIKI)}")


def zmierz(wskaznik: str = "RSI", prog: float = 30, kierunek: str = "ponizej",
           po_ilu: int = 10, ile_swiec: int = 300,
           spread_proc: float = 0.02, losowan: int = 20) -> dict:
    """To samo co zmierz_prog, ale dla dowolnego z czterech wskaźników.

    Dostępne: RSI, Bollinger (położenie w kanale), ADX, ATR_proc.
    """
    import analiza

    swiece = analiza._swiece_z_wykresu(ile_swiec)
    if len(swiece) < 60:
        raise BladPomiaru(f"za mało świec: {len(swiece)}, potrzeba co najmniej 60")

    wartosci = _policz(wskaznik, swiece)
    od = 25  # tyle świec potrzebuje najdłuższy wskaźnik na rozbieg

    wejscia = []
    for i in range(od, len(swiece) - po_ilu):
        w = wartosci[i]
        if w is None:
            continue
        if (kierunek == "ponizej" and w < prog) or (kierunek == "powyzej" and w > prog):
            wejscia.append(i)

    if not wejscia:
        return {"wejsc": 0,
                "uwaga": f"warunek {wskaznik} {kierunek} {prog} nie wystąpił ani razu"}

    polowa = len(swiece) // 2
    pierwsza = _wynik_po(swiece, [i for i in wejscia if i < polowa], po_ilu, spread_proc)
    druga = _wynik_po(swiece, [i for i in wejscia if i >= polowa], po_ilu, spread_proc)
    prawdziwy = _wynik_po(swiece, wejscia, po_ilu, spread_proc)

    losowe = []
    for _ in range(losowan):
        prob = random.sample(range(od, len(swiece) - po_ilu),
                             min(len(wejscia), len(swiece) - po_ilu - od - 1))
        w = _wynik_po(swiece, prob, po_ilu, spread_proc)
        if w.get("wejsc"):
            losowe.append(w["sredni_zwrot_proc"])

    placebo = round(statistics.mean(losowe), 4) if losowe else None
    przewaga = (round(prawdziwy["sredni_zwrot_proc"] - placebo, 4)
                if placebo is not None and prawdziwy.get("wejsc") else None)

    return {
        "warunek": f"{wskaznik} {kierunek} {prog}",
        "opis_wskaznika": WSKAZNIKI.get(wskaznik, ""),
        "swiec": len(swiece),
        "sprawdzane_po": f"{po_ilu} świecach",
        "spread_odjety_proc": spread_proc,
        "caly_okres": prawdziwy,
        "pierwsza_polowa": pierwsza,
        "druga_polowa": druga,
        "placebo_sredni_zwrot": placebo,
        "przewaga_nad_placebo": przewaga,
        "wniosek": _wniosek(prawdziwy, placebo, przewaga, pierwsza, druga),
    }


def przeglad_wskaznikow(po_ilu: int = 10, ile_swiec: int = 300,
                        spread_proc: float = 0.02) -> dict:
    """Wszystkie cztery wskaźniki, sensowne progi, jeden przebieg.

    Odpowiada na pytanie: czy KTÓRYKOLWIEK z nich cokolwiek zapowiada
    na tym instrumencie i przedziale.
    """
    zestaw = [
        ("RSI", 30, "ponizej"), ("RSI", 70, "powyzej"),
        ("Bollinger", 10, "ponizej"), ("Bollinger", 90, "powyzej"),
        ("ADX", 30, "powyzej"), ("ADX", 15, "ponizej"),
        ("ATR_proc", 0.15, "powyzej"),
    ]

    wiersze = []
    for wsk, prog, kier in zestaw:
        try:
            w = zmierz(wsk, prog, kier, po_ilu, ile_swiec, spread_proc)
            c = w.get("caly_okres", {})
            wiersze.append({
                "warunek": f"{wsk} {kier} {prog}",
                "wejsc": c.get("wejsc", 0),
                "zwrot_proc": c.get("sredni_zwrot_proc"),
                "trafien_proc": c.get("trafien_proc"),
                "przewaga": w.get("przewaga_nad_placebo"),
                "wniosek": w.get("wniosek", "")[:70],
            })
        except Exception as e:
            wiersze.append({"warunek": f"{wsk} {kier} {prog}", "blad": str(e)[:60]})

    przeszly = [w for w in wiersze
                if w.get("wejsc", 0) >= 20
                and (w.get("zwrot_proc") or 0) > 0
                and (w.get("przewaga") or 0) > 0]

    return {
        "sprawdzono": len(wiersze),
        "wyniki": wiersze,
        "przeszly": [w["warunek"] for w in przeszly],
        "wniosek": (f"warunki z przewagą: {[w['warunek'] for w in przeszly]}"
                    if przeszly else
                    "żaden z siedmiu warunków nie dał przewagi na tych danych"),
    }


def przeglad_instrumentow(instrumenty: list | None = None,
                          po_ilu: int = 10, spread_proc: float = 0.02) -> dict:
    """Ten sam przegląd na kilku instrumentach i przedziałach.

    Wynik z jednego wykresu to jeden pomiar. Dopiero powtórzenie na innym
    instrumencie pokazuje, czy wniosek się utrzymuje, czy był przypadkiem.

    Każda pozycja to para (symbol, przedział). Wykres jest przełączany
    i przywracany na koniec.
    """
    import wykres

    instrumenty = instrumenty or [
        ("FX:EURUSD", "60"),
        ("FX:EURUSD", "D"),
        ("COMEX:GC1!", "60"),
        ("COINBASE:BTCUSD", "60"),
    ]

    stan_poczatkowy = wykres.stan()
    wyniki = {}

    for symbol, przedzial in instrumenty:
        klucz = f"{symbol} {przedzial}"
        try:
            # przelacz sprawdza krzyzowo, czy swiece naprawde naleza do instrumentu
            p = wykres.przelacz(symbol, przedzial)
            if not p.get("potwierdzone"):
                wyniki[klucz] = {
                    "pominiete": "świece nie potwierdziły instrumentu",
                    "szczegol": p.get("powod", "")[:70],
                }
                continue
            w = przeglad_wskaznikow(po_ilu, 300, spread_proc)
            wyniki[klucz] = {
                "sprawdzono": w["sprawdzono"],
                "przeszly": w["przeszly"],
                "najlepszy": _najlepszy(w["wyniki"]),
            }
        except Exception as e:
            wyniki[klucz] = {"blad": str(e)[:80]}

    try:
        wykres.przelacz(stan_poczatkowy["symbol"], stan_poczatkowy["interwal"])
    except Exception:
        pass

    wszystkie_przeszly = [w for r in wyniki.values() for w in r.get("przeszly", [])]

    return {
        "instrumentow": len(instrumenty),
        "stan_przywrocony": f"{stan_poczatkowy['symbol']} {stan_poczatkowy['interwal']}",
        "wyniki": wyniki,
        "warunki_ktore_przeszly_gdziekolwiek": sorted(set(wszystkie_przeszly)),
        "wniosek": (
            f"warunki z przewagą na przynajmniej jednym instrumencie: "
            f"{sorted(set(wszystkie_przeszly))}"
            if wszystkie_przeszly else
            f"na {len(instrumenty)} instrumentach żaden warunek nie dał przewagi"
        ),
    }


def _najlepszy(wiersze: list) -> dict | None:
    """Wiersz z najwyższym zwrotem — nawet gdy nie przeszedł, warto go widzieć."""
    z_wynikiem = [w for w in wiersze if w.get("zwrot_proc") is not None]
    if not z_wynikiem:
        return None
    n = max(z_wynikiem, key=lambda w: w["zwrot_proc"])
    return {"warunek": n["warunek"], "zwrot_proc": n["zwrot_proc"],
            "wejsc": n["wejsc"], "trafien_proc": n["trafien_proc"]}


def odniesienie_trzymanie(po_ilu: int = 10, ile_swiec: int = 300,
                          spread_proc: float = 0.02) -> dict:
    """Ile daje samo trzymanie przez N świec, bez żadnego sygnału.

    To uczciwszy punkt odniesienia niż losowe wejście: mówi, ile zarobiłby
    ktoś, kto wchodzi zawsze i nie patrzy na wskaźniki. Sygnał ma sens
    dopiero wtedy, gdy bije TĘ liczbę, nie samo placebo.
    """
    import analiza

    swiece = analiza._swiece_z_wykresu(ile_swiec)
    wszystkie = list(range(25, len(swiece) - po_ilu))
    return _wynik_po(swiece, wszystkie, po_ilu, spread_proc)


def czy_sygnal_czy_trend(wskaznik: str = "Bollinger", prog: float = 90,
                         kierunek: str = "powyzej", po_ilu: int = 10,
                         ile_swiec: int = 300, spread_proc: float = 0.02) -> dict:
    """Rozstrzyga, czy warunek naprawdę coś wnosi, czy tylko łapie trend.

    Porównuje cztery liczby: warunek, warunek odwrotny, samo trzymanie
    i losowe wejście. Prawdziwy sygnał bije trzymanie, a jego odwrotność
    wypada gorzej. Sam trend daje podobny wynik niezależnie od warunku.
    """
    odwrotny = "ponizej" if kierunek == "powyzej" else "powyzej"
    prog_odwrotny = 100 - prog if wskaznik == "Bollinger" else prog

    w = zmierz(wskaznik, prog, kierunek, po_ilu, ile_swiec, spread_proc)
    o = zmierz(wskaznik, prog_odwrotny, odwrotny, po_ilu, ile_swiec, spread_proc)
    trzymanie = odniesienie_trzymanie(po_ilu, ile_swiec, spread_proc)

    zw = w.get("caly_okres", {}).get("sredni_zwrot_proc")
    zo = o.get("caly_okres", {}).get("sredni_zwrot_proc")
    zt = trzymanie.get("sredni_zwrot_proc")

    nad_trzymaniem = round(zw - zt, 4) if zw is not None and zt is not None else None
    rozstep = round(zw - zo, 4) if zw is not None and zo is not None else None

    if nad_trzymaniem is None or rozstep is None:
        ocena = "za mało danych do rozstrzygnięcia"
    elif nad_trzymaniem <= 0:
        ocena = (f"warunek daje {zw}%, a samo trzymanie {zt}% — "
                 "sygnał nie wnosi nic ponad bycie na rynku")
    elif rozstep <= 0:
        ocena = (f"warunek i jego odwrotność dają podobnie ({zw}% i {zo}%) — "
                 "to trend, nie sygnał")
    else:
        ocena = (f"warunek bije trzymanie o {nad_trzymaniem} pp, a jego odwrotność "
                 f"wypada o {rozstep} pp gorzej — zachowuje się jak prawdziwy sygnał")

    return {
        "warunek": f"{wskaznik} {kierunek} {prog}",
        "warunek_odwrotny": f"{wskaznik} {odwrotny} {prog_odwrotny}",
        "zwrot_warunku_proc": zw,
        "zwrot_odwrotnego_proc": zo,
        "zwrot_trzymania_proc": zt,
        "zwrot_losowego_proc": w.get("placebo_sredni_zwrot"),
        "nad_trzymaniem_pp": nad_trzymaniem,
        "rozstep_warunek_odwrotny_pp": rozstep,
        "wejsc_warunku": w.get("caly_okres", {}).get("wejsc"),
        "ocena": ocena,
    }


def _demo():
    print("Pomiar: czy RSI poniżej 30 cokolwiek zapowiada\n")
    w = zmierz_prog("RSI", 30, "ponizej", po_ilu=10)
    for k, v in w.items():
        if isinstance(v, dict):
            print(f"  {k}:")
            for kk, vv in v.items():
                print(f"      {kk:22} {vv}")
        else:
            print(f"  {k:24} {v}")


if __name__ == "__main__":
    _demo()
