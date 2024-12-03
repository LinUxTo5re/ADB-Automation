import uiautomator2 as u2

device_id = "127.0.0.1:6555"  # Replace with your emulator ID
d = u2.connect(device_id)
print(d.info)  # Check device information

# Dump the current UI hierarchy
ui_dump = d.dump_hierarchy()
print(ui_dump)  # Print or save to a file for inspection
with open("ui_dump.xml", "w") as f:
    f.write(ui_dump)
