

#function to flatten nested structures into a list of words
def flatten_value(value):
    """ 
    This function takes a value which can be of type str, list, dict, or other types 
    and flattens it into a list of words/strings.
    """
    
    # if the value is a string
    if isinstance(value, str):
        return [value]
    
    # if the value is a list
    if isinstance(value, list):
        words=[]
        for item in value:
            words.extend(flatten_value(item))
        return words 
    
    # if the value is a dictionary
    if isinstance(value, dict):
        words = []
        for _, val in value.items():
            words.extend(flatten_value(val))
        return words 
    
    # for other unexpected types(int, float, bool,... ) 
    return [str(value)]           
