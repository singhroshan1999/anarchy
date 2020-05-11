def dispatch(disp,req,header): # disp = dictionary    req = queue
    if len(req) == 0: raise Exception
    uri = req.pop(0)
    if uri not in disp: raise Exception
    if len(req) == 0:
        return disp[uri](header)
    else:
        return dispatch(disp[uri],req,header)

