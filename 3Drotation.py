import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.text import Annotation

class Annotation3D(Annotation):
    '''Annotate the point xyz with text s'''

    def __init__(self, s, xyz, *args, **kwargs):
        Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
        self._verts3d = xyz        

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.xy=(xs,ys)
        Annotation.draw(self, renderer)

def annotate3D(ax, s, *args, **kwargs):
    '''add anotation text s to to Axes3d ax'''

    tag = Annotation3D(s, *args, **kwargs)
    ax.add_artist(tag)


Q = np.random.random((3,3)) 
E = np.eye(3)

print(Q)

u = Q[:,0]
v = Q[:,1]
w = Q[:,2]

#Gram–Schmidt process
u /= np.linalg.norm(u)

v -= v.dot(u)*u
v /= np.linalg.norm(v)

w -= w.dot(u)*u + w.dot(v)*v
w /= np.linalg.norm(w)

print(Q, u, v, w)

U = u.copy().reshape(3,1)
V = v.copy().reshape(3,1)
W = w.copy().reshape(3,1)

print(U@U.T + V@V.T + W@W.T)




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def GreatArc(u, v):
    """arc of a great circle containing x1 != x2 and the origin."""

    u=u.reshape(3,1)
    v=v.reshape(3,1)
    w = v - v.T@u*u
    w = w/np.sqrt( w.T@w )
    al = np.arccos( (u.T@v) /np.sqrt( (u.T@u)*(v.T@v) ) )
       
    N  = 10
    t  = np.linspace(0.0,float(al), N)
    t  = t.reshape(1,N)

    return u@np.cos(t) + w@np.sin(t)
    

#theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
#z = np.linspace(-2, 2, 100)
#r = z**2 + 1
#x = r * np.sin(theta)
#y = r * np.cos(theta)
#ax.plot(x, y, z, label='parametric curve')
#ax.legend()

EU = GreatArc(E[0,:],U)
EV = GreatArc(E[1,:],V)
EW = GreatArc(E[2,:],W)


ax.plot(EU[0,:], EU[1,:], EU[2,:])  
ax.plot(EV[0,:], EV[1,:], EV[2,:])  
ax.plot(EW[0,:], EW[1,:], EW[2,:]) 
 
ax.quiver([0,0,0], [0,0,0], [0,0,0], E[0,:], E[1,:], E[2,:], length=1.0, color = 'k')

annotate3D(ax, s='$e_1$', xyz=E[:,0], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom') 
annotate3D(ax, s='$e_2$', xyz=E[:,1], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom') 
annotate3D(ax, s='$e_3$', xyz=E[:,2], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom') 

annotate3D(ax, s='$u$', xyz=Q[:,0], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom') 
annotate3D(ax, s='$v$', xyz=Q[:,1], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom') 
annotate3D(ax, s='$w$', xyz=Q[:,2], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom') 


ax.quiver([0,0,0], [0,0,0], [0,0,0], Q[0,:], Q[1,:], Q[2,:], length=1.0, color = 'g')

ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_zlim(-1,1)

ax.set_aspect(1)
plt.show()
#plt.clf()
#plt.draw()


#now let's make a plane!
fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')

th = np.pi/200
co = np.cos(th)
si = np.sin(th)
A = U@U.T + co*V@V.T - si*V@W.T + si*W@V.T + co*W@W.T

B = np.random.normal(size=(3,30),scale=0.5)
RB = A@B

s = np.linspace(-1,1,20)
t = np.linspace(-1,1,20)
s, t = np.meshgrid(s, t)

X = V[0]*s + t*W[0]
Y = V[1]*s + t*W[1]
Z = V[2]*s + t*W[2]


for i in range(200):
    ax.clear()
    RB = A@RB 
    PB = RB - U@U.T@RB

#    ax.scatter( B[0,:], B[1,:], B[2,:],   '.',color='red')
    ax.scatter(RB[0,:],RB[1,:],RB[2,:],'.',color='red')
    ax.scatter(PB[0,:],PB[1,:],PB[2,:],'.',color='black')
    
    ax.plot_surface(X, Y, Z,color='gray',alpha=0.5)

#ax.quiver([0,0,0], [0,0,0], [0,0,0], E[0,:], E[1,:], E[2,:], length=1.0, color = 'k')

#annotate3D(ax, s='$e_1$', xyz=E[:,0], fontsize=10, xytext=(-3,3), textcoords='offset points', ha='right',va='bottom') 
#annotate3D(ax, s='$e_2$', xyz=E[:,1], fontsize=10, xytext=(-3,3), textcoords='offset points', ha='right',va='bottom') 
#annotate3D(ax, s='$e_3$', xyz=E[:,2], fontsize=10, xytext=(-3,3), textcoords='offset points', ha='right',va='bottom') 

    annotate3D(ax, s='$q_1$', xyz=Q[:,0], fontsize=10, xytext=(-3,3), textcoords='offset points', ha='right',va='bottom') 
    annotate3D(ax, s='$q_2$', xyz=Q[:,1], fontsize=10, xytext=(-3,3), textcoords='offset points', ha='right',va='bottom') 
    annotate3D(ax, s='$q_3$', xyz=Q[:,2], fontsize=10, xytext=(-3,3), textcoords='offset points', ha='right',va='bottom') 

    ax.quiver([0,0,0], [0,0,0], [0,0,0], Q[0,:], Q[1,:], Q[2,:], length=1.0, color = 'g')


#    plt.draw()
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_zlim(-1,1)
    ax.view_init(elev=30, azim=30)
    ax.set_aspect(1)
    plt.pause(0.05)
#    plt.clf()

