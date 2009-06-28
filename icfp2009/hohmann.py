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

def debug(vm, iteration):
	print str(iteration) + ': ',
	print '\tScore: ' + str(vm.memory().output(SCORE)),
	print '\tFuel: ' + str(vm.memory().output(FUEL)),
#	print '\tSx: ' + str(vm.memory().output(SX)),
#	print '\tSy: ' + str(vm.memory().output(SY)),
	print '\tDistance: ' + str(RAD),
	print '\tTarget: ' + str(vm.memory().output(TARGET_RADIUS)),
	print '\tOffset: ' + str(OFFSET)

MU = 6.67428e-11 * 6e24

vm = Vm('/home/greghaynes/icfp/binaries/bin1.obf')
vm.memory().setInput(CONFIG, 1001)
vm.cycle()
debug(vm, 0)

DIST = (vm.memory().output(SX)**2 + vm.memory().output(SY)**2)**.5
ORIG_DIST = DIST
TARGET_DIST = vm.memory().output(TARGET_RADIUS)
THETA = math.atan2(vm.memory().output(SY), vm.memory().output(SX))

V = (MU/DIST)**.5
Vx = (vm.memory().output(SX)/DIST) * V
Vy = (vm.memory().output(SY)/DIST) * V

A = MU/(DIST**2)
Ax = A * math.cos(THETA) * -1
Ay = A * math.sin(THETA) * -1

dV = (MU/DIST)**.5 * ((2*TARGET_DIST/(DIST+TARGET_DIST))**.5 - 1)
dVx = dV * (vm.memory().output(SX)/DIST)
dVy = dV * (vm.memory().output(SY)/DIST)

# Enter transfer elipse
vm.memory().setInput(2, dVy)
vm.memory().setInput(3, dVx)
vm.cycle()
vm.memory().setInput(2, 0)
vm.memory().setInput(3, 0)
debug(vm, 1)
i = 0
psx = 0
psx = 0
while i < 18874:
	vm.cycle()
	RAD = (vm.memory().output(SX)**2 + vm.memory().output(SY)**2)**.5
	OFFSET = RAD - TARGET_DIST
	debug(vm, i)
	psx = vm.memory().output(SX)
	psy = vm.memory().output(SY)
	i += 1

cvx = vm.memory().output(SX) - psx
cvy = vm.memory().output(SY) - psy
cv = (cvx**2 + cvy**2)**.5
nv = (MU/RAD)**.5
nv = nv - cv
nvx = (vm.memory().output(SX)/RAD) * nv
nvy = (vm.memory().output(SY)/RAD) * nv

sdV = (MU/DIST)**.5 * (1 - ((2*TARGET_DIST)/(ORIG_DIST+TARGET_DIST))**.5)
sdVx = sdV * (vm.memory().output(SX)/RAD)
sdVy = sdV * (vm.memory().output(SY)/RAD)
# Enter outer orbit
vm.memory().setInput(2, sdVy)
vm.memory().setInput(3, sdVx)
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
#	DOFFSET = OFFSET - PREVOFFSET
#	if DOFFSET < 0:
#		ymag = (vm.memory().output(SY) / DIST)*(.3*DOFFSET)
#		xmag = (vm.memory().output(SX) / DIST)*(.3*DOFFSET)
	PREVOFFSET = OFFSET
