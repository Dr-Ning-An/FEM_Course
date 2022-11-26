# Created by Su, Yulin and An, Ning
# Nov. 26, 2022
# This file performs a stress analysis of a plate with a hole
# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

l = 30.0 # mm
r = 2.0 # mm
p = 30.0 # MPa

# Mesh size
GlobalMeshSize = 0.5
LocalMeshSize = 0.05

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE) 


Mdb()

# Create Part
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-l, l), 
    point2=(l, -l))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0.0, r))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=1.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# Material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Density(table=((2.81e-09, ), )) # t/mm3
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((71000.0, 0.33),  )) # MPa
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.getSequenceFromMask(('[#1 ]', 
    ), ), name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
    'Section-1', thicknessAssignment=FROM_SECTION)

# Assembly
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])


# Step
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')


# Load
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    -l, 0.0, 0.5), )), name='Set-1')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-1'], u1=0.0, 
    u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    l, 0.0, 0.5), )))
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, field='', magnitude=-p, name='Load-1', region=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-1'])


# Mesh
# Circle
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=4.24, name='__profile__', sheetSize=169.71, 
    transform=
    mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces.findAt((l/2.0, 0.0, 1.0), ), 
    sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges.findAt((l, 0.0, 1.0), ), sketchOrientation=RIGHT, 
    origin=(0.0, 0.0, 1.0)))
mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.0, 0.0), point1=(5.0*r, 0.0)) # Draw a circle
mdb.models['Model-1'].parts['Part-1'].PartitionCellBySketch(cells=
    mdb.models['Model-1'].parts['Part-1'].cells, sketch=mdb.models['Model-1'].sketches['__profile__'], 
    sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces.findAt((l/2.0, 0.0, 1.0), ), 
    sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges.findAt((l, 0.0, 1.0), ))
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].parts['Part-1'].PartitionCellBySweepEdge(cells=
    mdb.models['Model-1'].parts['Part-1'].cells, 
    edges=(mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.0*r, 0.0, 1.0), ), ), sweepPath=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((l, -l, 0.5), ))

# Cut
Plane1 = mdb.models['Model-1'].parts['Part-1'].DatumPlaneByPrincipalPlane(offset=0.0, 
    principalPlane=XZPLANE)
Plane2 = mdb.models['Model-1'].parts['Part-1'].DatumPlaneByPrincipalPlane(offset=0.0, 
    principalPlane=YZPLANE)
mdb.models['Model-1'].parts['Part-1'].PartitionCellByDatumPlane(cells=
    mdb.models['Model-1'].parts['Part-1'].cells, datumPlane=
    mdb.models['Model-1'].parts['Part-1'].datums[Plane1.id])
mdb.models['Model-1'].parts['Part-1'].PartitionCellByDatumPlane(cells=
    mdb.models['Model-1'].parts['Part-1'].cells, datumPlane=
    mdb.models['Model-1'].parts['Part-1'].datums[Plane2.id])

# Mesh
# Global Size
mdb.models['Model-1'].parts['Part-1'].seedPart(size=GlobalMeshSize)

# Local Size
mdb.models['Model-1'].parts['Part-1'].seedEdgeBySize(
    edges=mdb.models['Model-1'].parts['Part-1'].edges.findAt(((0.0, 2.5*r, 1.0), ), ((0.0, -2.5*r, 1.0), ), ((2.5*r, 0.0, 1.0), ), ((-2.5*r, 0.0, 1.0), ), 
          ((r*cos(pi/4.0), r*sin(pi/4.0), 1.0), ), ((-r*cos(pi/4.0), r*sin(pi/4.0), 1.0), ), ((-r*cos(pi/4.0), -r*sin(pi/4.0), 1.0), ), ((r*cos(pi/4.0), -r*sin(pi/4.0), 1.0), ),), 
    size=LocalMeshSize)

mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), 
    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].parts['Part-1'].cells, ))


# # Job
mdb.models['Model-1'].rootAssembly.regenerate()

jobName = "plate_with_hole"
mdb.Job(model='Model-1', name=jobName)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()


# Postprocessing: Create a cylindrical coordinate system and show hoop stress 

o3 = session.openOdb(name= jobName + '.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].makeCurrent()

odb = session.odbs[jobName + '.odb']
scratchOdb = session.ScratchOdb(odb)
scratchOdb.rootAssembly.DatumCsysByThreePoints(name='CSYS-1', 
    coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 1.0, 0.0))
dtm = scratchOdb.rootAssembly.datumCsyses['CSYS-1']
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    transformationType=USER_SPECIFIED, datumCsys=dtm)

session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_UNDEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT, 
    'S22'), )
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
mdb.save()
