from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUttered, ActionExecuted, UserUtteranceReverted, ActiveLoop
from rasa_sdk.executor import CollectingDispatcher


class ActionCustomFallback(Action):
    """
    Rasa Action for using service search with Rasa Core fallback

    Methods
    -------
    name()
        Returns name of the Action

    run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict)
        Returns list of events
    """

    def name(self) -> Text:
        return "action_custom_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message.get("text", None)
        if not latest_message or (latest_message and latest_message.startswith("/")):
            dispatcher.utter_message(template="utter_default")
            return [UserUtteranceReverted()]

        if tracker.active_loop:
            deactive_loop_events = [ActiveLoop(
                None), SlotSet("requested_slot", None)]
        else:
            deactive_loop_events = []

        latest_lang = tracker.latest_message.get(
            "metadata", {}).get("language", None)
        session_started_metadata = tracker.slots.get(
            "session_started_metadata", {})
        if latest_lang != session_started_metadata.get("language", None):
            session_started_metadata["language"] = latest_lang
            lang_change_event = [
                SlotSet("session_started_metadata", session_started_metadata)]
        else:
            lang_change_event = []

        return deactive_loop_events + lang_change_event + [ActionExecuted("action_listen")] + [SlotSet("core_fallback_service_search_text", latest_message)] + [UserUttered("/core_fallback_service_search", {
            "intent": {"name": "core_fallback_service_search", "confidence": 1.0},
            "entities": [],
            "metadata": {"language": latest_lang or session_started_metadata.get("language")}
        })]
