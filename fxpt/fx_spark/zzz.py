# all runtime commands
for c in sorted(m.runTimeCommand(q=True, commandArray=True)):
    print c, m.runTimeCommand(c, q=True, annotation=True)
# also see -category(-cat)


# maya commands
import inspect
import types
def isBuiltin(x):
    return type(x) == types.BuiltinFunctionType
watch(sorted([e for e in inspect.getmembers(m, isBuiltin) if True]))
print type(m.nurbsSquare)
print type(len)