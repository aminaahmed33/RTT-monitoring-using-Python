Project Summary
This project focuses on monitoring RTT (Round Trip Time) between colocation facilities to detect anomalies in network performance. It builds on outputs from earlier scripts that analyzed traceroutes, identified colocation facilities, and mapped peering interconnections.

What This Script Does
The script uses output files (named with link) generated from previous steps to monitor RTT anomalies.
It identifies unusual patterns in RTT between colocation facilities, helping to detect potential network performance issues.
What Has Already Been Done
Traceroute data was fetched and analyzed using RIPE Atlas.
Colocation facilities were identified, and peering interconnections were mapped using tools like PeeringDB.
These tasks were completed in separate scripts and are not part of this script.
Tools Used
RIPE Atlas for collecting traceroute data.
PeeringDB for network and facility information.
Custom Scripts for RTT monitoring and anomaly detection.
