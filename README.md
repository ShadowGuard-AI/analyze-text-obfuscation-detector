![The seabed listening array: housings bolted to plates on a quiet floor, a cable sagging into blue hush, nothing readable](intro-banner.png)

# analyze-text-obfuscation-detector

![A line of hydrophones receding on a sagging cable, the nearest housing carrying the worn stencil name](banner.png)

![A reef turquoise hydrophone housing on a bolted plate with three coral pink listening rings broken at an orange crack](logo.png)

![The array in three depth bands: light shafts and rising bubbles, fixed housings with spreading listening rings, shells and a pearl strand near](scene.svg)


# analyze-text-obfuscation-detector
Identifies various text obfuscation techniques used to mask potentially malicious code or content, such as character substitution, encoding, or insertion of whitespace. Reports detected obfuscation types and potential severity. Severity is derived from how many of the three checks hit: none when no check hits, low for one, medium for two, and high for three; it appears in the console summary and in the output CSV. Base64 detection tests the whole file as one blob and also extracts candidate base64 tokens from the text and tests each one, so a base64 string embedded in ordinary prose is detected. - Focused on Data analysis and reporting


![Major section divider](sep-heavy.svg)

> Sponge cluster note: the severity scale counts hits across exactly three checks. One hit is low, two are medium, three are high, and no hit is none.

> Sponge cluster note: the usage line names no input file argument, even though the detector works on a file or text. How the material reaches the detector is not spelled out in the source.

## Install
`git clone https://github.com/ShadowGuardAI/analyze-text-obfuscation-detector`


![Major section divider](sep-heavy.svg)

## Usage
`./analyze-text-obfuscation-detector [params]`


![Major section divider](sep-heavy.svg)

## Parameters
- `-h`: Show help message and exit
- `-o`: Path to the output CSV file for results.
- `-v`: Enable verbose logging.


![Major section divider](sep-heavy.svg)

## License
Copyright (c) ShadowGuardAI
