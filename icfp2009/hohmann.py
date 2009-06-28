# -*- coding: utf-8 -*-
from core import Vm, CONFIG
import math

SCORE = 0
FUEL = 1
SX = 2
SY = 3
TARGET_RADIUS = 4
RAD = 0
OFFSET = 9999999

outfile = open('out.dat', 'w')

def debug(vm, iteration):
	print str(iteration) + ': ',
	print '\tScore: ' + str(vm.memory().output(SCORE)),
	print '\tFuel: ' + str(vm.memory().output(FUEL)),
#	print '\tSx: ' + str(vm.memory().output(SX)),
#	print '\tSy: ' + str(vm.memory().output(SY)),
	print '\tDistance: ' + str(RAD),
	print '\tTarget: ' + str(vm.memory().output(TARGET_RADIUS)),
	print '\tOffset: ' + str(OFFSET)
	outfile.write('%f,%f\n' % (vm.memory().output(SX), vm.memory().output(SY)))

MU = 6.67428e-11 * 6e24

vm = Vm('../binaries/bin1.obf')
vm.memory().setInput(CONFIG, 1001)
vm.cycle()
debug(vm, 0)

DIST = (vm.memory().output(SX)**2 + vm.memory().output(SY)**2)**.5
TARGET_DIST = vm.memory().output(TARGET_RADIUS)
THETA = math.atan2(vm.memory().output(SY), vm.memory().output(SX))

V = (MU/DIST)**.5
Vx = V * math.sin(THETA) * -1
Vy = V * math.cos(THETA)

A = MU/(DIST**2)
Ax = A * math.cos(THETA) * -1
Ay = A * math.sin(THETA) * -1

dV = (MU/DIST)**.5 * ((2*TARGET_DIST/(DIST+TARGET_DIST))**.5 - 1)
dVx = dV * math.sin(THETA) * -1
dVy = dV * math.cos(THETA)

sdV = -1 * (MU/TARGET_DIST)**.5 * (1 - (2 * (TARGET_DIST/(DIST+TARGET_DIST)))**.5)
sdVx = sdV * math.sin(THETA) * -1
sdVy = sdV * math.cos(THETA)

# Enter transfer elipse
vm.memory().setInput(2, dVx)
vm.memory().setInput(3, dVy)
vm.cycle()
vm.memory().setInput(2, 0)
vm.memory().setInput(3, 0)
debug(vm, 1)
i = 0
while OFFSET < -50 or OFFSET > 50:
	vm.cycle()
	RAD = (vm.memory().output(SX)**2 + vm.memory().output(SY)**2)**.5
	OFFSET = RAD - vm.memory().output(TARGET_RADIUS)
	debug(vm, i)
	i += 1

# Enter outer orbit
vm.memory().setInput(2, sdVx)
vm.memory().setInput(3, sdVy)
vm.cycle()
ymag = 0
xmag = 0
PREVOFFSET = OFFSET
for i in xrange(10000):
	vm.cycle()
	vm.memory().setInput(2, xmag)
	vm.memory().setInput(3, ymag)
	ymag = 0
	xmag = 0
	RAD = (vm.memory().output(SX)**2 + vm.memory().output(SY)**2)**.5
	OFFSET = RAD - vm.memory().output(TARGET_RADIUS)
	debug(vm, i)
	DOFFSET = OFFSET - PREVOFFSET
	if DOFFSET < 0:
		ymag = (vm.memory().output(SY) / DIST)*(.3*DOFFSET)
		xmag = (vm.memory().output(SX) / DIST)*(.3*DOFFSET)
	PREVOFFSET = OFFSET
