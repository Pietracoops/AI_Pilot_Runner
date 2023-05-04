import src.utilities as utilities
import src.runner as runner
from XPlaneApi import XPlaneClient
import os
import time
import shutil
from pathlib import Path
from owlready2 import *
import src.deviation as deviation
import win32gui

# Project Specific Variables
ROOT_DIR = Path(__file__).parent.resolve()
ONT_DIR = ROOT_DIR / "PilotAI_reference" / "ontologie" / "RDF_XML"
SIM_API_VER = "v1.0.6"
SIM_API_NAME = "libXplane-udp-client.exe"
SUBSCRIPTIONS_NAME = "Subscriptions.yaml"
ONTOLOGY_NAMES = ["old_domain.owl", "old_task.owl"]

# seq1 = [1, 2, 3, 4, 5]
# seq2 = [2, 3, 4, 5, 6]
# # Create DeviationModel object
# deviation_obj = deviation.DeviationModel(deviation.tmp_task_dict, deviation.tmp_action_criticality_dict)
# deviation_obj.deviation_analysis(seq1, seq2)

# Find the XPlane Window
hWnd = win32gui.FindWindow(None, "X-System")

# Start the C++ Simulator API Server
sim_api_path = Path(os.getcwd(), "../", "API", SIM_API_VER)
sim_yaml_path = f"{str(sim_api_path)}/{SUBSCRIPTIONS_NAME}"
subscriptions_yaml_path = Path(os.getcwd(), "Subscriptions.yaml")
if os.path.exists(sim_api_path):
    print(f"Found Simulator API version: {SIM_API_VER}")
    os.environ['PATH'] = os.environ['PATH'] + ";" + str(sim_api_path)
    shutil.copy2(subscriptions_yaml_path, sim_yaml_path)
    SimAPI = utilities.ProcessManager(SIM_API_NAME, sim_api_path)
    time.sleep(3) # Let API start
else:
    raise Exception("Simulator API not found, terminating AI Pilot Runner")


api_client = XPlaneClient("Runner")
#Call the connect command
if not api_client.connect():
    print("Connection client 1 failed")
    exit()


ontology_rebuild = True

sim_runner = runner.Runner(hWnd, sim_yaml_path, api_client, 10, 0)
if ontology_rebuild == True:
    print("Rebuilding Ontology...")
    sim_runner.build_ontology_hierarchy(ONT_DIR, ONTOLOGY_NAMES)  # Run this to load ontology from owl files
    sim_runner.save_ontology_hierarchy("ontology_obj.pkl")
else:
    sim_runner.build_ontology_hierarchy(ONT_DIR, ONTOLOGY_NAMES, "ontology_obj.pkl") # Run this to load from pickle file (faster)

sim_runner.modify_ontology_class()
sim_runner.generate_sequences_from_ontology()
sim_runner.model_initialization()

sim_runner.run_simulation_loop()


while True: # Uncomment this to run the API gui indefinitely
    pass

print("Program Complete.")


