from nautilus_trader.model.data import BarType
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.model.identifiers import StrategyId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.objects import Quantity
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import BarSpecification
from datetime import datetime

class SimpleESStrategy(Strategy):
    """
    A simple strategy that enters every 10th candle and exits on the 3rd candle after entry.
    """
    
    def __init__(self):
        config = StrategyConfig(
            strategy_id="SIMPLE-ES-001",
        )
        super().__init__(config=config)
        
        # Strategy parameters
        self.entry_count = 0
        self.position_count = 0
        self.in_position = False
        
        # ES Futures configuration
        self.instrument_id = InstrumentId(
            symbol=Symbol("ESU25"),  # September 2025 contract
            venue=Venue("CME"),
        )
        self.bar_type = BarType(
            instrument_id=self.instrument_id,
            bar_spec=BarSpecification(
                step=1,
                aggregation=BarAggregation.MINUTE,
                price_type=PriceType.LAST,
            ),
        )
        
        # Initialize order log file
        self.order_log = open(f'orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w')
        self.order_log.write("Timestamp,Action,Price,Quantity\n")
        
    def on_start(self):
        """Actions to be performed on strategy start."""
        self.subscribe_bars(self.bar_type)
        
    def on_bar(self, bar):
        """Actions to be performed when the strategy receives a bar."""
        self.entry_count += 1
        
        # Check for entry condition (every 10th candle)
        if not self.in_position and self.entry_count % 10 == 0:
            self.enter_long(bar)
            self.in_position = True
            self.position_count = 0
            
        # Check for exit condition (3rd candle after entry)
        elif self.in_position:
            self.position_count += 1
            if self.position_count >= 3:
                self.exit_position(bar)
                self.in_position = False
                
    def enter_long(self, bar):
        """Enter a long position."""
        order = self.order_factory.market(
            instrument_id=self.instrument_id,
            order_side=OrderSide.BUY,
            quantity=Quantity.from_int(1),
        )
        self.submit_order(order)
        self.order_log.write(f"{bar.ts_event},BUY,{bar.close.as_double()},1\n")
        self.order_log.flush()
        
    def exit_position(self, bar):
        """Exit the current position."""
        order = self.order_factory.market(
            instrument_id=self.instrument_id,
            order_side=OrderSide.SELL,
            quantity=1,
        )
        self.submit_order(order)
        self.order_log.write(f"{bar.ts_event},SELL,{bar.close.as_double()},1\n")
        self.order_log.flush()
        
    def on_stop(self):
        """Actions to be performed when the strategy stops."""
        self.order_log.close() 