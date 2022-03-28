import re
from rasa_sdk.interfaces import Tracker

def nest_form_events(events: list) -> list:
    """Nest event list so that events of any form are nested below the event that starts the form

    Args:
        events (list)

    Returns:
        nested list of events
    """
    nested_events = []
    form_on = False
    start_events = 0
    for event in events:
        event = event.copy()
        is_form_starting_event = ('parse_data' in event.keys() and re.search('service_search$', event['parse_data']['intent']['name']) is not None) or (event.get('name') is not None and re.search('_form$', event.get('name')) is not None)
        is_form_ending_event = (event.get('event') == 'active_loop' and event.get('name') is None) or event.get('event') == 'action_execution_rejected'
        if is_form_starting_event and not form_on:
            form_on = True
            start_events =   start_events + 1
            event['form_events'] = []
            nested_events.append(event)
        elif form_on:
            nested_events[-1]['form_events'].append(event)
            if is_form_ending_event:
                form_on = False
        elif not form_on:
            nested_events.append(event)
        else:
            raise Exception("Something went wrong, event has not type")
    return(nested_events)

def get_previous_recommendable_intent(tracker: Tracker) -> list:
    """Gets the name of the intent that is was the goal of this action, ignores some auxillary events between.

    Args:
        tracker (Tracker)

    Returns:
        name of the intent
    """
    previous_intent_name = None
    previous_events = tracker.events
    nested_events = nest_form_events(previous_events)
    for previous_event in reversed(nested_events):
        if previous_event['event'] == 'user' and len(previous_event.get('parse_data', {}).get('intent_ranking', [])) > 0:
            previous_intent_name = previous_event['parse_data']['intent_ranking'][0]['name']
            break

    return previous_intent_name

def get_service_classes_from_events(tracker: Tracker) -> list:
    """Gets service class codes from intent name from previous events.

    Args:
        tracker (Tracker)

    Returns:
        list of found service classes
    """
    previous_events = tracker.events
    nested_events = nest_form_events(previous_events)
    service_class_regex = re.compile(
        'p\d{1,2}(?:[.]\d{1,2}){0,1}', re.IGNORECASE)
    found_service_classes = []
    for previous_event in reversed(nested_events):
        if previous_event['event'] == 'user' and len(previous_event.get('parse_data', {}).get('intent_ranking', [])) > 0:
            found_service_classes = re.findall(
                service_class_regex, previous_event['parse_data']['intent_ranking'][0]['name'])
            if len(found_service_classes) > 0:
                found_service_classes = list(set(
                    [found_service_class.upper() for found_service_class in found_service_classes]))
                break

    return found_service_classes


def get_life_events_from_events(tracker: Tracker) -> list:
    """Gets life events from intent name from previous events.

    Args:
        tracker (Tracker)

    Returns:
        list of found life events
    """
    previous_events = tracker.events
    nested_events = nest_form_events(previous_events)
    life_event_regex = re.compile(
        'ke\d{1,2}(?:[.]\d{1,2}){0,1}', re.IGNORECASE)
    found_life_events = []
    for previous_event in reversed(nested_events):
        if previous_event['event'] == 'user' and len(previous_event.get('parse_data', {}).get('intent_ranking', [])) > 0:
            found_life_events = re.findall(
                life_event_regex, previous_event['parse_data']['intent_ranking'][0]['name'])
            if len(found_life_events) > 0:
                found_life_events = list(
                    set([found_service_class.upper() for found_service_class in found_life_events]))
                break

    return found_life_events
