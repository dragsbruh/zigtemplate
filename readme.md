# zigtemplate

## installation

you need to install cookiecutter!! (which needs python 3)

```bash
pip install cookiecutter
```

or if youre based like me (literally)

```bash
pipx install cookiecutter
```

## using template

```bash
cookiecutter https://github.com/dragsbruh/zigtemplate.git
```

or again if youre based like me (and obv have ssh keys setup)

```bash
cookiecutter git@github.com:dragsbruh/zigtemplate.git
```

## about the template

it has a post gen script to automatically detect zig version and also set the correct fingerprint.
but it does not work if youre using anyzig.

the code has two files, `main.zig` which sets up gpa and calls `start()` (which lies in `<project_slug>.zig`) with it, and if `start()` specifically returns `error.Exit`, the `main()` returns status code 1. any other error it returns directly otherwise code 0.

```zig
// main.zig
pub fn main() !u8 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    start(allocator) catch |err| switch (err) {
        error.Exit => return 1,
        else => return err,
    };
    return 0;
}
```

```zig
// <project_name>.zig
pub fn start(allocator: std.mem.Allocator) anyerror!void {
    std.debug.print("hello from {s}!\n", .{"<project_name>"});
    // ... main app code here
}
```

i like returns because defer statements actually get to run, unlike `std.process.exit()`

## todo

- [ ] anyzig support

## quick add
