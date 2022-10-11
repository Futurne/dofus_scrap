def parse_armes_caracs(caracs: dict) -> dict:
    caracs = caracs.copy()
    for c_name, c_value in caracs.items():
        match c_name:
            case "CC":
                caracs["CC"] = tuple(c_value)
            case "Portée":
                match c_value:
                    case int() as a:
                        caracs["Portée"] = (a, a)
                    case [a, b]:
                        caracs["Portée"] = (a, b)
                    case _:
                        raise RuntimeError(f"Unknown caractéristique in {caracs}")
            case _:
                pass

    return caracs


def parse_bestiaire_caracs(caracs: dict) -> dict:
    caracs = caracs.copy()
    for c_name, c_value in caracs.items():
        match c_value:
            case int() as a:
                caracs[c_name] = (a, a)
            case [a, b]:
                caracs[c_name] = (a, b)
            case _:
                raise RuntimeError(f"Unknown caractéristique in {caracs}")

    return caracs


def parse_caracs(category: str, caracs: dict) -> dict:
    match category:
        case "Armes":
            return parse_armes_caracs(caracs)
        case "Bestiaire":
            return parse_bestiaire_caracs(caracs)
        case "Montures":
            return caracs.copy()
        case _:
            raise RuntimeError(
                f"Unknown category {category} when parsing caracteristics"
            )
