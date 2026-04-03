from typing import Any
from models import ItemizedReciept, SplitBreakdown
from sample_responses import itemized_reciept_sample, split_breakdown_sample

def split_calculator(itemized_reciept: ItemizedReciept, split_breakdown: SplitBreakdown) -> dict: 
    """
    for every item in the itemized reciept: 
        - see whether it exists in the split 
        - if it does exist in the split, see how many people split it
        - get the cost of the item from the itemized reciept 
        - split it by the number of people that got it 

        - for something to think about: 
            - if items from itemized reciept doesn't exist in the 
            who_got_what part 
            - we might need to pass the itemized_reciept to the 
            who_got_what so that the items line up 

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
    

    

        
        
        
            

    

    