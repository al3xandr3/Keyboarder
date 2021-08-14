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

Have you ever thought to yourself that i have all these keys in the keyboard: Pause, Insert, etc.. that i don't really use and that i wish they could do instead something else that i really need?

This is what keyboarder does, it lets you configure keys to actions. 

It includes 3 main functions:
1. Re-map keys, for example make F12 function as a "volume up", from a key to another key
2. Map keys to an application, and these can be combinations of keys, for example have "Control+4" trigger a .bat or .exe that you often run, kinda like a shortcut.
3. An included timer with background white noise, that i personally often use and that is configured to have a key associated with the start/pause

It runs as tray application, so that it does not get in the way.

<button class="btn"><i class="fa fa-download"></i><a href="https://github.com/al3xandr3/Keyboarder/releases/download/v1/Keyboarder.exe" style="color:white;"><b>  Download Release v1</b></a></button>


### Config

Many things can be configured, what keys to map to what functions, timer duration, etc. in the included json configuration file.
Find the configuration file from the system tray keyboarder menu


### Running it

Requires Microsoft Windows

Optional, but I include a shortcut to it in the `C:\%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` so that it start on every reboot, and is just all the time there, and my key shortcuts are always available.
