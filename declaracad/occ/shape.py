# -*- coding: utf-8 -*-
"""
Copyright (c) 2016-2018, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Sep 30, 2016

@author: jrm
"""
from atom.api import (
    Atom, Tuple, Instance, Bool, Str, Float, Property, Coerced, Typed,
    ForwardTyped, List, Enum, observe
)

from contextlib import contextmanager
from enaml.core.declarative import d_
from enaml.colors import ColorMember
from enaml.widgets.control import ProxyControl
from enaml.widgets.toolkit_object import ToolkitObject

#: TODO: This breaks the proxy pattern
from OCC.TopoDS import TopoDS_Face, TopoDS_Shell, TopoDS_Shape


class BBox(Atom):
    xmin = Float()
    ymin = Float()
    zmin = Float()
    xmax = Float()
    ymax = Float()
    zmax = Float()
    
    def _get_dx(self):
        return self.xmax-self.xmin
    
    dx = Property(_get_dx, cached=True)
    
    def _get_dy(self):
        return self.ymax-self.ymin
    
    dy = Property(_get_dy, cached=True)
    
    def _get_dz(self):
        return self.zmax-self.zmin
    
    dz = Property(_get_dz, cached=True)
    
    def __init__(self, xmin=0, ymin=0, zmin=0, xmax=0, ymax=0, zmax=0):
        super(BBox, self).__init__(xmin=xmin, ymin=ymin, zmin=zmin,
                                   xmax=xmax, ymax=ymax, zmax=zmax)
        
    def __getitem__(self, key):
        return (self.xmin, self.ymin, self.zmin, 
                self.xmax, self.ymax, self.zmax)[key]
    

class ProxyShape(ProxyControl):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Shape)
    
    def set_position(self, position):
        pass
    
    def set_direction(self, direction):
        pass
    
    def set_axis(self, axis):
        raise NotImplementedError
    
    def set_color(self, color):
        pass
    
    def set_transparency(self, alpha):
        pass
    
    def get_bounding_box(self):
        raise NotImplementedError


class ProxyFace(ProxyShape):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Face)
    
    def set_wire(self, wire):
        raise NotImplementedError


class ProxyBox(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Box)
    
    def set_dx(self, dx):
        raise NotImplementedError
    
    def set_dy(self, dy):
        raise NotImplementedError
    
    def set_dz(self, dz):
        raise NotImplementedError


class ProxyCone(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Cone)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_radius2(self, r):
        raise NotImplementedError
    
    def set_height(self, height):
        raise NotImplementedError
    
    def set_angle(self, angle):
        raise NotImplementedError


class ProxyCylinder(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Cylinder)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_height(self, height):
        raise NotImplementedError
    
    def set_angle(self, angle):
        raise NotImplementedError


class ProxyHalfSpace(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: HalfSpace)
    
    def set_surface(self, surface):
        raise NotImplementedError


class ProxyPrism(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Prism)
    
    def set_shape(self, surface):
        raise NotImplementedError
    
    def set_vector(self, vector):
        raise NotImplementedError
    
    def set_infinite(self, infinite):
        raise NotImplementedError
    
    def set_copy(self, copy):
        raise NotImplementedError
    
    def set_canonize(self, canonize):
        raise NotImplementedError


class ProxySphere(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Sphere)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_angle(self, a):
        raise NotImplementedError
    
    def set_angle2(self, a):
        raise NotImplementedError
    
    def set_angle3(self, a):
        raise NotImplementedError


class ProxyTorus(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Torus)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_radius2(self, r):
        raise NotImplementedError
    
    def set_angle(self, a):
        raise NotImplementedError
    
    def set_angle2(self, a):
        raise NotImplementedError


class ProxyWedge(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Wedge)
    
    def set_dx(self, dx):
        raise NotImplementedError
    
    def set_dy(self, dy):
        raise NotImplementedError
    
    def set_dz(self, dz):
        raise NotImplementedError
    
    def set_itx(self, itx):
        raise NotImplementedError 


class ProxyRevol(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Revol)
    
    def set_shape(self, shape):
        raise NotImplementedError
    
    def set_angle(self, angle):
        raise NotImplementedError
    
    def set_copy(self, copy):
        raise NotImplementedError


class ProxyRawShape(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: RawShape)

    def get_shape(self):
        raise NotImplementedError


class ProxyLoadShape(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: LoadShape)

    def set_path(self, path):
        raise NotImplementedError

    def set_loader(self, loader):
        raise NotImplementedError

    
class Shape(ToolkitObject):
    """ Abstract shape component that can be displayed on the screen 
    and represented by the framework. 
    
    Attributes  
    ----------
    
    position: Tuple
        A tuple or list of the (x, y, z) position of this shape. This is
        coerced into a Point.
    x: Float
    y: Float
    z: Float
        Alias to the position
    direction: Tuple
        A tuple or list of the (u, v, w) vector of this shape. This is
        coerced into a Vector.
    axis: Tuple
        A tuple or list of the (u, v, w) axis of this shape. This is
        coerced into a Vector that defines the x, y, and z orientation of
        this shape.
    tolerance: Float
        The tolerance to use for operations that may require it.
    color: Color
        A string representing the color of the shape.
    material: String
        A string represeting a pre-defined material which defines a color
        and luminosity of the shape.
    transparency: Float
        The opacity of the shape used for display.
    shape_edges: List
        A read only property that returns the list of edges this shape
        has (if any).
    shape_faces: List
        A read only property that returns the list of faces this shape
        has (if any).
    shape_shells: List
        A read only property that returns the list of surfaces this shape
        has (if any).

    Notes
    ------
    
    This shape's proxy holds an internal reference to the underlying shape 
    which can be accessed using `self.proxy.shape` if needed. The topology
    of the shape can be accessed using the `self.proxy.topology` attribute.
    
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyShape)
    
    #: Tolerance
    tolerance = d_(Float(10**-6, strict=False))
    
    #: Color
    color = d_(ColorMember()).tag(view=True, group='Display')

    #: Texture material
    material = d_(Enum(None, 'aluminium', 'brass', 'bronze', 'charcoal',
                       'chrome', 'copper', 'default', 'diamond', 'glass',
                       'gold', 'jade', 'metalized', 'neon_gnc', 'neon_phc',
                       'obsidian', 'pewter', 'plaster', 'plastic', 'satin',
                       'shiny_plastic', 'silver', 'steel', 'stone', 'water')
                  ).tag(view=True, group='Display')
    
    #: Transparency
    transparency = d_(Float(strict=False)).tag(view=True, group='Display')
    
    #: x position
    x = d_(Float(0, strict=False)).tag(view=True, group='Position')
    
    #: y position
    y = d_(Float(0, strict=False)).tag(view=True, group='Position')
    
    #: z position
    z = d_(Float(0, strict=False)).tag(view=True, group='Position')
    
    #: Position
    position = d_(Coerced(tuple))
    
    def _default_position(self):
        return (
            self.get_member('x').get_slot(self) or 0.0,
            self.get_member('y').get_slot(self) or 0.0,
            self.get_member('z').get_slot(self) or 0.0,
        )
    
    def _default_x(self):
        return self.position[0]
    
    def _default_y(self):
        return self.position[1]
    
    def _default_z(self):
        return self.position[2]
    
    @observe('x', 'y', 'z')
    def _update_position(self, change):
        self.position = self._default_position()
        
    def _observe_position(self, change):
        self.x, self.y, self.z = self.position
        
    #: Direction
    direction = d_(Coerced(tuple))
    
    def _default_direction(self):
        return (0, 0, 1)
    
    def _get_axis(self):
        return (self.position, self.direction)
    
    def _set_axis(self, axis):
        self.position, self.direction = axis
    
    #: Direction
    axis = d_(Property(_get_axis, _set_axis))
    
    def _get_edges(self):
        topo = self.proxy.topology
        if not topo:
            return []
        return [e for e in topo.edges()]
    
    #: Edges of this shape
    shape_edges = Property(_get_edges, cached=True)
    
    def _get_faces(self):
        topo = self.proxy.topology
        if not topo:
            return []
        return [e for e in topo.faces()]
    
    #: Faces of this shape
    shape_faces = Property(_get_faces, cached=True)

    def _get_shells(self):
        topo = self.proxy.topology
        if not topo:
            return []
        return [e for e in topo.shells()]

    #: Shells of this shape
    shape_shells = Property(_get_shells, cached=True)
    
    def _get_bounding_box(self):
        if self.proxy.shape:
            try:
                return self.proxy.get_bounding_box()
            except:
                pass
    
    #: Bounding box of this shape
    bbox = d_(Property(_get_bounding_box, cached=True))
    
    @observe('color', 'transparency')
    def _update_proxy(self, change):
        super(Shape, self)._update_proxy(change)
        if self.proxy:
            self.proxy.update_display(change)
    
    @observe('proxy.shape')
    def _update_properties(self, change):
        """ Update the cached topology references when the shape changes. """
        for k in ('shape_edges', 'shape_faces', 'shape_shells', 'bbox'):
            self.get_member(k).reset(self)
            
    def render(self):
        """ Generates and returns the actual shape from the declaration. 
        Enaml does this automatically when it's included in the viewer so this 
        is only neede when working with shapes manually.
        
        Returns
        -------
        shape: TopoDS_Shape 
            The shape generated by this declaration.
        
        """
        if not self.is_initialized:
            self.initialize()
        if not self.proxy_is_active:
            self.activate_proxy()
        return self.proxy.shape


class Face(Shape):
    """ A Face turns it's first child Wire into a surface. 
    
    Examples
    --------
    
    Add a Wire as a child 
        Face:
            Wire:
                # etc.. 
    
    """

    #: Reference to the implementation control
    proxy = Typed(ProxyFace)
    
    #: List of wires to use
    wires = d_(List())


class Box(Shape):
    """ A primitive Box shape.  
    
    Attributes
    ----------
    
    dx: Float
        Size or width of the box along the x-axis
    dy: Float
        Size or height of the box along the y-axis
    dz: Float
        Size or depth of the box along the z-axis  

    Examples
    --------
    
    Box:
        dx = 3  
        dy = 10
        # dx, dy, and dz are all 1 by default if omitted
    
    """
    #: Proxy shape
    proxy = Typed(ProxyBox)
    
    #: x size
    dx = d_(Float(1, strict=False)).tag(view=True)
    
    #: y size
    dy = d_(Float(1, strict=False)).tag(view=True)
    
    #: z size
    dz = d_(Float(1, strict=False)).tag(view=True)
    
    # TODO: Handle other constructors
    
    @observe('dx', 'dy', 'dz')
    def _update_proxy(self, change):
        super(Box, self)._update_proxy(change)


class Cone(Shape):
    """ A primitive Cone shape.
    
    Attributes
    ----------
    
    height: Float
        Height of the cone
    radius: Float
        Radius of the base of the cone
    radius2: Float
        Second radius of the base of the cone (to make it oval)  
    angle: 
        The angle to revolve (in radians) the base profile
            
    Examples
    --------

    Cone:
        height = 10
        radius = 5
        angle = math.pi/2
    
    """
    #: Proxy shape
    proxy = Typed(ProxyCone)
    
    #: Radius
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: Radius 2 size
    radius2 = d_(Float(0, strict=False)).tag(view=True)
    
    #: Height
    height = d_(Float(1, strict=False)).tag(view=True)
    
    #: Angle
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    @observe('radius', 'radius2', 'height', 'angle')
    def _update_proxy(self, change):
        super(Cone, self)._update_proxy(change)


class Cylinder(Shape):
    """ A primitive Cylinder shape.

    Attributes
    ----------
    
    height: Float
        Height of the cylinder
    radius: Float
        Radius of the base of the cylinder
    angle: 
        The angle to revolve (in radians) the base profile.
            
    Examples
    --------
    
    Cone:
        height = 10
        radius = 5
    
    """
    #: Proxy shape
    proxy = Typed(ProxyCylinder)
    
    #: Radius
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: Height
    height = d_(Float(1, strict=False)).tag(view=True)
    
    #: Angle
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    @observe('radius', 'height', 'angle')
    def _update_proxy(self, change):
        super(Cylinder, self)._update_proxy(change)


class HalfSpace(Shape):
    """ An infinite solid limited by a surface.

    Attributes
    ----------
    
    surface: Face or Shell
        Surface to divide
            
    Notes
    -----
    
     A half-space is an infinite solid, limited by a surface. It is built from 
     a face or a shell, which bounds it, and with a reference point, which 
     specifies the side of the surface where the matter of the half-space is 
     located. A half-space is a tool commonly used in topological operations 
     to cut another shape
            
    Examples
    --------
    
    #: TODO: This does not work
    
    Box: box:
        pass
    
    HalfSpace:
        shape = box.shape_faces[0]
        position = (1, 1, 1)
    
    """
    #: Proxy shape
    proxy = Typed(ProxyHalfSpace)
    
    #: Surface that is either a face or a Shell
    surface = d_(Instance((TopoDS_Face, TopoDS_Shell)))
                 
    @observe('surface')
    def _update_proxy(self, change):
        super(HalfSpace, self)._update_proxy(change)

        
class Prism(Shape):
    """ A Prism extrudes a Face into a solid or a Wire into a surface along 
    the given vector. 
    
    Attributes
    ----------
    
    shape: Shape to extrude or None
        Reference to the shape to extrude.
    vector: Tuple of (x, y, z)
        The extrusion vector.
    infinite: Bool
        Whether to extrude an infinte distance along the given vector.
    copy: Bool
        Copy the surface before extruding
    canonize: Bool
        Attempt to canonize in simple shapes
    
    Notes
    -----
    
    The first child node will be used as the shape if none is given.

            
    Examples
    --------
    
    Prism:
        Wire:
            Polygon:
                points = [(0,5,0), (2,6,0),  (5,4,0), (0,5,0)]
    
    """

    #: Proxy shape
    proxy = Typed(ProxyPrism)
    
    #: Shape to build prism from
    shape = d_(Instance(Shape)).tag(view=True)
    
    #: Vector to build prism from, ignored if infinite is true
    vector = d_(Tuple((float, int), default=(0, 0, 1))).tag(view=True)
    
    #: Infinite
    infinite = d_(Bool(False)).tag(view=True)
    
    #: Copy the surface
    copy = d_(Bool(False)).tag(view=True)
    
    #: Attempt to canonize
    canonize = d_(Bool(True)).tag(view=True)
    
    @observe('shape', 'vector', 'infinite', 'copy', 'canonize')
    def _update_proxy(self, change):
        super(Prism, self)._update_proxy(change)


class Sphere(Shape):
    """ A primitive Sphere shape. 
    
    Attributes
    ----------
    
    radius: Float
        Radius of the sphere
    angle: Float
        The angle to revolve (in radians) along the base profile.
    angle2: Float
        See notes
    angle3: Float
        See notes
    
    
    Notes
    --------
    
    Make a sphere of radius R. For all algorithms The resulting shape is 
    composed of:
    
    - a lateral spherical face
    - Two planar faces parallel to the plane z = 0 if the sphere is truncated 
      in the v parametric direction, or only one planar face if angle1 is 
      equal to -p/2 or if angle2 is equal to p/2 (these faces are circles in 
      case of a complete truncated sphere),
    - and in case of a portion of sphere, two planar faces to shut the shape.
      (in the planes u = 0 and u = angle).

            
    Examples
    --------
    
    Sphere:
        radius = 3
    
    Sphere:
        angle = math.pi/2
    
    """
    #: Proxy shape
    proxy = Typed(ProxySphere)
    
    #: Radius of sphere
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: angle 1
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    #: angle 2
    angle2 = d_(Float(0, strict=False)).tag(view=True)
    
    #: angle 3
    angle3 = d_(Float(0, strict=False)).tag(view=True)
    
    @observe('radius', 'angle', 'angle2', 'angle3')
    def _update_proxy(self, change):
        super(Sphere, self)._update_proxy(change)


class Torus(Shape):
    """ A primitive Torus shape (a ring like shape).

    Attributes
    ----------
    
    radius: Float
        Radius of the torus
    radius2: Float
        Radius of the torus profile
    angle:  Float
        The angle to revolve the torus (in radians).
    angle2: Float
        The angle to revolve the torus profile (in radians).
            
    Examples
    --------
    
    Torus:
        radius = 5
    
    """
    #: Proxy shape
    proxy = Typed(ProxyTorus)

    #: Radius of sphere
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: Radius 2
    radius2 = d_(Float(0, strict=False)).tag(view=True)
    
    #: angle 1
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    #: angle 2
    angle2 = d_(Float(0, strict=False)).tag(view=True)
    
    @observe('radius', 'radius2', 'angle1', 'angle2')
    def _update_proxy(self, change):
        super(Torus, self)._update_proxy(change)


class Wedge(Shape):
    """ A primitive Wedge shape.
    
    Attributes
    ----------
        
    dx: Float
        Size of the wedge along the x-axis
    dy: Float
        Size of the wedge along the y-axis
    dz:  Float
        Size of the wedge along the z-axis
    ltx: Float
        Size of the base before the wedge starts. Must be >= 0. 
        Defaults to 0.
            
    Examples
    --------
    
    Wedge:
        dy = 5
            
    """
    #: Proxy shape
    proxy = Typed(ProxyWedge)

    #: x size
    dx = d_(Float(1, strict=False)).tag(view=True)
    
    #: y size
    dy = d_(Float(1, strict=False)).tag(view=True)
    
    #: z size
    dz = d_(Float(1, strict=False)).tag(view=True)
    
    #: z size
    itx = d_(Float(0, strict=False)).tag(view=True)
    
    # TODO: Handle other constructors
    
    @observe('dx', 'dy', 'dz', 'itx')
    def _update_proxy(self, change):
        super(Wedge, self)._update_proxy(change)


class Revol(Shape):
    """ A Revol creates a shape by revolving a profile about an axis.
    
    Attributes
    ----------
        
    shape: Shape
        Shape to revolve. If not given, the first child will be used.
    angle: Float
        Angle to revolve (in radians) the base profile.
    copy:  Bool
        Make a copy of the referenced shape.
            
    Examples
    --------
    
    # This creates a cone of radius 4 and height 5.
    
    Revol:
        Wire:
            Segment:
                Looper:
                    iterable = [(0,0,0), (0,2,5),  (0,5,0), (0,0,0)]
                    Point:
                        position = loop_item
            
    """
    #: Proxy shape
    proxy = Typed(ProxyRevol)
    
    #: Shape to build prism from
    shape = d_(Instance(Shape)).tag(view=True)
    
    #: Angle to revolve
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    #: Copy the surface
    copy = d_(Bool(False)).tag(view=True)
    
    @observe('shape', 'angle', 'copy')
    def _update_proxy(self, change):
        super(Revol, self)._update_proxy(change)


class RawShape(Shape):
    """ A RawShape is a shape that delegates shape creation to the declaration.
    This allows custom shapes to be added to the 3D model hierarchy. Users
    should subclass this and implement the `create_shape` method.
    
    Examples
    --------
    
    from OCC.TopoDS import TopoDS_Shape
    from OCC.StlAPI import StlAPI_Reader
    
    class StlShape(RawShape):
        #: Loads a shape from an stl file
        def create_shape(self, parent):
            stl_reader = StlAPI_Reader()
            shape = TopoDS_Shape()
            stl_reader.Read(shape, './models/fan.stl')
            return shape
            
    
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyRawShape)

    def create_shape(self, parent):
        """ Create the shape for the control.
        This method should create and initialize the shape.
        
        Parameters
        ----------
        parent : shape or None
            The parent shape for the control.
        
        Returns
        -------
        result : shape
            The shape for the control.
        
        
        """
        raise NotImplementedError

    def get_shape(self):
        """ Retrieve the shape for display.
        
        Returns
        -------
        shape : shape or None
            The toolkit shape that was previously created by the
            call to 'create_shape' or None if the proxy is not
            active or the shape has been destroyed.
        """
        if self.proxy_is_active:
            return self.proxy.get_shape()


class LoadShape(Shape):
    """ Load a shape from the given path. Shapes can be repositioned and
    colored as needed.
    
    Attributes
    ----------
    
    path: String
        The path of the 3D model to load. Supported types are, .stl, .stp,
        .igs, and .brep
    
    
    Examples
    --------
    
    LoadShape:
        path = "examples/models/fan.stl"
        position = (10, 100, 0)
    
    """
    #: Proxy shape
    proxy = Typed(ProxyLoadShape)

    #: Path of the shape to load
    path = d_(Str())

    #: Loader to use
    loader = d_(Enum('auto', 'stl', 'stp', 'caf', 'iges', 'brep'))

    @observe('path', 'type')
    def _update_proxy(self, change):
        """ Base class implementation is sufficient"""
        super(LoadShape, self)._update_proxy(change)
