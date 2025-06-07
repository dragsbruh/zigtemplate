pub fn start(allocator: std.mem.Allocator) anyerror!void {
    std.debug.print("hello from {s}!\n", .{"{{cookiecutter.project_slug}}"});
    allocator.free(try allocator.alloc(u8, 32));
}

const std = @import("std");
