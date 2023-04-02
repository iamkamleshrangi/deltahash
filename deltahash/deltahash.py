from copy import deepcopy

def unmerge(original, extra):
    unmerged = {}
    for key, value in original.items():
        if key not in extra:
            if isinstance(value, dict):
                nested = easy_unmerge(value, {})
                if nested:
                    unmerged[key] = nested
            elif isinstance(value, list):
                if set(value) - set(extra.get(key, [])):
                    unmerged[key] = list(set(value) - set(extra.get(key, [])))
            else:
                unmerged[key] = value
        elif isinstance(value, dict) and key in extra and isinstance(extra[key], dict):
            nested = easy_unmerge(value, extra[key])
            if nested:
                unmerged[key] = nested
        elif isinstance(value, list) and key in extra and isinstance(extra[key], list):
            diff = set(value) - set(extra[key])
            if diff:
                unmerged[key] = list(diff)
    return unmerged

def merge(original, extra):
    merged = original.copy()
    for key, value in extra.items():
        if isinstance(value, dict) and key in original and isinstance(original[key], dict):
            merged[key] = easy_merge(original[key], value)
        elif isinstance(value, list) and key in original and isinstance(original[key], list):
            merged[key] = list(set(original[key] + value))
        else:
            merged[key] = value
    return merged

def diff(original, modified):
    removed = {}
    added = {}

    for key in original:
        if key not in modified:
            removed[key] = original[key]

        elif isinstance(original[key], dict):
            sub_removed, sub_added = diff(original[key], modified[key])
            if sub_removed:
                removed[key] = sub_removed
            if sub_added:
                added[key] = sub_added

        elif original[key] != modified[key]:
            removed[key] = original[key]
            added[key] = modified[key]

    for key in modified:
        if key not in original:
            added[key] = modified[key]
    return removed, added

def clone(original):
    return deepcopy(original)
