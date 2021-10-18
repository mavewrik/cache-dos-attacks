from __future__ import print_function
from __future__ import absolute_import

# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *
# Add the common scripts to our path
from caches_3 import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--l1i_size', help="L1 instruction cache size")
parser.add_option('--l1d_size', help="L1 data cache size")
parser.add_option('--l2_size', help="Unified L2 cache size")
parser.add_option("-c", "--cmd", default="", help="The binary to run in syscall emulation mode.")
parser.add_option("-o", "--options", default="", help="""The options to pass to the binary, use " " around the entire string""")
parser.add_option("-I", "--maxinsts", action="store", type="int", default=None, help="""Total number of instructions to simulate (default: run forever)""")

(opts, args) = parser.parse_args()

# create the system we are going to simulate
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'               # Use timing accesses
system.mem_ranges = [AddrRange('512MB')] # Create an address range

# Create a list of CPUs
cpus = 4
cpu = [TimingSimpleCPU(cpu_id = i) for i in range(cpus)]
system.cpu = cpu

# Set the cache line size of the system
system.cache_line_size = 64

# Create a memory bus, a system crossbar
system.membus = SystemXBar()

# Create a memory bus for L2, a coherent crossbar
system.l2bus = L2XBar()

for i in range(cpus):
	# Create an L1 instruction and data cache for each CPU
    system.cpu[i].icache = L1ICache(opts)
    system.cpu[i].dcache = L1DCache(opts)
    
	# Connect the instruction and data caches to the CPU
    system.cpu[i].icache.connectCPU(system.cpu[i])
    system.cpu[i].dcache.connectCPU(system.cpu[i])

    # Hook the CPU ports up to the l2bus
    system.cpu[i].icache.connectBus(system.l2bus)
    system.cpu[i].dcache.connectBus(system.l2bus)

# Create an L2 cache and connect it to the l2bus
system.l2cache = L2Cache(opts)
system.l2cache.connectCPUSideBus(system.l2bus)

# Connect the L2 cache to the membus
system.l2cache.connectMemSideBus(system.membus)

# create the interrupt controllers for each CPU and connect to the membus
for i in range(cpus):
    # create the interrupt controller for the CPU
    system.cpu[i].createInterruptController()
    # For x86 only, make sure the interrupts are connected to the memory
    # Note: these are directly connected to the memory bus and are not cached
    if m5.defines.buildEnv['TARGET_ISA'] == "x86":
        system.cpu[i].interrupts[0].pio = system.membus.master
        system.cpu[i].interrupts[0].int_master = system.membus.slave
        system.cpu[i].interrupts[0].int_slave = system.membus.master
    # simulation period
    if opts.maxinsts:
        system.cpu[i].max_insts_any_thread = opts.maxinsts

# Connect the system up to the membus
system.system_port = system.membus.slave

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Get benchmark program from command-line
bnchmrk = opts.cmd
# Get arguments for the benchmark program from command line
arguments = []
if opts.options != "":
    arguments = opts.options.split()

# For cpu0
# Create a process
process = Process(pid = 100)
# Set the command
if len(arguments) > 0:
    process.cmd = [bnchmrk] + arguments
else:
    process.cmd = [bnchmrk]
# Set the cpu to use the process as its workload and create thread contexts
system.cpu[0].workload = process
system.cpu[0].createThreads()	
	
# For cpu1
# Create a process
process = Process(pid = 101)
# Set the command
process.cmd = ['configs/code_module_3/write_attack']
# Set the cpu to use the process as its workload and create thread contexts
system.cpu[1].workload = process
system.cpu[1].createThreads()
	
# For cpu2
# Create a process
process = Process(pid = 102)
# Set the command
process.cmd = ['configs/code_module_3/write_attack']
# Set the cpu to use the process as its workload and create thread contexts
system.cpu[2].workload = process
system.cpu[2].createThreads()
	
# For cpu3
# Create a process
process = Process(pid = 103)
# Set the command
process.cmd = ['configs/code_module_3/write_attack']
# Set the cpu to use the process as its workload and create thread contexts
system.cpu[3].workload = process
system.cpu[3].createThreads()


# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))



