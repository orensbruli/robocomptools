## RoboComp development tools

This folder contains a set of tools created to facilitate the process of software development with RoboComp. Detailed information on each tool can be found in the corresponding README.md files.


### [Yakuake script](https://yakuake.kde.org)


This is a simple script to automatically start Yakuake with two named tabs and running programs.


        #!/bin/bash
        pkill -f icebox&

        qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
        sess0=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
        qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'rcnode'
        qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess0 'rcnode'

        qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession
        sess2=`qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.activeSessionId`
        qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'cd /home/robocomp/robocomp/components/miscomps/comp1'
        qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.runCommand 'bin/comp1 etc/config'
        qdbus org.kde.yakuake /yakuake/tabs org.kde.yakuake.setTabTitle $sess2 'comp1'

Additional blocks can be added to create and initialize new tabs in Yakuake.
Copy this code to a .sh file and execute it whenever you need to start your multi-component development environment.
