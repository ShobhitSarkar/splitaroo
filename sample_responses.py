from models import ItemizedReciept, SplitBreakdown

def itemized_reciept_sample() -> ItemizedReciept: 

    itemized_reciept = {

        "receipt": [
            {
                "name": "Caesar Salad",
                "price": 16
            },
            {
                "name": "Lasagna",
                "price": 18.5
            },
            {
                "name": "Grilled Salmon",
                "price": 24
            },
            {
                "name": "Spaghetti & Meatballs",
                "price": 30
            },
            {
                "name": "Glass House Wine",
                "price": 16
            },
            {
                "name": "Tiramisu",
                "price": 8.5
            }
        ]
    }

    return ItemizedReciept.model_validate(itemized_reciept)

def split_breakdown_sample() -> SplitBreakdown: 

    split_breakdown = {
        "items": [
            {
                "item": "Caesar Salad",
                "people": [
                    "James",
                    "Alice"
                ]
            },
            {
                "item": "Lasagna",
                "people": [
                    "James"
                ]
            },
            {
                "item": "Grilled Salmon",
                "people": [
                    "Alice"
                ]
            },
            {
                "item": "Spaghetti & Meatballs",
                "people": [
                    "James",
                    "Alice"
                ]
            },
            {
                "item": "Glass House Wine",
                "people": [
                    "James",
                    "Alice"
                ]
            },
            {
                "item": "Tiramisu",
                "people": [
                    "Alice"
                ]
            }
        ]
        }

    return SplitBreakdown.model_validate(split_breakdown)
