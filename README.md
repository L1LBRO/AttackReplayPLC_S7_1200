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

## Examples

Power on the PLC

```bash
python3 replay.py 192.168.1.100 power_on
````

Power off the PLC

```bash
python3 replay.py 192.168.1.100 power_off
````

Activate a digital output (Example Q0.0)

```bash
python3 replay.py 192.168.1.100 modify Q0.0 on
````

Deactivate a digital output (Example Q0.0)

```bash
python3 replay.py 192.168.1.100 modify Q0.0 off
````

## Contributions

If you want to improve this project, feel free to fork the repository and submit a pull request with your enhancements.

## Disclaimer

This project is intended for educational and auditing purposes in controlled environments only.
It must not be used for malicious activities or on production systems without explicit authorization.

## License

This project is licensed under the MIT License.
