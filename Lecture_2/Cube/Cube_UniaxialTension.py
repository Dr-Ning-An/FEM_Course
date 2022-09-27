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
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=1.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# Materials
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((1.0, 0.3), ))
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
mdb.models['Model-1'].rootAssembly.Set(name='Set-1', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((
    0.0, 0.0, 0.0), )))
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-1'], u1=SET, u2=SET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.Set(name='Set-2', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((
    1.0, 0.0, 0.0), )))
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-2'], u1=UNSET, u2=SET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.Set(name='Set-3', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((
    0.0, 1.0, 0.0), )))
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-3', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-3'], u1=SET, u2=UNSET, 
    u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)

# Load
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.5, 0.5, 1.0), )))
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)), distributionType=UNIFORM, field='', 
    localCsys=None, magnitude=1.0, name='Load-1', region=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-1'], traction=GENERAL)
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-2', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.5, 0.5, 0.0), )))
mdb.models['Model-1'].SurfaceTraction(createStepName='Step-1', directionVector=
    ((0.0, 0.0, 0.0), (0.0, 0.0, -1.0)), distributionType=UNIFORM, field='', 
    localCsys=None, magnitude=1.0, name='Load-2', region=
    mdb.models['Model-1'].rootAssembly.surfaces['Surf-2'], traction=GENERAL)

# Mesh
mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.2)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    distortionControl=DEFAULT),), regions=(
    mdb.models['Model-1'].parts['Part-1'].cells, ))

mdb.models['Model-1'].rootAssembly.regenerate()


# Job
jobName ='Cube_UniaxialTension'
mdb.Job(model='Model-1', name=jobName)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()