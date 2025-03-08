import multiprocessing
from src.utils.geidea_api import GeideaAPI, CheckStatusResult, TransactionResult
from src.config import settings

geidea_trx_processor = GeideaAPI(settings.pos_comport)


def _purchase_wrapper(
    trx_amount: int, trx_ecr_ref: str
):  # Wrapper function needed for passing as a pickle to another process
    return geidea_trx_processor.purchase(trx_amount, trx_ecr_ref)


def process_purchase_transaction(
    trx_amount: float, trx_ecr_ref: str
) -> tuple[bool, CheckStatusResult | TransactionResult]:
    terminal_status_resp = geidea_trx_processor.check_terminal_status()

    if not terminal_status_resp.response_code == 0:
        return False, terminal_status_resp

    trx_amount_cents = int(trx_amount * 100)

    # Run geidea_trx_processor.purchase in a separate interruptable process
    # to be able to time it out
    with multiprocessing.Pool(1) as pool:
        result = pool.apply_async(_purchase_wrapper, (trx_amount_cents, trx_ecr_ref))
        try:
            purchase_resp = result.get(timeout=settings.transaction_timeout_in_secs)
            purchase_success = purchase_resp.response_code == 0
            return purchase_success, purchase_resp

        except multiprocessing.TimeoutError:
            return False, CheckStatusResult(-16, "Purchase transaction timed out")
