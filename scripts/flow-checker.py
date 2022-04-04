
filename = "../voltha-logs/local-flows/flows.log"

file1 = open(filename, 'r')
Lines = file1.readlines()

flow_added = 0
flow_added_done = 0
flow_removed = 0
flow_removed_done = 0
# Strips the newline character
for line in Lines:

    if "flow-delete-strict response sent" in line:
        continue

    if "flow-add begin" in line:
        flow_added += 1
    elif "flow-add done" in line:
        flow_added_done += 1
    elif "flow-delete-strict begin" in line:
        flow_removed += 1
    elif "flow-delete-strict done" in line:
        flow_removed_done += 1
    elif "received-barrier-request" in line:
        flow_added = 0
        flow_added_done = 0
        flow_removed = 0
        flow_removed_done = 0
    elif "sent-barrier-response" in line:
        all_matched = True
        if flow_added != flow_added_done:
            print("Received %d done for %d adds" % (flow_added_done, flow_added))
            all_matched = False
        if flow_removed != flow_removed_done:
            print("Received %d done for %d removes" % (flow_removed_done, flow_removed))
            all_matched = False
        if not all_matched:
            print(line)
    # else:
    #     print(line.strip())