from .common_bot_messages import common_service_recommendation_bot_messages


def get_desc_and_summary(service: dict, language: str) -> tuple:
    service_desc = next(
        (item for item in service['service']['descriptions'][language] if language in item['type'] == 'Description'), None) if language in service['service']['descriptions'] else None
    service_summary = next(
        (item for item in service['service']['descriptions'][language] if item['type'] == 'Summary'), None) if language in service['service']['descriptions'] else None
    return service_desc, service_summary


def create_recommendation_carousel(services: list, language: str, fallback_language: str) -> dict:
    """Creates Rasa Webchat carousel UI for service recommendations.

    Args:
        services (list)

    Returns:
        dict
    """
    carousel_elements = []
    for service in services[:20]:
        carousel_element_buttons = []
        carousel_element_buttons.append({
            'title': common_service_recommendation_bot_messages.get('service_card_button_title').get(language, 'Lue lisää'),
            'type': 'web_url',
            'url': service['service']['id']
        })

        if language in service['service']['name'] and service['service']['name'][language] is not None:
            service_name = service['service']['name'][language]
        elif fallback_language in service['service']['name'] and service['service']['name'][fallback_language] is not None:
            service_name = service['service']['name'][fallback_language]
        else:
            names = service['service']['name'].values()
            names = [name for name in names if name]
            service_name = names[0] if len(names) > 0 else None

        # get desc or summary for wanted language
        service_desc, service_summary = get_desc_and_summary(service, language)
        if service_desc is None and service_summary is None:
            service_desc, service_summary = get_desc_and_summary(service, fallback_language)

        if service_desc is not None and len(service_desc['value']) < 200:
            carousel_element_subtitle = service_desc['value']
        elif service_summary is not None:
            carousel_element_subtitle = service_summary['value']
        else:
            # no wanted language found so just try get some other lang descs or summaries
            descriptions = service['service']['descriptions'].values()
            descriptions = [
                item for sublist in descriptions for item in sublist]
            service_descriptions = [
                item for item in descriptions if item['type'] == 'Description']
            service_summaries = [
                item for item in descriptions if item['type'] == 'Summary']
            if len(service_descriptions) > 0 and len(service_descriptions[0]['value']) < 200:
                carousel_element_subtitle = service_descriptions[0]['value']
            elif len(service_summaries) > 0:
                carousel_element_subtitle = service_summaries[0]['value']
            else:
                carousel_element_subtitle = None

        carousel_elements.append({
            'title': service_name,
            'subtitle': carousel_element_subtitle,
            # 'image_url': None,
            'buttons': carousel_element_buttons,
            'metadata': {
                'linkTarget': '_self'
            }
        })

    services_carousel = {
        'type': 'template',
        'payload': {
                'template_type': 'generic',
                'elements': carousel_elements
        }
    }
    return services_carousel
