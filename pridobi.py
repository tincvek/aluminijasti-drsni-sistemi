import requests

# Slovar strani, ki jih želim prenesti.
# Ključ = ime HTML datoteke
# Vrednost = URL spletne strani.
strani = {
    "reynaers_masterpatio.html":
        "https://www.reynaers.com/products/sliding-folding/masterpatio/technical-info",

    "reynaers_conceptpatio130.html":
        "https://www.reynaers.com/products/sliding-folding/conceptpatio-130/technical-info",

    "reynaers_conceptpatio155.html":
        "https://www.reynaers.com/products/sliding-folding/conceptpatio-155/technical-info",

    "reynaers_hifinity.html":
        "https://www.reynaers.com/products/sliding-folding/hifinity/technical-info",

    "reynaers_slimpatio68.html":
        "https://www.reynaers.com/products/sliding-folding/slimpatio-68/technical-info",

    "reynaers_conceptpatio68.html":
        "https://www.reynaers.com/products/sliding-folding/conceptpatio-68/technical-info",

    "aluk_sc140tt.html":
        "https://mideast.aluk.com/en/products/sliding-doors/sc140tt",

    "aluk_infinium.html":
        "https://ie.aluk.com/en_ie/products/folding-and-sliding-doors/infinium",

    "aluk_sc156.html":
        "https://uk.aluk.com/en-gb/products/folding-and-sliding-doors/sc156",

    "cortizo_corvision.html":
        "https://www.cortizo.com/en/sistemas/ver/55/cor-vision-sliding.html",

    "cortizo_corvisionevolution.html":
    "https://www.cortizo.com/en/sistemas/ver/183/cor-vision-evolution-sliding.html",

    "cortizo_4600plus.html":
        "https://www.cortizo.com/en/sistemas/ver/175/4600-plus-lift--slide.html",

    "cortizo_4700.html":
        "https://www.cortizo.com/en/sistemas/ver/92/4700-sliding.html",
}



for ime_datoteke, url in strani.items():

    
    odgovor = requests.get(url)

    # Izpiše ime datoteke, statusno kodo in dolžino HTML-ja.
    # preverjanje, ali se je stran pravilno prenesla.
    print(
        ime_datoteke,
        odgovor.status_code,
        len(odgovor.text)
    )

    # Statusna koda 200 pomeni: zahteva je bila uspešna in strežnik je vrnil spletno stran. Zato HTML shranimo samo, če je status 200.
    if odgovor.status_code == 200:

        
        with open(
            f"html-ji/{ime_datoteke}",
            "w",
            encoding="utf-8"
        ) as datoteka:

            
            datoteka.write(odgovor.text)