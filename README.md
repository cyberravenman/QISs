# QISs
This project is the implementation of a user-friendly graphical interface for interacting with IBM Quantum computers for cybersecurity tasks. Authors: Che_Guevara_22 and CyberRavenMan. This solution is under development, but it already includes the ability to collect information about quantum computers, start creating a random sequence of bits, and check the randomness of the sequence through NIST tests. At the same time, the program will tell you on which qubit it is best, in our opinion, to create this sequence.

Various versions of the project are presented in this repository. Each version is located in the corresponding directory.

Deployment of the environment for comfortable work:
- The following modules are available in the virtual environment: pip3: IPython, PyQt5, qiskit, qiskit-ibm-runtime, tabulate, debugpy in versions 0.1 and 0.2, matplotlib in version 0.3.5, pandas in version 0.3.7, qiskit[visualization], statsmodels, pytest in version 0.3.8;
- The API token is required for the solution to work, you can find it on https://quantum.ibm.com/ in your account profile.
- This Software should only run on Unix-like OS

For program to work correctly, it is required python3.9 and pip3. Software was testing on Ubuntu 18; Ubuntu 20.04.6 and Kali_Linux 2024.4.

But to quickly launch the software solution, you need to run the file 'run.sh', which is located in the directory of each version of the program.

We wish you productive work!
