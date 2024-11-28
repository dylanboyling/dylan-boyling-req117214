import logging

from constants import FAMILY_COMPOSITIONS 

logger = logging.getLogger()

def validate_winter_supplement_input_data(data):
    required_keys = {'id', 'numberOfChildren', 'familyComposition', 'familyUnitInPayForDecember'}
    missing_keys = required_keys - data.keys()
    if missing_keys:
        logger.info(f'Missing required input key(s) {missing_keys}')
        raise ValueError(f'Missing required input key(s) {missing_keys}')
    
    if data['familyComposition'] not in FAMILY_COMPOSITIONS:
        logger.info(f'familyComposition: {data['familyComposition']}')
        raise ValueError(f'Invalid family composition. Must be one single or couple.')
    
    if not isinstance(data['numberOfChildren'], int) or data['numberOfChildren'] < 0:
        logger.info(f'numberOfChildren: {data['numberOfChildren']}, type: {type(data['numberOfChildren'])}')
        raise ValueError('Invalid number of children. Must be a non-negative integer.')
    
    if not isinstance(data['familyUnitInPayForDecember'], bool):
        logger.info(f'familyUnitInPayForDecember: {data['familyUnitInPayForDecember']}, type: {type(data['familyUnitInPayForDecember'])}')
        raise ValueError('Invalid familyUnitInPayForDecember. Must be a boolean.')

