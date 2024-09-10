def GetFormattedProxy(proxy):
        
        if proxy == "":
            return None
        
        try:
            
            if '@' in proxy:
                return {"http": "http://" + proxy, "https": "http://" + proxy}
            
            elif len(proxy.split(':')) == 2:
                return {"http": "http://" + proxy, "https": "http://" + proxy}
            else:
                if '.' in proxy.split(':')[0]:
                    return {"http": "http://" + ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2]), "https": "http://" + ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])}
                else:
                    return {"http": "http://" + ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:]), "https": "http://" + ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])}

        except:
            return None
