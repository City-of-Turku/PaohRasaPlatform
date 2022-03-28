MUNICIPALITIES = [{
  "name": {
    "en": "Aura",
    "fi": "Aura",
    "sv": "Aura"
  },
  "id": "019"
},{
  "name": {
    "en": "Kaarina",
    "fi": "Kaarina",
    "sv": "S:t Karins"
  },
  "id": "202"
},{
  "name": {
    "en": "Koski Tl",
    "fi": "Koski Tl",
    "sv": "Koskis"
  },
  "id": "284"
},{
  "name": {
    "en": "Kustavi",
    "fi": "Kustavi",
    "sv": "Gustavs"
  },
  "id": "304"
},{
  "name": {
    "en": "Kimitoön",
    "fi": "Kemiönsaari",
    "sv": "Kimitoön"
  },
  "id": "322"
},{
  "name": {
    "en": "Laitila",
    "fi": "Laitila",
    "sv": "Letala"
  },
  "id": "400"
},{
  "name": {
    "en": "Lieto",
    "fi": "Lieto",
    "sv": "Lundo"
  },
  "id": "423"
},{
  "name": {
    "en": "Loimaa",
    "fi": "Loimaa",
    "sv": "Loimaa"
  },
  "id": "430"
},{
  "name": {
    "en": "Pargas",
    "fi": "Parainen",
    "sv": "Pargas"
  },
  "id": "445"
},{
  "name": {
    "en": "Marttila",
    "fi": "Marttila",
    "sv": "S:t Mårtens"
  },
  "id": "480"
},{
  "name": {
    "en": "Masku",
    "fi": "Masku",
    "sv": "Masku"
  },
  "id": "481"
},{
  "name": {
    "en": "Mynämäki",
    "fi": "Mynämäki",
    "sv": "Virmo"
  },
  "id": "503"
},{
  "name": {
    "en": "Naantali",
    "fi": "Naantali",
    "sv": "Nådendal"
  },
  "id": "529"
},{
  "name": {
    "en": "Nousiainen",
    "fi": "Nousiainen",
    "sv": "Nousis"
  },
  "id": "538"
},{
  "name": {
    "en": "Oripää",
    "fi": "Oripää",
    "sv": "Oripää"
  },
  "id": "561"
},{
  "name": {
    "en": "Paimio",
    "fi": "Paimio",
    "sv": "Pemar"
  },
  "id": "577"
},{
  "name": {
    "en": "Pyhäranta",
    "fi": "Pyhäranta",
    "sv": "Pyhäranta"
  },
  "id": "631"
},{
  "name": {
    "en": "Pöytyä",
    "fi": "Pöytyä",
    "sv": "Pöytyä"
  },
  "id": "636"
},{
  "name": {
    "en": "Raisio",
    "fi": "Raisio",
    "sv": "Reso"
  },
  "id": "680"
},{
  "name": {
    "en": "Rusko",
    "fi": "Rusko",
    "sv": "Rusko"
  },
  "id": "704"
},{
  "name": {
    "en": "Salo",
    "fi": "Salo",
    "sv": "Salo"
  },
  "id": "734"
},{
  "name": {
    "en": "Sauvo",
    "fi": "Sauvo",
    "sv": "Sagu"
  },
  "id": "738"
},{
  "name": {
    "en": "Somero",
    "fi": "Somero",
    "sv": "Somero"
  },
  "id": "761"
},{
  "name": {
    "en": "Taivassalo",
    "fi": "Taivassalo",
    "sv": "Tövsala"
  },
  "id": "833"
},{
  "name": {
    "en": "Turku",
    "fi": "Turku",
    "sv": "Åbo"
  },
  "id": "853"
},{
  "name": {
    "en": "Uusikaupunki",
    "fi": "Uusikaupunki",
    "sv": "Nystad"
  },
  "id": "895"
},{
  "name": {
    "en": "Vehmaa",
    "fi": "Vehmaa",
    "sv": "Vemo"
  },
  "id": "918"
}]

MUNICIPALITY_ADJACENCY = {
"019": ["423","636","704","853"],
"202": ["853","423","577","445","738"],
"322": ["445","738","734"],
"284": ["430","480","734","761"],
"304": ["833"],
"400": ["631","895","503","918"],
"423": ["019","853","636","577","202"],
"430": ["480","284","561","636"],
"480": ["284","734","577","423","636","430"],
"481": ["529","680","704","853","503"],
"503": ["400","918","481","853","636"],
"529": ["481","680","853"],
"538": ["503","481","704","636","853","019"],
"561": ["636","430"],
"577": ["734","738","423","202","480"],
"445": ["738","202","853"],
"631": ["400","895"],
"636": ["430","561","480","423","019","704","503","538"],
"680": ["853","704","481","529"],
"704": ["853","680","481","538"],
"734": ["761","284","480","577","738","322"],
"738": ["322","734","445","577","202"],
"761": ["734","284"],
"833": ["918","895","304"],
"853": ["680","704","529","445","019","202","423"],
"895": ["833","918","631","400"],
"918": ["400","833","895","503"]
}


def get_adjacent_municipalities(municipality):
    mun_ids = [mun.get("id") for mun in MUNICIPALITIES if municipality in mun.get("name").values()]
    all_ids = mun_ids
    for mun_id in mun_ids:
        other_ids = MUNICIPALITY_ADJACENCY.get(mun_id)
        all_ids = all_ids + other_ids
    mun_names = [mun.get("name").get('fi') for mun in MUNICIPALITIES if mun.get("id") in all_ids]
    return mun_names
        
    
    
    