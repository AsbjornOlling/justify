# Justify.py

Justify.py is a simple HTTP front-end for mopidy w/ the spotify extension.
Inspired by similar programs (see: festify, partify), justify orders the playlist according to number of votes on a track. 
Users can add songs and vote on songs added by others through a http interface.

I made this because I wanted to have a democratic playlist running on a Raspberry Pi for our Roskilde Festival camp (2017).
This is my first ever project that isn't either a plain excersize or a shitty bash script. 
I promise the programming is very terrible, and little to no maintenance will be done. Enjoy.

### Prerequisites

Justify.py has the following dependencies:

```
python (version >2.7)
mopidy (tested on version 2.1.0)
mopidy-spotify (tested on version 3.1.0)
bottle (tested on version 0.12)
python-mpd2 (tested on version 0.5.5)
ConfigParser (testded on version 3.5.0)
```

Justify.py does NOT work alongside other simultaneous mopidy front-ends. It crashes when is a song is added by other means.

### Installing

Install and configure [mopidy](https://github.com/mopidy/mopidy), and [mopidy-spotify](https://github.com/mopidy/mopidy-spotify). Make sure to set the connection_timeout value in the [mpd] section to something high.
I recommend testing with a simple frontend (like mpc or ncmpcpp) before setting up justify.py

Install python dependencies
```
pip install bottle
pip install python-mpd2  
pip install ConfigParser
```

Download this project
```
git clone https://github.com/AsbjornOlling/justify.py.git
```

Start mopidy first, then justify.py
```
mopidy &
cd justify.py & python ./justify.py
```
Then open http://localhost:9999/ in a browser to test it.

### Configuration

Configuration is done in the python script itself. A simpler config file is planned.

Near the top of the script, there's a section labelled "CONFIGURATION". This is where you change host and port for the server, and the minimum delay between votes on a track. It should be pretty self-explanatory.

Themeing is most easily done by switching out the css stylesheets in the head of the .tpl html files. Right now I'm just using the Cyborg bootstrap theme from bootswatch. Could easily be replaced with any other bootstrap theme.

‌‌‌‌
