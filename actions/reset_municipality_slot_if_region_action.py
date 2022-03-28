import logging
from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)

class ResetMunicipalitySlotIfRegion(Action):
    """
    Rasa Action for resetting municipality slot in case the whole region is selected.

    Methods
    -------
    name()
        Returns name of the Action

    run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict)
        Returns list of SlotSets to reset municipality slot.
    """

    def name(self) -> str:
        return 'action_reset_municipality_slot_if_region'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        slotset_list = []
        for slot in tracker.slots:
            if slot == 'municipality' and tracker.get_slot('municipality') == 'all':
                slotset_list.append(SlotSet(slot, None))
        return slotset_list
