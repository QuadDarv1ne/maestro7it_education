"""
Connection pooling utility for the chess application.
Implements connection pooling strategies for better resource management.
"""

import threading
import time
import logging
from collections import deque
from contextlib import contextmanager
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

class ConnectionPool:
    """
    Generic connection pool implementation for managing reusable resources.
    """
    
    def __init__(self, factory: Callable, max_size: int = 10, idle_timeout: int = 300):
        """
        Initialize connection pool.
        
        Args:
            factory: Function to create new connections
            max_size: Maximum number of connections in pool
            idle_timeout: Time in seconds before idle connections are closed
        """
        self.factory = factory
        self.max_size = max_size
        self.idle_timeout = idle_timeout
        self.pool = deque()
        self.lock = threading.RLock()
        self.active_connections = 0
        self.total_created = 0
        self.total_reused = 0
        
    def _create_connection(self) -> Any:
        """
        Create a new connection.
        
        Returns:
            New connection object
        """
        try:
            connection = self.factory()
            self.total_created += 1
            logger.debug(f"Created new connection. Total created: {self.total_created}")
            return connection
        except Exception as e:
            logger.error(f"Failed to create connection: {e}")
            raise
    
    def get_connection(self, timeout: float = 30.0) -> Any:
        """
        Get a connection from the pool.
        
        Args:
            timeout: Maximum time to wait for a connection
            
        Returns:
            Connection object
        """
        start_time = time.time()
        
        with self.lock:
            # Try to get an existing connection
            while self.pool:
                connection, last_used = self.pool.popleft()
                # Check if connection is still valid and not timed out
                if time.time() - last_used < self.idle_timeout:
                    self.active_connections += 1
                    self.total_reused += 1
                    logger.debug(f"Reused existing connection. Total reused: {self.total_reused}")
                    return connection
                else:
                    # Connection timed out, don't use it
                    try:
                        self._close_connection(connection)
                    except:
                        pass
            
            # No valid connections available, create new one if under limit
            if self.active_connections < self.max_size:
                connection = self._create_connection()
                self.active_connections += 1
                return connection
            else:
                # Pool is at maximum capacity
                logger.warning("Connection pool at maximum capacity")
        
        # Wait for a connection to become available
        while time.time() - start_time < timeout:
            time.sleep(0.1)
            with self.lock:
                if self.pool:
                    connection, last_used = self.pool.popleft()
                    if time.time() - last_used < self.idle_timeout:
                        self.active_connections += 1
                        self.total_reused += 1
                        logger.debug(f"Reused existing connection. Total reused: {self.total_reused}")
                        return connection
        
        raise TimeoutError("Timeout waiting for connection from pool")
    
    def return_connection(self, connection: Any) -> None:
        """
        Return a connection to the pool.
        
        Args:
            connection: Connection to return
        """
        with self.lock:
            self.active_connections -= 1
            if self.active_connections < 0:
                self.active_connections = 0
            
            # Add connection back to pool if pool isn't full
            if len(self.pool) < self.max_size - self.active_connections:
                self.pool.append((connection, time.time()))
                logger.debug("Returned connection to pool")
            else:
                # Pool is full, close the connection
                try:
                    self._close_connection(connection)
                    logger.debug("Closed connection (pool full)")
                except Exception as e:
                    logger.error(f"Error closing connection: {e}")
    
    def _close_connection(self, connection: Any) -> None:
        """
        Close a connection.
        
        Args:
            connection: Connection to close
        """
        try:
            if hasattr(connection, 'close'):
                connection.close()
            elif hasattr(connection, 'quit'):
                connection.quit()
            elif hasattr(connection, '__del__'):
                connection.__del__()
        except Exception as e:
            logger.warning(f"Error closing connection: {e}")
    
    def close_all(self) -> None:
        """Close all connections in the pool."""
        with self.lock:
            # Close all idle connections
            while self.pool:
                connection, _ = self.pool.popleft()
                try:
                    self._close_connection(connection)
                except Exception as e:
                    logger.error(f"Error closing connection: {e}")
            
            # Reset counters
            self.active_connections = 0
            logger.info("Closed all connections in pool")
    
    def get_stats(self) -> dict:
        """
        Get pool statistics.
        
        Returns:
            Dictionary with pool statistics
        """
        with self.lock:
            return {
                'pool_size': len(self.pool),
                'active_connections': self.active_connections,
                'max_size': self.max_size,
                'total_created': self.total_created,
                'total_reused': self.total_reused,
                'utilization_rate': (
                    (self.total_created + self.total_reused) / max(self.total_created, 1)
                    if self.total_created > 0 else 0
                )
            }

class StockfishEnginePool:
    """
    Specialized connection pool for Stockfish engines.
    """
    
    def __init__(self, max_engines: int = 5, idle_timeout: int = 600):
        """
        Initialize Stockfish engine pool.
        
        Args:
            max_engines: Maximum number of engines in pool
            idle_timeout: Time in seconds before idle engines are closed
        """
        self.max_engines = max_engines
        self.idle_timeout = idle_timeout
        self.pool = deque()
        self.lock = threading.RLock()
        self.active_engines = 0
        self.total_created = 0
        self.total_reused = 0
        self.skill_level_configs = {}  # Track skill level for each engine
        
    def _create_engine(self, skill_level: int = 5) -> Any:
        """
        Create a new Stockfish engine.
        
        Args:
            skill_level: Skill level for the engine
            
        Returns:
            Stockfish engine instance
        """
        try:
            from stockfish import Stockfish
            import os
            
            # Find Stockfish executable
            stockfish_path = self._find_stockfish_executable()
            if not stockfish_path:
                raise RuntimeError("Stockfish executable not found")
            
            # Create engine
            engine = Stockfish(path=stockfish_path)
            
            # Configure engine
            engine.set_skill_level(skill_level)
            engine.set_depth(10)
            engine.update_engine_parameters({
                'Threads': 2,
                'Hash': 128,
                'Contempt': 0,
                'Ponder': False
            })
            
            self.total_created += 1
            logger.info(f"Created new Stockfish engine with skill level {skill_level}. Total created: {self.total_created}")
            return engine
        except Exception as e:
            logger.error(f"Failed to create Stockfish engine: {e}")
            raise
    
    def _find_stockfish_executable(self) -> Optional[str]:
        """
        Find Stockfish executable in various possible locations.
        
        Returns:
            Path to Stockfish executable or None if not found
        """
        import os
        import shutil
        
        # Common executable names
        executable_names = [
            'stockfish.exe',    # Windows
            'stockfish',        # Linux/Mac
            'stockfish_15_x64.exe',
            'stockfish_14_x64.exe',
            'stockfish-windows-x86-64.exe',
            'stockfish-linux-x64',
            'stockfish-mac-x64'
        ]
        
        # Common search paths
        search_paths = [
            os.path.dirname(__file__),
            os.path.join(os.path.dirname(__file__), '..'),
            os.path.join(os.path.dirname(__file__), 'engines'),
            os.path.expanduser('~'),
            os.path.expanduser('~/stockfish'),
            '/usr/local/bin',
            '/usr/bin',
            'C:\\Program Files\\Stockfish',
            'C:\\Program Files (x86)\\Stockfish'
        ]
        
        # Check environment variable
        env_path = os.getenv('STOCKFISH_PATH')
        if env_path:
            search_paths.insert(0, env_path)
        
        # Try to find executable
        for search_path in search_paths:
            if search_path and os.path.exists(search_path):
                # Check direct path first
                if os.path.isfile(search_path) and any(search_path.endswith(ext) for ext in ['.exe', '']):
                    return search_path
                
                # Check in directory
                for exe_name in executable_names:
                    full_path = os.path.join(search_path, exe_name)
                    if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                        return full_path
        
        # Check system PATH
        for exe_name in executable_names:
            try:
                path = shutil.which(exe_name)
                if path:
                    return path
            except:
                pass
        
        return None
    
    def get_engine(self, skill_level: int = 5, timeout: float = 30.0) -> Any:
        """
        Get a Stockfish engine from the pool.
        
        Args:
            skill_level: Desired skill level
            timeout: Maximum time to wait for an engine
            
        Returns:
            Stockfish engine instance
        """
        start_time = time.time()
        
        with self.lock:
            # Try to get an existing engine with matching skill level
            temp_pool = []
            while self.pool:
                engine_info = self.pool.popleft()
                engine, last_used, engine_skill_level = engine_info
                
                # Check if engine is still valid and not timed out
                if time.time() - last_used < self.idle_timeout:
                    # If skill level matches or we can reconfigure, use it
                    if engine_skill_level == skill_level:
                        self.active_engines += 1
                        self.total_reused += 1
                        logger.debug(f"Reused existing Stockfish engine. Total reused: {self.total_reused}")
                        return engine
                    else:
                        # Try to reconfigure engine skill level
                        try:
                            engine.set_skill_level(skill_level)
                            self.skill_level_configs[id(engine)] = skill_level
                            self.active_engines += 1
                            self.total_reused += 1
                            logger.debug(f"Reused and reconfigured Stockfish engine. Total reused: {self.total_reused}")
                            return engine
                        except:
                            # If reconfiguration fails, keep engine for later
                            temp_pool.append((engine, last_used, engine_skill_level))
                else:
                    # Engine timed out, close it
                    try:
                        engine.quit()
                    except:
                        pass
            
            # Put back unused engines
            self.pool.extend(temp_pool)
            
            # No valid engines available, create new one if under limit
            if self.active_engines < self.max_engines:
                engine = self._create_engine(skill_level)
                self.skill_level_configs[id(engine)] = skill_level
                self.active_engines += 1
                return engine
            else:
                # Pool is at maximum capacity
                logger.warning("Stockfish engine pool at maximum capacity")
        
        # Wait for an engine to become available
        while time.time() - start_time < timeout:
            time.sleep(0.1)
            with self.lock:
                if self.pool:
                    engine, last_used, engine_skill_level = self.pool.popleft()
                    if time.time() - last_used < self.idle_timeout:
                        # Try to reconfigure if needed
                        if engine_skill_level != skill_level:
                            try:
                                engine.set_skill_level(skill_level)
                                self.skill_level_configs[id(engine)] = skill_level
                            except:
                                # If reconfiguration fails, put engine back
                                self.pool.append((engine, last_used, engine_skill_level))
                                continue
                        
                        self.active_engines += 1
                        self.total_reused += 1
                        logger.debug(f"Reused existing Stockfish engine. Total reused: {self.total_reused}")
                        return engine
                    else:
                        # Engine timed out, close it
                        try:
                            engine.quit()
                        except:
                            pass
        
        raise TimeoutError("Timeout waiting for Stockfish engine from pool")
    
    def return_engine(self, engine: Any) -> None:
        """
        Return a Stockfish engine to the pool.
        
        Args:
            engine: Engine to return
        """
        with self.lock:
            self.active_engines -= 1
            if self.active_engines < 0:
                self.active_engines = 0
            
            # Get current skill level
            skill_level = self.skill_level_configs.get(id(engine), 5)
            
            # Add engine back to pool if pool isn't full
            if len(self.pool) < self.max_engines - self.active_engines:
                self.pool.append((engine, time.time(), skill_level))
                logger.debug("Returned Stockfish engine to pool")
            else:
                # Pool is full, close the engine
                try:
                    engine.quit()
                    logger.debug("Closed Stockfish engine (pool full)")
                except Exception as e:
                    logger.error(f"Error closing Stockfish engine: {e}")
                
                # Remove from skill level tracking
                if id(engine) in self.skill_level_configs:
                    del self.skill_level_configs[id(engine)]
    
    def close_all(self) -> None:
        """Close all engines in the pool."""
        with self.lock:
            # Close all idle engines
            while self.pool:
                engine, _, _ = self.pool.popleft()
                try:
                    engine.quit()
                except Exception as e:
                    logger.error(f"Error closing Stockfish engine: {e}")
            
            # Clear skill level tracking
            self.skill_level_configs.clear()
            
            # Reset counters
            self.active_engines = 0
            logger.info("Closed all Stockfish engines in pool")
    
    def get_stats(self) -> dict:
        """
        Get pool statistics.
        
        Returns:
            Dictionary with pool statistics
        """
        with self.lock:
            return {
                'pool_size': len(self.pool),
                'active_engines': self.active_engines,
                'max_engines': self.max_engines,
                'total_created': self.total_created,
                'total_reused': self.total_reused,
                'utilization_rate': (
                    (self.total_created + self.total_reused) / max(self.total_created, 1)
                    if self.total_created > 0 else 0
                )
            }

# Global connection pool instances
stockfish_pool = StockfishEnginePool(max_engines=5, idle_timeout=600)

@contextmanager
def get_stockfish_engine(skill_level: int = 5):
    """
    Context manager for getting a Stockfish engine from the pool.
    
    Args:
        skill_level: Desired skill level for the engine
    """
    engine = None
    try:
        engine = stockfish_pool.get_engine(skill_level)
        yield engine
    finally:
        if engine:
            stockfish_pool.return_engine(engine)