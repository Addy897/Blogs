def parseLoginUser(data:dict) -> bool:
    if(not data.get("email") and not data.get('phone')):
        return False
    if(not data.get("password")):
        return False
    return True
def parseRegisterUser(data:dict):
    if(not data.get("fname")):
        return False
    if(not data.get("password")):
        return False
    if(not data.get("lname")):
        return False
    if(not data.get("email")):
        return False
    if(not data.get("pfPhoto")):
        return False
    if(not data.get("phone")):
        return False
    return True