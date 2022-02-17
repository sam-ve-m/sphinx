# STANDARD LIBS
import re
from typing import Union


def is_cpf_valid(cpf: Union[int, str]) -> bool:
    # Check if type is int and convert to str
    if not isinstance(cpf, str) and isinstance(cpf, int):
        cpf = str(cpf)

    # Check if type is str
    if not isinstance(cpf, str):
        return False

    # Checks if string has 11 characters
    if len(cpf) != 11:
        return False

    # Remove some unwanted characters
    cpf = re.sub("[^0-9]", "", cpf)

    # Verify if CPF number is equal
    if (
        cpf == "00000000000"
        or cpf == "11111111111"
        or cpf == "22222222222"
        or cpf == "33333333333"
        or cpf == "44444444444"
        or cpf == "55555555555"
        or cpf == "66666666666"
        or cpf == "77777777777"
        or cpf == "88888888888"
        or cpf == "99999999999"
    ):
        return False

    sum = 0
    weight = 10

    """ Calculating the first cpf check digit. """
    for n in range(9):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifying_digit = 11 - sum % 11

    if verifying_digit > 9:
        first_verifying_digit = 0
    else:
        first_verifying_digit = verifying_digit

    """ Calculating the second check digit of cpf. """
    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifying_digit = 11 - sum % 11

    if verifying_digit > 9:
        second_verifying_digit = 0
    else:
        second_verifying_digit = verifying_digit

    if cpf[-2:] == "%s%s" % (first_verifying_digit, second_verifying_digit):
        return True
    return False


def is_cnpj_valid(cnpj: Union[int, str]) -> bool:

    # Check if type is int and convert to str
    if not isinstance(cnpj, str) and isinstance(cnpj, int):
        cnpj = str(cnpj)

    # Check if type is str
    if not isinstance(cnpj, str):
        return False

    # Checks if string has 11 characters
    if len(cnpj) != 14:
        return False

    # Remove some unwanted characters
    cnpj = re.sub("[^0-9]", "", cnpj)

    sum = 0
    weight = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    """ Calculating the first cnpj check digit. """
    for n in range(12):
        value = int(cnpj[n]) * weight[n]
        sum = sum + value

    verifying_digit = sum % 11

    if verifying_digit < 2:
        first_verifying_digit = 0
    else:
        first_verifying_digit = 11 - verifying_digit

    """ Calculating the second check digit of cnpj. """
    sum = 0
    weight = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for n in range(13):
        sum = sum + int(cnpj[n]) * weight[n]

    verifying_digit = sum % 11

    if verifying_digit < 2:
        second_verifying_digit = 0
    else:
        second_verifying_digit = 11 - verifying_digit

    if cnpj[-2:] == "%s%s" % (first_verifying_digit, second_verifying_digit):
        return True
    return False
