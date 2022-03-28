from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher


class ResetSlots(Action):
    """
    Rasa Action for resetting all slots.

    Methods
    -------
    name()
        Returns name of the Action

    run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict)
        Returns AllSlotsReset() event
    """

    def name(self) -> str:
        return 'action_reset_slots'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        return [AllSlotsReset()]
