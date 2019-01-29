# -*- coding: utf-8 -*-
import re


def is_repeated_pattern(string):
    """
        Controla si la cadena string contiene patrones de texto repetido como por ejemplo: "aaaaa", "dadadad", etc
    """
    match = False
    re_repeated_pattern = re.compile(ur"(\w{2,})(\1)")
    if re_repeated_pattern.match(string):
        match = True
    return match
