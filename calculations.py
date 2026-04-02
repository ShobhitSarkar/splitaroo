from typing import Any
from models import ItemizedReciept, SplitBreakdown
from sample_responses import itemized_reciept_sample, split_breakdown_sample

def split_calculator() -> Any: 
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

    itemized_reciept = itemized_reciept_sample()
    split_breakdown = split_breakdown_sample() 

    print("---------- this is the split breakdown----------")
    
    # print(split_breakdown)

    for thing in split_breakdown.items: 
        for item in itemized_reciept.receipt: 
            if thing == item: 
                print(f"FOUND CORRESPONDING ITEM: {thing}, {item}")
                
        
        # print(thing.item)
        
    
    
    # print("------------ this is the itemized reciept -------------------")    
    # for item in itemized_reciept.receipt:
        
    
    #     print(item.name)
    

    return None 

split_calculator()
    

    

        
        
        
            

    

    