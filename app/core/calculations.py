from typing import Any
from app.schemas.models import ItemizedReciept, SplitBreakdown

def split_calculator(itemized_reciept: ItemizedReciept, split_breakdown: SplitBreakdown) -> dict: 
    """
    meat of the splitting algorithm 

    takes in an itemized reciept, who got what and then returns the per person split 

    """

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
    

    

        
        
        
            

    

    