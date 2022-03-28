import logging
from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from .service_recommender_call import get_slot_values, call_service_recommender
from .municipality_adjacency import get_adjacent_municipalities
from .get_bot_language import get_bot_language

logger = logging.getLogger(__name__)


class RecommendServicesWholeRegion(Action):
    """
    Rasa Action for getting service recommendations using the service recommender API. 

    Methods
    -------
    name()
        Returns name of the Action

    run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict)
        Returns list of Rasa Events, e.g. SlotSet()
    """

    def name(self) -> str:
        return 'action_recommend_services_whole_region'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        try:
            language, fallback_language = get_bot_language(tracker)

            need_text, municipality = get_slot_values(tracker)
            if not need_text:
                dispatcher.utter_message(response="utter_recommendation_error")
                return [SlotSet("recommend_services_success", False)]

            municipalities = get_adjacent_municipalities(municipality)

            return call_service_recommender(dispatcher, tracker, domain, municipalities, need_text, language, fallback_language)
        except:
            dispatcher.utter_message(response="utter_recommendation_error")
            return [SlotSet("recommend_services_success", False)]
