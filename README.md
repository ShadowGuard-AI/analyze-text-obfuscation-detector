![Twig close up where the stick insect's legs grip the bark and its head lifts clear of the line of the wood, scarlet berries soft behind it](intro-banner.png)

# analyze-text-obfuscation-detector

![Spray of bare twigs against soft leaf green, two stick insects hidden along separate twigs at different depths and one scarlet berry cluster at the frame edge](banner.png)

![One bare brown twig running diagonally with a single stick insect laid exactly along it, its body the same colour and line as the wood, and one scarlet berry at the twig's tip](logo.png)

![The array in three depth bands: light shafts and rising bubbles, fixed housings with spreading listening rings, shells and a pearl strand near](scene.svg)


Identifies various text obfuscation techniques used to mask potentially malicious code or content, such as character substitution, encoding, or insertion of whitespace. Reports detected obfuscation types and potential severity. Severity is derived from how many of the three checks hit: none when no check hits, low for one, medium for two, and high for three; it appears in the console summary and in the output CSV. Base64 detection tests the whole file as one blob and also extracts candidate base64 tokens from the text and tests each one, so a base64 string embedded in ordinary prose is detected, focusing on data analysis and reporting.


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
