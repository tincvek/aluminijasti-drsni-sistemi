import csv
import os
from pydoc import text
import re
import html


html_mapa = "html-ji"
csv_mapa = "podatki"
csv_ime_datoteke = "sistemi.csv"


def preberi_datoteko(mapa, ime_datoteke):
    
    #Prebere vsebino HTML datoteke in jo vrne kot niz.
    
    path = os.path.join(mapa, ime_datoteke)

    with open(path, "r", encoding="utf-8") as file_in:
        text = file_in.read()

    return text


def html_to_text(page_content):
    
    #Iz HTML-ja odstrani značke in naredi besedilo,
    #po katerem lahko iščemo z regularnimi izrazi.
    

    # odstrani javascript in css
    text = re.sub(r"<script.*?</script>", " ", page_content,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?</style>", " ", text,
                  flags=re.DOTALL | re.IGNORECASE)

    # odstrani HTML značke
    text = re.sub(r"<[^>]+>", " ", text)

    # pretvori npr. &amp; v &
    text = html.unescape(text)

    # več presledkov spremeni v enega
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def poisci_vrednosti(vzorec, text):
    
    #Poišče podatek z regularnim izrazom.
    #Če ga ne najde, vrne prazen niz.
    

    rezultat = re.search(vzorec, text, flags=re.IGNORECASE)

    if rezultat is None:
        return ""

    return rezultat.group(1).strip()


def najdi_podatke_sistemov(page_content, ime_datoteke):
    
    #Iz HTML-ja izlušči tehnične podatke in vrne slovar.
    

    text = html_to_text(page_content)

    # proizvajalec bomo zaenkrat določili iz imena datoteke
    if ime_datoteke.lower().startswith("reynaers"):
        proizvajalec = "Reynaers"
    elif ime_datoteke.lower().startswith("aluk"):
        proizvajalec = "AluK"
    elif ime_datoteke.lower().startswith("schuco"):
        proizvajalec = "Schüco"
    elif ime_datoteke.lower().startswith("cortizo"):
        proizvajalec = "Cortizo"
    else:
        proizvajalec = ""

    # ime sistema iz imena datoteke
    sistem = ime_datoteke.replace(".html", "")
    sistem = sistem.replace("reynaers_", "")
    sistem = sistem.replace("aluk_", "")
    sistem = sistem.replace("schuco_", "")
    sistem = sistem.replace("cortizo_", "")
    sistem = sistem.replace("_", " ")

    toplotna_prehodnost = poisci_vrednosti(r"(?:Thermal insulation\s*-\s*Uw|Uw value|Thermal transmittance|U value W/m²K \(Double glazing\)\s*:).*?<?\s*(\d+[.,]\d+)", text)

    max_visina = poisci_vrednosti(r"(?:Max\.?\s*height of vent|Max sash height|Max Frame Height|Maximum sash dimensions.*?Height\s*\(H\)).*?(\d+)", text)

    max_sirina = poisci_vrednosti(r"(?:Max\.?\s*width of vent|Max sash width|Maximum sash dimensions.*?Width\s*\(L\)).*?(\d+)", text)

    max_teza = poisci_vrednosti(r"(?:Max\.?\s*weight of vent|Maximum sash load|Maximum sash weight|Max sash weight|Max Vent Weight|Holds up to).*?(\d+)\s*kg?", text)

    globina_okvirja = poisci_vrednosti(r"(?:Depth\s+frame\s+2[- ]rail|Frame depth|Frame dimension|frame_dimension).*?(\d+)", text)

    najvecja_debelina_stekla = poisci_vrednosti(r"(?:Max\.?\s*glass thickness|Max glass thickness|Glazing\s*Max\.|Glazing thickness).*?(\d+)(?:\s*mm)?(?:\s*-\s*(\d+)\s*mm)?", text)

    steklo = re.search(r"(?:Max\.?\s*glass thickness|Max glass thickness|Glazing\s*Max\.|Glazing thickness).*?(\d+)\s*mm(?:\s*-\s*(\d+)\s*mm)?",text,flags=re.IGNORECASE)

    if steklo:
        if steklo.group(2):
            max_steklo = steklo.group(2)
        else:
            max_steklo = steklo.group(1)

    zrakotesnost = poisci_vrednosti(r"(?:Air tightness|Air permeability)(?:\s*\(Pa\))?\s*:?\s*(Class\s*\d+)", text)

    vodotesnost = poisci_vrednosti(r"(?:Water tightness|Watertightness|Water resistance)(?:\s*\(Pa\))?\s*:?\s*(Class\s*(?:E\d+|\d+[A-Z]?))", text)

    veter = poisci_vrednosti(r"(?:Wind load resistance|Wind resistance|Wind load)(?:\s*\(Pa\))?\s*:?\s*(Class\s*[A-Z]\d+)", text)

    aww = re.search(r"AWW Classification.*?(\d+)\s*/\s*([A-Z]?\d+[A-Z]?)\s*/\s*([A-Z]\d+)",text,flags=re.IGNORECASE)

    if aww:
        zrakotesnost = "Class " + aww.group(1)
        vodotesnost = "Class " + aww.group(2)
        veter = "Class " + aww.group(3)

    return {
    "proizvajalec": proizvajalec,
    "sistem": sistem,
    "toplotna_prehodnost": toplotna_prehodnost,
    "max_visina_mm": max_visina,
    "max_sirina_mm": max_sirina,
    "max_teza_kg": max_teza,
    "globina_okvirja_mm": globina_okvirja,
    "najvecja_debelina_stekla_mm": najvecja_debelina_stekla,
    "zrakotesnost": zrakotesnost,
    "vodotesnost": vodotesnost,
    "odpornost_na_veter": veter
}


def pridobi_sisteme_iz_mape(mapa):
    
    #Prebere vse HTML datoteke iz mape in iz vsake
    # naredi slovar z enim sistemom.
    

    sistemi = []

    for ime_datoteke in os.listdir(mapa):

        if ime_datoteke.endswith(".html"):
            page_content = preberi_datoteko(mapa, ime_datoteke)

            sistem = najdi_podatke_sistemov(page_content, ime_datoteke)

            sistemi.append(sistem)

    return sistemi


def write_csv(fieldnames, rows, mapa, ime_datoteke):
    os.makedirs(mapa, exist_ok=True)

    path = os.path.join(mapa, ime_datoteke)

    with open(path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def main():

    sistemi = pridobi_sisteme_iz_mape(html_mapa)


    fieldnames = [
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

    write_csv(
        fieldnames,
        sistemi,
        csv_mapa,
        csv_ime_datoteke
    )

    


if __name__ == "__main__":
    main()