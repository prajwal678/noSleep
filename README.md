# noSleep

#### Tired of having your system turn off in between a boring long build and lose progress? use noSleep

### How to run
```bash
git clone https://github.com/prajwal678/noSleep.git
cd noSleep

```
```bash
python main.py <duration_in_minutes>

```
### Making it an executable binary
__FOR LINUX(and macOS i guess)__

setting up pyinstaller
```bash
python -m venv noSleep
source noSleep/bin/activate
pip install pyinstaller

```

to make the binary and add it to local/bin
```bash
pyinstaller --onefile --name="noSleep" main.py
sudo mv dist/noSleep /usr/local/bin/
sudo chmod +x /usr/local/bin/noSleep

```


- Will restore old sleep settings once program ends thus not having to keep changing it manually everytime you're building and can be run on the terminal.

