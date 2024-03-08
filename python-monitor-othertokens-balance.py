from decimal import Decimal
from web3 import Web3
import json

from web3.middleware import geth_poa_middleware
from dotenv import dotenv_values

# 加载环境变量
config = dotenv_values(".env")

# BSC节点的RPC端点
bsc_rpc = config['BSC_RPC']

# 账户地址和私钥
RECEIVE_ADDRESS = config['RECEIVE_ADDRESS']
WATCH_PRIVATE_KEY = config['WATCH_PRIVATE_KEY']

# 监控的地址和固定余额
watch_address = config['WATCH_ADDRESS']
fixed_balance = float(config['FIXED_BALANCE'])
chain_id = int(config['CHAIN_ID'])

# 获取代币地址列表
token_address_list_str = config['TOKEN_ADDRESS_LIST']

# 初始化Web3对象
web3 = Web3(Web3.HTTPProvider(bsc_rpc))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# 加载账户
account = web3.eth.account.from_key(WATCH_PRIVATE_KEY)
# 获取 ERC20 代币合约 ABI
# 读取当前目录下的 JSON 文件
with open('erc20abi.json', 'r') as f:
    erc20_abi = json.load(f)

print(account)

# 获取 ERC20 代币合约实例
def get_erc20_contract(token_address):
    return web3.eth.contract(address=web3.to_checksum_address(token_address), abi=erc20_abi)

# 获取当前块号
def get_current_block_number():
    return web3.eth.block_number


# 监听事件
def monitor_othertokens_balance():
    token_address_list = token_address_list_str.split(',')

    while True:

        for token_address in token_address_list:
            try:
                block_num=get_current_block_number()
                contract = get_erc20_contract(token_address)
                token_balance = contract.functions.balanceOf(watch_address).call()
                if token_balance > 0:        
                    # 创建代币合约实例
                    # print(f"get_erc20_contract {token_address}")

                    # 获取账户余额
                    token_balance_show = web3.from_wei(contract.functions.balanceOf(watch_address).call(), 'ether')
                    print(f"get_erc20_contract token{token_address} :token_balance {token_balance_show}")

                    # 发送代币交易

                    nonce = web3.eth.get_transaction_count(watch_address,"pending")
                    gas_price = web3.eth.gas_price

                    tx = contract.functions.transfer(RECEIVE_ADDRESS, token_balance).build_transaction({
                        'from': watch_address,
                        'chainId': chain_id,  # BSC的chainId为56
                        'gasPrice': gas_price,
                        'nonce': nonce,
                    })
                    gas_limit = web3.eth.estimate_gas(transaction=tx)
                    print(gas_limit)
                    tx['gas'] = gas_limit
                    signed_tx = web3.eth.account.sign_transaction(tx, private_key=WATCH_PRIVATE_KEY)
                    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                    htx_hash=web3.to_hex(tx_hash)
                    print(f"Token Transfer for {token_address} - Transaction Hash: {htx_hash} finished")
                else:
                    print(f"block_num:{block_num} no money change")
                    continue
            except Exception as e:
                print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    monitor_othertokens_balance()
