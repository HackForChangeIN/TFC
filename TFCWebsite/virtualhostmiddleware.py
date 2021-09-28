virtual_hosts = {
    # Staging env
    "*.staging.forchange.in": "TFC.urls",
    "staging.forchange.in": "TFC.urls",
    "staging.hackforchange.co.in": "HFCCore.urls",

    # Production
    "*.forchange.in": "TFC.urls",
    "www.forchange.in": "TFC.urls",
    "www.hackforchange.co.in": "HFCCore.urls",

    # Local Dev
    "*.dev.forchange.in:8000": "TFC.urls",
    "dev.forchange.in:8000": "TFC.urls",
    "dev.hackforchange.co.in:8000": "HFCCore.urls",
    
}


class VirtualHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # let's configure the root urlconf
        host = request.get_host()
        #print('hostname=', host)
        request.urlconf = virtual_hosts.get(host)
        #print('urlgoes to=', request.urlconf)

        response = self.get_response(request)
        # print(response)
        return response
