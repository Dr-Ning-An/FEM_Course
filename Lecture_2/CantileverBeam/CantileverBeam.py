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

L = 200.0; # Length
T = 20.0; # Thickness
W = 25.0; # Width
meshSize = 2.0; # Global size of mesh

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE) 

Mdb()

# Create Part 
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=400.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(
    point1=(0.0, 0.0), 
    point2=(L, T))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=W, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# Material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((209000.0, 0.3), 
    ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells, name='Set-1')
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

# Boundary Conditions
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.0, T/2.0, W/2.0), )), name='Set-1')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-1'], u1=SET, u2=SET, 
    u3=SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    L/2.0, T, W/2.0), )))
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, field='', magnitude=0.5, name='Load-1', region=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-1'])

# Mesh
mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=meshSize)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    distortionControl=DEFAULT),), regions=(
    mdb.models['Model-1'].parts['Part-1'].cells, ))

mdb.models['Model-1'].rootAssembly.regenerate()

# Job
jobName ='CantileverBeam'
mdb.Job(model='Model-1', name=jobName)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()
