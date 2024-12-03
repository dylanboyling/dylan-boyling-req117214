import logging

from rules_engine import calculate_supplement
from validation import validate_winter_supplement_input_data

logger = logging.getLogger(__name__)

def winter_supplement_message_handler(topic_id, input_data):
    logger.info(f'Received message on topic {topic_id} with ID: {input_data.get('id', 'unknown_id')}')
    try:
        validate_winter_supplement_input_data(input_data)
    except ValueError as e:
        logger.info(f'Input validation error on topic {topic_id}: {e}')
        return {
            "id": input_data.get('id', 'unknown_id'),
            "error": str(e)
        }

    calculated_amounts = calculate_supplement(
        'winter_supplement',
        input_data['numberOfChildren'],
        input_data['familyComposition'],
        input_data['familyUnitInPayForDecember']
    )

    return {
        "id": input_data['id'],
        "isEligible": input_data['familyUnitInPayForDecember'],
        "baseAmount": calculated_amounts['baseAmount'],
        "childrenAmount": calculated_amounts['childrenAmount'],
        "supplementAmount": calculated_amounts['supplementAmount']
    }
