## 1. Wstęp

Celem projektu było stworzenie interaktywnej aplikacji do szukania rozwiązania problemu komiwojażera
z wykorzystaniem algorytmu genetycznego. Program daje dużą swobodę w dostosowaniu parametrów
uruchomieniowych algorytmu, a więc ma charakter głównie edukacyjny, nie służy do znajdowania
rozwiązania w sposób optymalny w każdym przypadku. Dzięki temu użytkownik może samodzielnie
przekonać się jak różny dobór tych parametrów wpływa na szybkość czy skuteczność działania.
Program posiada graficzny interfejs użytkownika i na bieżąco wizualizuje przebieg algorytmu,
zarówno w postaci grafiki przedstawiającej najkrótszą znalezioną do tej pory ścieżkę jak
i też statystyk w formie tekstowej.

## 2. Problem komiwojażera:

Problem komiwojażera jest opisany w teorii grafów jako poszukiwanie takiego cyklu Hamiltona, dla którego suma wag krawędzi tego cyklu będzie najmniejsza. Potocznie, często przedstawiany jest jako problem obwoźnego sprzedawcy, który najmniejszym kosztem musi odwiedzić N miast i wrócić do punktu startowego, przy czym każde z nich odwiedza tylko raz. W przypadku gdy nie mamy nałożonych ograniczeń na poruszanie się pomiędzy miastami (graf jest zupełny), istnieje (n-1)! takich cykli. Problem jest NP-trudny, wraz ze wzrostem liczby miast, rozwiązanie problemu w sposób tradycyjny staje się bardzo czasochłonne, w pewnym momencie praktycznie niemożliwe do wykonania przy obecnie dostępnej mocy obliczeniowej. W przedstawionym programie kosztem przejścia jest odległość między miastami w przestrzeni euklidesowej.

## 3. Algorytm genetyczny

Jednym z możliwych sposobów redukcji czasu potrzebnego na rozwiązanie problemu jest zastosowanie algorytmów genetycznych. Jak wszystkie metody sztucznej inteligencji, dobrze sprawdzają się one w sytuacjach, gdy algorytm nie jest znany lub klasyczne podejście jest zbyt czasochłonne lub kosztowne. Algorytm genetyczny nie gwarantuje znalezienia najlepszego rozwiązania, ale oferuje znalezienie rozwiązania na tyle dobrego, aby satysfakcjonowało ono użytkownika, biorąc pod uwagę czas w jakim zostało znalezione. Taka definicja pozostawia szerokie pole do interpretacji, co rozumiemy poprzez rozwiązanie satysfakcjonujące oraz jaki czas można uznać za wystarczająco krótki. Można uznać to jednak za dużą zaletę tego podejścia, ponieważ dzięki temu można je łatwo dostosować do dziedziny w której operujemy lub osobistych preferencji użytkownika. Dla przykładu, programy wykorzystujące algorytmy genetyczne w przemyśle komercyjnym potrafią liczyć się kilka tygodni wykorzystując przy tym ogromną moc obliczeniową, podczas gdy przeciętny użytkownik prezentowanego tutaj programu może oczekiwać efektów po kilku sekundach czy minutach działania. Również w przypadku dokładności znalezionego rozwiązania, wymagania stawiane w przemyśle są nieporównywalnie większe od oczekiwań przeciętnego użytkownika tej aplikacji. Korzystając z tego programu można być zaskoczonym jak szybko proponowane są rozwiązania problemu, które subiektywnie można uznać za sensowne, tj. zbliżone do rozwiązania optymalnego, którego znalezienie trwałoby jednak o kilka rzędów wielkości dłużej.

## 4. Graficzny interfejs użytkownika - biblioteka PyQt

PyQt jest nakładką umożliwiającą wykorzystanie w Pythonie frameworku Qt, napisanego w C++, który umożliwia tworzenie graficznych interfejsów użytkownika niezależnie od platformy. Napisaną z ich użyciem aplikację można z powodzeniem uruchomić na wszystkich najpopularniejszych systemach, zarówno desktopowych (Linux, Windows, macOS) jak i mobilnych (Android, iOS, BlackBerry), a także wielu innych. Framework wspiera ponadto wiele innych obszarów, takich jak wątki, operacje sieciowe, wyrażenia regularne, połączenia z bazą danych, SVG czy XML. Przy spełnieniu pewnych założeń obie biblioteki mogą być używane w sposób darmowy, ponieważ PyQt dostępny jest pod licencją GNU GPL v3, natomiast sam Qt operuje pod LGPL.
Głównym elementem frameworka są tzw. widgety, obsługujące funkcjonalność interfejsu i interakcję z użytkownikiem. Istnieje wiele predefiniowanych widgetów, natomiast użytkownik ma też możliwość tworzenia własnych. Układ widgetów w oknie programu można dostosować za pomocą layoutów, treści mogą być wyświetlane w wielu oknach. Dostępnych jest również wiele typów okien dialogowych, umożliwiających
np. obsługę plików. Aplikacja działa na bazie tzw. pętli wydarzeń (ang. event loop), gdzie wszystkie akcje użytkownika takie jak przesunięcie kursora czy wpisanie czegoś z klawiatury obsługiwane są w kolejności wystąpienia. Komunikacja pomiędzy elementami interfejsy odbywa się za pomocą sygnałów i slotów. Widget może emitować sygnał w odpowiedzi na jakieś zdarzenie (np. kliknięcie). Sygnał ten może zostać obsłużony przez slot,
tj. dowolną funkcję która została podpięta pod pewien sygnał. Jeden sygnał może zostać obsłużony przez kilka slotów, tak samo jak jeden slot może być podpięty do wielu sygnałów.

## 5. Opis aplikacji

Po uruchomieniu programu widoczne jest główne okno aplikacji. Dokładny wygląd przycisków, paska czy kolor tła będzie różnił się w zależności od używanej platformy i ustawień systemowych.

Okno podzielone jest na dwie główne części. Prawa strona odpowiedzialna jest za wczytanie danych, ustawienie opcji programu, uruchomienie algorytmu oraz wyświetlanie statystyk. Lewa strona, na białym tle, odpowiada za wyświetlanie położenia miast i zmieniającego się na bieżąco najlepszego znalezionego do tej pory rozwiązania.
Dane mogą zostać wczytane z pliku tekstowego. Powinien on zawierać dwie kolumny oddzielone spacją, każdy wiersz zawiera współrzędną x i y danego miasta. Przykładowy plik dołączony jest do programu. Gdy klikniemy przycisk “Losuj”, program zapyta użytkownika o liczbę miast i wylosuje ich współrzędne. Po załadowaniu danych, program wyświetli miasta na kwadratowej mapie. W przypadku gdy teren na którym znajdują się miasta wczytane z pliku nie jest w formie kwadratu, współrzędne są skalowane, ale wyłącznie do celów wyświetlania. Wszelkie obliczenia i szukanie rozwiązania odbywają się na oryginalnych współrzędnych.

Użytkownik ma możliwość dostosowania następujących parametrów:

- rozmiar populacji: ile osobników będzie liczyło każde pokolenie, liczba nie zmienia się przez cały czas działania algorytmu
- wybór rodziców: jaka część populacji zostanie wybrana jako rodzice, którzy w operacji krzyżowania utworzą osobników potomnych do następnego pokolenia
- prawdopodobieństwo mutacji: określa prawdopodobieństwo z jakim nowo utworzony potomek może ulec mutacji
- dociekliwość: określa skłonność algorytmu do dalszego poszukiwania, w sytuacji gdy przez pewien czas nie poprawia się dotąd znalezione najlepsze rozwiązanie. Im większa dociekliwość, tym algorytm niechętniej się "poddaje". Parametr bezpośrednio steruje dopuszczalną liczbą iteracji bez poprawy rozwiązania, po których algorytm się zatrzyma.
- przekazuj rodziców: w przypadku gdy zaznaczone, do następnego pokolenia przekazywani są również rodzice, w przeciwnym wypadku nowa generacja zostanie utworzona w 100% z osobników potomnych

Po uruchomieniu programu przyciskiem start, na bieżąco wyświetlane są statystyki działania, takiej jak numer pokolenia, długość najkrótszej znalezionej do tej pory ścieżki oraz uśredniona długość dla całej populacji. Pasek pozostałego czasu, jest wizualizacją dociekliwości. Gdy algorytm utknął na pewnym rozwiązaniu i w kolejnych iteracjach nie może znaleźć lepszego, dociekliwość wyczerpuje się. Kiedy spadnie do zera, algorytm zatrzymuje się. W momencie znalezienia lepszego rozwiązania, pasek regeneruje się.
