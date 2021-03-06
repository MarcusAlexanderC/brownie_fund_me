from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account, 
    deploy_mocks, 
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
#from web3 import Web3

def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract
    
    # if we are on a persistent network like rinkeby, use the associated address 
    # otherwise, deploy mocks
    #if network.show_active() != "development":
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        #print(f"The active network is {network.show_active()}")
        #print(f"Deploying Mocks...")
        #if len(MOckV3Aggregator) <= 0:
        #    #mock_aggregator = MockV3Aggregator.deploy(
        #    MockV3Aggregator.deploy(    
        #        #18, 2000000000000000000000, {"from":account}
        #        18, Web3.toWei(2000, "ether"), {"from":account}
        #    )
        #print("Mocks Deployed!")
        #price_feed_address = mock_aggregator.address
        #price_feed_address = MockV3Aggregator[-1].address
        #print("Mocks Deployed!")
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address


    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account}, 
        #publish_source=True,
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(f"Contract deployed to {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()