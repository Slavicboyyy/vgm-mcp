#!/usr/bin/env python3
"""VGM MCP — warstwa wykresu. Steruje otwartą kartą TradingView przez CDP.

W przeciwieństwie do warstwy danych ta wymaga uruchomionej przeglądarki
z otwartą kartą TradingView. Port bierze ze zmiennej VGM_CDP_PORT,
domyślnie 9222 (tyle mają zwykle przeglądarki uruchomione z debugowaniem).

Sięga po wewnętrzne API strony: `window.TradingViewApi._activeChartWidgetWV.value()`.
To nie jest udokumentowane przez TradingView i może przestać działać po ich
aktualizacji — dlatego `zdrowie()` sprawdza dostępność, zanim cokolwiek zrobisz.
"""
from __future__ import annotations

import json
import os
import time
import urllib.request

try:
    import websocket
except ImportError:  # pragma: no cover
    websocket = None

PORT = int(os.environ.get("VGM_CDP_PORT", "9222"))
API = "window.TradingViewApi._activeChartWidgetWV.value()"
_licznik = [0]


class BladWykresu(Exception):
    """Cokolwiek, co uniemożliwia sterowanie wykresem — z czytelnym powodem."""


def _karta():
    if websocket is None:
        raise BladWykresu(
            "brakuje pakietu websocket-client — zainstaluj: pip install websocket-client")
    try:
        surowe = urllib.request.urlopen(
            f"http://localhost:{PORT}/json", timeout=10).read()
    except Exception as e:
        raise BladWykresu(
            f"przeglądarka nie odpowiada na porcie {PORT} ({type(e).__name__}). "
            "Uruchom ją z debugowaniem albo ustaw VGM_CDP_PORT."
        ) from e

    for t in json.loads(surowe):
        if "tradingview.com" in t.get("url", ""):
            return t
    raise BladWykresu(
        "żadna karta nie ma otwartego TradingView — otwórz wykres i spróbuj ponownie")


def _wykonaj(kod: str, czekaj: float = 25):
    k = _karta()
    _licznik[0] += 1
    nr = _licznik[0]
    ws = websocket.create_connection(k["webSocketDebuggerUrl"], timeout=czekaj)
    try:
        ws.send(json.dumps({
            "id": nr,
            "method": "Runtime.evaluate",
            "params": {"expression": kod, "returnByValue": True, "awaitPromise": True},
        }))
        koniec = time.time() + czekaj
        while time.time() < koniec:
            o = json.loads(ws.recv())
            if o.get("id") != nr:
                continue
            r = o.get("result", {})
            if "exceptionDetails" in r:
                raise BladWykresu(r["exceptionDetails"].get("text", "błąd w przeglądarce"))
            return r.get("result", {}).get("value")
        raise BladWykresu(f"przeglądarka nie odpowiedziała w {czekaj}s")
    finally:
        ws.close()


def _na_wykresie(cialo: str) -> str:
    """Owija kod w dostęp do wykresu i przechwytywanie błędów."""
    return f"""
    (function(){{
      try {{
        var api = window.TradingViewApi;
        if (!api || !api._activeChartWidgetWV) return {{blad: 'strona nie udostępnia API wykresu'}};
        var ch = api._activeChartWidgetWV.value();
        if (!ch) return {{blad: 'wykres jeszcze się nie wczytał'}};
        {cialo}
      }} catch(e) {{ return {{blad: String(e && e.message || e)}}; }}
    }})()
    """


def _sprawdz(w):
    if isinstance(w, dict) and "blad" in w:
        raise BladWykresu(w["blad"])
    return w


# ── odczyt ──────────────────────────────────────────────────────────────
def zdrowie() -> dict:
    """Czy da się sterować wykresem — sprawdź to przed resztą."""
    wynik = {"port": PORT, "przegladarka": False, "karta_tv": False,
             "api_wykresu": False, "gotowy": False}
    try:
        k = _karta()
        wynik["przegladarka"] = True
        wynik["karta_tv"] = True
        wynik["tytul"] = k.get("title", "")[:70]
    except BladWykresu as e:
        wynik["powod"] = str(e)
        if "port" not in str(e):
            wynik["przegladarka"] = True
        return wynik

    try:
        w = _wykonaj(_na_wykresie("return {ok: true, symbol: ch.symbol()};"))
        if isinstance(w, dict) and w.get("ok"):
            wynik["api_wykresu"] = True
            wynik["gotowy"] = True
            wynik["symbol"] = w.get("symbol")
        else:
            wynik["powod"] = (w or {}).get("blad", "nieznany")
    except BladWykresu as e:
        wynik["powod"] = str(e)
    return wynik


def stan() -> dict:
    """Co jest teraz na wykresie: instrument, przedział czasu, typ, wskaźniki."""
    return _sprawdz(_wykonaj(_na_wykresie("""
        var st = [];
        try {
          st = ch.getAllStudies().map(function(s){
            return {id: s.id, nazwa: s.name || s.title || '?'};
          });
        } catch(e) {}
        var ks = [];
        try {
          ks = ch.getAllShapes().map(function(s){
            return {id: s.id, nazwa: s.name || '?'};
          });
        } catch(e) {}
        return {
          symbol: ch.symbol(),
          interwal: ch.resolution(),
          typ_wykresu: ch.chartType(),
          wskazniki: st,
          rysunki: ks
        };
    """)))


def wskazniki() -> list:
    """Lista wskaźników wiszących na wykresie."""
    return _sprawdz(_wykonaj(_na_wykresie("""
        return ch.getAllStudies().map(function(s){
          return {id: s.id, nazwa: s.name || s.title || '?'};
        });
    """)))


def rysunki() -> list:
    """Lista rysunków na wykresie: linie, poziomy, kształty."""
    return _sprawdz(_wykonaj(_na_wykresie("""
        return ch.getAllShapes().map(function(s){
          return {id: s.id, nazwa: s.name || '?'};
        });
    """)))


# ── zmiany ──────────────────────────────────────────────────────────────
def ustaw_symbol(symbol: str) -> dict:
    """Zmienia instrument na wykresie."""
    s = json.dumps(symbol)
    return _sprawdz(_wykonaj(_na_wykresie(f"""
        ch.setSymbol({s});
        return {{ok: true, symbol: {s}}};
    """)))


def ustaw_interwal(interwal: str) -> dict:
    """Zmienia przedział czasu. Przyjmuje 1, 5, 15, 60, 240, D, W, M."""
    i = json.dumps(str(interwal))
    return _sprawdz(_wykonaj(_na_wykresie(f"""
        ch.setResolution({i});
        return {{ok: true, interwal: {i}}};
    """)))


def ustaw_typ(typ: int) -> dict:
    """Zmienia typ wykresu. 0 słupki, 1 świece, 3 linia, 9 Heikin Ashi."""
    return _sprawdz(_wykonaj(_na_wykresie(f"""
        ch.setChartType({int(typ)});
        return {{ok: true, typ: {int(typ)}}};
    """)))


def swiece(ile: int = 100) -> dict:
    """Świece historyczne z wykresu: czas, otwarcie, szczyt, dołek, zamknięcie, wolumen.

    Bierze je z serii, którą wykres i tak ma wczytaną, więc nie potrzeba osobnego
    źródła danych ani konta. Ile świec jest dostępnych, zależy od tego, ile
    wykres zdążył wczytać — zwykle kilkaset.
    """
    n = max(1, min(int(ile), 5000))
    w = _sprawdz(_wykonaj(_na_wykresie(f"""
        var cw = ch._chartWidget;
        if (!cw) return {{blad: 'brak dostępu do modelu wykresu'}};
        var zrodla = cw.model().model().dataSources();
        var seria = null;
        for (var i = 0; i < zrodla.length; i++) {{
          if (!zrodla[i].metaInfo && zrodla[i].bars) {{ seria = zrodla[i]; break; }}
        }}
        if (!seria) return {{blad: 'nie znalazłem serii świec'}};
        var b = seria.bars();
        var pierwszy = b.firstIndex(), ostatni = b.lastIndex();
        var od = Math.max(pierwszy, ostatni - {n} + 1);
        var out = [];
        for (var k = od; k <= ostatni; k++) {{
          var v = b.valueAt(k);
          if (v) out.push(v);
        }}
        return {{dostepnych: b.size(), zwrocono: out.length, swiece: out}};
    """), czekaj=40))

    nazwane = []
    for s in w.get("swiece", []):
        if len(s) >= 5:
            nazwane.append({
                "czas": s[0],
                "otwarcie": s[1], "szczyt": s[2], "dolek": s[3], "zamkniecie": s[4],
                "wolumen": s[5] if len(s) > 5 else None,
            })
    return {"dostepnych": w.get("dostepnych"), "zwrocono": len(nazwane), "swiece": nazwane}


def zrzut(sciezka: str | None = None, zamknij_okna: bool = True) -> dict:
    """Zapisuje obraz wykresu do pliku PNG.

    Dzięki temu model może wykres OBEJRZEĆ, nie tylko odczytać z niego liczby.
    Domyślnie najpierw zamyka okna zachęt, które lubią zasłonić widok.
    """
    import base64
    import pathlib
    import tempfile

    if zamknij_okna:
        try:
            _wykonaj("""
                (function(){
                  var n = 0;
                  document.querySelectorAll(
                    'button[aria-label*="lose"],button[data-name="close"],[class*="closeButton"]'
                  ).forEach(function(b){ try { b.click(); n++; } catch(e){} });
                  document.dispatchEvent(new KeyboardEvent('keydown',
                    {key:'Escape', keyCode:27, bubbles:true}));
                  return n;
                })()
            """)
            time.sleep(1.5)
        except BladWykresu:
            pass  # zamykanie okien to wygoda, nie warunek

    k = _karta()
    _licznik[0] += 1
    nr = _licznik[0]
    ws = websocket.create_connection(k["webSocketDebuggerUrl"], timeout=45)
    try:
        ws.send(json.dumps({"id": nr, "method": "Page.captureScreenshot",
                            "params": {"format": "png"}}))
        koniec = time.time() + 45
        while time.time() < koniec:
            o = json.loads(ws.recv())
            if o.get("id") != nr:
                continue
            d = o.get("result", {}).get("data")
            if not d:
                raise BladWykresu("przeglądarka nie zwróciła obrazu")
            surowe = base64.b64decode(d)
            if sciezka is None:
                sciezka = tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False, prefix="vgm-wykres-").name
            p = pathlib.Path(sciezka)
            p.write_bytes(surowe)
            return {"plik": str(p), "bajtow": len(surowe),
                    "tytul": k.get("title", "")[:70]}
        raise BladWykresu("przeglądarka nie odpowiedziała w 45s")
    finally:
        ws.close()


def wartosci() -> list:
    """Bieżące wartości wszystkich wskaźników NA WYKRESIE.

    To jest powód, dla którego warstwa przeglądarki w ogóle istnieje: czyta
    również wskaźniki własne, napisane w Pine, których publiczne API nie zna.
    """
    return _sprawdz(_wykonaj(_na_wykresie("""
        var cw = ch._chartWidget;
        if (!cw) return {blad: 'brak dostępu do modelu wykresu'};
        var zrodla = cw.model().model().dataSources();
        var wynik = [];
        for (var i = 0; i < zrodla.length; i++) {
          var s = zrodla[i];
          if (!s.metaInfo) continue;
          try {
            var meta = s.metaInfo();
            var nazwa = meta.description || meta.shortDescription || '';
            if (!nazwa) continue;
            var wart = [];
            try {
              var d = s.data && s.data();
              var b = d && d.last ? d.last() : null;
              if (b && b.value) wart = b.value.slice(1);
            } catch(e) {}
            if (wart.length) wynik.push({nazwa: nazwa, wartosci: wart});
          } catch(e) {}
        }
        return wynik;
    """)))


def dodaj_wskaznik(nazwa: str) -> dict:
    """Dodaje wskaźnik na wykres po pełnej nazwie.

    Nazwa musi być dokładna, tak jak w oknie wyboru wskaźników TradingView,
    np. "Relative Strength Index", "Moving Average Exponential", "Volume".
    """
    n = json.dumps(nazwa)
    w = _sprawdz(_wykonaj(_na_wykresie(f"""
        var cel = (ch._chartWidget && ch._chartWidget.createStudy) ? ch._chartWidget : ch;
        if (!cel.createStudy) return {{blad: 'ta wersja strony nie pozwala dodać wskaźnika'}};
        cel.createStudy({n}, false, false, []);
        return {{ok: true, dodano: {n}}};
    """)))
    time.sleep(2)  # wskaźnik wchodzi na wykres z opóźnieniem
    return w


def usun_wskaznik(identyfikator: str) -> dict:
    """Usuwa jeden wskaźnik po identyfikatorze z `wskazniki()`."""
    i = json.dumps(identyfikator)
    return _sprawdz(_wykonaj(_na_wykresie(f"""
        var lista = ch.getAllStudies();
        for (var k = 0; k < lista.length; k++) {{
          if (lista[k].id === {i}) {{
            ch.removeEntity ? ch.removeEntity({i}) : null;
            return {{ok: true, usuniete: {i}}};
          }}
        }}
        return {{blad: 'nie ma wskaźnika o takim identyfikatorze'}};
    """)))


def _demo():
    print("1. zdrowie")
    z = zdrowie()
    for k, v in z.items():
        print(f"   {k:14} {v}")
    if not z.get("gotowy"):
        print("\n   wykres niedostępny — reszta testów pominięta")
        return 1

    print("\n2. stan wykresu")
    s = stan()
    print(f"   symbol:     {s['symbol']}")
    print(f"   interwal:   {s['interwal']}")
    print(f"   typ:        {s['typ_wykresu']}")
    print(f"   wskazniki:  {len(s['wskazniki'])} {[w['nazwa'] for w in s['wskazniki']][:4]}")
    print(f"   rysunki:    {len(s['rysunki'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_demo())
