import datetime
import pytz
from rasa_sdk.events import ReminderScheduled
from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSetReminder(Action):
    """
    Rasa Action for setting reminder if user doesn't give feedback. 

    Methods
    -------
    name()
        Returns name of the Action

    run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict)
        Returns list of Rasa Events, e.g. SlotSet()
    """

    def name(self) -> str:
        return 'action_set_feedback_reminder'

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: dict,
    ) -> list:

        date = datetime.datetime.now(pytz.timezone('Europe/Helsinki')) + datetime.timedelta(seconds=25)

        reminder = ReminderScheduled(
            intent_name='EXTERNAL_feedback_reminder',
            trigger_date_time=date,
            name='feedback_reminder',
            kill_on_user_message=True,
        )

        return [reminder]
