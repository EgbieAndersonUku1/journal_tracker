from re import match


def is_string_a_match(reg_expression_pattern, str_to_match):
    return match(reg_expression_pattern, str_to_match)




