# Povzetek pogovora s ChatGPT pri seminarski nalogi

Ta datoteka vsebuje izbrane in skrajšane dele pogovora s ChatGPT med izdelavo seminarske naloge **Analiza aluminijastih drsnih sistemov**. To ni dobeseden prepis celotnega pogovora, ampak izbor zahtevnejših delov, predvsem tam, kjer sem potrebovala pomoč pri regularnih izrazih, izluščanju podatkov iz HTML-ja, prilagajanju kode različnim proizvajalcem in analizi podatkov.

---

## 1. Zakaj mi pri nekaterih straneh podatke najde, pri Schüco pa ne, če jih jaz normalno vidim na spletni strani?

**Jaz:**  
Zakaj mi pri Schüco ne najde podatkov, če jih jaz na spletni strani vidim? Pri Reynaers pa recimo normalno dela.

**ChatGPT:**  
To se lahko zgodi zato, ker vsebina, ki jo vidiš v brskalniku, ni nujno že v začetnem HTML-ju, ki ga dobi `requests`.

Ko narediš:

```python
odgovor = requests.get(url)
```

in potem:

```python
odgovor.text
```

dobiš HTML, ki ga spletni strežnik pošlje ob zahtevi. Nekatere spletne strani pa del podatkov dodajo šele kasneje z JavaScriptom.

To pomeni, da lahko v brskalniku vidiš npr. tehnične podatke, ampak če jih iščeš v:

```python
odgovor.text
```

jih sploh ni.

Najprej je smiselno preveriti, ali se iskani izraz sploh pojavi v prenesenem HTML-ju:

```python
if "Thermal transmittance" in odgovor.text:
    print("Podatek obstaja v HTML-ju.")
else:
    print("Podatka ni v HTML-ju.")
```

Lahko iščeš tudi kakšno konkretno številko ali naslov tehnične lastnosti:

```python
print("Uw" in odgovor.text)
print("Air permeability" in odgovor.text)
print("Water tightness" in odgovor.text)
```

Če podatka ni v `odgovor.text`, regex ne more pomagati, ker regex išče samo po besedilu, ki ga dejansko ima na voljo.

Zato je bilo pri seminarski bolj smiselno izbrati proizvajalce, pri katerih so tehnični podatki prisotni že v HTML-ju, pridobljenem z `requests`. Tako sem ostala pri Reynaers, AluK in Cortizo, Schüco pa sem odstranila.

---

## 2. Kako naj ta cel HTML sploh spravim v neko normalno besedilo, da lahko potem regex išče po njem?

**Jaz:**  
HTML je ful nepregleden in ima noter vse mogoče tage, script, style pa ne vem kaj vse. Kako naj to očistim, da potem iščem samo po tekstu?

**ChatGPT:**  
Najlažje je narediti eno funkcijo, ki HTML po korakih očisti.

Uporabiš lahko:

```python
def html_v_besedilo(page_content):
    """Iz HTML-ja odstrani oznake in naredi navadno besedilo."""

    text = re.sub(
        r"<script.*?</script>",
        " ",
        page_content,
        flags=re.DOTALL | re.IGNORECASE
    )

    text = re.sub(
        r"<style.*?</style>",
        " ",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = html.unescape(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()
```

Kaj naredi vsak del:

```python
r"<script.*?</script>"
```

poišče celoten `<script> ... </script>` blok in ga zamenja s presledkom.

`re.DOTALL` pomeni, da `.` v regexu ujame tudi novo vrstico, kar je pomembno zato, ker je JavaScript pogosto napisan čez več vrstic.

`re.IGNORECASE` pa pomeni, da regex ne ločuje med velikimi in malimi črkami.

Enako velja za:

```python
r"<style.*?</style>"
```

Nato:

```python
r"<[^>]+>"
```

odstrani HTML značke, na primer:

```html
<div>
<span>
<p>
<h2>
```

`html.unescape(text)` pretvori HTML zapise, na primer:

```text
&amp; -> &
&nbsp; -> presledek
```

Na koncu:

```python
re.sub(r"\s+", " ", text)
```

več zaporednih presledkov, tabulatorjev ali novih vrstic spremeni v en sam presledek.

Tako iz zelo dolgega HTML dokumenta dobiš navadno besedilo, po katerem so regularni izrazi veliko lažji.

---

## 3. A rabim res za vsak podatek posebej cel `re.search`, ker bo tega ful?

**Jaz:**  
A moram za vsako stvar pisat posebej `re.search`, `if`, `group` in vse to? Ker imam višino, širino, težo, Uw, steklo...

**ChatGPT:**  
Ni treba. Bolje je narediti eno pomožno funkcijo, ki jo potem uporabiš za različne podatke.

```python
def poisci_vrednost(vzorec, text):
    """Poišče vrednost z regularnim izrazom.
    Če je ne najde, vrne prazen niz.
    """

    rezultat = re.search(
        vzorec,
        text,
        flags=re.IGNORECASE
    )

    if rezultat is None:
        return ""

    return rezultat.group(1).strip()
```

Potem lahko isto funkcijo uporabiš večkrat:

```python
toplotna_prehodnost = poisci_vrednost(
    r"Uw value.*?(\d+[.,]\d+)",
    text
)

najvecja_visina = poisci_vrednost(
    r"Max sash height.*?(\d+)",
    text
)

najvecja_sirina = poisci_vrednost(
    r"Max sash width.*?(\d+)",
    text
)
```

Pomemben del je:

```python
rezultat.group(1)
```

To vrne vsebino prve zajete skupine v oklepajih.

Če je regex:

```python
r"Uw value.*?(\d+[.,]\d+)"
```

in je besedilo:

```text
Uw value 1.3 W/m²K
```

bo:

```python
rezultat.group(1)
```

vrnil:

```text
1.3
```

Če ni zadetka, funkcija vrne:

```python
""
```

in program zaradi manjkajočega podatka ne pade.

---

## 4. Meni še vedno ni jasno kaj pomenijo vsi ti znaki v regexu, lahko mi razložiš čist po delih?

**Jaz:**  
Kaj pomenijo `.*?`, `\d+`, `\s*`, `(?:...)` pa vsi ti znaki? Ker zgleda kot random znaki haha.

**ChatGPT:**  
Najpomembnejši deli, ki jih uporabljaš v tej seminarski:

### `\d`

Pomeni eno števko.

```python
r"\d"
```

ujame na primer:

```text
7
```

### `\d+`

Pomeni eno ali več števk.

```python
r"\d+"
```

ujame:

```text
7
52
400
3300
```

### `\s`

Pomeni whitespace, torej presledek, tabulator ali novo vrstico.

### `\s*`

Pomeni nič ali več presledkov.

Na primer:

```python
r"52\s*mm"
```

ujame oboje:

```text
52mm
52 mm
```

### `.`

Pomeni skoraj katerikoli znak.

### `.*`

Pomeni nič ali več poljubnih znakov.

### `.*?`

To je podobno kot `.*`, ampak išče čim krajši možni del.

Na primer:

```python
r"Uw value.*?(\d+[.,]\d+)"
```

pomeni:
1. najdi `Uw value`,
2. nato pojdi naprej čez poljubno besedilo,
3. ustavi se pri prvi decimalni številki.

### `[.,]`

Pomeni pika ali vejica.

Zato:

```python
r"\d+[.,]\d+"
```

ujame:

```text
0.8
1.4
1,7
```

### `(...)`

Navaden oklepaj ustvari zajeto skupino.

Na primer:

```python
r"Uw value.*?(\d+[.,]\d+)"
```

številka v oklepaju je tista vrednost, ki jo kasneje dobiš z:

```python
group(1)
```

### `(?:...)`

To je skupina, ki jo uporabiš samo za združevanje možnosti, ne pa za shranjevanje.

Na primer:

```python
r"(?:Uw value|Thermal transmittance).*?(\d+[.,]\d+)"
```

pomeni:

```text
Uw value
ALI
Thermal transmittance
```

Nato pa prva prava zajeta skupina ostane samo številka.

---

## 5. Kako naredim en regex za vse tri proizvajalce, če vsak isto stvar napiše drugače?

**Jaz:**  
Reynaers ima eno ime, AluK drugo, Cortizo tretje. Kako naredim, da mi ni treba imet za vsakega čisto svoje kode?

**ChatGPT:**  
Za isto tehnično lastnost lahko v enem regexu navedeš več možnih zapisov.

Na primer za toplotno prehodnost:

```python
toplotna_prehodnost = poisci_vrednost(
    r"(?:Thermal insulation\s*-\s*Uw"
    r"|Uw value"
    r"|Thermal transmittance"
    r"|U value W/m²K \(Double glazing\)\s*:)"
    r".*?<?\s*(\d+[.,]\d+)",
    text
)
```

Razlaga:

```python
(?:A|B|C|D)
```

pomeni, da se lahko ujame katerikoli od teh zapisov.

Torej lahko regex najde podatke, če stran uporablja:

```text
Thermal insulation - Uw
Uw value
Thermal transmittance
U value W/m²K (Double glazing):
```

Del:

```python
.*?
```

dovoli, da je med imenom lastnosti in številko še nekaj drugega besedila.

Del:

```python
<?\s*
```

dovoli tudi zapis, kjer se pojavi:

```text
< 1.3
```

ali samo:

```text
1.3
```

Na koncu:

```python
(\d+[.,]\d+)
```

zajame decimalno vrednost.

Enako lahko narediš za višino:

```python
najvecja_visina = poisci_vrednost(
    r"(?:Max\.?\s*height of vent"
    r"|Max sash height"
    r"|Max Frame Height"
    r"|Maximum sash dimensions.*?Height\s*\(H\))"
    r".*?(\d+)",
    text
)
```

Za širino:

```python
najvecja_sirina = poisci_vrednost(
    r"(?:Max\.?\s*width of vent"
    r"|Max sash width"
    r"|Maximum sash dimensions.*?Width\s*\(L\))"
    r".*?(\d+)",
    text
)
```

Za največjo težo:

```python
najvecja_teza = poisci_vrednost(
    r"(?:Max\.?\s*weight of vent"
    r"|Maximum sash load"
    r"|Maximum sash weight"
    r"|Max sash weight"
    r"|Max Vent Weight"
    r"|Holds up to)"
    r".*?(\d+)\s*kg?",
    text
)
```

Tako en `izlusci.py` podpira več različnih zapisov, ne da bi za vsak sistem pisala svojo funkcijo.

---

## 6. Kaj pa okvir? Pri enem proizvajalcu mi ga najde, pri Cortizo pa ne.

**Jaz:**  
Zakaj mi globino okvirja pri Reynaers najde, pri Cortizo pa ne? A lahko dam nek dodaten regex samo za Cortizo?

**ChatGPT:**  
Ja. Najprej narediš splošen regex:

```python
globina_okvirja = poisci_vrednost(
    r"(?:Depth\s+frame\s+2[- ]rail"
    r"|Frame depth"
    r"|Frame dimension"
    r"|frame_dimension)"
    r".*?(\d+)",
    text
)
```

Če pri Cortizo to ne zadostuje, lahko dodaš fallback.

Najprej določiš proizvajalca:

```python
if ime_datoteke.lower().startswith("reynaers"):
    proizvajalec = "Reynaers"

elif ime_datoteke.lower().startswith("aluk"):
    proizvajalec = "AluK"

elif ime_datoteke.lower().startswith("cortizo"):
    proizvajalec = "Cortizo"

else:
    proizvajalec = ""
```

Nato:

```python
if proizvajalec == "Cortizo" and globina_okvirja == "":
    globina_okvirja = poisci_vrednost(
        r"Frame.*?(\d+)\s*mm",
        text
    )
```

Torej:
1. najprej poskusi splošni regex,
2. če ni rezultata in je proizvajalec Cortizo,
3. poskusi še dodatni vzorec.

To je uporabno, kadar ima en proizvajalec posebno strukturo zapisa.

---

## 7. Pri steklu imam nekje samo eno številko, nekje pa razpon. Kako naj vzamem vedno največjo?

**Jaz:**  
Pri debelini stekla mi enkrat piše recimo 52 mm, nekje pa 38–52 mm. Jaz rabim max debelino. Kako naj regex ve katero naj vzame?

**ChatGPT:**  
Tu je bolje uporabiti `re.search()` neposredno, ker želiš možnost dveh zajetih skupin.

```python
steklo = re.search(
    r"(?:Max\.?\s*glass thickness"
    r"|Max glass thickness"
    r"|Glazing\s*Max\."
    r"|Glazing thickness)"
    r".*?(\d+)\s*mm"
    r"(?:\s*-\s*(\d+)\s*mm)?",
    text,
    flags=re.IGNORECASE
)
```

Prva skupina:

```python
steklo.group(1)
```

je prva številka.

Druga skupina:

```python
steklo.group(2)
```

je druga številka, če obstaja.

Potem:

```python
if steklo:
    if steklo.group(2):
        najvecja_debelina_stekla = steklo.group(2)
    else:
        najvecja_debelina_stekla = steklo.group(1)
```

Primer 1:

```text
Max glass thickness 52 mm
```

rezultat:

```text
group(1) = 52
group(2) = None
```

zato shrani:

```text
52
```

Primer 2:

```text
Glazing thickness 38 mm - 52 mm
```

rezultat:

```text
group(1) = 38
group(2) = 52
```

zato shrani:

```text
52
```

To je bolj pravilno, ker stolpec predstavlja največjo dovoljeno debelino stekla.

---

## 8. Pri AluK so zrak, voda pa veter vsi skupaj v eni vrstici, kako naj to spravim v tri stolpce?

**Jaz:**  
AluK ima nekaj `AWW Classification 4 / 8A / A4`. Kako to razbijem posebej na zrakotesnost, vodotesnost pa veter?

**ChatGPT:**  
Tu lahko en regex zajame tri različne vrednosti.

```python
razredi_tesnjenja = re.search(
    r"AWW Classification.*?"
    r"(\d+)\s*/\s*"
    r"([A-Z]?\d+[A-Z]?)\s*/\s*"
    r"([A-Z]\d+)",
    text,
    flags=re.IGNORECASE
)
```

Če ima stran:

```text
AWW Classification 4 / 8A / A4
```

bo:

```python
razredi_tesnjenja.group(1)
```

vrnil:

```text
4
```

```python
razredi_tesnjenja.group(2)
```

vrnil:

```text
8A
```

in:

```python
razredi_tesnjenja.group(3)
```

vrnil:

```text
A4
```

Nato jih shraniš:

```python
if razredi_tesnjenja:
    zrakotesnost = (
        "Class " + razredi_tesnjenja.group(1)
    )

    vodotesnost = (
        "Class " + razredi_tesnjenja.group(2)
    )

    odpornost_na_veter = (
        "Class " + razredi_tesnjenja.group(3)
    )
```

Tako iz ene vrstice na spletni strani dobiš tri ločene stolpce v CSV datoteki.

---

## 9. Kako naj naredim regex za zrakotesnost, vodotesnost pa veter pri ostalih proizvajalcih?

**Jaz:**  
Kaj pa Reynaers pa Cortizo, kjer ni AWW skupaj? Kako naj tam posebej najdem classe?

**ChatGPT:**  
Za vsak tip lahko narediš splošen regex.

### Zrakotesnost

```python
zrakotesnost = poisci_vrednost(
    r"(?:Air tightness|Air permeability)"
    r"(?:\s*\(Pa\))?"
    r".*?(Class\s*\d+)",
    text
)
```

Ta regex sprejme:

```text
Air tightness
Air permeability
Air tightness (Pa)
Air permeability (Pa)
```

in nato išče zapis:

```text
Class 4
Class4
```

### Vodotesnost

```python
vodotesnost = poisci_vrednost(
    r"(?:Water tightness"
    r"|Watertightness"
    r"|Water resistance)"
    r"(?:\s*\(Pa\))?"
    r".*?(Class\s*(?:E\d+|\d+[A-Z]?))",
    text
)
```

Ta del:

```python
(?:E\d+|\d+[A-Z]?)
```

lahko ujame na primer:

```text
E750
E1200
8A
7B
```

### Odpornost na veter

```python
odpornost_na_veter = poisci_vrednost(
    r"(?:Wind load resistance"
    r"|Wind resistance"
    r"|Wind load)"
    r"(?:\s*\(Pa\))?"
    r".*?(Class\s*[A-Z]\d+)",
    text
)
```

To ujame na primer:

```text
Class C5
Class B5
Class A4
```

Po teh treh splošnih regexih lahko še vedno dodaš AluK AWW klasifikacijo, ki ob uspešnem zadetku te tri vrednosti prepiše.

---

## 10. Kako naj sploh naredim eno funkcijo, ki iz ene HTML strani vrne vse podatke za en sistem?

**Jaz:**  
Okej, zdaj imam vse te regexe, ampak kako naj to dam skupaj, da iz ene strani dobim en cel sistem?

**ChatGPT:**  
Lahko narediš eno glavno funkcijo, ki:
1. HTML spremeni v navadno besedilo,
2. ugotovi proizvajalca,
3. določi ime sistema,
4. poišče vse tehnične podatke,
5. vrne slovar.

Primer jedra funkcije:

```python
def najdi_podatke_sistemov(page_content, ime_datoteke):

    text = html_v_besedilo(page_content)

    if ime_datoteke.lower().startswith("reynaers"):
        proizvajalec = "Reynaers"

    elif ime_datoteke.lower().startswith("aluk"):
        proizvajalec = "AluK"

    elif ime_datoteke.lower().startswith("cortizo"):
        proizvajalec = "Cortizo"

    else:
        proizvajalec = ""

    sistem = ime_datoteke.replace(".html", "")
    sistem = sistem.replace("reynaers_", "")
    sistem = sistem.replace("aluk_", "")
    sistem = sistem.replace("cortizo_", "")
    sistem = sistem.replace("_", " ")

    toplotna_prehodnost = poisci_vrednost(
        r"(?:Thermal insulation\s*-\s*Uw"
        r"|Uw value"
        r"|Thermal transmittance"
        r"|U value W/m²K \(Double glazing\)\s*:)"
        r".*?<?\s*(\d+[.,]\d+)",
        text
    )

    najvecja_visina = poisci_vrednost(
        r"(?:Max\.?\s*height of vent"
        r"|Max sash height"
        r"|Max Frame Height"
        r"|Maximum sash dimensions.*?Height\s*\(H\))"
        r".*?(\d+)",
        text
    )

    najvecja_sirina = poisci_vrednost(
        r"(?:Max\.?\s*width of vent"
        r"|Max sash width"
        r"|Maximum sash dimensions.*?Width\s*\(L\))"
        r".*?(\d+)",
        text
    )

    najvecja_teza = poisci_vrednost(
        r"(?:Max\.?\s*weight of vent"
        r"|Maximum sash load"
        r"|Maximum sash weight"
        r"|Max sash weight"
        r"|Max Vent Weight"
        r"|Holds up to)"
        r".*?(\d+)\s*kg?",
        text
    )

    globina_okvirja = poisci_vrednost(
        r"(?:Depth\s+frame\s+2[- ]rail"
        r"|Frame depth"
        r"|Frame dimension"
        r"|frame_dimension)"
        r".*?(\d+)",
        text
    )

    if proizvajalec == "Cortizo" and globina_okvirja == "":
        globina_okvirja = poisci_vrednost(
            r"Frame.*?(\d+)\s*mm",
            text
        )

    najvecja_debelina_stekla = poisci_vrednost(
        r"(?:Max\.?\s*glass thickness"
        r"|Max glass thickness"
        r"|Glazing\s*Max\."
        r"|Glazing thickness)"
        r".*?(\d+)",
        text
    )

    zrakotesnost = poisci_vrednost(
        r"(?:Air tightness|Air permeability)"
        r"(?:\s*\(Pa\))?"
        r".*?(Class\s*\d+)",
        text
    )

    vodotesnost = poisci_vrednost(
        r"(?:Water tightness"
        r"|Watertightness"
        r"|Water resistance)"
        r"(?:\s*\(Pa\))?"
        r".*?(Class\s*(?:E\d+|\d+[A-Z]?))",
        text
    )

    odpornost_na_veter = poisci_vrednost(
        r"(?:Wind load resistance"
        r"|Wind resistance"
        r"|Wind load)"
        r"(?:\s*\(Pa\))?"
        r".*?(Class\s*[A-Z]\d+)",
        text
    )

    return {
        "proizvajalec": proizvajalec,
        "sistem": sistem,
        "toplotna_prehodnost": toplotna_prehodnost,
        "max_visina_mm": najvecja_visina,
        "max_sirina_mm": najvecja_sirina,
        "max_teza_kg": najvecja_teza,
        "globina_okvirja_mm": globina_okvirja,
        "najvecja_debelina_stekla_mm":
            najvecja_debelina_stekla,
        "zrakotesnost": zrakotesnost,
        "vodotesnost": vodotesnost,
        "odpornost_na_veter": odpornost_na_veter
    }
```

To je glavna funkcija, ki poveže vse posamezne regexe.

---

## 11. Kako naredim, da gre čez vse HTML-je v mapi in ne rabim vsakega posebej?

**Jaz:**  
Kako naredim, da samo vržem vse HTML datoteke v `html-ji`, potem pa naj program sam gre čez vse?

**ChatGPT:**  
Uporabiš `os.listdir()`.

```python
def pridobi_sisteme_iz_mape(mapa):

    sistemi = []

    for ime_datoteke in os.listdir(mapa):

        if ime_datoteke.endswith(".html"):

            page_content = preberi_datoteko(
                mapa,
                ime_datoteke
            )

            sistem = najdi_podatke_sistemov(
                page_content,
                ime_datoteke
            )

            sistemi.append(sistem)

    return sistemi
```

Potek je:
1. `os.listdir(mapa)` vrne vse datoteke v mapi,
2. preveriš, ali se ime konča z `.html`,
3. prebereš datoteko,
4. izluščiš podatke,
5. slovar dodaš v seznam `sistemi`.

Tako lahko kasneje dodaš še kakšno novo HTML datoteko, ne da bi spreminjala samo zanko.

---

## 12. Zakaj mi je tukaj začelo rumeno podčrtovat `ime_datoteke`, ko sem preimenovala `filename`?

**Jaz:**  
Preimenovala sem `filename` v `ime_datoteke`, zdaj pa mi tukaj ne gre in je podčrtano. Zakaj?

**ChatGPT:**  
Težava je bila, da so bila imena spremenljivk spremenjena samo na nekaterih mestih.

Na primer:

```python
for filename in os.listdir(directory):
```

ampak spodaj:

```python
page_content = preberi_datoteko(
    directory,
    ime_datoteke
)
```

`ime_datoteke` tukaj ne obstaja, ker je zanka še vedno definirala spremenljivko `filename`.

Pravilno mora biti dosledno:

```python
def pridobi_sisteme_iz_mape(mapa):

    sistemi = []

    for ime_datoteke in os.listdir(mapa):

        if ime_datoteke.endswith(".html"):

            page_content = preberi_datoteko(
                mapa,
                ime_datoteke
            )

            sistem = najdi_podatke_sistemov(
                page_content,
                ime_datoteke
            )

            sistemi.append(sistem)

    return sistemi
```

Pri preimenovanju je zato treba spremeniti vse pojavitve:

```text
directory -> mapa
filename -> ime_datoteke
systems -> sistemi
system -> sistem
pattern -> vzorec
match -> rezultat
```

Če eno staro ime ostane, Python tega novega imena ne pozna.

---

## 13. Kako naj vse te slovarje na koncu spravim v en CSV?

**Jaz:**  
Okej, imam seznam vseh sistemov. Kako to zapišem v `sistemi.csv`, da bodo ključi stolpci?

**ChatGPT:**  
Za to je primeren `csv.DictWriter`.

```python
def zapisi_csv(
    imena_stolpcev,
    rows,
    mapa,
    ime_datoteke
):

    os.makedirs(
        mapa,
        exist_ok=True
    )

    path = os.path.join(
        mapa,
        ime_datoteke
    )

    with open(
        path,
        "w",
        encoding="utf-8",
        newline=""
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=imena_stolpcev
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)
```

`fieldnames` določa vrstni red stolpcev.

Primer:

```python
imena_stolpcev = [
    "proizvajalec",
    "sistem",
    "toplotna_prehodnost",
    "max_visina_mm",
    "max_sirina_mm",
    "max_teza_kg",
    "globina_okvirja_mm",
    "najvecja_debelina_stekla_mm",
    "zrakotesnost",
    "vodotesnost",
    "odpornost_na_veter"
]
```

Vsak slovar iz seznama `sistemi` se nato zapiše kot ena vrstica.

---

## 14. Zakaj mi pandas kaže toplotno prehodnost kot `object`, če so pa noter številke?

**Jaz:**  
Zakaj mi `toplotna_prehodnost` ni številka? Nekje imam 1,7, drugje 0.8.

**ChatGPT:**  
Ker so decimalke zapisane na dva različna načina.

Na primer:

```text
1,7
0.8
```

Pandas zaradi vejice stolpec lahko obravnava kot besedilo.

Najprej zamenjaš:

```text
,
```

s:

```text
.
```

in nato pretvoriš v `float`.

```python
SISTEMI["toplotna_prehodnost"] = (
    SISTEMI["toplotna_prehodnost"]
    .str.replace(",", ".", regex=False)
    .astype(float)
)
```

Po tem lahko preveriš:

```python
SISTEMI.dtypes
```

in stolpec mora biti:

```text
float64
```

Potem lahko normalno delaš:

```python
SISTEMI["toplotna_prehodnost"].mean()
```

ali:

```python
SISTEMI.sort_values(
    "toplotna_prehodnost"
)
```

---

## 15. Kako naj najdem pet najboljših glede izolacije in zakaj sortiram tako?

**Jaz:**  
Kako naredim top 5 najbolj izoliranih? Pa a dam `ascending=False` ali ne?

**ChatGPT:**  
Pri Uw velja: nižja vrednost pomeni boljšo toplotno izolativnost.

Zato sortiraš od najmanjše proti največji:

```python
SISTEMI.sort_values(
    "toplotna_prehodnost"
).head()
```

Privzeto je:

```python
ascending=True
```

zato tega ni treba posebej napisati.

Če bi dala:

```python
ascending=False
```

bi dobila sisteme z največjo Uw vrednostjo, kar bi pomenilo slabšo toplotno izolativnost.

---

## 16. Kako naredim neko primerjavo proizvajalcev, ne samo posameznih sistemov?

**Jaz:**  
Kako lahko primerjam Reynaers, AluK in Cortizo skupaj, recimo povprečno višino, širino pa težo?

**ChatGPT:**  
Za to uporabiš `groupby`.

```python
SISTEMI.groupby("proizvajalec")[
    [
        "max_visina_mm",
        "max_sirina_mm",
        "max_teza_kg"
    ]
].mean()
```

To združi vrstice po proizvajalcu in izračuna povprečje.

Če želiš še graf:

```python
SISTEMI.groupby("proizvajalec")[
    [
        "max_visina_mm",
        "max_sirina_mm",
        "max_teza_kg"
    ]
].mean().plot(
    kind="bar",
    figsize=(10, 6),
    title="Primerjava povprečnih dimenzij in nosilnosti po proizvajalcu"
)
```

Tako dobiš za vsakega proizvajalca tri stolpce:
- povprečna največja višina,
- povprečna največja širina,
- povprečna največja teža.

---

## 17. Kaj naj dam pod grafe in tabele? A je dovolj samo komentar nad kodo?

**Jaz:**  
A moram pod vsak graf še nekaj napisat? Ker nad kodo imam že komentar, kaj funkcija naredi.

**ChatGPT:**  
Komentar nad kodo in Markdown pod grafom imata drugačen namen.

Komentar nad kodo:

```python
# Prikaže stolpčni graf povprečne toplotne prehodnosti po proizvajalcih.
```

razloži, kaj dela koda.

Markdown pod grafom pa razloži rezultat, na primer:

```text
Graf prikazuje povprečno toplotno prehodnost sistemov posameznega proizvajalca. Primerjava omogoča pregled razlik v povprečni toplotni izolativnosti med proizvajalci.
```

Pri bolj konkretnih grafih lahko napišeš tudi ugotovitev, na primer:

```text
Graf prikazuje primerjavo povprečne največje višine, širine in dovoljene teže sistemov proizvajalcev AluK, Cortizo in Reynaers. Reynaers ima v analiziranem naboru v povprečju nekoliko večjo največjo višino in dovoljeno težo, medtem ko ima Cortizo nekoliko večjo povprečno širino.
```

Pri tabelah, kot so:

```python
SISTEMI.head()
SISTEMI.info()
SISTEMI.dtypes
```

ni treba pod vsako posebej pisati razlage.

Pri analitičnih tabelah pa je smiselno, na primer:

```python
SISTEMI.sort_values(
    "toplotna_prehodnost"
).head()
```

in pod tabelo:

```text
Tabela prikazuje pet sistemov z najnižjo toplotno prehodnostjo. Nižja vrednost Uw pomeni boljšo toplotno izolativnost.
```

---

## 18. Kako naj v zaključku napišem nekaj dejanskega in ne samo da sem naredila analizo?

**Jaz:**  
Kaj lahko napišem v zaključek, da bo dejansko nek sklep in ne samo "naredila sem grafe"?

**ChatGPT:**  
Zaključek naj povzame dejanske ugotovitve in omejitve.

Primer:

```text
Na podlagi analize lahko ugotovimo, da se aluminijasti drsni sistemi različnih proizvajalcev precej razlikujejo glede toplotne prehodnosti, največjih dimenzij, nosilnosti in drugih tehničnih lastnosti.

Pri toplotni prehodnosti imajo nekateri sistemi izrazito nižje vrednosti Uw, kar pomeni boljšo toplotno izolativnost. Razlike so opazne tudi pri največjih dovoljenih dimenzijah in nosilnosti, saj nekateri sistemi omogočajo bistveno večje in težje steklene elemente.

Večina analiziranih sistemov dosega visok razred zrakotesnosti, medtem ko se pri vodotesnosti in odpornosti na veter pojavlja več različnih razredov.

Iz analize lahko sklepamo, da ni enega sistema, ki bi bil najboljši po vseh kriterijih hkrati. Nekateri sistemi izstopajo pri izolativnosti, drugi pri dimenzijah ali nosilnosti, zato je izbira primernega sistema odvisna od zahtev posameznega projekta.

Pri izdelavi naloge je bilo pomembno tudi to, da proizvajalci tehnične podatke zapisujejo na različne načine. Zaradi tega je bilo treba regularne izraze prilagoditi več različnim zapisom iste tehnične lastnosti.
```

Ta zadnji del je pomemben, ker pove tudi nekaj o samem programerskem problemu seminarske, ne samo o rezultatih grafov.

---

## Povzetek uporabe ChatGPT

ChatGPT sem uporabljala predvsem pri:
- razlagi regularnih izrazov,
- sestavljanju regexov za različne proizvajalce,
- iskanju napak pri izluščanju podatkov,
- razlagi razlik med HTML-jem in vsebino, naloženo z JavaScriptom,
- čiščenju HTML besedila,
- razdeljevanju skupnih AWW razredov na več stolpcev,
- obravnavi razponov pri debelini stekla,
- popravljanju imen spremenljivk,
- zapisovanju podatkov v CSV,
- pretvorbi podatkovnih tipov v pandas,
- izdelavi primerjav in grafov,
- oblikovanju Markdown razlag, uvoda, zaključka in README datoteke.

Največ pomoči sem potrebovala pri delu z regularnimi izrazi, ker Reynaers, AluK in Cortizo iste tehnične lastnosti na spletnih straneh zapisujejo na različne načine. Končne rezultate sem sproti preverjala z zagonom programov in pregledom ustvarjene CSV datoteke ter analiz v Jupyter Notebooku.
