from dataclasses import dataclass

from supplier.gigachat_supplier import GigachatSupplier


@dataclass
class ChatService:
    gigachat_supplier: GigachatSupplier

    def send_message(self, message: str) -> str:
        return self.gigachat_supplier.single_message(message)
