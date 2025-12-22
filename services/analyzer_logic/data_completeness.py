

# get data completeness ratio used in confidence score calculation
def get_data_completeness_ratio(current_price, average_price, lowest_price, highest_price, seller_count) -> float:
        present_fields = sum([
            current_price is not None,
            average_price is not None,
            lowest_price is not None,
            highest_price is not None,
            seller_count is not None
        ])
        return present_fields / 5