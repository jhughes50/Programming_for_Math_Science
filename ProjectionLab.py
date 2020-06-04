import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from itertools import product

##################
# Initialization #
##################
# Use this space to initialize objects used for the whole script.
# The domain is the set of values for each x,y,z dimension in the unit cube.
domain = [0,1] # use the unit cube (in question 3)
fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')

def perspective(x, a, u, d, h):
    """ Given a matrix of points, create a projection matrix of those
    points on an image plane.
        x -- N by 3 coordinate Matrix
        a -- Point where the camera aperture is
        u -- direction in which the camera points
        d -- scalar distance between the image plane and camera
        h -- horizontal basis vector for the image plane
        """

    x = x.T # resize the point matrix to be 3 x N
    nCols = x.shape[1] # number of columns in x
    I3 = np.ones((3,1)) # column vectos of ones
    IN = np.ones((nCols,1)) # 1 x N vector of ones

    # Given any two vectors, a and b, a vector v which is perpendicular
    # to both is the cross product of a and b. The vertical basis for
    # the image plane is the cross product of the horizontal basis (h)
    # and camera direction (u).
    #
    # Because h and u are originally defined as 3 x 1 matrices, they need to
    # be reshaped to column vectors. The cross product is then reshaped
    # back into a 3 x 1 matrix.
    v = np.cross(h.reshape(3,), u.reshape(3,)).reshape(3,1)

    # We now have a horizontal and vertical basis for the plane, now
    # we need an origin point. This can easily be chosen using the equation
    # for a line. Given a point where the camera is (a) and a direction
    # it is facing (u), any point on that line can be found by scaling
    # the vector u.
    x0 = a + d*u #origin in the image plane
    #x0 is, by definition, in this plane!!

    # The formula for projection in Rolf's lecture included a c, which
    # we are going to define right now. After picking an origin, we
    # multiply that point with the camera direction vector to
    c = float(x0.T@u) #c used to define image plane by x dot u = c

    # Translating the language of linear algebra to Python looks like
    # this. Try writing out the function on paper and comparing the
    # variables to these two statements.
    numerator   = a@(u.T@x-c) + (c - u.T@a)*x
    denominator =  I3@u.T@(x - a@IN.T)
    per = numerator/denominator

    # per is a perspective matrix of points which all lie on the image plane.
    # These comprise the image projection, and you should think of that plane
    # as a regular Cartesian grid. Keeping that in mind, the points in per
    # exist in 3-space, but also lie on the same plane.
    #
    # We know the origin, horitzontal, and vertical bases of the plane,
    # and with those we can derive the respective x and y coordinates of a
    # 3D object projected onto a plane.
    xCoords = h.T@(per-x0)
    yCoords = v.T@(per-x0)

    ##########################
    # Create the image plane #
    ##########################
    # These next statements also are unnecessary, but it is nice
    # to visualize where in 3D space the image plane exists. The
    # matrices s and t define the size of that gray mesh.
    s = np.linspace(-2,2,20)
    t = np.linspace(-2,2,20)
    s, t = np.meshgrid(s,t)
    X = x0[0] + s*h[0] + t*v[0] # The coordinates
    Y = x0[1] + s*h[1] + t*v[1] #   of the plane
    Z = x0[2] + s*h[2] + t*v[2] #     lying in 3-space

    ax.plot_surface(X,Y,Z,color = 'gray', alpha=0.5) # plot the mesh grid
    ax.scatter(*a,color='green') # plot the camera aperture
    ax.quiver(*x0,*u,length=0.5) # plot the camera direction vector
    ax.quiver(*x0,*h,length=0.5) # the horizontal basis
    ax.quiver(*x0,*v,length=0.5) # the vertical basis
    ax.scatter(*per)

    # Setting the length of the axes and labels
    ax.set_xlim(-2,1.5)
    ax.set_ylim(-2,1.5)
    ax.set_zlim(-2,1.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

    plt.plot(xCoords,yCoords)
    plt.show()

    return per

# This might seem complicated, but we can break this statement down
# starting from the innermost data type
#  product(...) returns the cartesian product of input iterables,
# so a 2D X 2D X 2D creates eight three-dimensional co'ordinates.
#  list() creates a list from the iterable
#  np.array() is our versatile vector provided by numpy
# Summarized, this statement returns a 3x8 coordinate matrix
# of the unit cube
points = np.array(list(product(domain,domain,domain)))
ax.scatter3D(points[:,0], points[:,1], points[:,2]) # Plot the cube vertices

# This next bit does not pertain to the lab, I am just prettying
# up the graph. You should just work with the 3x8 points matrix.
# For those interested, I am creating a collection of the faces
# of a cube so the shape has some charcter, rather than looking
# like a collection of points. Purely a cosmetic touch.
verts=[[points[0],points[1],points[3],points[2]],
 [points[0],points[1],points[5],points[4]],
 [points[2],points[3],points[7],points[6]],
 [points[1],points[3],points[7],points[5]],
 [points[4],points[5],points[7],points[6]],
 [points[6],points[4],points[0],points[2]]]
faces = Poly3DCollection(verts,
edgecolors='g', linewidths=1.5)
faces.set_facecolor((0.,1.,1.,0.1))  # make it cyan #00ffff
ax.add_collection3d(faces)

###########################
#   Defining my Vectors   #
###########################
# Here is when it starts getting fun (unless you've been enjoying the ride
# all long). Now that we know how to project a 3D image onto a 2D plane, it
# is time to start thinking about all the possible image planes to chose from.
# There are three variables you get to select somewhat arbitrarily:
#   a -- the point in space where the camera hole is
#   u -- the direction the camera is pointing
#   h -- a horizontal vector forming one of the bases for our image plane
# The camera can be position anywhere, but you should take care to point it
# in the direction of the object. As for h, we can just use any vector perpendicular
# to u (the three vectors u,v,h will all be perpendicular). There are a lot
# of possibilities, but let's just rotate u by 90 degrees along the y axis.
# Mathematically, given a vector u: the rotation is (-u[1], u[0], u[2]).
a = np.array([2.5,0.5,0.5]).reshape(3,1)
u = np.array([-1.5,0.5,0.5]).reshape(3,1)
u = u/np.linalg.norm(u)

h = np.array([-u[1], u[0], u[2]]).reshape(3,1)
h = h/np.linalg.norm(h)
d = 0.5

per = perspective(points, a, u, d, h)

##################
# Question 4 #####
# Now you need to select three different viewing angles for the box and
# get the perspective projection for those. Look at the 3D plot and try to match
# the green dot with the vector pointing in the same direction. Now imagine
# that this is your eye and the plane is the projection of those 3D points
# onto your retina. Do the points of the cube match the pattern of the points
# on the plane? Eye-ball it.
# a = ...
# u = ...
# u = u/np.linalg.norm(u)
# h = np.array([-u[1], u[0], u[2]]).reshape(3,1)
# h = h/np.linalg.norm(h)
# d = ...
# per = perspective(points, a, u, d, h)
