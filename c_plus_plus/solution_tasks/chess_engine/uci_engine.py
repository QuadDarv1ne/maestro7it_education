#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from core.uci_protocol import UCIProtocolHandler
from core.chess_engine_wrapper import ChessEngineWrapper

if __name__ == "__main__":
    try:
        engine = ChessEngineWrapper()
        uci_handler = UCIProtocolHandler(engine)
        uci_handler.run()
    except KeyboardInterrupt:
        print("info string Engine terminated by user")
    except Exception as e:
        print(f"info string Fatal error: {e}")
