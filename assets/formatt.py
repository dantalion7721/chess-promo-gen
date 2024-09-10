def GetFormattedProxy(proxy):
    if not proxy:
        return None

    try:
        if '@' in proxy:
            proxy = "http://" + proxy
        else:
            proxy = "http://" + proxy

        return proxy

    except Exception as e:
        return None
