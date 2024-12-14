from typing import Any, Dict


class TokenHolder:
    def __init__(self, token_id, token_name, address, balance):
        self.token_id = token_id
        self.token_name = token_name
        self.address = address
        self.balance = balance

    def to_dict(self) -> Dict[str, Any]:
        return {
            'token_id': self.token_id,
            'token_name': self.token_name,
            'address': self.address,
            'balance': self.balance
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TokenHolder':
        return cls(
            token_id=data['token_id'],
            token_name=data['token_name'],
            address=data['address'],
            balance=data['balance']
        )

    def __repr__(self) -> str:
        return f"TokenHolder(token_id='{self.token_id}', token_name='{self.token_name}', address='{self.address}', balance={self.balance})"
