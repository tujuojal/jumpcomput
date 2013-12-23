
from dolfin import *

dt = 0.1 # time step
alpha = 1 #constant
beta = .2 #constant
#exact test function
g = Expression("1 + x[0]*x[0] + \
    alpha*x[1]*x[1] + beta*t ", \
    alpha = alpha, beta = beta, t= 0)

#right hand side constant function
f = Constant(beta - 2 - 2*alpha)


mesh = UnitSquareMesh(4,4)
V = FunctionSpace(mesh,'Lagrange',2)
u = TrialFunction(V)
v = TestFunction(V)
#initial values for the timestepping
u0 = project(g,V)
u1 = Function(V)
#updating
#g.t = t
#boundary condition
bc = DirichletBC(V, g, "on_boundary")
#the variational formulation
a = u*v*dx + dt*inner(grad(u), grad(v))*dx
L = u0*v*dx + dt*f*v*dx


#first assembly before timestepping
A = assemble(a)

T = 1.8
t = dt

while t <= T:
    b = assemble(L)
    g.t = t
    bc.apply(A,b)
    solve(A,u1.vector(),b)

    t += dt
    u0.assign(u1)
    plot(u0)

plot(u0)
interactive()

g.t=T-dt
exact = project(g, V)
plot(exact)
interactive()

error = exact - u0
plot(error)
interactive()
err= errornorm(exact,u0,norm_type='l2',degree_rise=2,mesh=None)
print err 
