from typing import Any
from app.schemas.models import ItemizedReciept, SplitBreakdown


def split_calculator(
    itemized_reciept: ItemizedReciept, split_breakdown: SplitBreakdown
) -> dict:
    """
    meat of the splitting algorithm

    takes in an itemized reciept, who got what and then returns the per person split

    """
    if itemized_reciept is None: 
        raise Exception("Itemized Reciept is None")

    if split_breakdown is None: 
        raise Exception("Split Breakdown is None")

    if not isinstance(itemized_reciept, ItemizedReciept): 
        raise Exception("Itemized Reciept is not the correct shape.")

    if not isinstance(split_breakdown, SplitBreakdown): 
        raise Exception("The split breakdown is not the correct shape.")
    

    reciept_dict = {}
    people_dict = {}

    ## building the reciept dictionary
    for item in itemized_reciept.receipt:
        reciept_dict[item.name] = item.price

    ## building the people dictionary
    for shared_item in split_breakdown.items:
        for person in shared_item.people:
            people_dict[person] = 0

    ## meat of the problem
    for shared_item in split_breakdown.items:
        if shared_item.item in reciept_dict:
            cost_per_person = reciept_dict[shared_item.item] / len(shared_item.people)

            for person in shared_item.people:
                people_dict[person] += cost_per_person

    return people_dict


"""
sam = 6.5 + 3.5 = 10 
alice = 6.5 
"""