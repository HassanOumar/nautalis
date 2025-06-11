#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2025 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

from nautilus_trader.adapters.interactive_brokers.common import IB
from nautilus_trader.adapters.interactive_brokers.config import IBMarketDataTypeEnum
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersDataClientConfig
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersExecClientConfig
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersInstrumentProviderConfig
from nautilus_trader.adapters.interactive_brokers.config import SymbologyMethod
from nautilus_trader.adapters.interactive_brokers.factories import InteractiveBrokersLiveDataClientFactory
from nautilus_trader.adapters.interactive_brokers.factories import InteractiveBrokersLiveExecClientFactory
from nautilus_trader.config import LiveDataEngineConfig
from nautilus_trader.config import LoggingConfig
from nautilus_trader.config import RoutingConfig
from nautilus_trader.config import TradingNodeConfig
from nautilus_trader.live.node import TradingNode
from simple_es_strategy import SimpleESStrategy

# Configure the instrument provider
instrument_provider = InteractiveBrokersInstrumentProviderConfig(
    symbology_method=SymbologyMethod.IB_SIMPLIFIED,
    load_ids=frozenset(["ESU25.CME"]),  # ES September 2025 contract
)

# Configure the trading node
config_node = TradingNodeConfig(
    trader_id="TESTER-001",
    logging=LoggingConfig(log_level="INFO"),
    data_clients={
        IB: InteractiveBrokersDataClientConfig(
            ibg_host="127.0.0.1",
            ibg_port=7497,
            ibg_client_id=1,
            handle_revised_bars=False,
            use_regular_trading_hours=True,
            market_data_type=IBMarketDataTypeEnum.DELAYED_FROZEN,  # Using delayed data for testing
            instrument_provider=instrument_provider,
        ),
    },
    exec_clients={
        IB: InteractiveBrokersExecClientConfig(
            ibg_host="127.0.0.1",
            ibg_port=7497,
            ibg_client_id=1,
            account_id="DU7482745",  # This must match with the IB Gateway/TWS node is connecting to
            instrument_provider=instrument_provider,
            routing=RoutingConfig(
                default=True,
            ),
        ),
    },
    data_engine=LiveDataEngineConfig(
        time_bars_timestamp_on_close=False,  # Will use opening time as `ts_event` (same like IB)
        validate_data_sequence=True,  # Will make sure DataEngine discards any Bars received out of sequence
    ),
    timeout_connection=90.0,
    timeout_reconciliation=5.0,
    timeout_portfolio=5.0,
    timeout_disconnection=5.0,
    timeout_post_stop=2.0,
)

# Instantiate the node with a configuration
node = TradingNode(config=config_node)

# Instantiate our strategy
strategy = SimpleESStrategy()

# Add our strategy
node.trader.add_strategy(strategy)

# Register client factories with the node
node.add_data_client_factory(IB, InteractiveBrokersLiveDataClientFactory)
node.add_exec_client_factory(IB, InteractiveBrokersLiveExecClientFactory)
node.build()

# Stop and dispose of the node with SIGINT/CTRL+C
if __name__ == "__main__":
    try:
        node.run()
    finally:
        node.dispose() 