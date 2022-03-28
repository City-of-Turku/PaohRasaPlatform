from rasa_sdk.interfaces import Tracker


def get_bot_language(tracker: Tracker) -> str:
    fallback_language = tracker.slots.get("fallback_language")
    language = tracker.latest_message.get("metadata", {}).get(
        "language")
    if language not in ['fi', 'en', 'sv']:
        language = fallback_language if fallback_language and fallback_language in [
            'fi', 'en', 'sv'] else 'fi'
    return language, fallback_language
