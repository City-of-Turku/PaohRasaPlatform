import logging
from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)

class ResetServiceNeedTextSlots(Action):
    """
    Rasa Action for resetting all service need text slots.

    Methods
    -------
    name()
        Returns name of the Action

    run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict)
        Returns list of SlotSets to reset service need text slots.
    """

    def name(self) -> str:
        return 'action_reset_need_text_slots'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        latest_message = tracker.latest_message.get("text", None)
        slotset_list = []
        for slot in tracker.slots:
            if 'service_search_text' in slot:
                if tracker.get_slot(slot) != latest_message and latest_message and not latest_message.startswith("/"):
                    slotset_list.append(SlotSet(slot, latest_message))
                elif tracker.get_slot(slot) == latest_message:
                    pass
                else:
                    slotset_list.append(SlotSet(slot, None))
        return slotset_list
