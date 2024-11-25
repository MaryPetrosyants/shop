from rest_framework.throttling import UserRateThrottle

class CustomUserRateThrottle(UserRateThrottle):

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                self.scope = 'admin'
            else:
                self.scope = 'user'
        else:
          
            self.scope = 'anon'
   
        return super().get_cache_key(request, view)

       