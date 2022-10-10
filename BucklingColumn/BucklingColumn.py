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
r = 1.0; # Radius 
E = 200.0E3; # Elastic Modulus
nu = 0.3; # Poisson's ratio


# Part
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=400.0)
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    0.0, L))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseWire(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# Material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((E, nu), ))

# Cross-section
mdb.models['Model-1'].CircularProfile(name='Profile-1', r=r)
mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='Material-1', name='Section-1', poissonRatio=0.0, 
    profile='Profile-1', temperatureVar=LINEAR)
mdb.models['Model-1'].parts['Part-1'].Set(edges=
    mdb.models['Model-1'].parts['Part-1'].edges, name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
    'Section-1', thicknessAssignment=FROM_SECTION)
# Beam Orientation
mdb.models['Model-1'].parts['Part-1'].assignBeamSectionOrientation(method=
    N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'])

# Assembly
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])

# Step
mdb.models['Model-1'].BuckleStep(name='BucklingStep', numEigen=30, previous='Initial', vectors=38)

# Boundary Condition
mdb.models['Model-1'].rootAssembly.Set(name='Set-Bottom', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((0.0, 0.0, 0.0), )))
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-Bottom'], 
    u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
#
mdb.models['Model-1'].rootAssembly.Set(name='Set-Top', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.findAt(((0.0, L, 0.0), )))
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-Top'], 
    u1=SET, u2=UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.regenerate()

# Load
mdb.models['Model-1'].ConcentratedForce(cf2=-1.0, 
    createStepName='BucklingStep', distributionType=UNIFORM, field='', localCsys=None, name='Load-1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Set-Top'])

# Mesh
mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=L/200.0)
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=B31, elemLibrary=STANDARD), ), regions=(
    mdb.models['Model-1'].parts['Part-1'].edges, ))
mdb.models['Model-1'].parts['Part-1'].generateMesh()

# Job
jobName ='BucklingColumn'
mdb.Job(model='Model-1', name=jobName)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()



##############################################################
## Extract EigenValues from Linear Buckling Analysis
## https://anning003.com/extract-eigenvalues/
##############################################################

stepName = 'BucklingStep'

from odbAccess import*
from abaqusConstants import*
import string
import numpy as np
import os
import re

odb = openOdb(path = jobName+'.odb')

outfile = open(jobName + '.csv', 'w')
outfile.write('EigenValue'+ '\n')

for fm in range(1, len(odb.steps[stepName].frames)):

  text = odb.steps[stepName].frames[fm].description
  EigenValue = [float(i) for i in re.findall("\\d+\\.\\d+", text)]
  outfile.write(str(EigenValue[0]) + '\n')

outfile.close()

odb.close()
