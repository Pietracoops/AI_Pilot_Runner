import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib

# list of files with takeoffs
list_of_takeoff_files = [
"1617239081361_R00000117_2.1.parquet",
"1617249012061_R00000117_2.1.parquet",
"1617263665370_R00000035_2.1.parquet",
"1617423203118_R00000035_2.1.parquet",
"1617426902718_R00000035_2.1.parquet",
"1617429955818_R00000035_2.1.parquet",
"1617490143718_R00000035_2.1.parquet",
"1617583380318_R00000035_2.1.parquet",
"1617644336001_R00000117_2.1.parquet",
"1617645663101_R00000117_2.1.parquet",
"1617646225001_R00000117_2.1.parquet",
"1617658240701_R00000117_2.1.parquet",
"1617660146901_R00000117_2.1.parquet",
"1617660667801_R00000117_2.1.parquet",
"1617664095618_R00000035_2.1.parquet",
"1617680525201_R00000117_2.1.parquet",
"1617681881701_R00000117_2.1.parquet",
"1617701909301_R00000117_2.1.parquet",
"1617703310001_R00000117_2.1.parquet",
"1617704231501_R00000117_2.1.parquet",
"1617719900301_R00000117_2.1.parquet",
"1617727425801_R00000117_2.1.parquet",
"1617743347001_R00000117_2.1.parquet",
"1617744914718_R00000035_2.1.parquet",
"1617749013701_R00000117_2.1.parquet",
"1617751051401_R00000117_2.1.parquet",
"1617754503601_R00000117_2.1.parquet",
"1617757186801_R00000117_2.1.parquet",
"1617761176801_R00000117_2.1.parquet",
"1617764131101_R00000117_2.1.parquet",
"1617770490101_R00000117_2.1.parquet",
"1617783971901_R00000117_2.1.parquet",
"1617785352101_R00000117_2.1.parquet",
"1617786001901_R00000117_2.1.parquet",
"1617801372201_R00000117_2.1.parquet",
"1617808924501_R00000117_2.1.parquet",
"1617826058201_R00000117_2.1.parquet",
"1617831029018_R00000035_2.1.parquet",
"1617831883601_R00000117_2.1.parquet",
"1617833083401_R00000117_2.1.parquet",
"1617833578801_R00000117_2.1.parquet",
"1617846504401_R00000117_2.1.parquet",
"1617851583001_R00000117_2.1.parquet",
"1617873266901_R00000117_2.1.parquet",
"1617874654401_R00000117_2.1.parquet",
"1617875163901_R00000117_2.1.parquet",
"1617900490001_R00000117_2.1.parquet",
"1617911353801_R00000117_2.1.parquet",
"1617912908301_R00000117_2.1.parquet",
"1617915314501_R00000117_2.1.parquet",
"1617917284701_R00000117_2.1.parquet",
"1617917926001_R00000117_2.1.parquet",
"1617923531818_R00000035_2.1.parquet",
"1617924572501_R00000117_2.1.parquet",
"1617925880501_R00000117_2.1.parquet",
"1617931579901_R00000117_2.1.parquet",
"1617933149701_R00000117_2.1.parquet",
"1617936950401_R00000117_2.1.parquet",
"1617937454801_R00000117_2.1.parquet",
"1617943256818_R00000035_2.1.parquet",
"1617946979618_R00000035_2.1.parquet",
"1617947062718_R00000035_2.1.parquet",
"1617959927801_R00000117_2.1.parquet",
"1617966297501_R00000117_2.1.parquet",
"1617972961501_R00000117_2.1.parquet",
"1617974034201_R00000117_2.1.parquet",
"1617974552401_R00000117_2.1.parquet",
]

pilot_inputs = [
"Vehicle/Ancillaries/Lighting/APUFire/Pushbutton",
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
"StandardAircraft/ControlDirectionalPosition"

#"StandardAircraft/FMSApproachType",
#"StandardAircraft/AutothrottleOn",
#"StandardAircraft/AutolandOn",
#"StandardAircraft/AutopilotOn",
#"Vehicle/Autopilot/FCU/Altitude/Selected/1",
#"Vehicle/Ancillaries/Brake/AutoBrake/Active",
#"Vehicle/Avionics/TCAS/ResolutionAdvisory/VerticalSpeed/Target",
#"StandardAircraft/TCASMode",
#"StandardAircraft/FlareModeOn",
#"StandardAircraft/FlightDirectorOn",
#"StandardAircraft/AngleOfAttack",
#"StandardAircraft/AngleOfSideslip",
#"StandardAircraft/PitchAngle",
#"StandardAircraft/PitchRate",
#"StandardAircraft/BankAngle",
#"StandardAircraft/RollRate",
#"StandardAircraft/Heading",
#"StandardAircraft/YawRate",
#"StandardAircraft/AirspeedU",
#"StandardAircraft/AirspeedV",
#"StandardAircraft/AirspeedW",
#"StandardAircraft/GroundSpeedU",
#"StandardAircraft/RateOfClimb",
#"StandardAircraft/GforceU",
#"StandardAircraft/GforceV",
#"StandardAircraft/GforceW",
#"StandardAircraft/Latitude",
#"StandardAircraft/Longitude",
#"StandardAircraft/AltitudeAGL",
#"StandardAircraft/AltitudeMSL",
#"StandardAircraft/AltitudePressure",
#"StandardAircraft/AltitudeAboveRunwayThreshold",
#"StandardAircraft/AirspeedIndicated",
#"StandardAircraft/AirspeedCalibrated",
#"StandardAircraft/AirspeedTrue",
#"StandardAircraft/Mach",
#"StandardAircraft/GroundSpeed",
#"Vehicle/FlightInstr/ADC/ComputedAirspeed/1/LeftChannel/Value",
#"Vehicle/FlightInstr/ADC/ComputedAirspeed/1/RightChannel/Value",
#"Vehicle/AircraftDisplays/EIS/VerticalSpeed/TCASTarget/Green",
#"Vehicle/Ancillaries/Lighting/TAWS/Warning/Light/On",
#"Vehicle/Avionics/EGPWS/WarningActive",
#"StandardAircraft/Engine1N1",
#"StandardAircraft/Engine2N1",
#"StandardAircraft/Engine1ThrustLeverAngle",
#"StandardAircraft/Engine2ThrustLeverAngle",
#"StandardAircraft/EngineAllReverserFault",
#"StandardAircraft/EngineFireWarningActive",
#"StandardAircraft/NoseWheelSteeringAngle",
#"StandardAircraft/FlightDirectorPitchError",
#"StandardAircraft/TrackDeviationLateral",
#"StandardAircraft/TrackDeviationVertical",
#"StandardAircraft/DistanceToTouchdown",
#"StandardAircraft/DistanceToRunwayEnd",
#"StandardAircraft/LateralDeviationRunwayCenterline",
#"StandardAircraft/ApproachPathLateralAngle",
#"StandardAircraft/ApproachPathLateralAngleDeviation",
#"StandardAircraft/ApproachPathLateralAngleTarget",
#"StandardAircraft/ApproachPathVerticalAngle",
#"StandardAircraft/ApproachPathVerticalAngleDeviation",
#"StandardAircraft/ApproachPathVerticalAngleSelected",
#"StandardAircraft/ApproachPathVerticalAngleTarget",
#"StandardAircraft/Track",
#"StandardAircraft/Drift",
#"StandardAircraft/DriftRunway",
#"Vehicle/Flight/Ground/Force/Gear/Left",
#"Vehicle/Flight/Ground/Force/Gear/Nose",
#"Vehicle/Flight/Ground/Force/Gear/Right",
#"StandardAircraft/CrashState",
#"StandardAircraft/CrashActive",
#"StandardAircraft/TailStrikeState",
#"StandardAircraft/GlideslopeDeviation",
#"StandardAircraft/GlideslopeTrackActive",
#"StandardAircraft/HydraulicGreenPressure",
#"StandardAircraft/HydraulicYellowPressure",
#"StandardAircraft/HydraulicBluePressure",
#"StandardAircraft/HydraulicBluePressureLow",
#"StandardAircraft/HydraulicGreenPressureLow",
#"StandardAircraft/HydraulicYellowPressureLow",
#"StandardAircraft/LandingGearsHandlePosition",
#"StandardAircraft/TirePressureLow",
#"StandardAircraft/LandingGearsCollapseOn",
#"StandardAircraft/LocalizerDeviation",
#"StandardAircraft/LocalizerTrackActive",
#"StandardAircraft/MasterCautionOn",
#"StandardAircraft/MinimumDecisionAltitudeAGL",
#"StandardAircraft/MinimumDecisionAltitudeMSL",
#"StandardAircraft/MinimumDecisionAltitudePressure",
#"SyntheticEnv/RadioAids/Runway/EndToThreshold",
#"StandardAircraft/AircraftOnGround",
#"StandardAircraft/AircraftOnGroundAccurate",
#"Ownship/Flight/AircraftOnGround",
#"StandardAircraft/StallWarningOn",
#"Vehicle/Pressurization/CabinPressure/CabinAltitude",
#"Vehicle/Ancillaries/Oxygen/OxygenMask/Flow/Captain",
#"Vehicle/Ancillaries/Oxygen/OxygenMask/Flow/FirstOfficer"

]



def process_parquet_file(subdir, file, pilot_input):
    df = pd.read_parquet(os.path.join(subdir, file), engine='fastparquet')
    #csv_output_path = os.path.join("E:/research/DataProcessing/A320-Telemetry/Deviations/csv_files", file + ".csv")
    #df.to_csv(csv_output_path, sep=',', encoding='utf-8')

    main_list = []
    main_list.append(df[pilot_input])

    return main_list[0]

def graph_input(list, filename_list, graph_path):
    print("Entering graphing function")
    # We will only graph 3 at a time
    size_of_sublist = 15

    largest_size = 0
    for element in list:
        if element.shape[0] > largest_size:
            largest_size = element.shape[0]

    name_list = []
    np_arr = np.array(list[0])
    np_arr = np.pad(np_arr, (0,largest_size-np_arr.shape[0]), constant_values=0)
    name_list.append(filename_list[0])
    for i in range (1, size_of_sublist):
        tmp_arr = np.array(list[i])
        tmp_arr = np.pad(tmp_arr, (0,largest_size-tmp_arr.shape[0]), constant_values=0)
        if len(np_arr.shape) > 1:
            tmp_arr = tmp_arr[np.newaxis]
            np_arr = np.append(np_arr, tmp_arr.T, axis=1)
        else:
            np_arr = np.stack((np_arr, tmp_arr), axis=-1)
        name_list.append(filename_list[i])

    # Reshape
    np_arr = np.reshape(np_arr, (largest_size, size_of_sublist))

    df = pd.DataFrame(np_arr)
    df.columns = name_list
    df.plot(title=f'{list[0].name} vs time', grid=True, alpha=0.5, subplots=True, figsize=(19.20, 10.80))
    #df.plot.area(stacked=False)
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.xlabel("time (1/10 sec)")
    filename = list[0].name.replace('/','_')
    plt.savefig(f'{graph_path}\\{filename}_{size_of_sublist}_subplots.jpg', bbox_inches='tight', dpi=300)

    df.plot(title=f'{list[0].name} vs time', grid=True, alpha=0.5, subplots=False, figsize=(19.20, 10.80))
    plt.savefig(f'{graph_path}\\{filename}_{size_of_sublist}.jpg', bbox_inches='tight', dpi=1000)

    plt.cla()
    plt.clf()
    plt.close("all")

    print("Entering graphing function")

def process_files():
    # Get current directory
    current_directory = os.getcwd()
    telemetry_path = str(pathlib.PurePath(current_directory, "A320-Telemetry/Deviations/telemetry"))
    graph_path = str(pathlib.PurePath(current_directory, "A320-Telemetry/Deviations/graphs"))

    # Loop through files
    data_list = []
    filename_list = []
    for entry in pilot_inputs:
        for subdir, dirs, files in os.walk(telemetry_path):
            for file in files:
                if file in list_of_takeoff_files:
                    print(os.path.join(subdir, file))
                    data_list.append(process_parquet_file(subdir, file, entry))
                    filename_list.append(file)
        graph_input(data_list, filename_list, graph_path)
        data_list.clear()
        filename_list.clear()
