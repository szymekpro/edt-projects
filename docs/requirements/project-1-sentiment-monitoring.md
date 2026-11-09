# Projekt 1 – Inteligentny system monitorowania opinii

## 1. Cel

Zbudować aplikację, która:

1. **Pobiera teksty z Internetu** – przez API lub web scraping.
   Dopuszczalne jest również pobieranie tekstów **wyłącznie na potrzeby predykcji**
   (czyli dane treningowe mogą być statyczne, np. z Kaggle).
2. **Automatycznie analizuje sentyment** tekstów: **pozytywny / negatywny**.
3. **Udostępnia prosty graficzny interfejs użytkownika (GUI).**
4. Korzysta z **dowolnego źródła danych**, np.:
   - opinie z serwisów produktowych,
   - komentarze z mediów społecznościowych,
   - recenzje filmów.

## 2. Wymagania szczegółowe

### 2.1 Dane

| ID | Wymaganie |
|----|-----------|
| P1-D-01 | **Dane do predykcji muszą pochodzić z Internetu** (API lub web scraping). To wymaganie obowiązkowe. |
| P1-D-02 | Dane treningowe mogą pochodzić z: (a) danych zgromadzonych wcześniej, np. zbiór z Kaggle, lub (b) danych pobieranych z Internetu w czasie rzeczywistym. |
| P1-D-03 | Dane treningowe i dane do predykcji **mogą pochodzić z różnych źródeł**, pod warunkiem że zbiory są **spójne pod względem struktury i charakteru** (np. ta sama domena – recenzje; zbliżony język, długość, styl tekstu, ta sama skala etykiet). |
| P1-D-04 | Źródło danych jest dowolne (opinie produktowe, social media, recenzje filmów itp.). |

### 2.2 Model analizy sentymentu

| ID | Wymaganie |
|----|-----------|
| P1-M-01 | Klasyfikacja sentymentu: **pozytywny / negatywny** (klasyfikacja binarna). |
| P1-M-02 | Model **może być trenowany, o ile tego wymaga** (trening jest więc wymagany tylko wtedy, gdy wybrane podejście go potrzebuje). |
| P1-M-03 | Jeśli model jest trenowany: na danych zgromadzonych wcześniej (np. Kaggle) **lub** na danych pobieranych z Internetu w czasie rzeczywistym. |
| P1-M-04 | Analiza sentymentu odbywa się **automatycznie** (bez ręcznego oznaczania pobranych tekstów). |

### 2.3 Aplikacja i GUI

| ID | Wymaganie |
|----|-----------|
| P1-G-01 | Aplikacja posiada **prosty GUI**. |
| P1-G-02 | GUI umożliwia uruchomienie pobrania tekstów z Internetu i obejrzenie wyniku analizy sentymentu. |

> Treść zadania nie określa dokładnych widoków GUI – poniżej propozycje nieobowiązkowe.

## 3. Propozycje (nieobowiązkowe, do decyzji zespołu)

- Wybór źródła/zapytania (np. produkt, film, hasło) w GUI.
- Lista pobranych tekstów z etykietą sentymentu i pewnością modelu.
- Podsumowanie: udział pozytywnych/negatywnych, wykres.
- Eksport wyników (CSV).
- Ocena jakości modelu (accuracy, F1, macierz pomyłek) na zbiorze testowym.

## 4. Kryteria „zrobione” (wynikające z treści)

- [x] Teksty do predykcji pobierane z Internetu (TMDB API).
- [x] Automatyczna klasyfikacja pozytywny/negatywny.
- [x] Działający prosty GUI (Tkinter).
- [ ] Udokumentowane źródło danych i spójność IMDB↔TMDB – **w raporcie PL** (w repo: `docs/requirements/` + README projektu).
- [x] Wytrenowany model: `train` + `evaluate` (metryki na teście IMDB).

## 5. Podjęte decyzje

Kryterium wyboru: najprostsze, najczytelniejsze i najszybsze do wykonania.

| Kwestia | Decyzja | Uzasadnienie |
|---------|---------|--------------|
| Język tekstów | **Angielski** | Największy wybór zbiorów i modeli. |
| Raport końcowy | **Tylko po polsku** | Wymóg zespołu. Kod, komentarze i komunikaty aplikacji po angielsku. |
| Dane treningowe | **Kaggle: IMDB Dataset of 50K Movie Reviews** | Gotowe etykiety pos/neg, zbalansowany, dane statyczne (dozwolone, P1-D-02). |
| Dane do predykcji | **TMDB API** (recenzje filmów po tytule) | Legalne API zamiast scrapingu, darmowy klucz. Ta sama domena (recenzje filmów), język i styl co zbiór treningowy, co spełnia P1-D-03. |
| Model | **Klasyczne ML: TF-IDF + Logistic Regression** (scikit-learn) | Trening w sekundach/minutach na CPU, łatwa interpretacja, prosta ewaluacja. |
| Interfejs | **GUI w Tkinterze** | Spełnia wymóg GUI (P1-G-01), jest w bibliotece standardowej (brak dodatkowych zależności). Logika wyłącznie w `pipeline`. |

Planowany układ okna: pole na tytuł filmu + przycisk „Fetch and analyze”, tabela recenzji (fragment tekstu | sentyment | pewność), podsumowanie (udział pozytywnych/negatywnych), pasek statusu z błędami.
Trening i ewaluacja są uruchamiane osobno jako skrypty: `python -m opinion_monitor.training.train` i `python -m opinion_monitor.training.evaluate`.

## 6. Ryzyka i uwagi

- **Tkinter i wątki.** Zapytania sieciowe muszą działać w osobnym wątku, inaczej okno się zawiesza podczas pobierania.
- **Przesunięcie domeny.** Recenzje TMDB są krótsze i bardziej nieformalne niż IMDB 50K (dłuższe). Opisać w raporcie. Opcjonalnie sprawdzić ręcznie próbkę wyników.
- **Brak etykiet w TMDB.** Recenzje z TMDB mają tylko ocenę liczbową (część bez niej), więc trafność na danych z Internetu można oszacować tylko na małej, ręcznie sprawdzonej próbce.
- **Klucz API.** Wymaga rejestracji w TMDB; trzymany w `.env`, nie w repozytorium.

## 7. Otwarte decyzje

- Liczba pobieranych recenzji na zapytanie i sposób obsługi filmów bez recenzji.
- Czy dodać klasę neutralną – wymaganie mówi tylko o pozytywny/negatywny, więc domyślnie nie.

## 8. Plan spełnienia wymagań

### Jak działa system

- **Trening:** zbiór Kaggle IMDB 50K → czyszczenie tekstu → TF-IDF + Logistic Regression → zapis modelu do `models/sentiment_model.joblib`.
- **Predykcja:** tytuł filmu w GUI → `data_sources` pobiera recenzje z TMDB API → to samo czyszczenie tekstu → model → wynik w tabeli GUI.
- GUI woła tylko `pipeline`; pobieranie z sieci działa w osobnym wątku.

### Mapowanie wymagań

| Wymaganie | Jak je spełniamy | Gdzie w kodzie |
|-----------|------------------|----------------|
| Pobieranie tekstów z Internetu (cel 1, P1-D-01) | Recenzje z TMDB API; dane do predykcji pochodzą wyłącznie z Internetu | `data_sources/api_source.py` |
| Dane treningowe mogą być statyczne (P1-D-02) | Trening na zbiorze Kaggle IMDB 50K (wariant „dane zgromadzone wcześniej”) | `training/dataset.py` |
| Różne źródła treningu i predykcji, ale spójne (P1-D-03) | IMDB i TMDB to recenzje filmów po angielsku, ten sam styl i skala etykiet; uzasadnienie i różnicę długości tekstów opisujemy w raporcie | raport (PL) |
| Dowolne źródło danych (P1-D-04) | Recenzje filmów (przykład podany wprost w zadaniu) | – |
| Automatyczna analiza sentymentu pozytywny/negatywny (cel 2, P1-M-01, P1-M-04) | Klasyfikacja binarna bez ręcznego etykietowania pobranych tekstów | `model/sentiment_model.py` |
| Model trenowany, o ile tego wymaga (P1-M-02, P1-M-03) | Własny model trenowany na danych z Kaggle; ewaluacja: accuracy, precision/recall/F1, macierz pomyłek | `training/train.py`, `training/evaluate.py` |
| Prosty GUI (cel 3, P1-G-01) | Okno Tkinter: pole na tytuł, przycisk, tabela wyników, podsumowanie | `gui/app.py` |
| GUI uruchamia pobieranie i pokazuje wynik (P1-G-02) | Przycisk „Fetch and analyze” wywołuje `pipeline`; tabela z etykietą i pewnością oraz udział pozytywnych/negatywnych | `gui/app.py`, `pipeline.py` |

### Stan implementacji

- Kod: trening, GUI, TMDB, `evaluate`, `evaluate_web`.
- Raport końcowy (PL) – poza repozytorium.
- Etykiety sentymentu w TMDB: tylko przybliżenie przez ocenę użytkownika (`evaluate_web`) lub ocena ręczna w GUI.
