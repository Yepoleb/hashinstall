# hashinstall

Restore game installations using a list of file hashes. Intended to bypass broken installers in scripts by simply copying the files from CD. Often this is not enough to get the software to properly work and additional registry entries need to be set. This tool is mostly intended to be used as part of scripts.

## Creating manifest

To create a manifest the software needs to be installed somewhere already. This can be a separate PC or a VM. I like running the original installer in a VM to index the files and then leverage the performance and comfort of wine on the host. The command is run like this:

```sh
python3 createmanifest.py -m manifest.json /path/to/installation
```

## Restoring the installation

For multi-CD installs all disks should be mounted at the same time. cab files need to be extracted with cabextract or unshield to a separate directory. The command can then be run like this:

```sh
python3 installscript.py -m manifest.json -d ~/Games/myGame /mnt/cdrom1 /mnt/cdrom2 /tmp/cab1 /tmp/cab2 ...
```

## Manifest format

JSON file with a variable size list of 3 element lists describing the files.

1. Relative path to the file
2. SHA256 hash
3. File size in bytes


```js
[
  [
    "sounds/background.wav"
    "15c64ec72a82dee96cefba33d5b7f0d658c6e008d0bf43cdeeac928990c32d51"
    10533
  ]
]
```

## Examples

An example is provided in the `manifests` directory.

## License

GPLv3
