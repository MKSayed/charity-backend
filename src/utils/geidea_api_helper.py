from src.utils.geidea_api import GeideaAPI, CheckStatusResult, TransactionResult
from src.config import settings

geidea_trx_processor = GeideaAPI(settings.pos_comport)


def process_purchase_transaction(trx_amount: float, ) -> tuple[bool, CheckStatusResult | TransactionResult] :
    terminal_status_resp = geidea_trx_processor.check_terminal_status()

    if not terminal_status_resp.response_code == 0:
        return False, terminal_status_resp
    
    purchase_resp = geidea_trx_processor.purchase(int(trx_amount * 100),
                                                   '0000000000000003')
    
    purchase_success = purchase_resp.response_code == 0
    return purchase_success, purchase_resp