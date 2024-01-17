# Skript pro srovnání datových služeb v Pythonu

Tento Python skript je navržen pro použití v prostředí datového skladu firmy. Slouží k volání jedné ze tří datových služeb, kde každá služba existuje na dvou různých systémech. Skript provádí identická volání na obě služby, zaznamenává doby odezvy a porovnává obsah odpovědí.
Jde tedy o nástroj, který zároveň umožňuje spouštět Unit testy transformací Elastic Pipelines - zda data doputovala do ElasticSearch Indexu v totožném formátu v jakém se nachází v Oracle Databázi, a navíc nástroj umožňuje jednoduché performance testy DB vs. Elastic z pohledu odezvy pro jednoho uživatele služeb (paralelní volání obou služeb více uživateli najednou se testuje skrze Locust framework viz. kapitola Locust a testování zátěže).

## Předpoklady

- Python 3.x
- Požadované knihovny Pythonu (specifikovány v `requirements.txt`)

## Instalace

1. Naklonujte tento repozitář na svůj lokální počítač.

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Nainstalujte požadované knihovny Pythonu.

```bash
pip install -r requirements.txt
```

## Použití

Pro spuštění skriptu použijte následující příkaz:
```bash
python main.py <file_path> [-a <agg_type>] [-i <index>] [--visualize] [--test]
```

### Argumenty

- `file_path` (povinný): Cesta k JSON souboru s daty k zpracování.

Volitelné argumenty:

- `-a, --agg <agg_type>`: Typ agregace k provedení (vyberte z 1, 2 nebo 3). Výchozí hodnota je 1.

- `-i, --index <index>`: Index dotazu k zpracování (např. 0 nebo 1-3). Použijte tuto volbu, pokud chcete testovat pouze podmnožinu dat ze souboru.

- `--visualize`: Pokud je tento příznak poskytnut, na konci skriptu bude také zobrazena vizualizace pomocí knihovny Pyplot zobrazující časy odezvy a volání, která se neshodují.

- `--test`: Pokud je poskytnuto, skript provede volání na testovacích prostředích Oracle a ElasticSearch. Výchozím nastavením jsou vývojová prostředí.

## Příklad použití

```bash
# Spusťte skript s povinnými a volitelnými argumenty
python main.py data.json -a 2 -i 1-3 --visualize --test
```

V tomto příkladu skript zpracovává data z `data.json`, provádí agregaci typu 2, zpracovává dotazy od indexu 1 do 3, vizualizuje výsledky a volá na testovacích prostředích.

### Formát dat

Data v vstupním JSON souboru mají formát národní pro služby databáze Oracle s některými úpravami. Hlavní klíče/parametry každého volání služby musí být první v pořadí ve souboru. Hodnoty hlavních klíčů jsou uloženy ve vnořeném poli. Pokud existuje více vnořených polí s hlavními klíči, každé z těchto polí bude prováděno jako samostatné volání. Tedy v příkladu volání uvedeném výše se pro první sadu dat provedou 3 samostatná volání služby.

Příklad formátu dat:

```json
[
    {
        "partnerKeys": [
            [3960547, 3960548], [3960547], [3960548]
        ],
        "offerProcessedFlag": false
    },
    {
        "partnerKeys": [
            [4968026]
        ],
        "offerProcessedFlag": true,
        "offerValidFromEnd": "2023-12-21",
        "offerValidFromStart": "2023-08-21",
        "offerValidToEnd": "2024-11-21",
        "offerValidToStart": "2023-11-21",
        "offerStatus": {
            "entrySystemSpecificId": "string",
            "systemId": "string",
            "entryId": "ZR_ZOPI.E0003"
        }
    },
    {
        "organizationUnitKeys": [
            [92001], [79660]
        ],
        "offerProcessedFlag": true
    },
    {
        "organizationUnitKeys": [
            [79660, 20104020]
        ],
        "offerValidFromStart": "2022-04-25T09:05:40Z",
        "offerProcessedFlag": false
    }
]
```

## Výstup

Skript provede zvolená volání služeb na obou systémech a poskytne srovnání doby odezvy a obsahu odpovědí. Srovnání je během běhu skriptu vypisováno na příkazovou řádku a zároveň jsou všechna jednotlivá volání uložena do csv souboru log_X.csv. Do csv souboru je ukládán čas volání služeb, odezva služeb z obou systémů, typ služby (tedy typ agregace), počet nepovinných parametrů, počet elementů navrácených voláním služby a pokud se obsah odpovědí služby mezi databází a ElasticSearchem liší, tak také index/pozice chyby v odpovědi, rozdílné hodnoty a celkový počet chyb/rozdílů v daném volání.

**Ukázka výstupu:**

příkazový řádek:
```
=======
Database list: [[3649891, 79536, 'Petra', 'Juliusová', 1]]
Database response took 0.09028315544128418 seconds.
Elasticsearch list: [['3649891', '79536', 'Petra', 'Juliusová', 1]]
Elasticsearch response took 0.06245732307434082 seconds.
=======
Database list: [[5814522, 79660, 'login', 'QYCPRRPA094', 126]]
Database response took 0.11236119270324707 seconds.
Elasticsearch list: [['5814522', '79660', 'login', 'QYCPRRPA094', 95]]
Elasticsearch response took 0.0713965892791748 seconds.
The responses have different values at index 4: 126 and 95

```

csv soubor:

|   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|
|date|dbTime|esTime|aggType|optionalParams|diffIndex|diffDbValue|diffEsValue|elements|mistakes|
|14:34:07|0.03993344306945801|0.03095388412475586|3|1|[]|[]|[]|5|0|
|14:34:08|0.036702632904052734|0.03459668159484863|3|2|[4]|[126]|[95]|5|1|
vizualizace:

## Licence

Tento projekt je licencován pod licencí MIT - viz soubor [LICENSE](LICENSE) pro podrobnosti.
