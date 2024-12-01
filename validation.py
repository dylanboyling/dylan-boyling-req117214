import logging

from constants import FAMILY_COMPOSITIONS 

logger = logging.getLogger()

def validate_winter_supplement_input_data(data):
    required_keys = {'id', 'numberOfChildren', 'familyComposition', 'familyUnitInPayForDecember'}

    validate_keys(required_keys, data)
    validate_key_in_set(data['familyComposition'], FAMILY_COMPOSITIONS)
    validate_non_negative_int(data['numberOfChildren'], "number of children")
    validate_bool(data['familyUnitInPayForDecember'])

def validate_keys(required_keys, data):
    missing_keys = required_keys - data.keys()
    if missing_keys:
        logger.info(f'Missing required input key(s) {missing_keys}')
        raise ValueError(f'Missing required input key(s) {missing_keys}')
    
def validate_key_in_set(key, set, field_name):
    if key not in set:
        logger.info(f'{field_name}: {key}')
        raise ValueError(f'Invalid {field_name} Must be one of {set}.')
    
def validate_non_negative_int(value, field_name):
    if not isinstance(value, int) or value < 0:
        logger.info(f'{field_name}: {value}, type: {type(value)}')
        raise ValueError(f'Invalid {field_name}. Must be a non-negative integer.')

def validate_bool(value, field_name):
    if not isinstance(value, bool):
        logger.info(f'{field_name}: {value}, type: {type(value)}')
        raise ValueError(f'Invalid {field_name}. Must be a boolean.')