# DestinyWwiseParserScript
Python script to create and parse .json files created by [WwiseParser](https://github.com/xyx0826/WwiseParser), semi specialized for Destiny and Destiny 2

## Usage
`[better_]parse[_wwise].py <.bnk file name/hash/path>`
Note: If you just use the hash or name, you must set either the bnk_directory or packages_path inside parse.py.

Helpful list of all bnks linked to an activity:
- [Witch Queen List](https://gist.github.com/nblockbuster/71c61328d3106d101f26751998588ac6) (being updated as more gets added)
- [Beyond Light List](https://gist.github.com/nblockbuster/7151b8b66632c70e2649d40ffd614544)

#### Optional Command Line Arguments
`[better_]parse[_wwise].py <path to bnk file/bnk file name(0000-0000)/bnk hash(xxxxxx80)> wav/wavconv/d1/prebl wav/wavconv/d1/prebl`
- wav/wavconv: Auto-exports all wavs used in that bnk. (Requires setting packages path in the file).
- d1/prebl: Should switch to pre-bl or d1 version for wav/bnk extraction. (Requires setting packages path in the file & downloading Resources.zip).
## Planned Features
- ~~GUI~~
- - Implemented into [DMV](https://github.com/nblockbuster/DestinyMusicViewer)
