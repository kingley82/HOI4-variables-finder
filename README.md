# HOI4-variables-finder
A simple program that can find any variable you type in game files.  
Tested on Windows. <ins>May</ins> not work on Linux/MacOS
**CASE SENSETIVE!!**

<img src="https://github.com/kingley82/HOI4-variables-finder/blob/main/images/preview.png?raw=true" alt="preview" >

In `config.json` you see two settings: `gamepath` and `priority`. In `gamepath` you can type a path to your HOI4, or just leave it blank - program will ask you to choose it. `priority` have 2 options:
1. Only defined pathes will be scanned by program
2. They will be scanned in order that they written.  

Example, if you leave it as default, program will do this
```scan root/common -> scan root/history -> scan root/events -> scan root/interface -> scan root/gfx```.  
You can do with this parameter what you want:
1. Reorder pathes (`["history", "gfx", "interface", "common", "events"]`)
2. Add new pathes (`["common", "history", "events", "interface", "gfx", "map", "music"]`)
3. Add subpathes (`["common/ai_strategy", "common/decisions", "history", "events", "interface", "gfx"]`)

Program will scan content of files, if they extensions are `*.txt`, `*.gui` or `*.gfx`. Also, program will check every filename, and add they to list too, if filename contains entired searchword. Results of matching filename will displayed with mark (see screenshot)
