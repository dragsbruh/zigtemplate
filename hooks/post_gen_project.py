import re
import subprocess

build_zig_zon = "./build.zig.zon"
fingerprint_regex = r"0x[0-9a-fA-F]+"


def replace_in_file(path: str, replacements: dict[str, str]):
    with open(path, "r") as f:
        content = f.read()
    for key, val in replacements.items():
        if not (key in content):
            raise Exception(
                f"replacement error: {key} not found in {path} while replacing")
        content = content.replace(key, val)
    with open(path, "w") as f:
        f.write(content)


def extract_zig_vars(zig_text: str):
    lines = zig_text.splitlines()
    result: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if line.startswith('.name'):
            result['name'] = line.split('=')[1].strip().strip(',').strip('.')
        elif line.startswith('.minimum_zig_version'):
            result['minimum_zig_version'] = line.split(
                '=')[1].strip().strip(',').strip('"')
        elif line.startswith('.fingerprint'):
            result['fingerprint'] = line.split('=')[1].strip().strip(',')
    return result


def main():
    with open(build_zig_zon, 'r') as f:
        vars = extract_zig_vars(f.read())

    placeholder_fingerprint = vars['fingerprint']
    placeholder_version = vars['minimum_zig_version']
    placeholder_project_name = vars['name']

    # -- REPLACE ZIG VERSION AND PROJECT NAME --

    process = subprocess.run(["zig", "version"], capture_output=True)
    process.check_returncode()

    version = process.stdout.decode().strip()

    replace_in_file(build_zig_zon, {
        placeholder_version: version,
        placeholder_project_name: "{{cookiecutter.project_slug}}",
    })

    # -- REPLACE FINGERPRINT --

    process = subprocess.run(["zig", "build"], capture_output=True)
    output = process.stderr.decode()

    if process.returncode != 0:
        matches = re.findall(fingerprint_regex, output)
        if len(matches) != 2:
            print(output)
            raise Exception(
                f"fingerprint error: expected zig build to give exactly 2 fingerprints, got {len(matches)}, zig output has been printed above")

        replace_in_file(build_zig_zon, {
            placeholder_fingerprint: matches[1]
        })

    # -- FORMATTING --

    process = subprocess.run(["zig", "fmt", "."])
    process.check_returncode()


if __name__ == "__main__":
    main()
