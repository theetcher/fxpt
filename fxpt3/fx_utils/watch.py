# ----------------------------------------------------------------------------------------------------------------------
def watch(arg, desc='var', offset=''):

    argType = watchParseType(arg)

    if argType == 'int':
        watchVar(arg, desc, argType, offset)
    elif argType == 'bool':
        watchVar(arg, desc, argType, offset)
    elif argType == 'float':
        watchVar(arg, desc, argType, offset)
    elif argType == 'str':
        watchVar(arg, desc, argType, offset)
    elif argType == 'NoneType':
        watchVar(arg, desc, argType, offset)
    elif argType == 'tuple':
        watchArr(arg, desc, argType, offset)
    elif argType == 'list':
        watchArr(arg, desc, argType, offset)
    elif argType == 'dict':
        watchArr(arg, desc, argType, offset)
    elif argType == 'set':
        watchSet(arg, desc, argType, offset)
    # else:
    #     watchClass(arg, desc, argType, offset)
    else:
        watchVar(arg, desc, argType, offset)


# ----------------------------------------------------------------------------------------------------------------------
def wtrace(arg):
    print('#trace: ' + str(arg))


# ----------------------------------------------------------------------------------------------------------------------
def watchParseType(arg):
    argTypeParse = str(arg.__class__).split("'")
    if len(argTypeParse) == 1:
        return argTypeParse[0]
    else:
        return argTypeParse[1]


# ----------------------------------------------------------------------------------------------------------------------
def watchStrQuot(string):
    if isinstance(string, str):
        return '"'
    else:
        return ''


# ----------------------------------------------------------------------------------------------------------------------
def watchSorted(items):
    # py3 can't compare mixed types (e.g. int and str dict keys), fall back to sorting by string
    try:
        return sorted(items)
    except TypeError:
        return sorted(items, key=str)


# ----------------------------------------------------------------------------------------------------------------------
def watchVar(arg, desc, argType, offset=''):
    print('#watch: ' + offset + desc + '(' + argType + ') = ' + watchStrQuot(arg) + str(arg) + watchStrQuot(arg))


# ----------------------------------------------------------------------------------------------------------------------
def watchArr(arg, desc, argType, offset=''):
    titleString = '#watch: ' + offset + '----- ' + desc + '(' + argType + ') -----'
    print(titleString)
    if argType == 'dict':
        keys = watchSorted(arg.keys())
    else:
        keys = range(len(arg))
    for i in keys:
        print(
            '#watch: '
            + offset
            + desc
            + '['
            + watchStrQuot(i)
            + str(i)
            + watchStrQuot(i)
            + '] = '
            + watchStrQuot(arg[i])
            + str(arg[i])
            + watchStrQuot(arg[i])
        )
    print('#watch: ' + offset + ''.join(['-' for i in range(len(titleString) - 8)]))


# ----------------------------------------------------------------------------------------------------------------------
def watchSet(arg, desc, argType, offset=''):
    titleString = '#watch: ' + offset + '----- ' + desc + '(' + argType + ') -----'
    print(titleString)
    i = 0
    for value in watchSorted(arg):
        print(
            '#watch: '
            + offset
            + desc
            + '['
            + watchStrQuot(i)
            + str(i)
            + watchStrQuot(i)
            + '] = '
            + watchStrQuot(value)
            + str(value)
            + watchStrQuot(value)
        )
        i += 1
    print('#watch: ' + offset + ''.join(['-' for i in range(len(titleString) - 8)]))


# ----------------------------------------------------------------------------------------------------------------------
def watchClass(arg, desc, argType, offset=''):
    print('#watch: ' + offset + '-------- ' + desc + '(' + argType + ') ---------')
    offset += '|  '
    for i in sorted(arg.__dict__.keys()):
        watch(arg.__dict__[i], i, offset)
    offset = offset[:-3]
    print('#watch: ' + offset + '----- end of ' + desc + '(' + argType + ') -----')


# ----------------------------------------------------------------------------------------------------------------------
def watchTest():
    """Print a sample of every supported type. Run: from fxpt3.fx_utils import watch; watch.watchTest()"""

    class MyClass3:
        def __init__(self):
            self.first3 = 3
            self.second3 = 'second3'
            self.third3 = (3, 30, 300)

    class MyClass2:
        def __init__(self):
            self.first2 = 2
            self.second2 = 'second2'
            self.third2 = (2, 20, 200)
            self.classProperty2 = MyClass3()

    class MyClass:
        def __init__(self):
            self.first = 1
            self.second = 'second'
            self.third = (1, 10, 100)
            self.classProperty = MyClass2()

    samples = [
        ('varString', 'simple string'),
        ('varInteger', 10),
        ('varFloat', 567.872),
        ('varBool', True),
        ('varNone', None),
        ('varTupleString', ('aaa', 'bbb', 'ccc')),
        ('varTupleEmpty', ()),
        ('varTupleMixed', ('aaa', 10, 'ccc')),
        ('varTupleInteger', (10, 555, 99)),
        ('varTupleFloat', (10.736, 555.836, 99.928)),
        ('varListString', ['aaa', 'bbb', 'ccc']),
        ('varListInteger', [10, 555, 99]),
        ('varListFloat', [10.736, 555.836, 99.928]),
        ('varDictString', {'mercury': 'first', 'venus': 'second', 'earth': 'third', 'mars': 'fourth'}),
        ('varDictInteger', {'mercury': 1, 'venus': 2, 'earth': 3, 'mars': 4}),
        ('varDictFloat', {'mercury': 1.111, 'venus': 2.222, 'earth': 3.333, 'mars': 4.444}),
        ('varDictMixedKeys', {100: 1.111, 'venus': '2.222', 300: '3.333', 'mars': 4.444}),
        ('varSet', {3, 1, 2}),
        ('varSetMixed', {3, 'a', 1}),
        ('varMyClass', MyClass()),
    ]

    for desc, value in samples:
        watch(value, desc)

    # objects print as a single line through watch(); watchClass() expands their attributes recursively
    watchClass(MyClass(), 'varMyClass', 'MyClass')

    wtrace('watchTest finished')


if __name__ == '__main__':
    watchTest()
