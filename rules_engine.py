def calculate_base_amount(family_composition):
    match family_composition:
        case 'single':
            base_amount = 60
        case 'couple':
            base_amount = 120
        case _:
            raise ValueError(f"Invalid family composition: {family_composition}")

    return base_amount

def calculate_children_amount(number_of_children):
    PER_CHILD_AMOUNT = 20
    return number_of_children * PER_CHILD_AMOUNT

def calculate_winter_supplement(number_of_children, family_composition, december_eligible):
    if not december_eligible:
        ineligible_amount = 0.0
        return {
            'baseAmount': ineligible_amount,
            'childrenAmount': ineligible_amount,
            'supplementAmount': ineligible_amount
        }

    base_amount = calculate_base_amount(family_composition)
    children_amount = calculate_children_amount(number_of_children)
    supplement_amount = base_amount + children_amount

    return {
            'baseAmount': base_amount,
            'childrenAmount': children_amount,
            'supplementAmount': supplement_amount
    }