import os
import logging
import re
import requests
from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from .create_recommendation_carousel import create_recommendation_carousel
from .intent_utils import *
from .get_bot_language import get_bot_language

logger = logging.getLogger(__name__)


class RecommendServicesByClass(Action):
    """
    Rasa Action for getting service recommendations by service class using the service recommender API. 

    Methods
    -------
    name()
        Returns name of the Action

    run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict)
        Returns list of Rasa Events, e.g. SlotSet()
    """

    def name(self) -> str:
        return 'action_recommend_services_by_class'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        try:
            # check if frontend do not want to show recommendation cards in the chatwidget
            show_recommendations = tracker.get_slot('show_recommendations')
            # if explicitly set to False, don't show recommendations. If e.g. None still show recommendations 
            if show_recommendations == False:
                return [SlotSet("recommend_services_success", True)]
            language, fallback_language = get_bot_language(tracker)

            service_classes = get_service_classes_from_events(tracker)
            # get also life events but not used atm because PTV doesn't have much life event data
            life_events = get_life_events_from_events(tracker)

            municipality = tracker.get_slot('municipality')
            if municipality:
                municipalities = [municipality]
            else:
                municipalities = []

            if not service_classes:
                dispatcher.utter_message(response="utter_recommendation_error")
                return [SlotSet("recommend_services_success", False)]

            body = {
                "include_channels": True,
                "municipalities": municipalities,
                "life_events": [],
                "service_classes": service_classes,
                "translate_missing_texts": True
            }
            r = requests.post(
                os.environ['RASA_ACTIONS_SERVICE_RECOMMENDER_ENDPOINT']+'/servicesFiltered', json=body)
            if r.status_code != 200:
                logging.error(r.text)
                dispatcher.utter_message(response="utter_recommendation_error")
                return [SlotSet("recommend_services_success", False)]

            services = r.json()
            if len(services) == 0:
                dispatcher.utter_message(
                    response="utter_recommendation_no_services")
                return [SlotSet("recommend_services_success", False)]

            services_carousel = create_recommendation_carousel(
                services, language, fallback_language)
            dispatcher.utter_message(attachment=services_carousel)

            return [SlotSet("recommend_services_success", True)]
        except Exception as e:
            logger.error(e)
            dispatcher.utter_message(response="utter_recommendation_error")
            return [SlotSet("recommend_services_success", False)]
