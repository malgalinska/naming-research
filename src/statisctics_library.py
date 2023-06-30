# Dodanie wystąpienia nazwy
def add_name_with_kind_to_stats(name, kind, stats_dictionary):
    if name is None:
        return
    
    if name == "self" or (name[:2] == "__" and name[-2:] == "__") or name == "":
        return

    if "." in name:
        for module in name.split("."):
            add_name_with_kind_to_stats(module, kind, stats_dictionary)
        return

    if name not in stats_dictionary:
        stats_dictionary[name] = {"all": 0}
        stats_dictionary[name]["naming_style"] = style(name)
        stats_dictionary[name]["words"] = split_to_words(name)

    stats_dictionary[name]["all"] += 1

    if kind not in stats_dictionary[name]:
        stats_dictionary[name][kind] = 1
    else:
        stats_dictionary[name][kind] += 1


# Based on: https://peps.python.org/pep-0008/#descriptive-naming-styles
def style(name):
    name = name.strip("_")
    if len(name) == 0:
        return "ugly"

    if len(name) == 1:
        if name.islower():
            return "b" # single lowercase letter
        if name.isupper():
            return "B" # single uppercase letter
    
    if "_" in name:
        if name.islower():
            return "lower_case_with_underscores"
        if name.isupper():
            return "UPPER_CASE_WITH_UNDERSCORES"
        if name[0].isupper():
            return "Capitalized_Words_With_Underscores"
        return "camel_Snake_Case"
    
    if "-" in name:
        if name.islower():
            return "dash-case"
        if name.isupper():
            return "COBOL-CASE"
        return "ugly"
    
    if name.islower():
        return "lowercase"
    if name.isupper():
        return "UPPERCASE"
    if name[0].isupper():
        return "CapitalizedWords"
    return "mixedCase"
    

def split_to_words(name):
    name = name.strip("_")
    if len(name) == 0:
        return []
        
    if "_" in name:
        return name.lower().split("_")

    ret = []
    start_of_word = 0
    for i in range(1, len(name) - 1):
        if name[i].isupper() and (name[i + 1].islower() or name[i - 1].islower()):
            ret.append(name[start_of_word:i].lower())
            start_of_word = i

    if name[-1].isupper():
        ret.append(name[start_of_word:-1].lower())
        ret.append(name[-1].lower())
    else:
        ret.append(name[start_of_word:].lower())

    return ret
