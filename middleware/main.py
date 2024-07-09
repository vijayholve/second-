

class customeMiddleware:
    def __init__(self,get_responce) -> None:    
        self.get_responce=get_responce
    def __call__(self,request  ) :
        print("before")
        responce=self.get_responce(request)
        print("source of request is ",request.META.get('HTTP_USER_AGENT'))
        return  responce