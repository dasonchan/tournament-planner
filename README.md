Tournament Results Project by Dasheng Chen

How to Run
1. Install VirtualBox and Vagrant
2. Download the project and unzip it into vagrant/tournament
3. Open a terminal window and input "vagrant up"
4. Sign into vagrant via inputing "vagrant ssh"
5. Change the directory to vagrant/tournament using "cd vagrant/tournament"
6. Connect to the database using the following commands: "psql - CREATE DATABASE tournament; - \c tournament - \i tournament.sql - q"
7. Run the test by inputting "python tournament_test.py" in terminal