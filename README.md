# Barcode Battler Engine

Set of tools to simulate Barcode Battler II functionality.

This is mainly a translation and revision from https://github.com/finalfighter/BarcodeBattler2-Simulator old flash application and info compiled from http://barcodebattler.net/ and http://barcodebattler.co.uk/

## Requirements

Currently there is no more requirements only than a Python >= 3.9 version, and you are ready to go.

## Installation

```
pip install barcode-battler-engine
```

## Demo

This site generates on-the-fly the card information using this package, check it out https://cards.bimbiribase.xyz/barcodebattler/ac1d5f5c-89bf-48c8-ac09-3e474a566847/

## Import the module to read your barcodes

```
from barcodebattler.bb2.builder import BarcodeBattler2Builder
barcode_data = BarcodeBattler2Builder().build(barcode)
print(barcode_data)
barcode: 0451508035504, hp: 4500, st: 1500, df: 800, speed: 5, race: 0, job: 3, pp:5, mp:0, special: 50, post_read: False
```

## Reading barcodes using prompt

Test your cards using the `prompt_reader.py` tool

```
./prompt_reader.py
Enter barcode (type exit to finish): 0371110125502
+-----------+-----------------+
| Barcode   |   0371110125502 |
| Race      |          ANIMAL |
| Job       |       SOLDIER_2 |
+-----------+-----------------+
| HP        |            3700 |
| ST        |            1100 |
| DF        |            1000 |
+-----------+-----------------+
| MP        |               0 |
| PP        |               5 |
| Special   |              50 |
+-----------+-----------------+
| Read Mode |        PRE_READ |
+-----------+-----------------+
```

## How to test

Install the dev dependencies

```
pip install -r requirements/dev.pip
```

And execute the test like

```
python -m unittest
```
