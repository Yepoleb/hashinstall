# Zoo Tycoon 2: Ultimate Collection

## Installation

I used the files from https://www.myabandonware.com/game/zoo-tycoon-2-djr. Actual CDs probably work
just as well.

1. Mount the ISOs or copy the CD data onto your disk. You might get away with running the script
 on each CD invididually, but this is not tested.

2. Use the `cabextract` tool to extract `Disk1C~1.cab` from CD 1.

3. Run the script like this:

```sh
python3 installscript.py -m manifest.json -d ~/Games/ZT2 /mnt/cdrom1 /mnt/cdrom2 /mnt/cdrom3 /tmp/cab_extracted
```

`-d ~/Games/ZT2` specifies the installation path and the following paths are the 3 CDs and the
location of the extracted cab files. There is no need to set any registry keys, you can just run
the result with wine. It might be necessary to set the Windows version to Windows XP in winecfg.
