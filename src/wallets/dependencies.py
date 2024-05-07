from unit_of_work import UnitOfWork
from wallets.services import BalanceService, WalletGroupService, WalletImporterService, WalletService


def wallet_service() -> WalletService:
    return WalletService(UnitOfWork)


def wallet_importer_service() -> WalletImporterService:
    return WalletImporterService(UnitOfWork)


def wallet_group_service() -> WalletGroupService:
    return WalletGroupService(UnitOfWork)


def balance_service() -> BalanceService:
    return BalanceService(UnitOfWork)
