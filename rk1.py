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

    def __init__(self, grid_description, test_case, parent=None, is_left=None, is_leaf=False):
        self._parent = parent
        self._test_case = test_case
        self._is_leaf = is_leaf

        if parent is None:
            self._xmin = test_case._cxmin
            self._xmax = test_case._cxmax
            self._ymin = test_case._cymin
            self._ymax = test_case._cymax
            self._zmin = test_case._czmin
            self._zmax = test_case._czmax
            self._rmin = test_case._rmin
            self._rmax = test_case._rmax
        else:
            self._xmin = parent._xmin
            self._xmax = parent._xmax
            self._ymin = parent._ymin
            self._ymax = parent._ymax
            self._zmin = parent._zmin
            self._zmax = parent._zmax
            self._rmin = parent._rmin
            self._rmax = parent._rmax
            if is_left:
                if parent._d == 'cx':
                    self._xmax = parent._e
                elif parent._d == 'cy':
                    self._ymax = parent._e
                elif parent._d == 'cz':
                    self._zmax = parent._e
                elif parent._d == 'r':
                    self._rmax = parent._e
            else:
                if parent._d == 'cx':
                    self._xmin = parent._e
                elif parent._d == 'cy':
                    self._ymin = parent._e
                elif parent._d == 'cz':
                    self._zmin = parent._e
                elif parent._d == 'r':
                    self._rmin = parent._e

        if is_leaf:
            return
        
        slash = grid_description.find('/')
        self._d = grid_description[:slash]
        grid_description = grid_description[slash+1:-1]
        brace = grid_description.find('(')
        self._e = float(grid_description[:brace])

        grid_description = grid_description[brace+1:]
        sep_comma = Grid._find_sep_comma(grid_description)
        left_side = grid_description[:sep_comma]
        right_side = grid_description[sep_comma+1:]
        
        self._left_node = Grid(left_side, test_case, self, True, left_side == '#')
        self._right_node = Grid(right_side, test_case, self, False, right_side == '#')

    def _is_point_belongs(self, query):
        nearest_x = (self._xmin + self._xmax) / 2.0
        nearest_y = (self._ymin + self._ymax) / 2.0
        nearest_z = (self._zmin + self._zmax) / 2.0

        if query._px >= self._xmax:
            nearest_x = self._xmax
        if query._py >= self._ymax:
            nearest_y = self._ymax
        if query._pz >= self._zmax:
            nearest_z = self._zmax
        
        if query._px <= self._xmin:
            nearest_x = self._xmin
        if query._py <= self._ymin:
            nearest_y = self._ymin
        if query._pz <= self._zmin:
            nearest_z = self._zmin
        
        return True

    def find_subtree(self, query):
        if not self._is_point_belongs(query):
            return '*'
        else:
            if self._is_leaf:
                return '#'
            else:
                return '(%s,%s)' % (self._left_node.find_subtree(query), self._right_node.find_subtree(query))
    
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
