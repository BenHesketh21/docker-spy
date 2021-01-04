import os


def stage(stage_num, stage_des):
    message = f"================\n\nStage: {stage_num},{stage_des}"
    message += "\n\nContinue (<Enter>) Quit and Tear Down (qc) Quit (q)\n>>>"
    instruction = input(message)
    return instruction


# Stage 1 Create a new bridge network
stage_1 = stage(1, "This is a test stage as a proof of concept")
if stage_1== "q":
    exit(0)
elif stage_1 == "":
    os.system("echo 'docker ps' | pv -qL 20")
    os.system("docker ps")
elif stage_1 == "qc":
    exit(1)
# Create a container in the network
# Create nginx config
# Check connection

