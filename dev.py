class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'

x = MyClass()
print(x.f())
x.i = 1
y = MyClass()
print(x.i, y.i)
