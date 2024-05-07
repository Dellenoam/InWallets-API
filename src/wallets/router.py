from typing import Annotated, List, Sequence

from fastapi.staticfiles import StaticFiles

from auth.dependencies import get_access_token, token_service
from auth.services import TokenService
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from wallets.config import CHAINS
from wallets.dependencies import (
    balance_service,
    wallet_group_service,
    wallet_importer_service,
    wallet_service,
)
from wallets.models import Wallet, WalletGroup
from wallets.schemas import (
    ChainsSchema,
    ChainSchema,
    WalletCreateSchema,
    WalletDeleteSchema,
    WalletGroupCreateSchema,
    WalletGroupPatchSchema,
    WalletGroupPutSchema,
    WalletGroupSchema,
    WalletPatchSchema,
    WalletPutSchema,
    WalletSchema,
    ChainBalanceSchema,
)
from wallets.services import (
    BalanceService,
    WalletGroupService,
    WalletImporterService,
    WalletService,
)

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.get("/", status_code=200, response_model=List[WalletSchema])
async def get_wallets(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_service: Annotated[WalletService, Depends(wallet_service)],
) -> Sequence[Wallet]:
    user_data = await token_service.check_access_token(access_token)

    return await wallet_service.get_wallets(user_data["id"])


@router.post("/", status_code=201, response_model=List[WalletSchema])
async def import_wallets(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_importer_service: Annotated[
        WalletImporterService, Depends(wallet_importer_service)
    ],
    wallets: List[WalletCreateSchema],
) -> Sequence[Wallet]:
    user_data = await token_service.check_access_token(access_token)

    if not wallets:
        raise HTTPException(status_code=400, detail="No wallets to import")

    return await wallet_importer_service.import_wallets(wallets, user_data["id"])


@router.post("/xlsx/", status_code=201, response_model=List[WalletSchema])
async def import_wallets_xlsx(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_service: Annotated[WalletImporterService, Depends(wallet_importer_service)],
    wallets_xlsx: UploadFile,
) -> Sequence[Wallet]:
    user_data = await token_service.check_access_token(access_token)

    if not wallets_xlsx:
        raise HTTPException(status_code=400, detail="No wallets to import")

    return await wallet_service.import_wallets_xlsx(wallets_xlsx, user_data["id"])


@router.put("/", status_code=200, response_model=List[WalletSchema])
async def put_wallets(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_service: Annotated[WalletService, Depends(wallet_service)],
    wallets: List[WalletPutSchema],
) -> Sequence[Wallet]:
    user_data = await token_service.check_access_token(access_token)

    if not wallets:
        raise HTTPException(status_code=400, detail="No wallets to put")

    return await wallet_service.update_wallets(wallets, user_data["id"])


@router.patch("/", status_code=200, response_model=List[WalletSchema])
async def patch_wallets(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_service: Annotated[WalletService, Depends(wallet_service)],
    wallets: List[WalletPatchSchema],
) -> Sequence[Wallet]:
    user_data = await token_service.check_access_token(access_token)

    if not wallets:
        raise HTTPException(status_code=400, detail="No wallets to patch")

    return await wallet_service.update_wallets(wallets, user_data["id"])


@router.delete("/", status_code=204)
async def delete_wallets(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_service: Annotated[WalletService, Depends(wallet_service)],
    wallet_ids: List[WalletDeleteSchema],
) -> None:
    user_data = await token_service.check_access_token(access_token)

    if not wallet_ids:
        raise HTTPException(status_code=400, detail="No wallets to delete")

    await wallet_service.delete_wallets(wallet_ids, user_data["id"])


@router.get("/groups/", status_code=200, response_model=List[WalletGroupSchema])
async def get_user_wallet_groups(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_group_service: Annotated[WalletGroupService, Depends(wallet_group_service)],
) -> Sequence[WalletGroup]:
    user_data = await token_service.check_access_token(access_token)

    return await wallet_group_service.get_wallet_groups(user_data["id"])


@router.get(
    "/groups/{wallet_group_id}/", status_code=200, response_model=WalletGroupSchema
)
async def get_user_wallet_group(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_group_service: Annotated[WalletGroupService, Depends(wallet_group_service)],
    wallet_group_id: int,
) -> WalletGroup:
    user_data = await token_service.check_access_token(access_token)

    return await wallet_group_service.get_wallet_group(wallet_group_id, user_data["id"])


@router.post("/groups/", status_code=201, response_model=WalletGroupSchema)
async def create_group(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_group_service: Annotated[WalletGroupService, Depends(wallet_group_service)],
    wallet_group: WalletGroupCreateSchema,
) -> WalletGroup:
    user_data = await token_service.check_access_token(access_token)

    return await wallet_group_service.create_wallet_group(wallet_group, user_data["id"])


@router.put(
    "/groups{wallet_group_id}", status_code=200, response_model=WalletGroupSchema
)
async def put_group(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_group_service: Annotated[WalletGroupService, Depends(wallet_group_service)],
    wallet_group_id: int,
    wallet_group: WalletGroupPutSchema,
) -> WalletGroup:
    user_data = await token_service.check_access_token(access_token)

    return await wallet_group_service.update_wallet_group(
        wallet_group_id, wallet_group, user_data["id"]
    )


@router.patch(
    "/groups/{wallet_group_id}", status_code=200, response_model=WalletGroupSchema
)
async def patch_group(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_group_service: Annotated[WalletGroupService, Depends(wallet_group_service)],
    wallet_group_id: int,
    wallet_group: WalletGroupPatchSchema,
) -> WalletGroup:
    user_data = await token_service.check_access_token(access_token)

    return await wallet_group_service.update_wallet_group(
        wallet_group_id, wallet_group, user_data["id"]
    )


@router.delete("/groups/{wallet_group_id}/", status_code=204)
async def delete_group(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_group_service: Annotated[WalletGroupService, Depends(wallet_group_service)],
    wallet_group_id: int,
) -> None:
    user_data = await token_service.check_access_token(access_token)

    await wallet_group_service.delete_wallet_group(wallet_group_id, user_data["id"])


@router.get("/chains/", status_code=200, response_model=ChainsSchema)
async def get_chains(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
) -> ChainsSchema:
    # await token_service.check_access_token(access_token)

    return ChainsSchema(
        chains=[
            ChainSchema(
                name=chain, symbol=chain_info["currency"], logo=chain_info["chain_logo"]
            )
            for chain, chain_info in CHAINS.items()
        ]
    )


@router.get("/balance/", status_code=200, response_model=List[ChainBalanceSchema])
async def get_wallet_balance(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    selected_chains: List[ChainSchema],
    balance_service: Annotated[BalanceService, Depends(balance_service)],
) -> List[ChainBalanceSchema]:
    user_data = await token_service.check_access_token(access_token)

    for chain in selected_chains:
        if chain.name not in CHAINS:
            raise HTTPException(status_code=404, detail="Chain not found")

    return await balance_service.get_wallets_balance(user_data["id"], selected_chains)


@router.get("/{wallet_id}/", status_code=200, response_model=WalletSchema)
async def get_wallet(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    wallet_service: Annotated[WalletService, Depends(wallet_service)],
    wallet_id: int,
) -> Wallet:
    user_data = await token_service.check_access_token(access_token)

    return await wallet_service.get_wallet(wallet_id, user_data["id"])
