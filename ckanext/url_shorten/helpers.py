

def parse_request_parameters_to_dict(params):
    """
    This is request params parser should apply for both flask and pylons
    :return:
    """
    new_params = dict()
    for param in params:
        val = params[param]
        if isinstance(val, list):
            val = ",".join(val)
        new_params[param] = val
    return new_params
