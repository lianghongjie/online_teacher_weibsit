class A(object):
    def test(self, t):
        print 123, t
        print super(A, self).__init__()


class B(A):
    def d(self):
        print 242

B().test("rrrr")
