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

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE) 

Mdb()

# Part
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(1.0, 1.0))
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# Material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((210000.0, 0.3), 
    ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(faces=
    mdb.models['Model-1'].parts['Part-1'].faces, name='Set-1')
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
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1X', side1Edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    1.0, 0.5, 0.0), )))
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)), 
    distributionType=UNIFORM, field='', localCsys=None, magnitude=50.0, name=
    'Tension-X1', region=mdb.models['Model-1'].rootAssembly.surfaces['Surf-1X'], 
    traction=GENERAL)
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0)), 
    distributionType=UNIFORM, field='', localCsys=None, magnitude=30.0, name=
    'Shear-XY1', region=mdb.models['Model-1'].rootAssembly.surfaces['Surf-1X'], 
    traction=GENERAL)
#
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-2X', side1Edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    0.0, 0.5, 0.0), )))
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (-1.0, 0.0, 0.0)), 
    distributionType=UNIFORM, field='', localCsys=None, magnitude=50.0, name=
    'Tension-X2', region=mdb.models['Model-1'].rootAssembly.surfaces['Surf-2X'], 
    traction=GENERAL)
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (0.0, -1.0, 0.0)), 
    distributionType=UNIFORM, field='', localCsys=None, magnitude=30.0, name=
    'Shear-XY2', region=mdb.models['Model-1'].rootAssembly.surfaces['Surf-2X'], 
    traction=GENERAL)
#
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1Y', side1Edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    0.5, 1.0, 0.0), )))
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0)), 
    distributionType=UNIFORM, field='', localCsys=None, magnitude=-20.0, name=
    'Tension-Y1', region=mdb.models['Model-1'].rootAssembly.surfaces['Surf-1Y'], 
    traction=GENERAL)
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)), 
    distributionType=UNIFORM, field='', localCsys=None, magnitude=30.0, name=
    'Shear-YX1', region=mdb.models['Model-1'].rootAssembly.surfaces['Surf-1Y'], 
    traction=GENERAL)
#
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-2Y', side1Edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    0.5, 0.0, 0.0), )))
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (0.0, -1.0, 0.0)), 
    distributionType=UNIFORM, field='', localCsys=None, magnitude=-20.0, name=
    'Tension-Y2', region=mdb.models['Model-1'].rootAssembly.surfaces['Surf-2Y'], 
    traction=GENERAL)
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (-1.0, 0.0, 0.0)), 
    distributionType=UNIFORM, field='', localCsys=None, magnitude=30.0, name=
    'Shear-YX2', region=mdb.models['Model-1'].rootAssembly.surfaces['Surf-2Y'], 
    traction=GENERAL)

# Mesh
mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.1)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=CPE4, elemLibrary=STANDARD), ), regions=(
    mdb.models['Model-1'].parts['Part-1'].faces, ))

mdb.models['Model-1'].rootAssembly.regenerate()

# Job
jobName ='Cube_PlaneStrain'
mdb.Job(model='Model-1', name=jobName)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()
