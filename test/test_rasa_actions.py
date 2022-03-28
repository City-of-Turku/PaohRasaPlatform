from actions.service_recommender_action import RecommendServices
from rasa_sdk.executor import CollectingDispatcher
import unittest
from unittest.mock import MagicMock, patch
import json
import sys
import os
sys.path.append('actions')

SERVICE_RECOMMENDER_JSON_RESPONSE_SUCCESS = [
    {
        "service": {
            "id": "8c6e25e9-e186-49fd-852c-f6f168d1351f",
            "type": "Service",
            "subtype": None,
            "organizations": [
                {
                    "id": "c5f6914f-302e-41cc-bed7-4d4215aac640",
                    "name": "Kela"
                },
                {
                    "id": "c5f6914f-302e-41cc-bed7-4d4215aac640",
                    "name": "Kela"
                }
            ],
            "name": {
                "en": "Kela's benefits for the unemployed",
                "fi": "Kelan tuet työttömille",
                "sv": "FPA:s stöd för arbetslösa"
            },
            "descriptions": {
                "en": [
                    {
                        "value": "* labour market subsidy\n* basic unemployment allowance\n* commuting and relocation allowance\n* job alternation compensation",
                        "type": "Description"
                    },
                    {
                        "value": "Unemployed",
                        "type": "Summary"
                    }
                ],
                "fi": [
                    {
                        "value": "* työmarkkinatuki\n* peruspäiväraha\n* liikkuvuusavustus\n* vuorottelukorvaus",
                        "type": "Description"
                    },
                    {
                        "value": "Työttömät",
                        "type": "Summary"
                    }
                ],
                "sv": [
                    {
                        "value": "Arbetslösa",
                        "type": "Summary"
                    },
                    {
                        "value": "* arbetsmarknadsstöd\n* grunddagpenning \n* rörlighetsunderstöd\n* alterneringsersättning",
                        "type": "Description"
                    }
                ]
            },
            "requirement": {
                "en": "http://www.kela.fi/unemployment",
                "fi": "http://www.kela.fi/tyottomat",
                "sv": "www.fpa.fi/utanarbete"
            },
            "targetGroups": {
                "en": [
                    {
                        "name": "Finnish startups",
                        "code": "KR2.8"
                    },
                    {
                        "name": "Businesses and non-government organizations",
                        "code": "KR2"
                    },
                    {
                        "name": "Businesses operating in the domestic (Finnish) market",
                        "code": "KR2.3"
                    },
                    {
                        "name": "Citizens",
                        "code": "KR1"
                    }
                ],
                "fi": [
                    {
                        "name": "Yrityksen perustajat kotimaassa",
                        "code": "KR2.8"
                    },
                    {
                        "name": "Yritykset ja yhteisöt",
                        "code": "KR2"
                    },
                    {
                        "name": "Kotimarkkinoilla toimivat yritykset",
                        "code": "KR2.3"
                    },
                    {
                        "name": "Kansalaiset",
                        "code": "KR1"
                    }
                ],
                "sv": [
                    {
                        "name": "Inhemska företagsgrundare",
                        "code": "KR2.8"
                    },
                    {
                        "name": "Företag och samfund",
                        "code": "KR2"
                    },
                    {
                        "name": "Företag på den inhemska marknaden",
                        "code": "KR2.3"
                    },
                    {
                        "name": "Medborgare",
                        "code": "KR1"
                    }
                ]
            },
            "serviceClasses": {
                "en": [
                    {
                        "name": "Support and benefits for the unemployed",
                        "description": "This service subclass contains different types of financial support for unemployed jobseekers, support eligibility criteria and services related to applying for support.",
                        "code": "P10.6"
                    },
                    {
                        "name": "Working life rules and collective agreements",
                        "description": "This service subclass contains issues related to employment contracts and terms of employment, pay, and equality and flexibility in working life, including telework and part-time work, from the service point of view.",
                        "code": "P10.3"
                    }
                ],
                "fi": [
                    {
                        "name": "Työttömän tuet ja etuudet",
                        "description": "Tässä palvelualaluokassa käsitellään työttömälle työnhakijalle suunnattuja erilaisia taloudellisia tukia, niiden saamisen edellytyksiä ja tukien hakupalveluja.",
                        "code": "P10.6"
                    },
                    {
                        "name": "Työelämän säännöt ja työehtosopimukset",
                        "description": "Tähän palvelualaluokkaan kuuluvat palvelujen näkökulmasta työsopimuksiin ja -ehtoihin, palkkaukseen, työelämän yhdenvertaisuuteen ja joustoihin kuten etä- ja osa-aikatyöhön liittyvät asiat.",
                        "code": "P10.3"
                    }
                ],
                "sv": [
                    {
                        "name": "Stöd och förmåner för arbetslösa",
                        "description": "I denna serviceundergrupp behandlas olika ekonomiska stödformer för arbetslösa arbetssökande, förutsättningar för beviljande av dem och tjänster för ansökan om stöd.",
                        "code": "P10.6"
                    },
                    {
                        "name": "Arbetslivets regler och kollektivavtal",
                        "description": "Denna serviceundergrupp omfattar ärenden relaterade till arbetsavtal och -villkor, löner, jämställdhet och flexibilitet i arbetslivet, såsom distans- och deltidsarbete.",
                        "code": "P10.3"
                    }
                ]
            },
            "areas": {
                "en": [],
                "fi": [],
                "sv": []
            },
            "lastUpdated": "2021-06-15T07:37:25.395000"
        },
        "channels": [
            {
                "id": "16d63b97-0b8f-4f72-95e7-7cc2f9ab9e15",
                "type": "EChannel",
                "areaType": "Nationwide",
                "organizationId": "c5f6914f-302e-41cc-bed7-4d4215aac640",
                "serviceIds": [
                    "105837fa-97d2-4f9a-916e-09fe7ca19e52",
                    "b5b82555-9852-4a77-89bd-7dcd332d4f11",
                    "7d655de8-76fd-4f24-bb92-e8f49e153e88",
                    "b84af2c2-824f-4b27-a599-fa28de4e437c",
                    "f8dd3060-543c-47ba-abba-a14fc1feacb3",
                    "ff059acf-de3f-468d-8b6a-9a492d301cda",
                    "6529e1c2-b9ac-4f00-8e8b-6d13616ccf81",
                    "8c6e25e9-e186-49fd-852c-f6f168d1351f",
                    "3ef3f1ef-6754-4308-8ef4-deef416b081e",
                    "b5c945e5-a4d6-47b9-9362-0fe0f20adc2e",
                    "30fe7757-32ad-4ea7-a8e4-857b44f81160",
                    "dae7ba63-46af-4130-995d-1e88cafaa70c",
                    "e0556386-0ffa-40f2-98aa-770b42dd792a",
                    "579991be-f40f-4913-8130-0e07592b50c4",
                    "e52f663f-df44-426c-b401-147d4ebd19cc",
                    "aeb60b1d-2872-4841-9704-652246948990",
                    "76472df7-25ed-4c55-94dd-fa3dd98ee862",
                    "58a4bf82-dc19-4ca5-a57d-a0ef39d0e89d",
                    "506d84d5-0ecf-400a-8b74-f9bd990dab7b",
                    "3456be0a-a126-43af-a364-f24e24786cb1",
                    "5ecdee89-0459-4b27-8271-206f314b801b",
                    "b0372b6c-5ab5-4dd1-92e5-bde71dd25488",
                    "52693b89-c7da-4c61-80df-b6f871672064",
                    "ad234c6c-e24c-4d0f-8698-81980502278d",
                    "caba7a03-40b7-439e-871d-1d9081bd3299",
                    "a0a34972-1af4-41d2-ac89-198ce1875e4f",
                    "7fd28107-d7d6-4158-96d1-fad0bd8c7499",
                    "19a31135-a9d6-4926-a20b-bfe7db1780d3",
                    "05f6a1fd-925f-46f0-b0d2-8a92881710a6",
                    "9b6eb134-2764-47bd-9b98-e04f3a50b88b",
                    "b7e6eddc-0f49-4bfa-876c-53fa01ba7907",
                    "e09e783a-6363-412e-bed2-4082768c914d",
                    "0157fe90-43d2-40e4-895a-a9446829d1d8"
                ],
                "name": {
                    "en": "Kela's online customer service",
                    "fi": "Kelan Asiointipalvelu",
                    "sv": "FPA:s e-tjänst"
                },
                "descriptions": {
                    "en": [
                        {
                            "value": "Check your own data, apply for benefits, send supporting documents and report changes.",
                            "type": "Summary"
                        },
                        {
                            "value": "In Kela's online customer service you can check your own data, apply for benefits, send supporting documets and report changes. You can handle almost all your transactions with Kela on the Internet. ",
                            "type": "Description"
                        }
                    ],
                    "fi": [
                        {
                            "value": "Tarkastele omia Kela-tietojasi, hae etuuksia, lähetä liitteitä ja ilmoita muutoksista. Voit hoitaa lähes kaikki Kela-asiasi verkossa.",
                            "type": "Summary"
                        },
                        {
                            "value": "Kelan verkkoasiointipalvelussa voit tarkastella omia Kela-tietojasi, hakea etuuksia, lähettää liitteitä ja ilmoittaa muutoksista. Voit hoitaa lähes kaikki Kela-asiasi verkossa.",
                            "type": "Description"
                        }
                    ],
                    "sv": [
                        {
                            "value": "Kontrollera dina uppgifter hos FPA, ansök om förmåner, skicka bilagor och meddela förändringar. Du kan sköta så gott som alla FPA-ärenden på nätet.",
                            "type": "Summary"
                        },
                        {
                            "value": "I FPA:s e-tjänst kan du kontrollera dina egna uppgifter hos FPA, ansöka om förmåner, skicka bilagor och meddela förändringar. Du kan sköta så gott som alla FPA-ärenden på nätet. ",
                            "type": "Description"
                        }
                    ]
                },
                "webPages": {
                    "en": [
                        "https://asiointi.kela.fi/go_app?lg=en"
                    ],
                    "fi": [
                        "https://asiointi.kela.fi/go_app"
                    ],
                    "sv": [
                        "https://asiointi.kela.fi/go_app?lg=sv"
                    ]
                },
                "emails": {
                    "en": [],
                    "fi": [
                        "tekninentuki@kela.fi"
                    ],
                    "sv": []
                },
                "phoneNumbers": {
                    "en": [],
                    "fi": [],
                    "sv": []
                },
                "areas": {
                    "en": [],
                    "fi": [],
                    "sv": []
                },
                "addresses": {
                    "en": [],
                    "fi": [],
                    "sv": []
                },
                "lastUpdated": "2021-06-16T07:19:48.498000"
            },
            {
                "id": "fbeff57b-fdb7-4acc-9344-9d97193bf910",
                "type": "ServiceLocation",
                "areaType": "Nationwide",
                "organizationId": "c5f6914f-302e-41cc-bed7-4d4215aac640",
                "serviceIds": [
                    "e52f663f-df44-426c-b401-147d4ebd19cc",
                    "579991be-f40f-4913-8130-0e07592b50c4",
                    "30fe7757-32ad-4ea7-a8e4-857b44f81160",
                    "3ef3f1ef-6754-4308-8ef4-deef416b081e",
                    "aeb60b1d-2872-4841-9704-652246948990",
                    "76472df7-25ed-4c55-94dd-fa3dd98ee862",
                    "e0556386-0ffa-40f2-98aa-770b42dd792a",
                    "6529e1c2-b9ac-4f00-8e8b-6d13616ccf81",
                    "8c6e25e9-e186-49fd-852c-f6f168d1351f",
                    "dae7ba63-46af-4130-995d-1e88cafaa70c",
                    "b5c945e5-a4d6-47b9-9362-0fe0f20adc2e",
                    "ff059acf-de3f-468d-8b6a-9a492d301cda"
                ],
                "name": {
                    "en": None,
                    "fi": "Haukiputaan palvelupiste",
                    "sv": "Servicestället i Haukipudas"
                },
                "descriptions": {
                    "en": [],
                    "fi": [
                        {
                            "value": "Kelan palvelupiste",
                            "type": "Summary"
                        },
                        {
                            "value": "Kelan palvelupisteessä opastetaan ja neuvotaan kaikissa Kelan etuuksiin liittyvissä asioissa. Voit hakea etuuksia ja toimittaa liitteet myös asiointipalvelussamme osoitteessa www.kela.fi/asiointi. Lue myös mahdollisuudesta ajanvaraukseen: www.kela.fi/ajanvaraus.",
                            "type": "Description"
                        }
                    ],
                    "sv": [
                        {
                            "value": "Fpa:s serviceställe",
                            "type": "Summary"
                        },
                        {
                            "value": "På FPA:s serviceställe kan du få information och rådgivning om alla FPA-förmåner. Du kan också ansöka om förmåner och lämna in bilagor i vår e-tjänst på adressen www.fpa.fi/etjanst. Läs mer om hur du bokar tid på adressen www.fpa.fi/tidsbokning.",
                            "type": "Description"
                        }
                    ]
                },
                "webPages": {
                    "en": [],
                    "fi": [],
                    "sv": []
                },
                "emails": {
                    "en": [],
                    "fi": [],
                    "sv": []
                },
                "phoneNumbers": {
                    "en": [],
                    "fi": [],
                    "sv": []
                },
                "areas": {
                    "en": [],
                    "fi": [],
                    "sv": []
                },
                "addresses": {
                    "en": [
                        {
                            "type": "Location",
                            "subtype": "Single",
                            "streetNumber": "15",
                            "postalCode": "90830",
                            "latitude": "7229135.399",
                            "longitude": "422665.198",
                            "streetName": "Simppulantie",
                            "postOffice": "HAUKIPUDAS",
                            "municipalityCode": "564",
                            "municipalityName": "Aura"
                        },
                        {
                            "type": "Postal",
                            "subtype": "PostOfficeBox",
                            "streetNumber": None,
                            "postalCode": None,
                            "latitude": None,
                            "longitude": None,
                            "streetName": None,
                            "postOffice": None,
                            "municipalityCode": None,
                            "municipalityName": None
                        }
                    ],
                    "fi": [
                        {
                            "type": "Location",
                            "subtype": "Single",
                            "streetNumber": "15",
                            "postalCode": "90830",
                            "latitude": "7229135.399",
                            "longitude": "422665.198",
                            "streetName": "Simppulantie",
                            "postOffice": "HAUKIPUDAS",
                            "municipalityCode": "564",
                            "municipalityName": "Aura"
                        },
                        {
                            "type": "Postal",
                            "subtype": "PostOfficeBox",
                            "streetNumber": None,
                            "postalCode": None,
                            "latitude": None,
                            "longitude": None,
                            "streetName": None,
                            "postOffice": None,
                            "municipalityCode": None,
                            "municipalityName": None
                        }
                    ],
                    "sv": [
                        {
                            "type": "Location",
                            "subtype": "Single",
                            "streetNumber": "15",
                            "postalCode": "90830",
                            "latitude": "7229135.399",
                            "longitude": "422665.198",
                            "streetName": "Simppulantie",
                            "postOffice": "HAUKIPUDAS",
                            "municipalityCode": "564",
                            "municipalityName": "Aura"
                        },
                        {
                            "type": "Postal",
                            "subtype": "PostOfficeBox",
                            "streetNumber": None,
                            "postalCode": None,
                            "latitude": None,
                            "longitude": None,
                            "streetName": None,
                            "postOffice": None,
                            "municipalityCode": None,
                            "municipalityName": None
                        }
                    ]
                },
                "lastUpdated": "2021-06-28T01:00:00.719000"
            }
        ],
        "score": 0.8303728304964242
    },
]
SERVICE_RECOMMENDER_JSON_RESPONSE_ERROR = {
    "detail": [
        {
            "loc": [
                "body",
                48
            ],
            "msg": "Expecting value: line 4 column 1 (char 48)",
            "type": "value_error.jsondecode",
            "ctx": {
                    "msg": "Expecting value",
                    "doc": "{\n  \"need_text\": \"string\",\n  \"municipality_id\":\n}",
                    "pos": 48,
                    "lineno": 4,
                    "colno": 1
            }
        }
    ]
}

# Test class for Rasa Tracker store which contains chatbot user message data


class TestRasaTracker():
    def __init__(self):
        self.slots = {
            'general_service_search_text': 'olispa kahvia',
            'municipality': 'turku',
            "fallback_language": "fi",
            "session_started_metadata": {
                "language": "it"
            }
        }
        self.latest_message = {
            "intent": {
                "id": -4114183629044666000,
                "name": "public_transport",
                "confidence": 0.9920039772987366
            },
            "entities": [],
            "text": "joukkoliikenne",
            "message_id": "a4d3a71843eb449689e0eb4dc34ca7e9",
            "metadata": {
                "language": "fi"
            },
            "intent_ranking": [
            ]
        }
        self.events = [
            {
                "event": "action",
                "timestamp": 1628670810.1175656,
                "name": "action_session_start",
                "confidence": 1
            },
            {
                "event": "session_started",
                "timestamp": 1628670810.117589
            },
            {
                "event": "action",
                "timestamp": 1628670810.117605,
                "name": "action_listen"
            },
            {
                "event": "user",
                "timestamp": 1628670810.1180103,
                "text": "/get_started",
                "parse_data": {
                    "intent": None,
                    "entities": [],
                    "message_id": "d2f0600da3bc4648998c9727469121ce",
                    "metadata": {},
                    "intent_ranking": [
                        {
                            "name": "get_started",
                            "confidence": 1
                        }
                    ]
                },
                "input_channel": "webchat",
                "message_id": "d2f0600da3bc4648998c9727469121ce",
                "metadata": {}
            },
            {
                "event": "user_featurization",
                "timestamp": 1628670810.1396117,
                "use_text_for_featurization": False
            },
            {
                "event": "action",
                "timestamp": 1628670810.1396365,
                "name": "utter_get_started",
                "policy": "policy_2_AugmentedMemoizationPolicy",
                "confidence": 1
            },
            {
                "event": "bot",
                "timestamp": 1628670810.1396775,
                "metadata": {
                    "template_name": "utter_get_started"
                },
                "text": "Moi! Autan sinua löytämään palveluita eri elämäntilanteisiisi liittyen Varsinais-Suomen alueelta.\n\nYmmärrän helpoiten melko lyhyitä viestejä tai voit myös klikkailla nappeja.",
                "data": {}
            },
            {
                "event": "action",
                "timestamp": 1628670810.1663811,
                "name": "utter_get_started_choose_life_event",
                "policy": "policy_2_AugmentedMemoizationPolicy",
                "confidence": 1
            },
            {
                "event": "bot",
                "timestamp": 1628670810.166434,
                "metadata": {
                    "template_name": "utter_get_started_choose_life_event"
                },
                "text": "Kuvaile ensiksi, millaiseen elämäntilanteeseen tarvitsisit apua tai voit myös etsiä vapaasti palveluita 😊",
                "data": {
                    "buttons": [
                        {
                            "title": "Työttömäksi jääminen",
                            "type": "postback",
                            "payload": "/ke8_losing_job"
                        },
                        {
                            "title": "Velkaantuminen",
                            "type": "postback",
                            "payload": "/ke9_debt"
                        },
                        {
                            "title": "Omaisen kuolema",
                            "type": "postback",
                            "payload": "/ke14_death"
                        },
                        {
                            "title": "Etsi vapaasti palveluita",
                            "type": "postback",
                            "payload": "/service_search"
                        }
                    ]
                }
            },
            {
                "event": "action",
                "timestamp": 1628670810.1708252,
                "name": "action_listen",
                "policy": "policy_2_AugmentedMemoizationPolicy",
                "confidence": 1
            },
            {
                "event": "user",
                "timestamp": 1628670821.483857,
                "text": "/service_search",
                "parse_data": {
                    "intent": None,
                    "entities": [],
                    "message_id": "7c25cbf27151428589d7fc51620e508a",
                    "metadata": {},
                    "intent_ranking": [
                        {
                            "name": "service_search",
                            "confidence": 1
                        }
                    ],
                    "text": "<Etsi vapaasti palveluita>"
                },
                "input_channel": "webchat",
                "message_id": "7c25cbf27151428589d7fc51620e508a",
                "metadata": {}
            },
            {
                "event": "user_featurization",
                "timestamp": 1628670821.5257907,
                "use_text_for_featurization": False
            },
            {
                "event": "action",
                "timestamp": 1628670821.5258121,
                "name": "general_service_search_form",
                "policy": "policy_2_AugmentedMemoizationPolicy",
                "confidence": 1
            },
            {
                "event": "active_loop",
                "timestamp": 1628670821.5258555,
                "name": "general_service_search_form"
            },
            {
                "event": "bot",
                "timestamp": 1628670821.5258627,
                "metadata": {
                    "linkTarget": "_blank",
                    "userInput": "show",
                    "forceOpen": False,
                    "forceClose": False,
                    "pageChangeCallbacks": None,
                    "pageEventCallbacks": None,
                    "template_name": "utter_ask_general_service_search_text"
                },
                "text": "Kuvaile ensiksi palvelutarvettasi",
                "data": {}
            },
            {
                "event": "slot",
                "timestamp": 1628670821.5258706,
                "name": "requested_slot",
                "value": "general_service_search_text"
            },
            {
                "event": "action",
                "timestamp": 1628670821.5335426,
                "name": "action_listen",
                "policy": "policy_1_RulePolicy",
                "confidence": 1
            },
            {
                "event": "user",
                "timestamp": 1628670831.59987,
                "text": "haluaisin mennä uimarannalle",
                "parse_data": {
                    "intent": None,
                    "entities": [],
                    "text": "haluaisin mennä uimarannalle",
                    "message_id": "1a5dad116ee34938b11f68e60c1814ba",
                    "metadata": {},
                    "intent_ranking": [
                        {
                            "id": 1679135316125928700,
                            "name": "chitchat.bye",
                            "confidence": 0.8972764015197754,
                            "canonical": "hei hei"
                        }
                    ]
                },
                "input_channel": "webchat",
                "message_id": "1a5dad116ee34938b11f68e60c1814ba",
                "metadata": {}
            },
            {
                "event": "user_featurization",
                "timestamp": 1628670831.625026,
                "use_text_for_featurization": False
            },
            {
                "event": "action",
                "timestamp": 1628670831.625047,
                "name": "general_service_search_form",
                "policy": "policy_1_RulePolicy",
                "confidence": 1
            },
            {
                "event": "slot",
                "timestamp": 1628670831.6250882,
                "name": "general_service_search_text",
                "value": "haluaisin mennä uimarannalle"
            },
            {
                "event": "bot",
                "timestamp": 1628670831.6250937,
                "metadata": {
                    "template_name": "utter_ask_municipality"
                },
                "text": "Kerrotko vielä, mistä kunnasta haluat palveluita?",
                "data": {}
            },
            {
                "event": "slot",
                "timestamp": 1628670831.6250968,
                "name": "requested_slot",
                "value": "municipality"
            },
            {
                "event": "action",
                "timestamp": 1628670831.6321259,
                "name": "action_listen",
                "policy": "policy_1_RulePolicy",
                "confidence": 1
            },
            {
                "event": "user",
                "timestamp": 1628670839.1954765,
                "text": "turku",
                "parse_data": {
                    "intent": None,
                    "entities": [
                        {
                            "entity": "municipality_entity",
                            "start": 0,
                            "end": 5,
                            "confidence_entity": 0.9993183612823486,
                            "value": "turku",
                            "extractor": "DIETClassifier"
                        }
                    ],
                    "text": "turku",
                    "message_id": "e8c8472b6ec04644a241510e418b5332",
                    "metadata": {},
                    "intent_ranking": [
                        {
                            "id": 8390830771550880000,
                            "name": "service_municipality_choice",
                            "confidence": 0.999856173992157,
                            "canonical": "haluan palveluita turusta"
                        }
                    ]
                },
                "input_channel": "webchat",
                "message_id": "e8c8472b6ec04644a241510e418b5332",
                "metadata": {}
            },
            {
                "event": "user_featurization",
                "timestamp": 1628670839.203917,
                "use_text_for_featurization": False
            },
            {
                "event": "action",
                "timestamp": 1628670839.2039268,
                "name": "general_service_search_form",
                "policy": "policy_1_RulePolicy",
                "confidence": 1
            },
            {
                "event": "slot",
                "timestamp": 1628670839.2039347,
                "name": "municipality",
                "value": "turku"
            },
            {
                "event": "active_loop",
                "timestamp": 1628670839.203938
            },
            {
                "event": "slot",
                "timestamp": 1628670839.203941,
                "name": "requested_slot"
            },
            {
                "event": "action",
                "timestamp": 1628670839.9863353,
                "name": "action_recommend_services",
                "policy": "policy_2_AugmentedMemoizationPolicy",
                "confidence": 1
            }
        ]

    def get_slot(self, key):
        return self.slots[key]


# This method will be used by the mock to replace requests.post to service recommender API
def mocked_requests_post(*args, **kwargs):

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def text(self):
            return json.dumps(self.json_data)

    if args[0] == 'request_success/services/recommend':
        return MockResponse(SERVICE_RECOMMENDER_JSON_RESPONSE_SUCCESS, 200)
    elif args[0] == 'request_error/services/recommend':
        return MockResponse(SERVICE_RECOMMENDER_JSON_RESPONSE_ERROR, 400)


class TestRasaActionsRecommendServices(unittest.TestCase):

    def setUp(self):
        self.tracker = TestRasaTracker()

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_recommend_services_action_success(self, mock_post):
        os.environ['RASA_ACTIONS_SERVICE_RECOMMENDER_ENDPOINT'] = 'request_success'
        dispatcher = CollectingDispatcher()
        action = RecommendServices()
        action.run(dispatcher, self.tracker, None)

        self.assertEqual(
            dispatcher.messages[0]['attachment']['payload']['elements'][0][
                'title'], SERVICE_RECOMMENDER_JSON_RESPONSE_SUCCESS[0]['service']['name']['fi']
        )

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_recommend_services_action_error(self, mock_post):
        os.environ['RASA_ACTIONS_SERVICE_RECOMMENDER_ENDPOINT'] = 'request_error'
        dispatcher = CollectingDispatcher()
        action = RecommendServices()
        action.run(dispatcher, self.tracker, None)
        self.assertEqual(
            dispatcher.messages[0]['response'], 'utter_recommendation_error')


if __name__ == '__main__':
    unittest.main()
