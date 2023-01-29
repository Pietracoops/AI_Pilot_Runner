import processing
import pathlib
import os


parameter_ont2cae_scaling = {
               'SideStickPositionX': '1', # Units may be wrong
               'SideStickPositionY': '1', # Units may be wrong
               'Engine1FireSwitch': '1',
               'Engine2FireSwitch': '1',
               'Engine2MasterSwitchPosition': '1',
               'Engine1MasterSwitchPosition': '1',
               'EGT': '1',
               'AutoThrustMode': '1',
               'AutoPilotMasterSwitch': '1',
               'AltitudeMode': '1',
               'Agent2Switch': '1',
               'Agent1Switch': '1',
               'ParkBrakePosition': '1',
               'SpeedBrakeLeverPosition': '1',
               'Brake': '1', # Need to validate this
               'LandingGearLeverPosition': '1',
               'Speed': '1',
               'SpeedTrend': '1',
               'VSIIndicator': '1',
               'VSIIndication': '1',
               'RadioAltitude': '1',
               'SpoilerMode': '1',
               'TCASMode': '1',
               'VisualIndication': '1',
               'trimDirection': '1',
               'MasterSwitchWarningSwitchPress': '1',  # This is probably wrong
               'RadioTransmitting': '1',
               'TailWind':'1',
               'CrossWind':'1',
               'VerballyAnnounce': '1',
               'Engine1Failure': '1',# this might not be accurate
               'Engine2Failure': '1',# this might not be accurate
               'LandingGearPosition':'1',
               'Airspeed':'1',
               'LeftThrustLever':'100', # This should be Engine1ThrustLever
               'RightThrustLever':'100', # This should be Engine2ThrustLever
               'TimeInterval': '1', # What is this!
               'FMAIndication': '1',
               'FMSDirection': '1',
               'Altitude':'1',
               'FlapLever':'1',
               'PFD': '1',
               'TCASAlert': '1',
               'RudderPedals':'1', # This label was made up by me (units may also be wrong)
               'Pitch':'1',
               'WindShearWarning':'1'
}

action_ont2cae_dict = {
               'SideStickPositionX': 'StandardAircraft/ControlLateralPosition', # Units may be wrong
               'SideStickPositionY': 'StandardAircraft/ControlLongitudinalPosition', # Units may be wrong
               'Engine1FireSwitch': 'Vehicle/Ancillaries/Lighting/EngineFire/Pushbutton/1',
               'Engine2FireSwitch': 'Vehicle/Ancillaries/Lighting/EngineFire/Pushbutton/2',
               'Engine2MasterSwitchPosition': 'None_1',
               'Engine1MasterSwitchPosition': 'None_2',
               'EGT': 'None_3',
               'AutoThrustMode': 'StandardAircraft/AutothrottleOn',
               'AutoPilotMasterSwitch': 'StandardAircraft/AutopilotOn',
               'AltitudeMode': 'Vehicle/Autopilot/FCU/Altitude/Selected/1',
               'Agent2Switch': 'Vehicle/Ancillaries/Lighting/EngineFire/Pushbutton/2',
               'Agent1Switch': 'Vehicle/Ancillaries/Lighting/EngineFire/Pushbutton/1',
               'ParkBrakePosition': 'StandardAircraft/ParkingBrakeActive',
               'SpeedBrakeLeverPosition': 'StandardAircraft/SpeedBrakeActive',
               'Brake': 'StandardAircraft/BrakePressureCaptain', # Need to validate this
               'LandingGearLeverPosition': 'StandardAircraft/LandingGearsHandlePosition',
               'Speed': 'StandardAircraft/GroundSpeedU',
               'SpeedTrend': 'None_4',
               'VSIIndicator': 'StandardAircraft/RateOfClimb',
               'VSIIndication': 'None_5',
               'RadioAltitude': 'StandardAircraft/AltitudeAGL',
               'SpoilerMode': 'None_6',
               'TCASMode': 'StandardAircraft/TCASMode',
               'VisualIndication': 'None_7',
               'trimDirection': 'None_8',
               'MasterSwitchWarningSwitchPress': 'StandardAircraft/MasterCautionOn',  # This is probably wrong
               'RadioTransmitting': 'None_9',
               'TailWind':'StandardAircraft/WindV',
               'CrossWind':'StandardAircraft/WindU',
               'VerballyAnnounce': 'None_10',
               'Engine1Failure': 'StandardAircraft/Engine1FlameOut',# this might not be accurate
               'Engine2Failure': 'StandardAircraft/Engine2FlameOut',# this might not be accurate
               'LandingGearPosition':'StandardAircraft/LandingGearsHandlePosition',
               'Airspeed':'StandardAircraft/AirspeedU',
               #'LeftThrustLever':'StandardAircraft/Engine1ThrustLeverAngle', # This should be Engine1ThrustLever
               #'RightThrustLever':'StandardAircraft/Engine2ThrustLeverAngle', # This should be Engine2ThrustLever
               'LeftThrustLever':'StandardAircraft/Engine1N1', # This should be Engine1ThrustLever
               'RightThrustLever':'StandardAircraft/Engine2N1', # This should be Engine2ThrustLever
               'TimeInterval': 'None_11', # What is this!
               'FMAIndication': 'None_12',
               'FMSDirection': 'None_13',
               'Altitude':'StandardAircraft/AltitudeAGL',
               'FlapLever':'StandardAircraft/FlapsHandlePosition',
               'PFD': 'None_14',
               'TCASAlert': 'None_15',
               'RudderPedals':'StandardAircraft/ControlDirectionalPosition', # This label was made up by me (units may also be wrong)
               'Pitch':'StandardAircraft/PitchAngle',
               'WindShearWarning':'StandardAircraft/WindshearPredictiveWarningOn'
               } 

action_cae2ont_dict = {}


cae_log_vars = ["Vehicle/Ancillaries/Lighting/APUFire/Pushbutton",
                "StandardAircraft/BrakePressureCaptain",
                "StandardAircraft/BrakePressureFirstOfficer",
                "StandardAircraft/SpeedBrakeActive",
                "StandardAircraft/ParkingBrakeActive",
                "StandardAircraft/EvacuationCommandOn",
                "StandardAircraft/RadioPassengerActive",
                "StandardAircraft/RadioVhfActive",
                "Vehicle/Ancillaries/Lighting/EngineFire/Pushbutton/1",
                "Vehicle/Ancillaries/Lighting/EngineFire/Pushbutton/2",
                "StandardAircraft/FlapsHandlePosition",
                "StandardAircraft/FlapsFault",
                "StandardAircraft/SlatsPosition",
                "Vehicle/Avionics/EGPWS/FlapOverride/Switch/2",
                "StandardAircraft/ControlLateralPosition",
                "StandardAircraft/ControlLongitudinalPosition",
                "Vehicle/FlightCtrl/EFCS/ELAC/SideStick/Pitch/Captain",
                "Vehicle/FlightCtrl/EFCS/ELAC/SideStick/Pitch/FirstOfficer",
                "StandardAircraft/ControlDirectionalPosition",
                'Vehicle/FlightCtrl/EFCS/ELAC/SideStick/Pitch/Captain',
                'StandardAircraft/AutothrottleOn',
                'Vehicle/Autopilot/FCU/Altitude/Selected/1',
                'StandardAircraft/AutopilotOn',
                'Vehicle/Autopilot/FCU/Altitude/Selected/1',
                'StandardAircraft/LandingGearsHandlePosition',
                'StandardAircraft/GroundSpeedU',
                'StandardAircraft/RateOfClimb',
                'StandardAircraft/AltitudeAGL',
                'StandardAircraft/TCASMode',
                'StandardAircraft/MasterCautionOn']

cae_log_inputs = ["Vehicle/Ancillaries/Lighting/APUFire/Pushbutton",
                  "StandardAircraft/BrakePressureCaptain",
                  "StandardAircraft/BrakePressureFirstOfficer",
                  "StandardAircraft/SpeedBrakeActive",
                  "StandardAircraft/ParkingBrakeActive",
                  "StandardAircraft/EvacuationCommandOn",
                  "StandardAircraft/RadioPassengerActive",
                  "StandardAircraft/RadioVhfActive",
                  "Vehicle/Ancillaries/Lighting/EngineFire/Pushbutton/1",
                  "Vehicle/Ancillaries/Lighting/EngineFire/Pushbutton/2",
                  "StandardAircraft/FlapsHandlePosition",
                  "StandardAircraft/FlapsFault",
                  "StandardAircraft/SlatsPosition",
                  "Vehicle/Avionics/EGPWS/FlapOverride/Switch/2",
                  "StandardAircraft/ControlLateralPosition",
                  "StandardAircraft/ControlLongitudinalPosition",
                  #"Vehicle/FlightCtrl/EFCS/ELAC/SideStick/Pitch/Captain",
                  #"Vehicle/FlightCtrl/EFCS/ELAC/SideStick/Pitch/FirstOfficer",
                  "StandardAircraft/ControlDirectionalPosition",
                  "StandardAircraft/FMSApproachType",
                  "StandardAircraft/AutothrottleOn",
                  "StandardAircraft/AutolandOn",
                  "StandardAircraft/AutopilotOn",
                  "Vehicle/Autopilot/FCU/Altitude/Selected/1",
                  "Vehicle/Ancillaries/Brake/AutoBrake/Active",
                  "Vehicle/Avionics/TCAS/ResolutionAdvisory/VerticalSpeed/Target",
                  "StandardAircraft/TCASMode",
                  "StandardAircraft/FlareModeOn",
                  "StandardAircraft/FlightDirectorOn",
                  "StandardAircraft/LandingGearsHandlePosition",]

cae_log_context = ["StandardAircraft/Engine1FlameOut",
                    "StandardAircraft/Engine2FlameOut",
                    "StandardAircraft/EngineAllFlameOut",
                    "StandardAircraft/EngineFlameOut",
                    "StandardAircraft/CloudLayerBaseAltitudeAGL",
                    "StandardAircraft/RunwayVisualRange",
                    "StandardAircraft/BrakingAction",
                    "StandardAircraft/TouchdownZoneVisible",
                    "StandardAircraft/SlatsFault",
                    "StandardAircraft/StabilizerFault",
                    "Vehicle/ISS/Glideslope/Fail",
                    "StandardAircraft/HydraulicGreenEnginePumpFault",
                    "StandardAircraft/HydraulicYellowEnginePumpFault",
                    "StandardAircraft/HydraulicYellowElectricalPumpFault",
                    "StandardAircraft/HydraulicBlueElectricalPumpFault",
                    "StandardAircraft/HydraulicPowerTransferUnitFault",
                    "Vehicle/Malf/SideStick/Fault/Captain",
                    "Vehicle/Malf/SideStick/Fault/FirstOfficer",
                    "Vehicle/Malf/Engine/BirdStrike/HighVibrations/Left",
                    "Vehicle/Malf/Engine/BirdStrike/HighVibrations/Right",
                    "Vehicle/Malf/Engine/BirdStrike/Stall/Left",
                    "Vehicle/Malf/Engine/BirdStrike/Stall/Right",
                    "Vehicle/Malf/Engine/SeriousDamage/AbruptPowerLoss/Left",
                    "Vehicle/Malf/Engine/SeriousDamage/AbruptPowerLoss/Right",
                    "Vehicle/Malf/Engine/SeriousDamage/UnextinguishableFire/Left",
                    "Vehicle/Malf/Engine/SeriousDamage/UnextinguishableFire/Right",
                    "Vehicle/Malf/Engine/Fire/ExtFirst/Left",
                    "Vehicle/Malf/Engine/Fire/ExtFirst/Right",
                    "Vehicle/Malf/Engine/FireExtSec/Left",
                    "Vehicle/Malf/Engine/FireExtSec/Right",
                    "Vehicle/Malf/Engine/FireUnext/Left",
                    "Vehicle/Malf/Engine/FireUnext/Right",
                    "Vehicle/Malf/EngFlameOut/NoDamage/Left",
                    "Vehicle/Malf/EngFlameOut/NoDamage/Right",
                    "Vehicle/Malf/EngFlameOut/Damage/Left",
                    "Vehicle/Malf/EngFlameOut/Damage/Right",
                    "Vehicle/Malf/ThrustReverser/Fault/Left",
                    "Vehicle/Malf/ThrustReverser/Fault/Right",
                    "Vehicle/Malf/ThrustLever/Fault/Left",
                    "Vehicle/Malf/ThrustLever/Fault/Right",
                    "Vehicle/Malf/AlternateLaw",
                    "Vehicle/Malf/DirectLaw",
                    "Vehicle/Malf/EGPWS/Fault",
                    "Vehicle/Malf/APUFireExt",
                    "Vehicle/Malf/APUFireUnext",
                    "Vehicle/Malf/Electrical/Apu/Fault",
                    "Vehicle/Malf/CargoFire/Aft",
                    "Vehicle/Malf/CargoFire/Fwd",
                    "Vehicle/Malf/Avionic/Smoke",
                    "StandardAircraft/RunwayLength",
                    "StandardAircraft/RunwayWidth",
                    "StandardAircraft/RunwayHeading",
                    "SyntheticEnv/RadioAids/Runway/FarEndLongitude",
                    "SyntheticEnv/RadioAids/Runway/FarEndLatitude",
                    "StandardAircraft/VspeedV1",    # The speed beyond which takeoff should no longer be aborted.
                    "StandardAircraft/VspeedV2",    # Takeoff safety speed. The speed at which the aircraft may safely climb with one engine inoperative.
                    "StandardAircraft/VspeedVr",    # Rotation speed. The speed at which the pilot begins to apply control inputs to cause the aircraft nose to pitch up, after which it will leave the ground
                    "StandardAircraft/VspeedVNE",   # Maximum operating limit speed.
                    "StandardAircraft/VspeedVMO",   # Never exceed speed.
                    "StandardAircraft/VspeedVAPP",  # Approach speed. Speed used during final approach with landing flap set
                    "StandardAircraft/VspeedVLS",   # Lowest selectable speed
                    "StandardAircraft/VspeedGreenDot",  # Speed allowing the highest climb gradient with one engine inoperative in clean configuration.
                    "StandardAircraft/WeightGross",
                    "StandardAircraft/WeightMaximumLanding",
                    "StandardAircraft/WindU",
                    "StandardAircraft/WindV",
                    "StandardAircraft/WindHorizontal",
                    "StandardAircraft/WindVertical",
                    "StandardAircraft/WindshearPredictiveWarningOn",
                    "StandardAircraft/WindshearReactiveWarningOn",
                    "Ownship/Flight/WindshearTriggered",
                    "Vehicle/FlightCtrl/FltWarn/AlphaMax/Speed"]

cae_log_aircraft_state = ["StandardAircraft/AngleOfAttack",
                            "StandardAircraft/AngleOfSideslip",
                            "StandardAircraft/PitchAngle",
                            "StandardAircraft/PitchRate",
                            "StandardAircraft/BankAngle",
                            "StandardAircraft/RollRate",
                            "StandardAircraft/Heading",
                            "StandardAircraft/YawRate",
                            "StandardAircraft/AirspeedU",
                            "StandardAircraft/AirspeedV",
                            "StandardAircraft/AirspeedW",
                            "StandardAircraft/GroundSpeedU",
                            "StandardAircraft/RateOfClimb",
                            "StandardAircraft/GforceU",
                            "StandardAircraft/GforceV",
                            "StandardAircraft/GforceW",
                            "StandardAircraft/Latitude",
                            "StandardAircraft/Longitude",
                            "StandardAircraft/AltitudeAGL",
                            "StandardAircraft/AltitudeMSL",
                            "StandardAircraft/AltitudePressure",
                            "StandardAircraft/AltitudeAboveRunwayThreshold",
                            "StandardAircraft/AirspeedIndicated",
                            "StandardAircraft/AirspeedCalibrated",
                            "StandardAircraft/AirspeedTrue",
                            "StandardAircraft/Mach",
                            "StandardAircraft/GroundSpeed",
                            "Vehicle/FlightInstr/ADC/ComputedAirspeed/1/LeftChannel/Value",
                            "Vehicle/FlightInstr/ADC/ComputedAirspeed/1/RightChannel/Value",
                            "Vehicle/AircraftDisplays/EIS/VerticalSpeed/TCASTarget/Green",
                            "Vehicle/Ancillaries/Lighting/TAWS/Warning/Light/On",
                            "Vehicle/Avionics/EGPWS/WarningActive",
                            "StandardAircraft/Engine1N1",
                            "StandardAircraft/Engine2N1",
                            "StandardAircraft/Engine1ThrustLeverAngle",
                            "StandardAircraft/Engine2ThrustLeverAngle",
                            "StandardAircraft/EngineAllReverserFault",
                            "StandardAircraft/EngineFireWarningActive",
                            "StandardAircraft/NoseWheelSteeringAngle",
                            "StandardAircraft/FlightDirectorPitchError",
                            "StandardAircraft/TrackDeviationLateral",
                            "StandardAircraft/TrackDeviationVertical",
                            "StandardAircraft/DistanceToTouchdown",
                            "StandardAircraft/DistanceToRunwayEnd",
                            "StandardAircraft/LateralDeviationRunwayCenterline",
                            "StandardAircraft/ApproachPathLateralAngle",
                            "StandardAircraft/ApproachPathLateralAngleDeviation",
                            "StandardAircraft/ApproachPathLateralAngleTarget",
                            "StandardAircraft/ApproachPathVerticalAngle",
                            "StandardAircraft/ApproachPathVerticalAngleDeviation",
                            "StandardAircraft/ApproachPathVerticalAngleSelected",
                            "StandardAircraft/ApproachPathVerticalAngleTarget",
                            "StandardAircraft/Track",
                            "StandardAircraft/Drift",
                            "StandardAircraft/DriftRunway",
                            "Vehicle/Flight/Ground/Force/Gear/Left",
                            "Vehicle/Flight/Ground/Force/Gear/Nose",
                            "Vehicle/Flight/Ground/Force/Gear/Right",
                            "StandardAircraft/CrashState",
                            "StandardAircraft/CrashActive",
                            "StandardAircraft/TailStrikeState",
                            "StandardAircraft/GlideslopeDeviation",
                            "StandardAircraft/GlideslopeTrackActive",
                            "StandardAircraft/HydraulicGreenPressure",
                            "StandardAircraft/HydraulicYellowPressure",
                            "StandardAircraft/HydraulicBluePressure",
                            "StandardAircraft/HydraulicBluePressureLow",
                            "StandardAircraft/HydraulicGreenPressureLow",
                            "StandardAircraft/HydraulicYellowPressureLow",
                            "StandardAircraft/TirePressureLow",
                            "StandardAircraft/LandingGearsCollapseOn",
                            "StandardAircraft/LocalizerDeviation",
                            "StandardAircraft/LocalizerTrackActive",
                            "StandardAircraft/MasterCautionOn",
                            "StandardAircraft/MinimumDecisionAltitudeAGL",
                            "StandardAircraft/MinimumDecisionAltitudeMSL",
                            "StandardAircraft/MinimumDecisionAltitudePressure",
                            "SyntheticEnv/RadioAids/Runway/EndToThreshold",
                            "StandardAircraft/AircraftOnGround",
                            "StandardAircraft/AircraftOnGroundAccurate",
                            "Ownship/Flight/AircraftOnGround",
                            "StandardAircraft/StallWarningOn",
                            "Vehicle/Pressurization/CabinPressure/CabinAltitude",
                            "Vehicle/Ancillaries/Oxygen/OxygenMask/Flow/Captain",
                            "Vehicle/Ancillaries/Oxygen/OxygenMask/Flow/FirstOfficer"]

def generate_cae_log_dictionaries():
    global action_cae2ont_dict
    # action_ont2cae_dict exists but we need the inverted mapping
    action_cae2ont_dict = {v: k for k, v in action_ont2cae_dict.items()}


def get_cae_log(filename, cae_log_vars):
    # Get current directory
    current_directory = os.getcwd()
    telemetry_path = str(pathlib.PurePath(current_directory, "A320-Telemetry/Deviations/telemetry"))

    cae_data = processing.process_parquet_file(telemetry_path, filename, cae_log_vars)

    return cae_data

def get_changed_vals(row, log_data, sensitivity):
    log_data = log_data.astype(float)
    prev_row = log_data.iloc[row - 1]  # Get prev Row
    current_row = log_data.iloc[row]  # Get current Row
    result_row = current_row - prev_row  # Find delta between the rows

    values_dict = {}
    for i in range(len(result_row)):
        val = result_row[i]
        if val >= sensitivity:
            values_dict[result_row.axes[0].values[i]] = val

    return values_dict

def get_current_data(row, log_data):
    log_data = log_data.astype(float)
    current_row = log_data.iloc[row]  # Get current Row
    return current_row

def get_cae_val_from_data(label_name, data):

    return_code = 0 # 0 = No Errors ; 1 = label not in dict or is equal to none ; 2 = not in any of the databases
    cae_value = 0
    current_data_inputs = data[0]
    current_data_context = data[1]
    current_data_aircraft_state = data[2]
    
    if not label_name in action_ont2cae_dict or action_ont2cae_dict[label_name] == None or "None" in action_ont2cae_dict[label_name]:
        return_code = 1
        return return_code, cae_value
    else:
        cae_label = action_ont2cae_dict[label_name]


    if cae_label in current_data_inputs:
        cae_value = current_data_inputs[cae_label]
    elif cae_label in current_data_context:
        cae_value = current_data_context[cae_label]
    elif cae_label in current_data_aircraft_state:
        cae_value = current_data_aircraft_state[cae_label]
    else:
        return_code = 2

    return return_code, cae_value