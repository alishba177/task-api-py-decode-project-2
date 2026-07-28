# "The Gatekeeper Rule" — Never trust the client.
# Every request body is checked in two layers before it reaches the data layer:
#   1. Syntactic validation -> is the shape/type of the data correct?
#   2. Semantic validation   -> does the value actually make sense (not empty, not too long, etc.)?


def validate_new_task(body):
    """
    Returns (error_response, validated_data).
    Exactly one of the two will be None.
    error_response is a dict ready to be jsonified with a 400 status.
    """
    if not isinstance(body, dict):
        return {"error": "Bad Request", "message": "Request body must be a JSON object."}, None

    title = body.get("title")
    completed = body.get("completed")

    # --- Syntactic validation ---
    if title is None:
        return {"error": "Bad Request", "message": "'title' is required in the request body."}, None

    if not isinstance(title, str):
        return {"error": "Bad Request", "message": "'title' must be a string."}, None

    if completed is not None and not isinstance(completed, bool):
        return {"error": "Bad Request", "message": "'completed' must be a boolean if provided."}, None

    # --- Semantic validation ---
    trimmed_title = title.strip()

    if len(trimmed_title) == 0:
        return {"error": "Bad Request", "message": "'title' cannot be empty."}, None

    if len(trimmed_title) > 100:
        return {"error": "Bad Request", "message": "'title' cannot exceed 100 characters."}, None

    return None, {"title": trimmed_title, "completed": bool(completed) if completed is not None else False}
