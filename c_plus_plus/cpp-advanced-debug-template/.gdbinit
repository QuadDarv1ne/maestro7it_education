set history save on
set history filename ~/.gdb_history
set print array on
set print array-indexes on
set print repeats 0
set print null-stop

define asm
    layout asm
    focus cmd
end

define src
    layout src
    focus cmd
end

# Улучшенный вывод STL контейнеров
python
import gdb
import re

class StdVectorPrinter:
    "Print std::vector"
    def __init__(self, val):
        self.val = val
        self.typename = val.type.strip_typedefs().name
        if not self.typename or self.typename.startswith('std::vector<'):
            self.typename = 'std::vector'
        self.size = val['_M_impl']['_M_finish'] - val['_M_impl']['_M_start']
        self.capacity = val['_M_impl']['_M_end_of_storage'] - val['_M_impl']['_M_start']
        
    def to_string(self):
        return f"{self.typename} of length {self.size}, capacity {self.capacity}"
        
    def children(self):
        start = self.val['_M_impl']['_M_start']
        for i in range(self.size):
            yield (f"[{i}]", (start + i).dereference())
            
gdb.pretty_printers.append(lambda val: StdVectorPrinter(val) if re.search('std::vector<.*>', str(val.type)) else None)
end
