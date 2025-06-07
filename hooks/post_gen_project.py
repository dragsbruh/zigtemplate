import re
import subprocess


def replace_in_file(path: str, replacements: dict[str, str]):
    with open(path, "r") as f:
        content = f.read()
    for key, val in replacements.items():
        content = re.sub(key, val, content)
    with open(path, "w") as f:
        f.write(content)


def main():
    placeholder_fingerprint = r"0x1234567890abcdef"
    placeholder_version = "ZIG_VERSION"

    process = subprocess.run(["zig", "version"], capture_output=True)
    process.check_returncode()

    version = process.stdout.decode().strip()

    replace_in_file(f"./build.zig.zon", {
        placeholder_version: version,
    })

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


if __name__ == "__main__":
    main()
