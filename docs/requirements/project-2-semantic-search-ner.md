# Projekt 2 – System wyszukiwania semantycznego i ekstrakcji wiedzy

> Status: **tylko wymagania**, brak szkieletu i kodu w repozytorium.

## 1. Cel

Zaprojektować i zaimplementować aplikację z **graficznym interfejsem użytkownika**, która umożliwia:

- tworzenie **bazy dokumentów tekstowych**,
- wyszukiwanie informacji **różnymi metodami**,
- automatyczne **rozpoznawanie encji nazwanych (NER)**.

System ma integrować:

1. zarządzanie dokumentami,
2. wyszukiwanie słów kluczowych,
3. wyszukiwanie TF-IDF,
4. wyszukiwanie semantyczne,
5. rozpoznawanie encji w dokumentach.

## 2. Zarządzanie bazą dokumentów

| ID | Wymaganie |
|----|-----------|
| P2-DB-01 | Dodawanie dokumentów **TXT i PDF**. |
| P2-DB-02 | **Automatyczne odczytywanie i przetwarzanie** treści dokumentów. |
| P2-DB-03 | **Przechowywanie dokumentów i ich metadanych.** |
| P2-DB-04 | **Przeglądanie** dokumentów. |
| P2-DB-05 | **Usuwanie** dokumentów. |
| P2-DB-06 | **Automatyczne przygotowywanie** dokumentów do wyszukiwania i analizy NER (np. indeksowanie, embeddingi, NER przy dodaniu). |

## 3. Moduł wyszukiwania informacji

Trzy metody wyszukiwania:

| ID | Metoda | Opis |
|----|--------|------|
| P2-S-01 | Słowa kluczowe | Wyszukiwanie dokumentów zawierających podane **słowa lub frazy**. |
| P2-S-02 | TF-IDF | Wyszukiwanie i **ranking** dokumentów na podstawie **podobieństwa tekstowego**. |
| P2-S-03 | Semantyczne | Znajdowanie dokumentów **podobnych znaczeniowo** do zapytania. |

Wymagania dla wyników i interfejsu wyszukiwania:

| ID | Wymaganie |
|----|-----------|
| P2-S-04 | Każdy wynik zawiera: **nazwę dokumentu**, **wynik dopasowania (score)**, **fragment tekstu związany z zapytaniem**. |
| P2-S-05 | Użytkownik może **otworzyć dokument** i przejrzeć jego treść. |
| P2-S-06 | Użytkownik wpisuje **jedno zapytanie** i widzi **obok siebie** wyniki: słów kluczowych, TF-IDF i semantycznego. |
| P2-S-07 | Dodatkowo można pokazać **różnice w kolejności dokumentów** między metodami (porównanie rankingów). |
| P2-S-08 | Wyniki wyszukiwania można **ograniczyć do dokumentów zawierających wskazaną encję lub określony typ encji** (powiązanie z NER). |

## 4. Moduł NER (Named Entity Recognition)

Automatyczne wykrywanie encji w dokumentach, w tym:

- **Osoby**
- **Organizacje**
- **Lokalizacje geograficzne**
- **Daty i okresy**
- **Inne kategorie** obsługiwane przez wybrany model

| ID | Wymaganie |
|----|-----------|
| P2-N-01 | Automatyczne wykrywanie encji powyższych typów. |
| P2-N-02 | Wyświetlanie wykrytych encji **wraz z typami** i **fragmentami tekstu**, w których występują. |
| P2-N-03 | W widoku dokumentu encje są **wyróżnione wizualnie** (np. kolorami wg typu). |
| P2-N-04 | **Wyszukiwanie encji** oraz **znajdowanie dokumentów**, w których występują. |
| P2-N-05 | Ograniczanie wyników wyszukiwania (sekcja 3) do dokumentów z daną encją lub typem encji (= P2-S-08). |

## 5. Graficzny interfejs użytkownika

Trzy główne widoki:

| Widok | Zawartość |
|-------|-----------|
| **Baza dokumentów** | Dodawanie, przeglądanie i usuwanie dokumentów. |
| **Wyszukiwarka** | Wybór metody wyszukiwania oraz przeglądanie wyników. |
| **Encje NER** | Lista wykrytych encji, filtrowanie według typu, przeglądanie dokumentów, w których występują. |

| ID | Wymaganie |
|----|-----------|
| P2-G-01 | Trzy powyższe widoki. |
| P2-G-02 | **Szczegóły dokumentu**, jego **metadane** i **wyróżnione encje** dostępne po wybraniu dokumentu z listy wyników lub z bazy dokumentów. |

## 6. Priorytety (wprost z treści)

- **Ważniejsza jest funkcjonalność** związana z przetwarzaniem i eksploracją danych tekstowych niż wygląd interfejsu i architektura aplikacji.
- **Najważniejsze**: możliwość **porównania** wyszukiwania słów kluczowych, TF-IDF i semantycznego.
- System powinien umożliwiać **porównywanie rankingów i wyników** uzyskanych różnymi metodami.

## 7. Dodatkowe funkcjonalności (rozszerzenia)

| ID | Rozszerzenie |
|----|--------------|
| P2-X-01 | Panel z **najczęściej występującymi encjami** (osoby, organizacje, lokalizacje). |
| P2-X-02 | Statystyki: **liczba dokumentów**. |
| P2-X-03 | Statystyki: **długości tekstów**. |
| P2-X-04 | Statystyki: **najczęściej występujące terminy**. |
| P2-X-05 | Statystyki: **rozkład wykrytych typów encji**. |
| P2-X-06 | Wizualizacja różnic w kolejności dokumentów między metodami. |

## 8. Kryteria „zrobione”

- [ ] Dodawanie TXT i PDF, odczyt treści, metadane, przeglądanie, usuwanie.
- [ ] Automatyczne przygotowanie dokumentów do wyszukiwania i NER.
- [ ] Trzy metody wyszukiwania z wynikiem: nazwa, score, fragment.
- [ ] Widok porównawczy: jedno zapytanie → trzy kolumny wyników.
- [ ] Porównanie rankingów (różnice w kolejności).
- [ ] NER: osoby, organizacje, lokalizacje, daty/okresy (+ inne).
- [ ] Wyróżnienie encji w widoku dokumentu.
- [ ] Wyszukiwanie encji i dokumentów z encją; filtrowanie wyszukiwarki po encji/typie.
- [ ] Trzy widoki GUI + szczegóły dokumentu.
- [ ] (Opcjonalnie) panel top encji i statystyki.

## 9. Otwarte decyzje

- Język dokumentów (PL / EN) → model NER i model embeddingów.
- Model NER (np. spaCy, HuggingFace) i embeddingów (np. sentence-transformers, wielojęzyczny).
- Przechowywanie: SQLite + pliki vs katalog + JSON; indeks wektorowy (FAISS / numpy).
- Technologia GUI.
