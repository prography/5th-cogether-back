from test_plus import TestCase as TestPlusTestCase


class TestCase(TestPlusTestCase):
    def response_204(self, response=None):
        response = self._which_response(response)
        self.assertEqual(response.status_code, 204)

    def get_check_302(self, url, *args, **kwargs):
        response = self.get(url, *args, **kwargs)
        self.response_302(response)
        return response

    def get_check_403(self, url, *args, **kwargs):
        response = self.get(url, *args, **kwargs)
        self.response_403(response)
        return response

    def get_check_404(self, url, *args, **kwargs):
        response = self.get(url, *args, **kwargs)
        self.response_404(response)
        return response

    def get_check_405(self, url, *args, **kwargs):
        response = self.get(url, *args, **kwargs)
        self.response_405(response)
        return response

    def get_check_500(self, url, *args, **kwargs):
        response = self.get(url, *args, **kwargs)
        self.assertEqual(response.status_code, 500)
        return response

    def post_check_201(self, url, *args, **kwargs):
        response = self.post(url, *args, **kwargs)
        self.response_201(response)
        return response

    def post_check_400(self, url, *args, **kwargs):
        response = self.post(url, *args, **kwargs)
        self.response_400(response)
        return response

    def post_check_403(self, url, *args, **kwargs):
        response = self.post(url, *args, **kwargs)
        self.response_403(response)
        return response

    def post_check_405(self, url, *args, **kwargs):
        response = self.post(url, *args, **kwargs)
        self.response_405(response)
        return response

    def patch_check_200(self, url, *args, **kwargs):
        response = self.patch(url, *args, **kwargs)
        self.response_200(response)
        return response

    def patch_check_400(self, url, *args, **kwargs):
        response = self.patch(url, *args, **kwargs)
        self.response_400(response)
        return response

    def patch_check_403(self, url, *args, **kwargs):
        response = self.patch(url, *args, **kwargs)
        self.response_403(response)
        return response

    def patch_check_404(self, url, *args, **kwargs):
        response = self.patch(url, *args, **kwargs)
        self.response_404(response)
        return response

    def patch_check_405(self, url, *args, **kwargs):
        response = self.patch(url, *args, **kwargs)
        self.response_405(response)
        return response

    def delete_check_204(self, url, *args, **kwargs):
        response = self.delete(url, *args, **kwargs)
        self.response_204(response)
        return response

    def delete_check_403(self, url, *args, **kwargs):
        response = self.delete(url, *args, **kwargs)
        self.response_403(response)
        return response
