class InputOverException(Exception):
    pass

class Grid(object):
    @staticmethod
    def _find_sep_comma(grid_description):
        counter = 0
        for i in range(0, len(grid_description)):
            if grid_description[i] == '(':
                counter = counter + 1
            if grid_description[i] == ')':
                counter = counter - 1
            if (grid_description[i] == ',') and (counter == 0):
                return i

    def __init__(self, grid_description, test_case, parent=None):
        self._parent = parent
        self._test_case = test_case
        slash = grid_description.find('/')
        self._d = grid_description[:slash]
        grid_description = grid_description[slash+1:-1]
        brace = grid_description.find('(')
        self._e = float(grid_description[:brace])
        grid_description = grid_description[brace+1:]
        sep_comma = Grid._find_sep_comma(grid_description)
        left_side = grid_description[:sep_comma]
        right_side = grid_description[sep_comma+1:]
        if left_side == '#':
            self._left_node = None
        else:
            self._left_node = Grid(left_side, test_case, self)
        if right_side == '#':
            self._right_node = None
        else:
            self._right_node = Grid(right_side, test_case, self)

    def _common_find_x(self, query):
        left_ok = self._e >= query._px
        right_ok = self._e <= query._px
        return (left_ok, right_ok)

    def _common_find_y(self, query):
        left_ok = self._e <= query._py
        right_ok = self._e > query._py
        return (left_ok, right_ok)

    def _common_find_z(self, query):
        left_ok = self._e <= query._pz
        right_ok = self._e > query._pz
        return (left_ok, right_ok)

    def _common_find(self, query):
        left_ok = False
        right_ok = False
        if self._d == 'cx':
            (left_ok, right_ok) = self._common_find_x(query)
        if self._d == 'cy':
            (left_ok, right_ok) = self._common_find_y(query)
        if self._d == 'cz':
            (left_ok, right_ok) = self._common_find_z(query)
        print('left_ok=%s, right_ok=%s query=%s coord=%s value=%s'%(left_ok, right_ok, query, self._d, self._e))
        
        if not (left_ok or right_ok):
            return '*'

        left_symbol = None
        if left_ok:
            if self._left_node is None:
                left_symbol = '#'
            else:
                left_symbol = self._left_node._common_find(query)
        else:
            left_symbol = '*'
        
        right_symbol = None
        if right_ok:
            if self._right_node is None:
                right_symbol = '#'
            else:
                right_symbol = self._right_node._common_find(query)
        else:
            right_symbol = '*'

        return '(%s,%s)' % (left_symbol, right_symbol)


    def find_subtree(self, query):
        if query._px < self._test_case._cxmin:
            return '*'
        elif query._px > self._test_case._cxmax:
            return '*'
        elif query._py < self._test_case._cymin:
            return '*'
        elif query._py > self._test_case._cymax:
            return '*'
        elif query._pz < self._test_case._czmin:
            return '*'
        elif query._pz > self._test_case._czmax:
            return '*'
        else:
            return self._common_find(query)

    
    def __str__(self):
        return "{%s/%s(%s,%s)}" % (self._d, self._e, '#' if self._left_node is None else self._left_node, '#' if self._right_node is None else self._right_node)

    def __repr__(self):
        return self.__str__()

class Query(object):
    def __init__(self, query):
        query = query.split(' ')
        self._px = float(query[0])
        self._py = float(query[1])
        self._pz = float(query[2])
        self._r = float(query[3])

    def __str__(self):
        return 'query:(%s %s %s %s)' % (self._px, self._py, self._pz, self._r)


    def __repr__(self):
        return self.__str__()


class TestCase(object):
    def _setup_constraining(self, line):
        parts = line.split(' ')
        self._cxmin = float(parts[0])
        self._cxmax = float(parts[1])
        self._cymin = float(parts[2])
        self._cymax = float(parts[3])
        self._czmin = float(parts[4])
        self._czmax = float(parts[5])
        self._rmin = float(parts[6])
        self._rmax = float(parts[7])

    def __init__(self, file_obj):
        text = []
        while 1:
            line = file_obj.readline()
            if line == '':
                raise InputOverException()
            line = line.strip(' \n\t')
            if line == '*':
                break
            text.append(line)
        self._name = text[0]
        text = text[1:]
        region = text[0]
        self._setup_constraining(region)
        text = text[1:]
        grid_description = []
        for line in text:
            grid_description.append(line)
            if (line[-1] != '(') and (line[-1] != ','):
                break
        text = text[len(grid_description):]
        grid_description = ''.join(grid_description)
        self._grid = Grid(grid_description, self)
        self._queries = [Query(i) for i in text]

    def execute(self):
        print(self._name)
        for query in self._queries:
            print(query)
            print(self._grid.find_subtree(query))


file_obj = open('input.txt', 'r')
test_cases = []

while 1:
    try:
        test_case = TestCase(file_obj)
    except InputOverException:
        break
    except Exception as e:
        raise e
    test_cases.append(test_case)

file_obj.close()
for case in test_cases:
    case.execute()
