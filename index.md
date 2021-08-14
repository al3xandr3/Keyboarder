<!-- Add icon library -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

<style>
  .btn {
  background-color: DodgerBlue;
  border: none;
  color: #fff;
  padding: 12px 30px;
  cursor: pointer;
  font-size: 20px;
}
.btn:hover {
  background-color: RoyalBlue;
}
</style>

<iframe width="560" height="315" src="https://www.youtube.com/embed/Zw5v4yVJjpg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<br>
### Keyboarder gives superpowers to your Keyboard

![Keyboarder](https://raw.githubusercontent.com/al3xandr3/Keyboarder/master/Keyboarder.png)

Have you ever thought to yourself that there's a bunch of keys in the keyboard: Pause, Insert, etc. that dont get much use, and would be great if they could be assigned instead to something more usefull, for your day-to-day use?

This is what *keyboarder* does, it lets you configure keys to actions. 

It includes 3 main functions:
1. Re-map keys, for example make F12 key to be a "volume up" key (that exists dedicated in some keyboards but not in others), or a "Control+PageUp" combination to be a "Home" key, etc... These can come in handy if you changed keyboard layout and the new layout is missing something that you use often.
2. Map keys to an application, for example have "Control+4" trigger a .bat or .exe that you often run, kinda like a shortcut.
3. A timer with included background white noise, that i personally often use and that is configured to start with a certain key

It runs as tray application, so that it does not get in the way.

<button class="btn"><i class="fa fa-download"></i><a href="https://github.com/al3xandr3/Keyboarder/releases/download/v1/Keyboarder.exe" style="color:white;"><b>  Download Release v1</b></a></button>


### Config

A configuration file lets you define what keys map to what functions, timer duration, etc. 
Find the configuration file from the system tray keyboarder menu, righ mouse click -> Config


### Running it

Requires Microsoft Windows

Optional, but I include a shortcut to it in the `C:\%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` so that it start on every reboot, and is just all the time there, and my key shortcuts are always available.
