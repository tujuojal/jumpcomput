
from dolfin import *

#parameters["form_compiler"]["cpp_optimize"] = True
#parameters["form_compiler"]["optimize"] = True

mesh = Mesh("dolfin-2.xml")
n = FacetNormal(mesh)

V = VectorFunctionSpace(mesh,'CG',2)
Q = FunctionSpace(mesh,'CG',1)
W = V * Q

#Define function and testfunction
w = Function(W)
(u , p) = split(w)
(v, q) = TestFunctions(W)

#define viscosity and bc
nu1 = Constant(0.2) #Expression("0.2+(1+pow(x[1],2))", degree=2)
p0 = Expression("1.0-x[0]", degree=1)
def viscosity(u):
    return 0.5*inner(u,u)**(1./6.)



W0 = W.sub(0) #subspace of the functionspace
#sub(0) is the V that is the velocity not the pressure
g = (0.0,0.0)
def u0_boundary(x, on_boundary):
    return on_boundary
bc = DirichletBC(W.sub(0), g, "on_boundary && !(near(x[0],0.0) || near(x[0],1.0))")

#Define variational form
epsilon = sym(grad(u))
F = (nu1*inner(epsilon, grad(v)) \
        - div(u)*q - div(v)*p)*dx \
        + p0*dot(v, n)*ds

solve(F == 0, w ,bc)

(u,p) = split(w)
nu = viscosity(u)

F = (nu*inner(epsilon, grad(v)) \
        - div(u)*q - div(v)*p)*dx \
        + p0*dot(v, n)*ds
solve(F == 0, w ,bc)
(u,p) = split(w)


plot(u, title="Velocity", interactive=True)
plot(p, title="Pressure", interactive=True)
"""
dF = derivative(F,w)
pde = NonlinearVariationalProblem(F, w, bc, dF)
solver = NonlinearVariationalSolver(pde)
solver.solve()

getting the subfunction

"""
