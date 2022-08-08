from django.conf import settings
import requests

class Paystack:
    PAYSTACK_PRIVATE_KEY = settings.PAYSTACK_PRIVATE_KEY
    base_url = 'https://api.paystack.co'

    def payment_process(self, reference, *args, **kwargs):
        path = f'/transaction/verify/{reference}'

        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_PRIVATE_KEY}",
            "Content-Type": 'application/json',
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']