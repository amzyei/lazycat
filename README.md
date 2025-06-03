﻿# LazyCat Terminal Emulator

LazyCat is a small terminal program for Linux. It uses little memory and is about 15K in size.

## Icon
![icon](icon/lazycat.png)

## Screenshots
- Version 0.1 (2025):
![screenshots](screenshots/1.png)

## How to Build and Run the C Version with Clockbar and VTE Terminal

### Build the clockbar C program:
```
make clockbar
```

### Install the LazyCat program on your system:
```
make install
```

### Run the program on your computer:
```
make run
```

### Install needed packages (GTK 3 and VTE development libraries):
```
make deps
```

This will install all packages needed to build and run the C version of LazyCat with clockbar and VTE terminal.

## Testing

Please check:
- The window title changes every second with the time.
- The terminal opens and works in the window.
- The program runs with no errors.
- The Makefile builds and runs the program well.
- The program can be installed and run on your system.
- The program can be run with the clockbar and VTE terminal.
