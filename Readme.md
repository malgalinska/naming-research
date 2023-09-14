Autor: Małgorzata Galińska

# Program oraz dane pracy magisterskiej "Strategie definiowania nazw identyfikatorów podczas tworzenia oprogramowania"

## Opis programu
Program składa się z 2 części. Pierwsza z nich przechodzi po skompresowanych plikach zawierających badane projekty i zbiera
dane do plików CSV. Druga tworzy na ich podstawie wykresy. Pliki źródłowe projektu znajdują się w katalogu `./src`.

## Instalacja

W celu uruchomienia programu należy zainstalować 2 wersje Pythona:
    `Python3.11.2`,
    `Python2.7.18`
oraz moduł colorama, najlepiej za pomocą:
    `pip install colorama`.

## Przygotowanie i uruchomienie

### Krok 1. Przygotowanie plików

Pobrane pliki z projektami skompresowanymi w formacie ZIP należy pogrupować w foldery i zapisać w folderze `./my_data`.
Dane z jednego folderu będą na jednym wykresie. Nazwa pliku będzie odpowiadała podpisom na osiach X wykresów.
Proponowanym rozwiązaniem jest grupowanie plików w folderach po nazwie projektu i nazywanie plików wersjami lub datami
wersji. Warto zwrócić uwagę, że dane na wykresie będą układały się w kolejności alfabetycznej, tak jak domyślnie pliki
w folderze. Należy o tym pamiętać, jeśli zależy nam na chronologii.

### Krok 2. Odpalenie skryptu zbierającego dane

`./src/repo_finder.py ./my_data`

Ten skrypt zbierze dane z wszystkich znalezionych plików zip i zapisze je w odpowiadających projektom plikach CSV
w tym samym drzewie katalogów.

### Krok 3. Odpalenie skryptu tworzącego wykresy

`./src/data_finder.py ./my_data ./my_plots`

Ten skrypt przeczyta dane zapisane w powstałych przed chwilą plikach CSV i stworzy na ich podstawie wykresy. Wykresy
będą zapisane w folderze `./my_plots`.

### Dodatkowe informacje

Wyjście diagnostyczne jest zapisywane w plikach `log.txt` oraz `plots_log.txt`. 

## Opis danych

Zebrane i wykorzystane w pracy dane w postaci plików CSV znajdują się w folderze `./data`. Dane w postaci wykresów
znajsują się w folderze `./plots`.
