# :red_book: Global COmments
- start


# :blue_book: Things logged
- [git hub emojes](https://gist.github.com/rxaviers/7360908)
- godot 4 gdextention not used yet

# :smoking: Compiling / Cross Compling
- conan profiles need to be swapped in run.py for cross compiling
  - :telescope: look into c++_static vs c++_shared vs libc++
- :hammer: in cmake lists the android version of godot-cpp must be linked (automate)
- :hammer: huh
- :beetle: fmt dosent compile well with libc++, which may be used for xcompiling on android (to check switch to libc++ in conan profile)






# :new_moon: plan :date30/Dec/2022   

- make a multi player game which takes a number(1-10) input from all players and generate a random number (1-10) if the number is the number is gussed correctly the player who guess wins, else it is added to the player score... if anyone reach >100 they win, else return > or < as approporiate

:lol:
## extern TODO:hammer:
- add extentions to saftware-games
- reintegrate xzlog.h in it's conan package




<!--ANCHOR[id=OlaFu] -->
## OnAccept
``` c++
void OnAccept(){
  //have sex
}

```