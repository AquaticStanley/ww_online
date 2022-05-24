# Installing
*NOTE - This is currently only tested on Linux, although it theoretically can work on Windows as well!*

You're going to want to run install.sh, this just creates the directory our dependencies are located in and clones the appropriate repos.

After this, in the top level directory, run:

`make build && cd build`

`cmake ..`

`make`

This should build the libraries the main python file needs to access the different parts of the dme core library. You should then be able to run:

`export PYTHONPATH=/path/to/shared/object/we/just/built python` to bring up a Python interpreter that knows about this library.

Inside the Python interpreter, type:

`import dme` 

If this succeeds, you have successfully built the library and it is usable. 

# Testing/Usage

This is now when you should start up your favorite Dolphin instance and boot up Wind Waker.

We'll be calling the main driver of the python code, ww_online.py, in a similar manner to before:

`export PYTHONPATH=/path/to/shared/object/we/just/built ww_online.py`

This should successfully hook up to your running Wind Waker instance and print relevant (?) information.

# Troubleshooting

If your process is reading zeroed values seemingly no matter what you do, or is failing to hook up to the dolphin process, you may need to call `sudo setcap` as described at https://github.com/aldelaro5/Dolphin-memory-engine.

There may be other dependencies I've forgotten about at this point - let me know and I'll add them here.
