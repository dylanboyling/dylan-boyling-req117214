from constants import BASE_AMOUNTS, INELIGIBLE_AMOUNT, PER_CHILD_AMOUNTS


def calculate_base_amount(program, family_composition, ):
    return BASE_AMOUNTS[program][family_composition]

def calculate_children_amount(program, number_of_children, ):  
    return PER_CHILD_AMOUNTS[program] * number_of_children

def calculate_supplement(program, number_of_children, family_composition, eligible):
    if not eligible:
        return {
            'baseAmount': INELIGIBLE_AMOUNT,
            'childrenAmount': INELIGIBLE_AMOUNT,
            'supplementAmount': INELIGIBLE_AMOUNT
        }

    base_amount = calculate_base_amount(program, family_composition)
    children_amount = calculate_children_amount(program, number_of_children)
    supplement_amount = base_amount + children_amount

    return {
            'baseAmount': base_amount,
            'childrenAmount': children_amount,
            'supplementAmount': supplement_amount
    }