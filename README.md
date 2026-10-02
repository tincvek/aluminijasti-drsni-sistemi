# Analiza aluminijastih drsnih sistemov

## Uvod

Pri projektni nalogi analiziram tehnične lastnosti aluminijastih drsnih sistemov različnih proizvajalcev. Podatke sem pridobila z uradnih spletnih strani proizvajalcev Reynaers, AluK in Cortizo.

Za posamezne sisteme sem zbrala podatke o toplotni prehodnosti, največji dovoljeni višini in širini, največji dovoljeni teži, globini okvirja, največji debelini stekla ter razredih zrakotesnosti, vodotesnosti in odpornosti na veter.

Namen projekta je primerjati posamezne aluminijaste drsne sisteme ter ugotoviti, kako se njihove tehnične lastnosti razlikujejo med proizvajalci.

## Pridobivanje podatkov

Datoteka `pridobi.py` s pomočjo knjižnice `requests` prenese HTML strani posameznih aluminijastih drsnih sistemov in jih shrani v mapo `html-ji`.

Datoteka `izlusci.py` nato prebere prenesene HTML datoteke, s pomočjo regularnih izrazov izlušči izbrane tehnične podatke ter jih shrani v datoteko `podatki/sistemi.csv`.

Ker različni proizvajalci tehnične podatke na svojih spletnih straneh zapisujejo na različne načine, so regularni izrazi prilagojeni različnim zapisom posameznih proizvajalcev.

## Datoteke

- `pridobi.py` – pridobivanje HTML strani s spleta
- `izlusci.py` – izluščanje tehničnih podatkov iz HTML datotek in zapis podatkov v CSV
- `analiza.ipynb` – analiza in grafični prikaz podatkov
- `podatki/sistemi.csv` – izluščeni podatki o aluminijastih drsnih sistemih
- `html-ji/` – lokalno shranjene HTML datoteke spletnih strani
- `.gitignore` – določa datoteke in mape, ki se ne shranjujejo v GitHub repozitorij

Mapa `html-ji` je vključena v `.gitignore`, zato se prenesene HTML datoteke ne shranjujejo v GitHub repozitorij.

## Uporaba

Za ponovno pridobivanje podatkov najprej zaženemo:

    python pridobi.py

Nato za izluščanje podatkov iz HTML datotek in izdelavo CSV datoteke zaženemo:

    python izlusci.py

Po zagonu se podatki shranijo v datoteko:

    podatki/sistemi.csv

Za analizo podatkov nato odpremo datoteko:

    analiza.ipynb

V Jupyter Notebooku zaženemo celice po vrsti.

## Analiza podatkov

V datoteki `analiza.ipynb` so podatki analizirani s pomočjo knjižnice `pandas`.

Analiza vključuje:

- pregled pridobljenih podatkov
- preverjanje podatkovnih tipov in manjkajočih vrednosti
- primerjavo toplotne prehodnosti sistemov
- primerjavo največjih dovoljenih višin in širin
- primerjavo največje dovoljene teže
- primerjavo največje dovoljene debeline stekla
- primerjavo globine okvirjev
- primerjavo proizvajalcev
- analizo zrakotesnosti
- analizo vodotesnosti
- analizo odpornosti na veter
- osnovni statistični pregled podatkov
- tabelarične prikaze rezultatov
- stolpčne, tortne, črtne in raztresene grafe

## Uporabljene knjižnice

Projekt uporablja naslednje Python knjižnice:

- `requests`
- `pandas`

Uporabljene so tudi standardne Python knjižnice:

- `csv`
- `os`
- `re`
- `html`

## Vir podatkov

Podatki so pridobljeni z uradnih spletnih strani proizvajalcev aluminijastih sistemov:

- Reynaers Aluminium
- AluK
- Cortizo

Za analizo so uporabljeni podatki, ki so bili objavljeni na spletnih straneh posameznih sistemov v času izdelave projekta.

## Zaključek

Projekt omogoča primerjavo različnih aluminijastih drsnih sistemov na podlagi njihovih tehničnih lastnosti.

Z avtomatskim pridobivanjem in izluščanjem podatkov je mogoče podatke različnih proizvajalcev združiti v enoten podatkovni nabor ter jih nato analizirati in grafično prikazati.

Ker proizvajalci podatke na svojih spletnih straneh zapisujejo na različne načine, je bilo pri izdelavi potrebno prilagoditi regularne izraze tako, da pravilno prepoznajo različne zapise enakih tehničnih lastnosti.

## Uporaba ChatGPT

Pri izdelavi seminarske naloge sem uporabljala ChatGPT za pomoč pri razlagi regularnih izrazov, odpravljanju napak v kodi, prilagajanju izluščanja podatkov različnim proizvajalcem ter pri analizi podatkov.

Podrobnejši povzetek uporabe ChatGPT je v datoteki `uporaba_chatgpt.md`.