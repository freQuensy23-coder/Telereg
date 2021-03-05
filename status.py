def status_encode(status: str) -> int:
    if status == "wait":
        return 0
    if status == "accepted":
        return 1
    else:
        raise Exception # TODO


def status_decode(status_code: int) -> str:
    if status_code == 0:
        return "wait"
    elif status_code == 1:
        return "accepted"
    else:
        raise Exception # TODO