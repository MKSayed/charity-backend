class PaymentService:
    def __init__(self, payment_processor: ExternalPaymentProcessor = None):
        self.processor = payment_processor or ExternalPaymentProcessor()

    def process_payment(self, amount: float, service_id: str):
        validate_payment_amount(amount)

        # Call external payment class
        transaction = self.processor.create_transaction(
            amount=amount, service_id=service_id
        )

        return format_payment_response(
            status=transaction.status, transaction_id=transaction.id
        )
