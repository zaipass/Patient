from django.utils.deprecation import MiddlewareMixin


class TokenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # print(request.headers, "====")
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        # print(dir(view_func), view_args, '=======>>>')
        pass
