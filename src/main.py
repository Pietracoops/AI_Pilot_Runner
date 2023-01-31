import src.utilities as utilities
import src.runner as runner
from XPlaneApi import XPlaneClient

import os
import time
import shutil
from pathlib import Path
from owlready2 import *


import src.deviation as deviation
ROOT_DIR = Path(__file__).parent.resolve()
ONT_DIR = ROOT_DIR / "PilotAI_reference" / "ontologie" / "RDF_XML"

SIM_API_VER = "v1.0.6"
SIM_API_NAME = "libXplane-udp-client.exe"
SUBSCRIPTIONS_NAME = "Subscriptions.yaml"
ONTOLOGY_NAMES = ["domain.owl", "task.owl"]

# seq1 = [1, 2, 3, 4, 5]
# seq2 = [2, 3, 4, 5, 6]
# #
# deviation.deviation_analysis(seq1, seq2)



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


sim_runner = runner.Runner(ONT_DIR, ONTOLOGY_NAMES, sim_yaml_path, api_client, 10, 0)


sim_runner.run_simulation_loop()


# list_of_actions = superclass.


print("Terminated.")


