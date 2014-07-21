
#----------------------------------------------------------------------------------------------------------------------
def watch(arg, desc = 'var', offset = ''):

    argType = watchParseType(arg)

    if      argType == 'int':       watchVar(arg, desc, argType, offset)
    elif    argType == 'bool':      watchVar(arg, desc, argType, offset)
    elif    argType == 'float':     watchVar(arg, desc, argType, offset)
    elif    argType == 'str':       watchVar(arg, desc, argType, offset)
    elif    argType == 'unicode':   watchVar(arg, desc, argType, offset)
    elif    argType == 'NoneType':  watchVar(arg, desc, argType, offset)
    elif    argType == 'tuple':     watchArr(arg, desc, argType, offset)
    elif    argType == 'list':      watchArr(arg, desc, argType, offset)
    elif    argType == 'dict':      watchArr(arg, desc, argType, offset)
    elif    argType == 'set':       watchSet(arg, desc, argType, offset)
#    else:                           watchClass(arg, desc, argType, offset)
    else:                           watchVar(arg, desc, argType, offset)

#----------------------------------------------------------------------------------------------------------------------
def wtrace(arg):
    print('#trace: ' + str(arg))

#######################################################################################################################

#----------------------------------------------------------------------------------------------------------------------
def watchParseType(arg):
    argTypeParse = str(arg.__class__).split("'")
    if len(argTypeParse) == 1:
        return argTypeParse[0]
    else:
        return argTypeParse[1]

#----------------------------------------------------------------------------------------------------------------------
def watchStrQuot(string):
    if type(string) == str or type(string) == unicode:
        return '"'
    else:
        return ''

#----------------------------------------------------------------------------------------------------------------------
def watchVar(arg, desc, argType, offset = ''):
    print('#watch: ' + offset + desc + '(' + argType + ') = ' + watchStrQuot(arg) + str(arg) + watchStrQuot(arg))

#----------------------------------------------------------------------------------------------------------------------
def watchArr(arg, desc, argType, offset = ''):
    titleString = '#watch: ' + offset + '----- ' + desc + '(' + argType + ') -----'
    print(titleString)
    if argType == 'dict':
        keys = sorted(arg.keys())
    else:
        keys = range(len(arg))
    for i in keys:
        print('#watch: ' + offset + desc + '[' + watchStrQuot(i) + str(i) + watchStrQuot(i) + '] = ' + watchStrQuot(arg[i]) + str(arg[i]) + watchStrQuot(arg[i]))
    print('#watch: ' + offset + ''.join(['-' for i in range(len(titleString) - 8)]))

#----------------------------------------------------------------------------------------------------------------------
def watchSet(arg, desc, argType, offset = ''):
    titleString = '#watch: ' + offset + '----- ' + desc + '(' + argType + ') -----'
    print(titleString)
    i = 0
    for value in sorted(arg):
        print('#watch: ' + offset + desc + '[' + watchStrQuot(i) + str(i) + watchStrQuot(i) + '] = ' + watchStrQuot(value) + str(value) + watchStrQuot(value))
        i += 1
    print('#watch: ' + offset + ''.join(['-' for i in range(len(titleString) - 8)]))

#----------------------------------------------------------------------------------------------------------------------
def watchClass(arg, desc, argType, offset = ''):
    print('#watch: ' + offset + '-------- ' + desc + '(' + argType + ') ---------')
    offset += '|  '
    for i in sorted(arg.__dict__.keys()):
        watch(arg.__dict__[i], i, offset)
    offset = offset[:-3]
    print('#watch: ' + offset + '----- end of ' + desc + '(' + argType + ') -----')


#######################################################################################################################

##### test stuff #####

#class MyClass3():
#    def __init__(self):
#        self.first3 = 3
#        self.second3 = 'second3'
#        self.third3 = (3, 30, 300)
#
#class MyClass2():
#    def __init__(self):
#        self.first2 = 2
#        self.second2 = 'second2'
#        self.third2 = (2, 20, 200)
#        self.classProperty2 = MyClass3()
#
#class MyClass():
#    def __init__(self):
#        self.first = 1
#        self.second = 'second'
#        self.third = (1, 10, 100)
#        self.gclassProperty = MyClass2()
#
#varInteger = 10
#varFloat = 567.872
#varString = 'simple string'
#
#varTupleString = ('aaa', 'bbb', 'ccc')
#varTupleString0 = ()
#varTupleString1 = ('aaa', 10, 'ccc')
#varTupleInteger = (10, 555, 99)
#varTupleFloat = (10.736, 555.836, 99.928)
#
#varListString = ['aaa', 'bbb', 'ccc']
#varListInteger = [10, 555, 99]
#varListFloat = [10.736, 555.836, 99.928]
#
#varDictString = {'mercury' : 'first', 'venus' : 'second', 'earth' : 'third', 'mars' : 'fourth'}
#varDictInteger = {'mercury' : 1, 'venus' : 2, 'earth' : 3, 'mars' : 4}
#varDictFloat = {'mercury' : 1.111, 'venus' : 2.222, 'earth' : 3.333, 'mars' : 4.444}
#varDict1 = {100 : 1.111, 'venus' : "2.222", 300 : "3.333", 'mars' : 4.444}
#
#varMyClass = MyClass()
#
#watch(varString, 'varString')
#watch(varInteger)
#watch(varFloat)
#
#watch(varTupleString, 'varTupleString')
#watch(varTupleString0, 'varTupleString0')
#watch(varTupleString1)
#watch(varTupleInteger)
#watch(varTupleFloat)
#
#watch(varListString)
#watch(varListInteger)
#watch(varListFloat)
#
#watch(varDictString)
#watch(varDictInteger)
#watch(varDictFloat)
#watch(varDict1)
#
#watch(varMyClass)