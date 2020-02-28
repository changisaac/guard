from panda import Panda
panda = Panda()
print(panda.serial_read(1))



gpsLocation (
  flags = 0,
  latitude = 0,
  longitude = 0,
  altitude = 0,
  speed = 0,
  bearing = 0,
  accuracy = 0,
  timestamp = 0,
  source = android,
  verticalAccuracy = 0,
  bearingAccuracy = 0,
  speedAccuracy = 0 
 )


carState (
  vEgo = 0,
  gas = 0,
  gasPressed = false,
  brake = 0,
  brakePressed = false,
  steeringAngle = 0,
  steeringTorque = 0,
  steeringPressed = false,
  gearShifter = unknown,
  steeringRate = 0,
  aEgo = 0,
  vEgoRaw = 0,
  standstill = false,
  brakeLights = false,
  leftBlinker = false,
  rightBlinker = false,
  yawRate = 0,
  genericToggle = false,
  doorOpen = false,
  seatbeltUnlatched = false,
  canValid = false,
  steeringTorqueEps = 0,
  clutchPressed = false
)
