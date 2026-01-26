# Cybersecurity Log Data Exploration (CIC-IDS-2017)

## Project Overview
This project explores high-dimensional cybersecurity network traffic data with the goal of
understanding its structure, limitations, and potential for visualization-driven insight.
The emphasis is on data acquisition, data understanding, and reproducible analytical
workflows, rather than on building or optimizing machine learning models.

The project treats the dataset as a real-world security artifact, focusing on how such data
is structured, labeled, and constrained by its collection methodology.

## Data Source & Provenance
The dataset used in this project is **CIC-IDS-2017**, obtained directly from the official
repository published by the **Canadian Institute for Cybersecurity (CIC)**.

- Dataset: CIC-IDS-2017
- Publisher: Canadian Institute for Cybersecurity, University of New Brunswick
- Collection period: July 3–7, 2017
- Data type: Flow-based network traffic records
- Flow generation tool: CICFlowMeter
- Labels: Benign and multiple attack categories (e.g., DDoS, PortScan, Web Attacks)

The files included in this repository correspond to the official CIC-IDS-2017 CSV release and
preserve the original filenames and structure provided by CIC Research.

Each record represents a summarized bidirectional network flow extracted from raw PCAP
captures, with a high-dimensional set of numerical features describing traffic behavior and
a ground-truth label assigned during controlled attack scenarios.

## Dataset Files
The dataset is organized by day and attack scenario:

| File | Day | Traffic Type |
|----|----|----|
| Monday-WorkingHours.pcap_ISCX.csv | Monday | Benign |
| Tuesday-WorkingHours.pcap_ISCX.csv | Tuesday | Mixed |
| Wednesday-workingHours.pcap_ISCX.csv | Wednesday | Mixed |
| Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv | Thursday | Web Attacks |
| Thursday-WorkingHours-Afternoon-Infiltration.pcap_ISCX.csv | Thursday | Infiltration |
| Friday-WorkingHours-Morning.pcap_ISCX.csv | Friday | Benign |
| Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv | Friday | Port Scan |
| Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv | Friday | DDoS |

Raw data files are stored unchanged under `data/raw/`.

## Data Characteristics
- High-volume, flow-based network traffic data
- High-dimensional numerical feature space derived from statistical flow metrics
- Presence of significant class imbalance between benign and attack traffic
- Potential issues including noise, missing values, and labeling assumptions inherited
  from the original experimental setup

## Reproducibility
All analysis in this repository is reproducible. The project follows a clear directory
structure separating raw data, notebooks, and source code, and includes an explicit
dependency list. Current notebooks focus on data loading, schema inspection, and initial
dataset understanding.

## Current Status
This repository currently focuses on data acquisition, validation of dataset structure,
and exploratory inspection of feature distributions and labels. More advanced exploratory
analysis, visualization techniques, and statistical methods will be introduced
incrementally in later stages of the project.
