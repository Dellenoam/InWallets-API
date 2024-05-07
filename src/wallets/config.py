CHAINS = {
    "Avalanche": {
        "currency": "AVAX",
        "rpc": [
            "https://avalanche.drpc.org",
            "https://avax.meowrpc.com",
            "https://endpoints.omniatech.io/v1/avax/mainnet/public",
        ],
        "usdt_contract_address": "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7",
        "usdc_contract_address": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
        "chain_logo": "/static/chains/avalanche-avax-logo.png",
    },
    "Polygon": {
        "currency": "MATIC",
        "rpc": [
            "https://polygon.llamarpc.com",
            "https://polygon.meowrpc.com",
            "https://polygon-bor-rpc.publicnode.com",
        ],
        "usdt_contract_address": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
        "usdc_contract_address": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "chain_logo": "/static/chains/polygon-matic-logo.png",
    },
    "Ethereum": {
        "currency": "ETH",
        "rpc": [
            "https://eth.llamarpc.com",
            "https://rpc.payload.de",
            "https://rpc.mevblocker.io",
        ],
        "usdt_contract_address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "usdc_contract_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "chain_logo": "/static/chains/ethereum-eth-logo.png",
    },
    "BNB Smart Chain": {
        "currency": "BNB",
        "rpc": [
            "https://bsc.meowrpc.com",
            "https://bsc-rpc.publicnode.com",
            "https://binance.llamarpc.com",
        ],
        "usdt_contract_address": "0x55d398326f99059ff775485246999027b3197955",
        "usdc_contract_address": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "chain_logo": "/static/chains/bnb-bnb-logo.png",
    },
    "Arbitrum One": {
        "currency": "ETH",
        "rpc": [
            "https://arbitrum.llamarpc.com",
            "https://endpoints.omniatech.io/v1/arbitrum/one/public",
            "https://arbitrum-one-rpc.publicnode.com",
        ],
        "usdt_contract_address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "usdc_contract_address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "chain_logo": "/static/chains/arbitrum-eth-logo.png",
    },
    "Optimism": {
        "currency": "ETH",
        "rpc": [
            "https://optimism-rpc.publicnode.com",
            "https://optimism.meowrpc.com",
            "https://endpoints.omniatech.io/v1/op/mainnet/public",
        ],
        "usdt_contract_address": "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58",
        "usdc_contract_address": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
        "chain_logo": "/static/chains/optimism-eth-logo.png",
    },
    "Fantom": {
        "currency": "FTM",
        "rpc": [
            "https://rpcapi.fantom.network",
            "https://fantom.drpc.org",
            "https://fantom-rpc.publicnode.com",
        ],
        "usdt_contract_address": "0x049d68029688eabf473097a2fc38ef61633a3c7a",
        "usdc_contract_address": "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75",
        "chain_logo": "/static/chains/fantom-ftm-logo.png",
    },
    "zkSync Era": {
        "currency": "ETH",
        "rpc": [
            "https://zksync.meowrpc.com",
            "https://zksync.drpc.org",
            "https://zksync-era.blockpi.network/v1/rpc/public",
        ],
        "usdc_contract_address": "0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4",
        "chain_logo": "/static/chains/zksync-eth-logo.png",
    },
    "Arbitrum Nova": {
        "currency": "ETH",
        "rpc": [
            "https://arbitrum-nova-rpc.publicnode.com",
            "https://arbitrum-nova.public.blastapi.io",
            "https://arbitrum-nova.publicnode.com",
        ],
        "usdc_contract_address": "0x750ba8b76187092b0d1e87e28daaf484d1b5273b",
        "chain_logo": "/static/chains/arbitrum_nova-eth-logo.png",
    },
    "Gnosis": {
        "currency": "XDAI",
        "rpc": [
            "https://rpc.gnosischain.com",
            "https://rpc.gnosis.gateway.fm",
            "https://gnosis-rpc.publicnode.com",
        ],
        "usdt_contract_address": "0x4ECaBa5870353805a9F068101A40E0f32ed605C6",
        "usdc_contract_address": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
        "chain_logo": "/static/chains/gnosis-xdai-logo.png",
    },
    "Celo": {
        "currency": "CELO",
        "rpc": [
            "https://forno.celo.org",
            "https://rpc.ankr.com/celo",
            "https://1rpc.io/celo",
        ],
        "usdc_contract_address": "0xcebA9300f2b948710d2653dD7B07f33A8B32118C",
        "chain_logo": "/static/chains/celo-celo-logo.png",
    },
    "Polygon zkEVM": {
        "currency": "ETH",
        "rpc": [
            "https://zkevm-rpc.com",
            "https://polygon-zkevm.blockpi.network/v1/rpc/public",
            "https://rpc.ankr.com/polygon_zkevm",
        ],
        "usdt_contract_address": "0x1e4a5963abfd975d8c9021ce480b42188849d41d",
        "usdc_contract_address": "0xa8ce8aee21bc2a48a5ef670afcc9274c7bbbc035",
        "chain_logo": "/static/chains/polygon_zkevm-eth-logo.png",
    },
    "Core": {
        "currency": "CORE",
        "rpc": [
            "https://core.public.infstones.com",
            "https://rpc-core.icecreamswap.com",
            "https://rpc.ankr.com/core",
        ],
        "usdt_contract_address": "0x900101d06A7426441Ae63e9AB3B9b0F63Be145F1",
        "usdc_contract_address": "0xa4151B2B3e269645181dCcF2D426cE75fcbDeca9",
        "chain_logo": "/static/chains/core-core-logo.png",
    },
    "Harmony": {
        "currency": "ONE",
        "rpc": [
            "https://api.harmony.one",
            "https://api.s0.t.hmny.io",
            "https://api.s1.t.hmny.io",
        ],
        "usdt_contract_address": "0x3c2b8be99c50593081eaa2a724f0b8285f5aba8f",
        "usdc_contract_address": "0x985458e523db3d53125813ed68c274899e9dfab4",
        "chain_logo": "/static/chains/harmony-one-logo.png",
    },
    "Base": {
        "currency": "ETH",
        "rpc": [
            "https://base.llamarpc.com",
            "https://base.gateway.tenderly.co",
            "https://base-rpc.publicnode.com",
        ],
        "usdc_contract_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "chain_logo": "/static/chains/base-eth-logo.png",
    },
    "Scroll": {
        "currency": "ETH",
        "rpc": [
            "https://scroll.drpc.org",
            "https://scroll.blockpi.network/v1/rpc/public",
            "https://scroll-mainnet.rpc.grove.city/v1/a7a7c8e2",
        ],
        "usdt_contract_address": "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
        "usdc_contract_address": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
        "chain_logo": "/static/chains/scroll-eth-logo.png",
    },
    "Moonbeam": {
        "currency": "GLMR",
        "rpc": [
            "https://moonbeam-rpc.dwellir.com",
            "https://moonbeam-rpc.publicnode.com",
            "https://rpc.ankr.com/moonbeam",
        ],
        "usdt_contract_address": "0xefaeee334f0fd1712f9a8cc375f427d9cdd40d73",
        "chain_logo": "/static/chains/moonbeam-glmr-logo.png",
    },
    "Moonriver": {
        "currency": "MOVR",
        "rpc": [
            "https://moonriver-rpc.publicnode.com",
            "https://moonriver.drpc.org",
            "https://rpc.api.moonriver.moonbeam.network",
        ],
        "usdt_contract_address": "0xe936caa7f6d9f5c9e907111fcaf7c351c184cda7",
        "usdc_contract_address": "0xe3f5a90f9cb311505cd691a46596599aa1a0ad7d",
        "chain_logo": "/static/chains/moonriver-movr-logo.png",
    },
    "Canto": {
        "currency": "CANTO",
        "rpc": [
            "https://canto-rpc.ansybl.io",
            "https://canto.slingshot.finance",
            "https://mainnode.plexnode.org:8545",
        ],
        "usdt_contract_address": "0xd567b3d7b8fe3c79a1ad8da978812cfc4fa05e75",
        "usdc_contract_address": "0x80b5a32E4F032B2a058b4F29EC95EEfEEB87aDcd",
        "chain_logo": "/static/chains/canto-canto-logo.png",
    },
    "Metis": {
        "currency": "METIS",
        "rpc": [
            "https://metis.drpc.org",
            "https://andromeda.metis.io/?owner=1088",
            "https://metis-mainnet.public.blastapi.io",
        ],
        "usdt_contract_address": "0xbb06dca3ae6887fabf931640f67cab3e3a16f4dc",
        "usdc_contract_address": "0xea32a96608495e54156ae48931a7c20f0dcc1a21",
        "chain_logo": "/static/chains/metis-mtst-logo.png",
    },
    "Linea": {
        "currency": "ETH",
        "rpc": [
            "https://rpc.linea.build",
            "https://linea.blockpi.network/v1/rpc/public",
            "https://linea.drpc.org",
        ],
        "chain_logo": "/static/chains/linea-eth-logo.png",
    },
    "Mantle": {
        "currency": "MNT",
        "rpc": [
            "https://mantle.drpc.org",
            "https://mantle-rpc.publicnode.com",
            "https://rpc.ankr.com/mantle",
        ],
        "usdt_contract_address": "0x201eba5cc46d216ce6dc03f6a759e8e766e956ae",
        "usdc_contract_address": "0x09bc4e0d864854c6afb6eb9a9cdf58ac190d0df9",
        "chain_logo": "/static/chains/mantle-mnt-logo.png",
    },
}

ABI = """
[
    {
        "constant": true,
        "inputs": [
            {
                "name": "who",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
]
"""
