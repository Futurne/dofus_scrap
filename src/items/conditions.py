#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, Union

from src.items.buff import Buff

CONDITIONS_TYPES = {
    "<",
    ">",
    "spécial",
}

NODE_TYPES = {
    "et",
    "ou",
    "null",
}


class ConditionsFeuille:
    def __init__(
        self,
        cond_type: str,
        left_buff: Optional[Buff] = None,
        right_value: Optional[int] = None,
        special_value: Optional[str] = None,
    ):
        self.cond_type = cond_type
        self.left_buff = left_buff
        self.right_value = right_value
        self.special_value = special_value

        assert cond_type in CONDITIONS_TYPES, f"Condition type {cond_type} unknown."

        if special_value is None:
            assert left_buff is not None and right_value is not None
        else:
            assert left_buff is None and right_value is None

    def __eq__(self, other) -> bool:
        return all(
            [
                self.cond_type == other.cond_type,
                self.left_buff == other.left_buff,
                self.right_value == other.right_value,
                self.special_value == other.special_value,
            ]
        )

    @staticmethod
    def from_dict(feuille: dict):
        cond_type = next(iter(feuille.keys()))
        match cond_type:
            case "spécial":
                return ConditionsFeuille(
                    cond_type,
                    None,
                    None,
                    feuille[cond_type],
                )
            case _:
                return ConditionsFeuille(
                    cond_type,
                    Buff(feuille[cond_type][0]),
                    feuille[cond_type][1],
                    None,
                )


class ConditionsNoeud:
    def __init__(
        self,
        node_type: str,
        children_nodes: list[Union[ConditionsFeuille, "self"]],
    ):
        self.node_type = node_type
        self.children_nodes = children_nodes

        assert node_type in NODE_TYPES, f"Node type of {node_type} unknown."

    def __eq__(self, other) -> bool:
        return self.node_type == other.node_type and all(
            [sc == so for sc, so in zip(self.children_nodes, other.children_nodes)]
        )

    @staticmethod
    def from_dict(conditions: dict):
        node_type = next(iter(conditions.keys()))
        children = conditions[node_type]
        parsed_children = []

        for child in children:
            child_key = next(iter(child.keys()))
            if child_key in NODE_TYPES:
                parsed_children.append(ConditionsNoeud.from_dict(child))
            elif child_key in CONDITIONS_TYPES:
                parsed_children.append(ConditionsFeuille.from_dict(child))
            else:
                raise RuntimeError(f"Unknown child key {child_key}.")

        return ConditionsNoeud(node_type, parsed_children)
