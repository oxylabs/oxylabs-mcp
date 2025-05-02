def convert_context_params(arguments: dict) -> dict:
    context_fields = ["category_id", "merchant_id", "currency", "autoselect_variant"]
    arguments_copy = {**arguments}

    for f in context_fields:
        if f in arguments_copy:
            if "context" not in arguments_copy:
                arguments_copy["context"] = []

            arguments_copy["context"].append({"key": f, "value": arguments_copy[f]})
            del arguments_copy[f]

    return arguments_copy
