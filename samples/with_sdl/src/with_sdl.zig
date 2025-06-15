const std = @import("std");
const sdl = @import("sdl2");

pub fn start(allocator: std.mem.Allocator) anyerror!void {
    _ = allocator; // FIXME: remove this line

    const resolution = .{
        .width = 640,
        .height = 480,
    };
    try sdl.init(.{
        .video = true,
        .events = true,
        .audio = true,
    });
    defer sdl.quit();

    var window = try sdl.createWindow(
        "with_sdl",
        .{ .centered = {} },
        .{ .centered = {} },
        resolution.width,
        resolution.height,
        .{ .vis = .shown },
    );
    defer window.destroy();

    var renderer = try sdl.createRenderer(window, null, .{ .accelerated = true });
    defer renderer.destroy();

    mainLoop: while (true) {
        while (sdl.pollEvent()) |ev| {
            switch (ev) {
                .quit => break :mainLoop,
                else => {},
            }
        }

        try renderer.setColor(.black);
        try renderer.clear();

        renderer.present();
    }
}
