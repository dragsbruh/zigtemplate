const std = @import("std");

pub fn start(allocator: std.mem.Allocator) anyerror!void {
    _ = allocator; // FIXME: remove this line

    _ = allocator;
    std.debug.print("hello from {s}!\n", .{"base"});
}
