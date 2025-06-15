import re
import subprocess


class ReplacementError(Exception):
    pass


def replace_in_file(path: str, replacements: dict[str, str]):
    with open(path, "r") as f:
        content = f.read()
    for key, val in replacements.items():
        if not (key in content):
            raise ReplacementError(f"{key} not found in {path} while replacing")
        content = content.replace(key, val)
    with open(path, "w") as f:
        f.write(content)


def main():
    placeholder_fingerprint = r"0x1234567890abcdef"
    placeholder_version = "ZIG_VERSION"
    placeholder_project_name = "PROJECT_NAME"
    placeholder_deps_code = "//DEPS_CODE"
    placeholder_deps_imports = "//DEPS_IMPORTS"
    placeholder_sample_code = "//SAMPLE_CODE"
    placeholder_sample_imports = """//SAMPLE_IMPORTS"""

    # -- REPLACE ZIG VERSION AND PROJECT NAME --

    process = subprocess.run(["zig", "version"], capture_output=True)
    process.check_returncode()

    version = process.stdout.decode().strip()

    replace_in_file(f"./build.zig.zon", {
        placeholder_version: version,
        placeholder_project_name: "{{cookiecutter.project_slug}}",
    })

    # -- REPLACE FINGERPRINT --

    process = subprocess.run(["zig", "build"], capture_output=True)

    if (process.returncode == 0):
        raise Exception(
            "expected return code for zig build to be non-zero to gain fingerprint")
    output = process.stderr.decode()

    matches = re.findall(r"0x[0-9a-fA-F]+", output)
    if len(matches) != 2:
        raise Exception(
            f"expected zig build to give exactly 2 fingerprints, got {len(matches)}")

    replace_in_file(f"./build.zig.zon", {
        placeholder_fingerprint: matches[1],
    })

    # -- OPTIONAL DEPENDENCIES --

    deps_code = ""
    deps_imports = ""

    use_sdl = str("{{cookiecutter.use_sdl}}") == "yes"
    if use_sdl:
        process = subprocess.run(
            ["zig", "fetch", "--save=sdl", "git+https://github.com/ikskuh/SDL.zig.git"])
        process.check_returncode()

        deps_imports += "const sdl = @import(\"sdl\");\n"
        deps_code += "const sdk = sdl.init(b, .{});\n\n"
        deps_code += "sdk.link(exe, .dynamic, sdl.Library.SDL2);\n"
        deps_code += "exe.root_module.addImport(\"sdl2\", sdk.getWrapperModule());\n\n"

    replace_in_file(f"./build.zig", {
        placeholder_deps_code: deps_code,
        placeholder_deps_imports: deps_imports
    })

    # -- SAMPLE CODE --

    sample_code = """
    _ = allocator;
    std.debug.print("hello from {s}!\\n", .{"{{cookiecutter.project_slug}}"});
    """

    sample_imports = ""

    if use_sdl:
        sample_imports = """const sdl = @import("sdl2");"""
        sample_code = """
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
        "{{cookiecutter.project_slug}}",
        .{ .centered = {} }, .{ .centered = {} },
        resolution.width, resolution.height,
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
    """

    replace_in_file("./src/{{cookiecutter.project_slug}}.zig", {
        placeholder_sample_code: sample_code,
        placeholder_sample_imports: sample_imports,
    })

    # -- FORMATTING --

    process = subprocess.run(["zig", "fmt", "."])
    process.check_returncode()


if __name__ == "__main__":
    main()
