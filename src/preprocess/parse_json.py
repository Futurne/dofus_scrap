#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pprint import pprint
from typing import Any, Union, Optional


ELEMENTS = {
    'Eau',
    'Terre',
    'Feu',
    'Air',
    'Neutre',
}

VALID_BUFFS = {
    'PA',
    'PM',
    'Portée',
    'Invocation(s)',
    'Vitalité',
    'Initiative',
    'Chance',
    'Force',
    'Intelligence',
    'Agilité',
    'Puissance',
    'Sagesse',
    '% Critique',
    'Pod(s)',
    'Tacle',
    'Fuite',
    'Dommage(s)',
    'Dommage(s) Poussée',
    'Dommage(s) Critiques',
    'Résistance(s) Poussée',
    'Résistance(s) Critiques',
    'Soin(s)',
    'Prospection',
    'Esquive PA',
    'Esquive PM',
    'Retrait PA',
    'Retrait PM',
    '% Dommages distance',
    '% Dommages mêlée',
    '% Résistance mêlée',
    '% Résistance distance',
    '% Dommages aux sorts',
    "% Dommages d'armes",
    'Dommage(s) Pièges',
    'Puissance (pièges)'
}

for value in ['Dommage(s)', 'Résistance(s)', '% Résistance']:
    for element in ELEMENTS:
        VALID_BUFFS.add(f'{value} {element}')

VALID_DMGS = {
    '(PV rendus)',
}

for value in ['dommages', 'vol']:
    for element in ELEMENTS:
        VALID_DMGS.add(f'({value} {element})')


BUFF_REGEX = '(' + '|'.join(
    b.replace('(', r'\(').replace(')', r'\)')
    for b in VALID_BUFFS
) + ')'

DMG_REGEX = '(' + '|'.join(
    b.replace('(', r'\(').replace(')', r'\)')
    for b in VALID_DMGS
) + ')'


class JsonParser:
    def __init__(self, data: dict[str, Any]):
        self.data = data
        self.parsed_data = dict()

    def log_value(self, name: str, value: Any):
        self.parsed_data[name] = value

    def parse_type(self, name: str, value: str):
        type_name, type_value = value.split(' : ')
        self.parsed_data[type_name] = type_value

    def parse_niveau(self, name: str, value: str):
        niveau = value.split(' : ')[1]
        if 'à' in niveau:
            niveaux = niveau.split(' à ')
            niveaux = [int(n) for n in niveaux]
        else:
            self.parsed_data[name] = int(niveau)

    def parse_effets(self, name: str, effets: list[str]):
        self.parsed_data[name] = list()
        degats = []
        for effet in effets:
            parsed = JsonParser.parse_effet(effet)
            if 'dégâts' in parsed:
                degats.append(parsed['dégâts'])
            else:
                self.parsed_data[name].append(parsed)

        if degats != []:
            self.parsed_data['dégâts'] = degats

    def parse_croisements(self, name: str, croisements: str):
        croisements = croisements.split('\n')
        croisements = [
            (croisements[i], croisements[i+1])
            for i in range(0, len(croisements), 2)
        ]
        self.parsed_data[name] = croisements

    def parse_bonus(self, name: str, bonus: list[str]):
        exp, butin = bonus
        self.parsed_data[name] = {
                ' '.join(exp.split(' ')[:-1]): int(exp.split(' ')[-1]),
                ' '.join(butin.split(' ')[:-1]): int(butin.split(' ')[-1]),
        }

    def parse_butins(self, name: str, butins: list[Union[list[str], str]]):
        def parse(butins: Union[str, list[str]]) -> dict[str, float]:
            if type(butins) is str:
                name, drop = butins.split(' | ')
                drop = drop.replace(' %', '')
                if ' - ' not in drop:
                    return {
                        name: float(drop)
                    }
                else:
                    min_drop, max_drop = drop.split(' - ')
                    min_drop, max_drop = float(min_drop), float(max_drop)
                    return {
                        name: (min_drop, max_drop)
                    }

            butins = [b.split(' | ') for b in butins]
            butins = {b[0]: b[1] for b in butins}
            for name, drop in butins.items():
                drop = drop.replace(' %', '')
                if ' - ' not in drop:
                    butins[name] = float(drop)
                else:
                    min_drop, max_drop = drop.split(' - ')
                    min_drop, max_drop = float(min_drop), float(max_drop)
                    butins[name] = (min_drop, max_drop)
            return butins


        if len(butins) == 2:
            butins, butins_cond = butins
            self.parsed_data['butins conditionnés'] = parse(butins_cond)

        self.parsed_data[name] = parse(butins)

    def parse_resistances(self, name: str, resistances: list[str]):
        resistances = [r.split(' : ') for r in resistances]
        range_regex = r'De\s(-?\d+)%\sà\s(-?\d+)%'
        parsed = []
        for element, values in resistances:
            range_match = re.search(range_regex, values)
            if range_match:
                min_res, max_res = range_match.groups()
                min_res, max_res = int(min_res), int(max_res)
                parsed.append({element: (min_res, max_res)})
            else:
                res = int(values.replace('%', ''))
                parsed.append({element: res})

        self.parsed_data[name] = parsed

    def parse_conditions(self, name: str, conditions: list[str]):
        conditions = conditions[0]
        conditions = JsonParser.group_par(conditions)
        conditions = JsonParser.parse_multiple_conds(conditions)
        conditions = JsonParser.parse_conditions_recursively(conditions)
        if conditions is not None:
            self.parsed_data[name] = conditions

    def parse_containers(self, c_name: str, c_value: str):
        parsing_methods = {
            'description': self.log_value,
            'effets': self.parse_effets,
            'effets évolutifs': self.parse_effets,
            'issu du croisement': self.parse_croisements,
            'bonus': self.parse_bonus,
            'butins': self.parse_butins,
            'résistances': self.parse_resistances,
            'sorts': self.log_value,
        }

        for name, value in c_value.items():
            parsing_methods[name](name, value)

    def parse(self) -> dict[str, Any]:
        parsing_methods = {
            'url': self.log_value,
            'erreur 404': self.log_value,
            'nom': self.log_value,
            'illustration_url': self.log_value,
            'type': self.parse_type,
            'containers': self.parse_containers,
            'niveau': self.parse_niveau,
        }

        for name, value in self.data.items():
            parsing_methods[name](name, value)

        return self.parsed_data

    @staticmethod
    def parse_effet(effet: str) -> dict[str, Union[str, dict]]:
        effet = effet.replace(r'{~ps}{~zs}', '(s)')
        values_r = r'^-?\d+(\sà\s-?\d+)?'
        standard_r = values_r + r'\s*' + f'({BUFF_REGEX}|{DMG_REGEX})$'
        match_standard = re.search(standard_r, effet)
        if not match_standard:
            # Effet special => keep str
            return {'special': effet}

        values = re.search(values_r, effet).group()
        if 'à' in values:
            min_value, max_value = values.split( 'à ')
            values = int(min_value), int(max_value)
        else:
            values = int(values)

        # Check for buff
        buff = re.search(BUFF_REGEX, effet)
        if buff:
            buff = buff.group()
            return {
                buff: values
            }

        # If it is not a buff it is a dmg
        dmg = re.search(DMG_REGEX, effet).group()
        dmg = dmg[1:-1]  # Remove parenthesis
        if dmg == 'PV rendus':
            return {
                'dégâts': {dmg: values}
            }

        dmg_type, element = dmg.split(' ')
        return {
            'dégâts': {
                element: values,
                'vol': dmg_type == 'vol',
            }
        }

    ###### - Static methods for conditions parsing - #####
    @staticmethod
    def parse_conditions_recursively(
            conditions: Union[str, dict[Any], list[Any]]
    ) -> Union[str, dict[Any], list[Any]]:
        match conditions:
            case str():
                standard_cond = r'.+\s(<|>)\s\d+'
                match_std = re.search(standard_cond, conditions)
                if not match_std:
                    return {'special': conditions}
                
                bool_op = match_std.group(1)
                left_cond, right_cond = conditions.split(f' {bool_op} ')
                return {
                    bool_op: (left_cond, int(right_cond))
                }
            case dict():
                return {
                    b: JsonParser.parse_conditions_recursively(c)
                    for b, c in conditions.items()
                }
            case list():
                return [
                    JsonParser.parse_conditions_recursively(c)
                    for c in conditions
                ]
            case None:
                return None
            case _:
                raise RuntimeError(conditions)

    @staticmethod
    def parse_multiple_conds(
        conditions: list[Any]
    ) -> Optional[dict[Optional[str], list]]:
        """Parse the 'et' and 'ou' conditions.
        """
        def parse_multiple_conds_recursive(
            conditions: list[Any]
        ) -> tuple[list[Any], Optional[str]]:
            """Recursively goes through all elements of the conditions
            and determines the boolean operations of the multiple conditions
            if there are any.

            Add the multiple conditions in dictionnaries such that bool_op -> list_of_conds.
            """
            bool_op = None
            parsed = []
            for idx, cond in enumerate(conditions):
                match cond:
                    case str():
                        multi_cond = r'\s(ou|et)\s'
                        cond = f' {cond} '
                        match_multi = re.search(multi_cond, cond)
                        if match_multi:
                            bool_op = match_multi.group(1)
                            conds = cond.split(f' {bool_op} ')
                            conds = [c.strip() for c in conds if c.strip() != '']
                            parsed.extend(conds)
                        else:
                            parsed.append(cond.strip())
                    case list():
                        sub_conds, sub_bool_op = parse_multiple_conds_recursive(cond)
                        if sub_conds != []:
                            if len(sub_conds) == 1:  # No boolean ops needed
                                sub_bool_op = None

                            parsed.append({
                                sub_bool_op: sub_conds
                            })

            return parsed, bool_op

        conds, bool_op = parse_multiple_conds_recursive(conditions)
        if conds != []:
            if len(conds) == 1:  # No boolean ops needed
                bool_op = None
            return {bool_op: conds}

        return None

    @staticmethod
    def group_par(my_string: str) -> list[Any]:
        """Parse the string to group together characters that are between parenthesis.
        """
        def add_str(groups: list, current_str: str):
            current_str = current_str.strip()
            if current_str != '':
                current_str = current_str.replace('~', '(s)')
                groups.append(current_str)

        def group_par_recursive(my_string: str) -> tuple[list[Any], int]:
            groups = []
            i = 0
            current_str = ''
            while i < len(my_string):
                c = my_string[i]

                match c:
                    case '(':
                        add_str(groups, current_str)
                        current_str = ''

                        new_groups, last_i = group_par_recursive(my_string[i+1:])
                        groups.append(new_groups)
                        i += last_i
                    case ')':
                        add_str(groups, current_str)
                        current_str = ''
                        i += 1
                        break
                    case _:
                        current_str += c

                i += 1

            add_str(groups, current_str)
            return groups, i

        my_string = my_string.replace('\n', ' ')
        my_string = my_string.replace('(s)', '~')
        my_string, _ = group_par_recursive(my_string)
        return my_string

