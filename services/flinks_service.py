import requests


class FlinksService:
    """
    A service class for interacting with the Flinks API.
    """

    BASE_URL = "https://sandbox.flinks.io/api/v4"

    @classmethod
    def check_balance(cls, bank_account_id: str, amount: float) -> bool:
        """
        Checks if the specified bank account has a balance greater than the specified amount.
        """
        url = f"{cls.BASE_URL}/banking/check_balance"
        headers = {"Authorization": "Bearer YOUR_FLINKS_API_KEY"}

        # Build the request body
        data = {
            "bankAccount": {"id": bank_account_id},
            "balanceAmount": {"amount": amount, "currency": "CAD"},
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=data)

        # Check if the request was successful and the balance is sufficient
        if response.status_code == 200:
            return response.json()["sufficientFunds"]
        else:
            raise Exception(f"Failed to check balance: {response.text}")
