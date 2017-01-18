# wacovi :speech_balloon::chart_with_upwards_trend:

**wacovi** - **W**hats**A**pp **co**nversation **vi**sualizer

Reads WhatsApp log file (on your own machine) and extracts several statistics (pandas) for visualizations (d3.js).

### Visualizations
* Stacked Area Chart: Total number of messages over days
* Hourly Activity Heatmap: Grouped by day of the week
* ... more coming soon

### Examples
|[![v1](https://raw.githubusercontent.com/saisasidhar/wacovi/master/screenshots/v1.png)](https://raw.githubusercontent.com/saisasidhar/wacovi/master/screenshots/v1.png)|[![v2](https://raw.githubusercontent.com/saisasidhar/wacovi/master/screenshots/v2.png)](https://raw.githubusercontent.com/saisasidhar/wacovi/master/screenshots/v2.png)|
|---|---|
| Stacked Area Chart | Activity Heatmap |

### Steps
* Run the python script ( `-i` option for your name in the log file, `-y` option for your conversation partner's name)

> `python extract.py -f log.txt -i "Ego" -y "Vos"`

* Open `index.html` in a web browser and navigate through the menu

### Dependencies
* Python >= 2.7
* pandas >= 0.19

### P.S.

Keep your WhatsApp log files safe and encrypted.
