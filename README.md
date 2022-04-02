# tts-dataset-prompts
 
This repository aims to be a decent set of sentences for people looking to clone their own voices (e.g. using [Tacotron 2](https://github.com/nvidia/tacotron2)).

Each set of 50 lines aims to fulfill the following criteria:
- each phoneme is represented at least once, according to [CMUdict](https://github.com/cmusphinx/cmudict) (differently-stressed versions of vowels count as separate phonemes; consonants need to be present twice)
- each phoneme is roughly as frequent as in regular speech (between 66% and 150% the frequency present in [Moby Dick](https://www.gutenberg.org/files/15/15-0.txt), unless the phoneme is only present 4 or fewer times in the batch)
- every line is of roughly equal length when spoken (14-18 syllables + non-final punctuation)
- words with context-dependent pronunciations (except very common ones, such as `the`) are avoided for ease of processing
- at least 10 lines contain commas
- at least 10 lines are made up of multiple shorter sentences (so that the AI learns to pause naturally)

Additional text files are provided for question and exclamation prompts, following the same rules. They have been separated because some text-to-speech architectures deal poorly with ending punctuation that affects the intonation of the whole sentence. It may be beneficial to use these to train a separate model, as recommended by [TALQu](https://utaforum.net/threads/talqu-an-unofficial-english-guide-thread-on-talqu-and-its-voice-model-creation.23552/) and as done for some voices in the Mekatron service (defunct).
