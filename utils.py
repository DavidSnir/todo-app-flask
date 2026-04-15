def check_json_fields(allowed_fileds: list[tuple[str, type]], user_data: dict) -> tuple[bool,dict]:
    """### Check if the user input is in the right format
    \n needs allowed filds list of tuples(key: value) and the user data (a json dict)
    \n*return True is the check was good*"""
    for key, value in user_data.items():
        if not (key,type(value)) in allowed_fileds:
            return False, {"error": f"the key {key} and value {value} combination is not allowed "}
    return True, {"status": "succses"}