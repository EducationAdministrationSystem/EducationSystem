class A:
	def f(self):
		print 'Assss'
class B(A):
	def g(self):
		super.f()
a = A()
a.f()
b = B()
b.f()
