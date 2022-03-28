from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class FallbackSetServiceSearchText(Action):
    """
    Rasa Action for setting fallback text into service search text.

    Methods
    -------
    name()
        Returns name of the Action

    run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict)
        Returns SlotSet() event
    """

    def name(self) -> str:
        return 'action_fallback_set_service_search_text'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        return [SlotSet("fallback_service_search_text", tracker.latest_message.get("text", None))]
