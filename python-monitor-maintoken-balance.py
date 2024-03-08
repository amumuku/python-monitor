from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import dotenv_values

import time
import logging
import re
import sys  # 导入 sys 模块
from logger_setup import logger  # 导入日志记录器

import logging.handlers

# 加载环境变量
config = dotenv_values(".env")

from mysql_config import connect_to_mysql, insert_data, close_mysql_connection

# BSC节点的RPC端点
bsc_rpc = config['BSC_RPC']

# 账户地址和私钥
RECEIVE_ADDRESS = config['RECEIVE_ADDRESS']
WATCH_PRIVATE_KEY = config['WATCH_PRIVATE_KEY']

# 监控的地址和固定余额
watch_address = config['WATCH_ADDRESS']
fixed_balance = float(config['FIXED_BALANCE'])
chain_id = int(config['CHAIN_ID'])


# 初始化Web3对象
web3 = Web3(Web3.HTTPProvider(bsc_rpc))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# 加载账户
account = web3.eth.account.from_key(WATCH_PRIVATE_KEY)

print(account)
# 获取当前块号
def get_current_block_number():
    return web3.eth.block_number

# 获取地址的BNB余额
def get_bnb_balance(address):
    return web3.eth.get_balance(address)

# 监听事件
def monitor_balance():

    while True:
        try:
            block_num=get_current_block_number()
            watch_address_check=web3.to_checksum_address(watch_address)
            balance = get_bnb_balance(watch_address_check)
            # 建立MySQL连接
            conn = connect_to_mysql()
            logger.info("connect mysql: {} ".format(conn.is_connected))
            # 将数据插入MySQL数据库
            insert_data(conn, 'qiang_bot', (
                watch_address,
                chain_id,
                balance, 
                block_num
                )
            )
            close_mysql_connection(conn)
            #插入数据库
            if balance > fixed_balance:        
                # 打印地址信息和余额
                print(f"地址: {watch_address}")
                print(f"当前BNB余额: {web3.from_wei(balance, 'ether')} BNB")

                # 创建交易参数
                nonce = web3.eth.get_transaction_count(watch_address_check)
                gas_price = web3.eth.gas_price
                # gas_limit = 2000000  # 设置合适的 gas limit

                # 估算 gas
                gas_estimate = web3.eth.estimate_gas({
                    'from': watch_address_check,
                    'to': RECEIVE_ADDRESS,
                    'value': balance,  
                })
                valuetosend = balance - (gas_estimate * gas_price)
                # 构造转账交易
                transaction = {
                    'to': RECEIVE_ADDRESS,
                    'value': valuetosend,  # 直接转移全部余额
                    'gas': gas_estimate,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                    'chainId': chain_id  # BSC链的链ID
                }

                # 签署交易
                signed_txn = web3.eth.account.sign_transaction(transaction, private_key=WATCH_PRIVATE_KEY)

                # 发送交易
                tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

                # 等待交易收据
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_token)
                print(f"转账成功，交易哈希: {tx_receipt.transactionHash.hex()}")
            else:
                print(f"block_num:{block_num} no money change")
                continue

        except Exception as e:
            print(f"发生错误: {e}")
if __name__ == "__main__":
    monitor_balance()
