# fake-enigma

class slot:
	def __init__(self):
		self.list = [ ]

	def get(self):
		return self.list

	def __call__(self):
		for x in self.list:
			x()

timers = set()

import time

from events import eventfnc

##################### ENIGMA BASE

class eTimer:
	def __init__(self):
		self.timeout = slot()
		self.next_activation = None
		print "NEW TIMER"

	def start(self, msec, singleshot = False):
		print "start timer", msec
		self.next_activation = time.time() + msec / 1000.0
		self.msec = msec
		self.singleshot = singleshot
		timers.add(self)

	def stop(self):
		timers.remove(self)

	def __repr__(self):
		return "<eTimer timeout=%s next_activation=%s singleshot=%s>" % (repr(self.timeout), repr(self.next_activation), repr(self.singleshot))

	def do(self):
		if self.singleshot:
			self.stop()
		self.next_activation += self.msec / 1000.0
		self.timeout()

def runIteration():
	running_timers = list(timers)
	assert len(running_timers), "no running timers, so nothing will ever happen!"
	running_timers.sort(key=lambda x: x.next_activation)

	print "running:", running_timers

	next_timer = running_timers[0]

	now = time.time()
	delay = next_timer.next_activation - now

	if delay > 0:
		time.sleep(delay)
		now += delay

	while len(running_timers) and running_timers[0].next_activation <= now:
		running_timers[0].do()
		running_timers = running_timers[1:]

stopped = False

def stop():
	global stopped
	stopped = True

def run(duration = 1000):
	stoptimer = eTimer()
	stoptimer.start(duration * 1000.0)
	stoptimer.callback.append(stop)
	while not stopped:
		runIteration()


##################### ENIGMA GUI

eSize = None
ePoint = None
gFont = None
eWindow = None
eLabel = None
ePixmap = None
eWindowStyleManager = None
loadPNG = None
addFont = None
gRGB = None
eWindowStyleSkinned = None
eButton = None
eListboxPythonStringContent = None
eListbox = None
eSubtitleWidget = None

class eEPGCache:
	@classmethod
	def getInstance(self):
		return self.instance

	instance = None

	def __init__(self):
		eEPGCache.instance = self

	def lookupEventTime(self, ref, query):
		return None

eEPGCache()

getBestPlayableServiceReference = None

class pNavigation:
	def __init__(self):
		self.m_event = slot()
		self.m_record_event = slot()

	@eventfnc
	def recordService(self, service):
		return iRecordableService(service)

	@eventfnc
	def stopRecordService(self, service):
		service.stop()

	@eventfnc
	def playService(self, service):
		return None

	def __repr__(self):
		return "pNavigation"

eRCInput = None
getPrevAsciiCode = None

class eServiceReference:

	isDirectory=1
	mustDescent=2
	canDescent=4
	flagDirectory=isDirectory|mustDescent|canDescent
	shouldSort=8
	hasSortKey=16
	sort1=32
	isMarker=64
	isGroup=128

	def __init__(self, ref):
		self.ref = ref
		self.flags = 0

	def toString(self):
		return self.ref

	def __repr__(self):
		return self.toString()

class iRecordableService:
	def __init__(self, ref):
		self.ref = ref

	@eventfnc
	def prepare(self, filename, begin, end, event_id):
		return 0

	@eventfnc
	def start(self):
		return 0

	@eventfnc
	def stop(self):
		return 0

	def __repr__(self):
		return "iRecordableService(%s)" % repr(self.ref)

quitMainloop = None

class eAVSwitch:
	@classmethod
	def getInstance(self):
		return self.instance

	instance = None

	def __init__(self):
		eAVSwitch.instance = self

	def setColorFormat(self, value):
		print "[eAVSwitch] color format set to %d" % value

	def setAspectRatio(self, value):
		print "[eAVSwitch] aspect ratio set to %d" % value

	def setWSS(self, value):
		print "[eAVSwitch] wss set to %d" % value

	def setSlowblank(self, value):
		print "[eAVSwitch] wss set to %d" % value

	def setVideomode(self, value):
		print "[eAVSwitch] wss set to %d" % value

	def setInput(self, value):
		print "[eAVSwitch] wss set to %d" % value

eAVSwitch()

eDVBVolumecontrol = None

class eRFmod:
	@classmethod
	def getInstance(self):
		return self.instance

	instance = None

	def __init__(self):
		eRFmod.instance = self

	def setFunction(self, value):
		print "[eRFmod] set function to %d" % value

	def setTestmode(self, value):
		print "[eRFmod] set testmode to %d" % value

	def setSoundFunction(self, value):
		print "[eRFmod] set sound function to %d" % value

	def setSoundCarrier(self, value):
		print "[eRFmod] set sound carrier to %d" % value

	def setChannel(self, value):
		print "[eRFmod] set channel to %d" % value

	def setFinetune(self, value):
		print "[eRFmod] set finetune to %d" % value

eRFmod()


class eDBoxLCD:
	@classmethod
	def getInstance(self):
		return self.instance

	instance = None

	def __init__(self):
		eDBoxLCD.instance = self

	def setLCDBrightness(self, value):
		print "[eDBoxLCD] set brightness to %d" % value

	def setLCDContrast(self, value):
		print "[eDBoxLCD] set contrast to %d" % value

	def setLED(self, value):
		print "[eDBoxLCD] set led button to %d" % value

	def setInverted(self, value):
		print "[eDBoxLCD] set inverted to %d" % value

eDBoxLCD()

Misc_Options = None

class eServiceCenter:
	@classmethod
	def getInstance(self):
		return self.instance

	instance = None

	def __init__(self):
		eServiceCenter.instance = self

	def info(self, ref):
		return None

eServiceCenter()

##################### ENIGMA CHROOT

print "import directories"
import Tools.Directories
print "done"

chroot="."

for (x, (y, z)) in Tools.Directories.defaultPaths.items():
	Tools.Directories.defaultPaths[x] = (chroot + y, z)

Tools.Directories.defaultPaths[Tools.Directories.SCOPE_SKIN] = ("../data/", Tools.Directories.PATH_DONTCREATE)
Tools.Directories.defaultPaths[Tools.Directories.SCOPE_CONFIG] = ("/etc/enigma2/", Tools.Directories.PATH_DONTCREATE)

##################### ENIGMA CONFIG

print "import config"
import Components.config
print "done"

my_config = [
"config.skin.primary_skin=None\n"
]

Components.config.config.unpickle(my_config)

##################### ENIGMA ACTIONS

class eActionMap:
	def __init__(self):
		pass


##################### ENIGMA STARTUP:

def init_nav():
	print "init nav"
	import Navigation, NavigationInstance
	NavigationInstance.instance = Navigation.Navigation()

def init_record_config():
	print "init recording"
	import Components.RecordingConfig
	Components.RecordingConfig.InitRecordingConfig()

def init_parental_control():
	print "init parental"
	from Components.ParentalControl import InitParentalControl
	InitParentalControl()

def init_all():
	# this is stuff from mytest.py
	init_nav()

	init_record_config()
	init_parental_control()

	import Components.InputDevice
	Components.InputDevice.InitInputDevices()

	import Components.AVSwitch
	Components.AVSwitch.InitAVSwitch()

	import Components.UsageConfig
	Components.UsageConfig.InitUsageConfig()

	import Components.Network
	Components.Network.InitNetwork()

	import Components.Lcd
	Components.Lcd.InitLcd()

	import Components.SetupDevices
	Components.SetupDevices.InitSetupDevices()

	import Components.RFmod
	Components.RFmod.InitRFmod()

	import Screens.Ci
	Screens.Ci.InitCiConfig()

class eInputDeviceManager(iObject):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    FEATURE_UNCONNECTED_KEYPRESS = _enigma.eInputDeviceManager_FEATURE_UNCONNECTED_KEYPRESS

    def getInstance():
        """getInstance() -> eInputDeviceManager"""
        return _enigma.eInputDeviceManager_getInstance()

    getInstance = staticmethod(getInstance)

    def start(self):
        """start(eInputDeviceManager self)"""
        return _enigma.eInputDeviceManager_start(self)


    def stop(self):
        """stop(eInputDeviceManager self)"""
        return _enigma.eInputDeviceManager_stop(self)


    def hasFeature(self, feature):
        """hasFeature(eInputDeviceManager self, int feature) -> bool"""
        return _enigma.eInputDeviceManager_hasFeature(self, feature)


    def available(self):
        """available(eInputDeviceManager self) -> bool"""
        return _enigma.eInputDeviceManager_available(self)


    def responding(self):
        """responding(eInputDeviceManager self) -> bool"""
        return _enigma.eInputDeviceManager_responding(self)


    def version(self):
        """version(eInputDeviceManager self) -> std::string"""
        return _enigma.eInputDeviceManager_version(self)


    def getDevice(self, address):
        """getDevice(eInputDeviceManager self, std::string const & address) -> eManagedInputDevicePtr"""
        return _enigma.eInputDeviceManager_getDevice(self, address)


    def getConnectedDevices(self):
        """getConnectedDevices(eInputDeviceManager self) -> eManagedInputDevicePtrList"""
        return _enigma.eInputDeviceManager_getConnectedDevices(self)


    def getAvailableDevices(self):
        """getAvailableDevices(eInputDeviceManager self) -> eManagedInputDevicePtrList"""
        return _enigma.eInputDeviceManager_getAvailableDevices(self)


    def rescan(self):
        """rescan(eInputDeviceManager self)"""
        return _enigma.eInputDeviceManager_rescan(self)


    def connectDevice(self, device):
        """connectDevice(eInputDeviceManager self, eManagedInputDevicePtr device)"""
        return _enigma.eInputDeviceManager_connectDevice(self, device)


    def disconnectDevice(self, device):
        """disconnectDevice(eInputDeviceManager self, eManagedInputDevicePtr device)"""
        return _enigma.eInputDeviceManager_disconnectDevice(self, device)


    def vibrate(self, device=0):
        """
        vibrate(eInputDeviceManager self, eManagedInputDevicePtr device=0)
        vibrate(eInputDeviceManager self)
        """
        return _enigma.eInputDeviceManager_vibrate(self, device)


    def setLedColor(self, *args):
        """
        setLedColor(eInputDeviceManager self, uint32_t rgb)
        setLedColor(eInputDeviceManager self, eManagedInputDevicePtr device, uint32_t rgb)
        """
        return _enigma.eInputDeviceManager_setLedColor(self, *args)


    def setLedColorIr(self, *args):
        """
        setLedColorIr(eInputDeviceManager self, uint32_t rgb)
        setLedColorIr(eInputDeviceManager self, eManagedInputDevicePtr device, uint32_t rgb)
        """
        return _enigma.eInputDeviceManager_setLedColorIr(self, *args)


    def setIrProtocol(self, device, isRepeat, irProtocol):
        """setIrProtocol(eInputDeviceManager self, eManagedInputDevicePtr device, bool isRepeat, IrProtocol irProtocol)"""
        return _enigma.eInputDeviceManager_setIrProtocol(self, device, isRepeat, irProtocol)


    def setIrKey(self, device, irKey):
        """setIrKey(eInputDeviceManager self, eManagedInputDevicePtr device, IrKey irKey)"""
        return _enigma.eInputDeviceManager_setIrKey(self, device, irKey)


    def resetIr(self, device):
        """resetIr(eInputDeviceManager self, eManagedInputDevicePtr device)"""
        return _enigma.eInputDeviceManager_resetIr(self, device)


    def getIrKeyCount(self, device):
        """getIrKeyCount(eInputDeviceManager self, eManagedInputDevicePtr device)"""
        return _enigma.eInputDeviceManager_getIrKeyCount(self, device)

    deviceStateChanged = _swig_property(_enigma.eInputDeviceManager_deviceStateChanged_get, _enigma.eInputDeviceManager_deviceStateChanged_set)
    unboundRemoteKeyPressed = _swig_property(_enigma.eInputDeviceManager_unboundRemoteKeyPressed_get, _enigma.eInputDeviceManager_unboundRemoteKeyPressed_set)
    irKeyCount = _swig_property(_enigma.eInputDeviceManager_irKeyCount_get, _enigma.eInputDeviceManager_irKeyCount_set)
    batteryLow = _swig_property(_enigma.eInputDeviceManager_batteryLow_get, _enigma.eInputDeviceManager_batteryLow_set)
    deviceListChanged = _swig_property(_enigma.eInputDeviceManager_deviceListChanged_get, _enigma.eInputDeviceManager_deviceListChanged_set)
eInputDeviceManager.start = new_instancemethod(_enigma.eInputDeviceManager_start, None, eInputDeviceManager)
eInputDeviceManager.stop = new_instancemethod(_enigma.eInputDeviceManager_stop, None, eInputDeviceManager)
eInputDeviceManager.hasFeature = new_instancemethod(_enigma.eInputDeviceManager_hasFeature, None, eInputDeviceManager)
eInputDeviceManager.available = new_instancemethod(_enigma.eInputDeviceManager_available, None, eInputDeviceManager)
eInputDeviceManager.responding = new_instancemethod(_enigma.eInputDeviceManager_responding, None, eInputDeviceManager)
eInputDeviceManager.version = new_instancemethod(_enigma.eInputDeviceManager_version, None, eInputDeviceManager)
eInputDeviceManager.getDevice = new_instancemethod(_enigma.eInputDeviceManager_getDevice, None, eInputDeviceManager)
eInputDeviceManager.getConnectedDevices = new_instancemethod(_enigma.eInputDeviceManager_getConnectedDevices, None, eInputDeviceManager)
eInputDeviceManager.getAvailableDevices = new_instancemethod(_enigma.eInputDeviceManager_getAvailableDevices, None, eInputDeviceManager)
eInputDeviceManager.rescan = new_instancemethod(_enigma.eInputDeviceManager_rescan, None, eInputDeviceManager)
eInputDeviceManager.connectDevice = new_instancemethod(_enigma.eInputDeviceManager_connectDevice, None, eInputDeviceManager)
eInputDeviceManager.disconnectDevice = new_instancemethod(_enigma.eInputDeviceManager_disconnectDevice, None, eInputDeviceManager)
eInputDeviceManager.vibrate = new_instancemethod(_enigma.eInputDeviceManager_vibrate, None, eInputDeviceManager)
eInputDeviceManager.setLedColor = new_instancemethod(_enigma.eInputDeviceManager_setLedColor, None, eInputDeviceManager)
eInputDeviceManager.setLedColorIr = new_instancemethod(_enigma.eInputDeviceManager_setLedColorIr, None, eInputDeviceManager)
eInputDeviceManager.setIrProtocol = new_instancemethod(_enigma.eInputDeviceManager_setIrProtocol, None, eInputDeviceManager)
eInputDeviceManager.setIrKey = new_instancemethod(_enigma.eInputDeviceManager_setIrKey, None, eInputDeviceManager)
eInputDeviceManager.resetIr = new_instancemethod(_enigma.eInputDeviceManager_resetIr, None, eInputDeviceManager)
eInputDeviceManager.getIrKeyCount = new_instancemethod(_enigma.eInputDeviceManager_getIrKeyCount, None, eInputDeviceManager)
eInputDeviceManager_swigregister = _enigma.eInputDeviceManager_swigregister
eInputDeviceManager_swigregister(eInputDeviceManager)

def eInputDeviceManager_getInstance():
    """eInputDeviceManager_getInstance() -> eInputDeviceManager"""
    return _enigma.eInputDeviceManager_getInstance()

class eManagedInputDevicePtrList(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __iter__(self):
        return self.iterator()

    def __init__(self, *args):
        _enigma.eManagedInputDevicePtrList_swiginit(self, _enigma.new_eManagedInputDevicePtrList(*args))
    __swig_destroy__ = _enigma.delete_eManagedInputDevicePtrList
eManagedInputDevicePtrList.iterator = new_instancemethod(_enigma.eManagedInputDevicePtrList_iterator, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__nonzero__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___nonzero__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__bool__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___bool__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__len__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___len__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__getslice__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___getslice__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__setslice__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___setslice__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__delslice__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___delslice__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__delitem__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___delitem__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__getitem__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___getitem__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.__setitem__ = new_instancemethod(_enigma.eManagedInputDevicePtrList___setitem__, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.pop = new_instancemethod(_enigma.eManagedInputDevicePtrList_pop, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.append = new_instancemethod(_enigma.eManagedInputDevicePtrList_append, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.empty = new_instancemethod(_enigma.eManagedInputDevicePtrList_empty, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.size = new_instancemethod(_enigma.eManagedInputDevicePtrList_size, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.swap = new_instancemethod(_enigma.eManagedInputDevicePtrList_swap, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.begin = new_instancemethod(_enigma.eManagedInputDevicePtrList_begin, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.end = new_instancemethod(_enigma.eManagedInputDevicePtrList_end, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.rbegin = new_instancemethod(_enigma.eManagedInputDevicePtrList_rbegin, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.rend = new_instancemethod(_enigma.eManagedInputDevicePtrList_rend, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.clear = new_instancemethod(_enigma.eManagedInputDevicePtrList_clear, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.get_allocator = new_instancemethod(_enigma.eManagedInputDevicePtrList_get_allocator, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.pop_back = new_instancemethod(_enigma.eManagedInputDevicePtrList_pop_back, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.erase = new_instancemethod(_enigma.eManagedInputDevicePtrList_erase, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.push_back = new_instancemethod(_enigma.eManagedInputDevicePtrList_push_back, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.front = new_instancemethod(_enigma.eManagedInputDevicePtrList_front, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.back = new_instancemethod(_enigma.eManagedInputDevicePtrList_back, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.assign = new_instancemethod(_enigma.eManagedInputDevicePtrList_assign, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.resize = new_instancemethod(_enigma.eManagedInputDevicePtrList_resize, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.insert = new_instancemethod(_enigma.eManagedInputDevicePtrList_insert, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.pop_front = new_instancemethod(_enigma.eManagedInputDevicePtrList_pop_front, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.push_front = new_instancemethod(_enigma.eManagedInputDevicePtrList_push_front, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList.reverse = new_instancemethod(_enigma.eManagedInputDevicePtrList_reverse, None, eManagedInputDevicePtrList)
eManagedInputDevicePtrList_swigregister = _enigma.eManagedInputDevicePtrList_swigregister
eManagedInputDevicePtrList_swigregister(eManagedInputDevicePtrList)

class IrProtocol(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    carrier_period = _swig_property(_enigma.IrProtocol_carrier_period_get, _enigma.IrProtocol_carrier_period_set)
    carrier_low = _swig_property(_enigma.IrProtocol_carrier_low_get, _enigma.IrProtocol_carrier_low_set)
    toggle_mask = _swig_property(_enigma.IrProtocol_toggle_mask_get, _enigma.IrProtocol_toggle_mask_set)
    startbits = _swig_property(_enigma.IrProtocol_startbits_get, _enigma.IrProtocol_startbits_set)
    start_ontime = _swig_property(_enigma.IrProtocol_start_ontime_get, _enigma.IrProtocol_start_ontime_set)
    start_totaltime = _swig_property(_enigma.IrProtocol_start_totaltime_get, _enigma.IrProtocol_start_totaltime_set)
    one_ontime = _swig_property(_enigma.IrProtocol_one_ontime_get, _enigma.IrProtocol_one_ontime_set)
    one_totaltime = _swig_property(_enigma.IrProtocol_one_totaltime_get, _enigma.IrProtocol_one_totaltime_set)
    zero_ontime = _swig_property(_enigma.IrProtocol_zero_ontime_get, _enigma.IrProtocol_zero_ontime_set)
    zero_totaltime = _swig_property(_enigma.IrProtocol_zero_totaltime_get, _enigma.IrProtocol_zero_totaltime_set)
    stopbits = _swig_property(_enigma.IrProtocol_stopbits_get, _enigma.IrProtocol_stopbits_set)
    stop_ontime = _swig_property(_enigma.IrProtocol_stop_ontime_get, _enigma.IrProtocol_stop_ontime_set)
    stop_totaltime = _swig_property(_enigma.IrProtocol_stop_totaltime_get, _enigma.IrProtocol_stop_totaltime_set)
    repeat_ms = _swig_property(_enigma.IrProtocol_repeat_ms_get, _enigma.IrProtocol_repeat_ms_set)
    repeat_id = _swig_property(_enigma.IrProtocol_repeat_id_get, _enigma.IrProtocol_repeat_id_set)
    IR_PROTO_NEC = _enigma.IrProtocol_IR_PROTO_NEC
    IR_PROTO_SIRC = _enigma.IrProtocol_IR_PROTO_SIRC
    IR_PROTO_JVC = _enigma.IrProtocol_IR_PROTO_JVC
    IR_PROTO_RC5 = _enigma.IrProtocol_IR_PROTO_RC5
    IR_PROTO_REP_NEC = _enigma.IrProtocol_IR_PROTO_REP_NEC
    IR_PROTO_REP_JVC = _enigma.IrProtocol_IR_PROTO_REP_JVC
    IR_PROTO_CUSTOM = _enigma.IrProtocol_IR_PROTO_CUSTOM
    IR_PROTO_REP_CUSTOM = _enigma.IrProtocol_IR_PROTO_REP_CUSTOM

    def __init__(self, carr_period, carr_low, tggl_mask, strtbits, start_on, start_total, one_on, one_total, zero_on, zero_total, stopbts, stop_on, stop_total, repeat_millis, repeat_proto_id):
        """__init__(IrProtocol self, uint16_t carr_period, uint16_t carr_low, uint32_t tggl_mask, uint8_t strtbits, uint16_t start_on, uint16_t start_total, uint16_t one_on, uint16_t one_total, uint16_t zero_on, uint16_t zero_total, uint8_t stopbts, uint16_t stop_on, uint16_t stop_total, uint8_t repeat_millis, uint8_t repeat_proto_id) -> IrProtocol"""
        _enigma.IrProtocol_swiginit(self, _enigma.new_IrProtocol(carr_period, carr_low, tggl_mask, strtbits, start_on, start_total, one_on, one_total, zero_on, zero_total, stopbts, stop_on, stop_total, repeat_millis, repeat_proto_id))
    __swig_destroy__ = _enigma.delete_IrProtocol
IrProtocol_swigregister = _enigma.IrProtocol_swigregister
IrProtocol_swigregister(IrProtocol)

class IrKey(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    CODE_POWER = _enigma.IrKey_CODE_POWER
    CODE_MODE = _enigma.IrKey_CODE_MODE
    CODE_MUTE = _enigma.IrKey_CODE_MUTE
    CODE_1 = _enigma.IrKey_CODE_1
    CODE_2 = _enigma.IrKey_CODE_2
    CODE_3 = _enigma.IrKey_CODE_3
    CODE_4 = _enigma.IrKey_CODE_4
    CODE_5 = _enigma.IrKey_CODE_5
    CODE_6 = _enigma.IrKey_CODE_6
    CODE_7 = _enigma.IrKey_CODE_7
    CODE_8 = _enigma.IrKey_CODE_8
    CODE_9 = _enigma.IrKey_CODE_9
    CODE_0 = _enigma.IrKey_CODE_0
    CODE_REWIND = _enigma.IrKey_CODE_REWIND
    CODE_FASTFORWARD = _enigma.IrKey_CODE_FASTFORWARD
    CODE_VOLUMEUP = _enigma.IrKey_CODE_VOLUMEUP
    CODE_VOLUMEDOWN = _enigma.IrKey_CODE_VOLUMEDOWN
    CODE_EXIT = _enigma.IrKey_CODE_EXIT
    CODE_CHANNELUP = _enigma.IrKey_CODE_CHANNELUP
    CODE_CHANNELDOWN = _enigma.IrKey_CODE_CHANNELDOWN
    CODE_INFO = _enigma.IrKey_CODE_INFO
    CODE_MENU = _enigma.IrKey_CODE_MENU
    CODE_AUDIO = _enigma.IrKey_CODE_AUDIO
    CODE_VIDEO = _enigma.IrKey_CODE_VIDEO
    CODE_UP = _enigma.IrKey_CODE_UP
    CODE_DOWN = _enigma.IrKey_CODE_DOWN
    CODE_LEFT = _enigma.IrKey_CODE_LEFT
    CODE_RIGHT = _enigma.IrKey_CODE_RIGHT
    CODE_OK = _enigma.IrKey_CODE_OK
    CODE_RED = _enigma.IrKey_CODE_RED
    CODE_GREEN = _enigma.IrKey_CODE_GREEN
    CODE_YELLOW = _enigma.IrKey_CODE_YELLOW
    CODE_BLUE = _enigma.IrKey_CODE_BLUE
    CODE_PREVIOUSSONG = _enigma.IrKey_CODE_PREVIOUSSONG
    CODE_PLAY = _enigma.IrKey_CODE_PLAY
    CODE_STOP = _enigma.IrKey_CODE_STOP
    CODE_NEXSONG = _enigma.IrKey_CODE_NEXSONG
    CODE_TEXT = _enigma.IrKey_CODE_TEXT
    CODE_RECORD = _enigma.IrKey_CODE_RECORD
    keycode = _swig_property(_enigma.IrKey_keycode_get, _enigma.IrKey_keycode_set)
    protocol_id = _swig_property(_enigma.IrKey_protocol_id_get, _enigma.IrKey_protocol_id_set)
    make_msg = _swig_property(_enigma.IrKey_make_msg_get, _enigma.IrKey_make_msg_set)
    make_len = _swig_property(_enigma.IrKey_make_len_get, _enigma.IrKey_make_len_set)
    break_msg = _swig_property(_enigma.IrKey_break_msg_get, _enigma.IrKey_break_msg_set)
    break_len = _swig_property(_enigma.IrKey_break_len_get, _enigma.IrKey_break_len_set)

    def __init__(self, keycode, proto_id, make_message, make_message_len, break_message, break_message_len):
        """__init__(IrKey self, int32_t keycode, uint8_t proto_id, uint32_t make_message, uint8_t make_message_len, uint32_t break_message, uint8_t break_message_len) -> IrKey"""
        _enigma.IrKey_swiginit(self, _enigma.new_IrKey(keycode, proto_id, make_message, make_message_len, break_message, break_message_len))
    __swig_destroy__ = _enigma.delete_IrKey
IrKey_swigregister = _enigma.IrKey_swigregister
IrKey_swigregister(IrKey)
	
