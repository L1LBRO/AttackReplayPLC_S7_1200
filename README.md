# ReplayAttackPLC_S7_1200

This Python script allows controlling a Siemens PLC via the S7 protocol.

## Provides the following functionalities:
- Power on the PLC.
- Power off the PLC.
- Modify the PLC digital outputs.

## Requirements
- Python 3.x
- Network connection to the Siemens PLC

## Usage

Run the script with the following parameters:

```bash
python3 replay.py [PLC_IP] [Action]
````

Available actions
 - power_on: Powers on the PLC
 - power_off: Powers off the PLC
 - modify [output] [on|off]: Changes the state of a PLC digital output

