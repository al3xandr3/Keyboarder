
# %% CMD commands reference
"""
conda activate main
cd "C:\\Users\\user\\Google Drive\\my\\projects\\Keyboarder"
python Keyboarder.py

# debug
pyinstaller --onefile --debug=all --log-level=WARN ^
    --onefile ^
    --add-data="default1.wav;." ^
    --add-data="exit_menu.png;." ^
    --add-data="key_tray.png;." ^
    --add-data="pause_tray.png;." ^
    --add-data="play_menu.png;." ^
    --add-data="stop_menu.png;." ^
    --add-data="timer_menu.png;." ^
    --add-data="timer_tray.png;." ^
    --add-data="settings_menu.png;." ^
    Keyboarder.py

# final
pyinstaller --onefile --windowed --icon=keyboard.ico ^
    --onefile ^
    --add-data="default1.wav;." ^
    --add-data="exit_menu.png;." ^
    --add-data="key_tray.png;." ^
    --add-data="pause_tray.png;." ^
    --add-data="play_menu.png;." ^
    --add-data="stop_menu.png;." ^
    --add-data="timer_menu.png;." ^
    --add-data="timer_tray.png;." ^
    --add-data="settings_menu.png;." ^
    Keyboarder.py


"""


# %%
import os
import sys
from PySide2 import QtWidgets, QtGui
from PySide2.QtWidgets import QSystemTrayIcon, QAction
import keyboard
import threading
from time import time
import datetime
import pyaudio
import wave
import json
import errno
from shutil import copyfile
    
# %%
    
file_path = os.path.dirname(os.path.abspath(__file__))

key_tray   = file_path + "\\key_tray.png"
timer_tray = file_path + "\\timer_tray.png"
pause_tray = file_path + "\\pause_tray.png"

play_menu   = file_path + "\\play_menu.png"
stop_menu   = file_path + "\\stop_menu.png"
conf_menu   = file_path + "\\settings_menu.png"
exit_menu   = file_path + "\\exit_menu.png"

audio_path = file_path + "\\default1.wav"

# %%

user_config      = os.environ.get('USERPROFILE') + '\\.keyboarder\\config.json'
user_config_path = os.path.dirname(user_config)

if os.path.exists(user_config) and os.path.isfile(user_config):
    config_path = user_config
else:
    data = {
        'start_showMessage': 'yes',
        'timer_audio': 'default1.wav',
        'timer_audio_enabled': 'yes',
        'timer_play_key': 'insert',
        'timer_time_left_key': 'ctrl+insert',
        'timer_duration_minutes': 25
    }
    data['remap_key'] = []
    data['remap_key'].append({
        'f10': 'volume mute',
        'f11': 'volume down',
        'f12': 'volume up',
        'ctrl+home': 'page up',
        'ctrl+end':  'page down'
    })
    data['remap_key_to_cmd'] = []
    data['remap_key_to_cmd'].append({
        'ctrl+1': 'C:\\Windows\\explorer.exe',
        'ctrl+2': 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
        'ctrl+3': 'C:\\Users\\user\\Google Drive\\my\\projects\\python\\ipynb\\JupyterLab.bat'
    })
    if not os.path.exists(os.path.dirname(user_config)):
        try:
            os.makedirs(os.path.dirname(user_config))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(user_config, 'w') as output:
        json.dump(data, output, indent=4)
    
    config_path = user_config

with open(config_path) as fp:
    config = json.load(fp)


# Copy audio also
wav1 = os.environ.get('USERPROFILE') + '\\.keyboarder\\default1.wav'
if not os.path.isfile(wav1):
        try:
            copyfile(audio_path, wav1)
        except OSError as exc: # Guard against race condition 
            if exc.errno != errno.EEXIST:
                raise

# %% 

class WavePlayerLoop(threading.Thread):
    CHUNK = 48000

    def __init__(self, filepath, loop=True):
        """
        Initialize `WavePlayerLoop` class.
        PARAM:
            -- filepath (String) : File Path to wave file.
            -- loop (boolean)    : True if you want loop playback.
                                   False otherwise.
        """
        super(WavePlayerLoop, self).__init__()
        self.filepath = os.path.abspath(filepath)
        self.loop = loop

    def run(self):
        # Open Wave File and start play!
        wf = wave.open(self.filepath, 'rb')
        player = pyaudio.PyAudio()        
    
        # Open Output Stream (based on PyAudio tutorial)
        stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)

        # PLAYBACK LOOP
        data = wf.readframes(self.CHUNK)
        while self.loop:
            stream.write(data)
            data = wf.readframes(self.CHUNK)
            if data == b'':  # If file is over then rewind.
                wf.rewind()
                data = wf.readframes(self.CHUNK)

        stream.close()
        player.terminate()

    def play(self):
        """
        Just another name for self.start()
        """
        self.start()

    def stop(self):
        """
        Stop playback
        """
        self.loop = False

# %%
class GUI():

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.w = QtWidgets.QWidget()
      
        menu = QtWidgets.QMenu(self.w)
        
        menu.addSeparator()
        sound = QAction('Sound')
        sound.setCheckable(True)
        if config['timer_audio_enabled'] == 'yes':
            sound.setChecked(True) 
        else:
            sound.setChecked(False) 
        sound.toggled.connect(self.onSoundOption)

        self.use_sound = True
        menu.addAction(sound)

        open_cal = menu.addAction("Start/Pause")
        open_cal.triggered.connect(self.pomodoro_operator)
        open_cal.setIcon(QtGui.QIcon(play_menu))
        
        reset = menu.addAction("Stop")
        reset.triggered.connect(self.pomodoro_stoper)
        reset.setIcon(QtGui.QIcon(stop_menu))
        
        menu.addSeparator()
        
        conf = menu.addAction("Config")
        conf.triggered.connect(self.open_config)
        conf.setIcon(QtGui.QIcon(conf_menu))
        
        menu.addSeparator()
        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QtGui.QIcon(exit_menu))
      

        self.tray = QSystemTrayIcon(self.w)
        self.tray.setIcon(QtGui.QIcon(key_tray))
        self.tray.setContextMenu(menu)
        self.tray.show()
        
        if config['start_showMessage'] == 'yes':
            self.tray.showMessage('Keyboarder', "Mouse hover on icon for tips", QtGui.QIcon(key_tray), 100)

        self.tray.activated.connect(self.onTrayIconActivated)

        self.pomodoro_duration = 60 * config['timer_duration_minutes']
        self.time_left         = 0
        self.paused            = False
        self.startTime         = 0
        self.endTime           = 0
        self.tray.setToolTip(self.instructions())

        # Keys remap
        keyboard.unhook_all()
        keyboard.add_hotkey(config['timer_time_left_key'], self.myToolTip, suppress=True)        
        keyboard.add_hotkey(config['timer_play_key'], self.pomodoro_operator, suppress=True)
        # keys
        for k,v in config['remap_key'][0].items():
            keyboard.add_hotkey(k, lambda x=v: keyboard.send(x), suppress=True)
        # cmd's
        for k,v in config['remap_key_to_cmd'][0].items():
            keyboard.add_hotkey(k, lambda x=v: os.startfile(x), suppress=True)


        if self.use_sound:  
            #self.player = WavePlayerLoop(audio_path)
            self.player = WavePlayerLoop(user_config_path + '\\' + config['timer_audio']) 
        
        sys.exit(self.app.exec_())
    
    def instructions(self):
        return """Key 'insert' to Start/Pause Timer
Keys 'ctrl+insert' to show time left on Timer
DoubleClick on icon to Start/Pause Timer
"""

    def open_config(self):
        os.system(f'explorer.exe "{os.path.dirname(user_config)}"')

    def myToolTip(self, other=""):
        
        if self.startTime != 0: # if running   

           if self.paused: # if not running

               time_left = self.time_left
           else:
               time_left = self.time_left - (time() - self.startTime)
               
           tleft = str(datetime.timedelta(seconds=time_left)).split('.', 2)[0]
           self.tray.showMessage("Timer", tleft, QtGui.QIcon(key_tray))
           return tleft

        else:
            return "Keyboarder"
            
    
    def onSoundOption(self, checked):
        self.use_sound = checked
    
    def onTrayIconActivated(self, reason):
        #print(reason, '--reason--')
        if reason == self.tray.DoubleClick:
            self.pomodoro_operator()

 
    def pomodoro_operator(self, other=""):
        if self.startTime == 0: # if not running
            self.start_pomodoro()
        else:
            self.pause_pomodoro()


    def start_pomodoro(self, other=""):
        """
        this function will open application
        :return:
        """
        if self.startTime == 0: # if not running
            #self.tray.showMessage("Keyboarder", f"Pomodoro Started: {self.pomodoro_name}", QtGui.QIcon(pom_path))     
            self.time_left = self.pomodoro_duration
            self.timer = threading.Timer(self.pomodoro_duration, self.end_pomodoro)
            self.startTime = time()
            self.timer.start()  # after 60 seconds, 'callback' will be called
            self.tray.setIcon(QtGui.QIcon(timer_tray))

            if self.use_sound:
                self.player = WavePlayerLoop(audio_path)
                self.player.play()

    
    def pause_pomodoro(self, other=""):
        
        if self.startTime != 0: # if running
                   
            if self.paused:
                #self.tray.showMessage("Keyboarder", "Pomodoro Resume", QtGui.QIcon(pom_path), 10000)  
                self.timer = threading.Timer(self.time_left, self.end_pomodoro)
                self.startTime = time()
                self.timer.start()
                self.paused = False
                self.tray.setIcon(QtGui.QIcon(timer_tray))

                if self.use_sound:
                    self.player = WavePlayerLoop(audio_path)
                    self.player.play()
            else:
                self.player.stop()
                self.timer.cancel()
                self.endTime = time()
                self.time_left = self.time_left - (time() - self.startTime)
                self.paused = True
                self.tray.setIcon(QtGui.QIcon(pause_tray))
                #self.stream.stop_stream()

                
    def end_pomodoro(self):
        self.tray.showMessage("Timer Ended!", "", QtGui.QIcon(timer_tray), 500000)     
        self.paused    = False
        self.startTime = 0
        self.time_left = 0
        self.endTime   = 0
        self.tray.setIcon(QtGui.QIcon(key_tray))        
        self.player.stop()
        
    def pomodoro_stoper(self):
        self.timer.cancel()
        self.paused    = False
        self.startTime = 0
        self.endTime   = 0
        self.time_left = 0
        self.tray.setIcon(QtGui.QIcon(key_tray))        
        self.player.stop()


GUI()


# check what is being pressed
#keyboard.on_press(lambda x: print(x), suppress=False)

#disconnect all events
#keyboard.unhook_all()

#keyboard.add_hotkey('a', lambda: keyboard.send('b'), suppress=True)




