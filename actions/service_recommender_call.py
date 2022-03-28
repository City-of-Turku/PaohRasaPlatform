import os
import logging
from typing import Tuple
import requests
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from .create_recommendation_carousel import create_recommendation_carousel

logger = logging.getLogger(__name__)


def get_slot_values(tracker: Tracker) -> Tuple[str, str]:
    """Gets service need text and municipality values from correct Rasa Tracker slots.

    Args:
        tracker (Tracker)

    Returns:
        Tuple[str, str]
    """
    previous_events = tracker.events
    form_name_prefix = None
    for previous_event in reversed(previous_events):
        if previous_event['event'] == 'action' and 'service_search_form' in previous_event['name']:
            form_name_prefix = previous_event['name'].split(
                'service_search_form')[0]
            break
    if form_name_prefix:
        if f'{form_name_prefix}service_search_text' in tracker.slots:
            need_text = tracker.get_slot(
                f'{form_name_prefix}service_search_text')
        else:
            need_text = tracker.get_slot('service_search_text')
        if f'{form_name_prefix}municipality' in tracker.slots:
            municipality = tracker.get_slot(f'{form_name_prefix}municipality')
        else:
            municipality = tracker.get_slot('municipality')
    else:
        need_text = tracker.get_slot('service_search_text')
        municipality = tracker.get_slot('municipality')

    return need_text, municipality


def call_service_recommender(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict, municipalities: list, need_text: str, language: str, fallback_language: str) -> list:
    """Gets the service recommendations

    Args:
        municipalities (list)
        need_text (str)

    Returns:
        list
    """

    # check if frontend do not want to show recommendation cards in the chatwidget
    try:
        show_recommendations = tracker.get_slot('show_recommendations')
        # if explicitly set to False, don't show recommendations. If e.g. None still show recommendations 
        if show_recommendations == False:
            return [SlotSet("recommend_services_success", True)]
    except:
        pass

    message_language = language
    if not language:
        message_language = fallback_language

    try:
        body = {
            "need_text": need_text,
            "municipalities": municipalities,
            "life_events": [],
            "service_classes": [],
            "top_k": 20,
            "language": message_language,
            "translate_missing_texts": True
        }
        r = requests.post(
            os.environ['RASA_ACTIONS_SERVICE_RECOMMENDER_ENDPOINT']+'/services/recommend', json=body)
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
