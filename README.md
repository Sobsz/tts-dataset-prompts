# tts-dataset-prompts
 
This repository aims to be a decent set of sentences for people looking to clone their own voices (e.g. using [Tacotron 2](https://github.com/nvidia/tacotron2)).

Each set of 50 lines aims to fulfill the following criteria:
- each phoneme is represented at least once, according to [CMUdict](https://github.com/cmusphinx/cmudict) (differently-stressed versions of vowels count as separate phonemes; consonants need to be present twice)
- each phoneme is roughly as frequent as in regular speech (between 50% and 150% the frequency present in [Moby Dick](https://www.gutenberg.org/files/15/15-0.txt), unless the phoneme is only present 4 or fewer times in the batch)
- every line is of roughly equal length when spoken (14-18 syllables + non-final punctuation)
- words with context-dependent pronunciations (except very common ones, such as `the`) are avoided for ease of processing
- at least 10 lines contain commas
- at least 10 lines are made up of multiple shorter sentences (so that the AI learns to pause naturally)

Additional text files will be provided for question and exclamation prompts, following the same rules. They have been separated because some text-to-speech architectures deal poorly with ending punctuation that affects the intonation of the whole sentence. It may be beneficial to use these to train a separate model, as recommended by [TALQu](https://utaforum.net/threads/talqu-an-unofficial-english-guide-thread-on-talqu-and-its-voice-model-creation.23552/) and as done for some voices in the Mekatron service (defunct).

This repo uses the [g2p-en](https://pypi.org/project/g2p-en/) library to determine phoneme counts, in order to match [Uberduck](https://uberduck.ai/)'s phonetization.

## Other good prompt sets
- (multilingual!) [Microsoft CustomVoice example scripts](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomVoice/script) (not all of the prompt lists are well-designed, e.g. [the en-US chat prompts](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/English%20(United%20States)_enUS/3000000001-3000000300_Chat.txt) only include /ʒ/ as part of the word "Indonesia")
- [Rainbow Passage](https://dailycues.com/learn/iqpedia/pages/rainbow-passage/) and [Grandfather Passage](https://dailycues.com/learn/iqpedia/pages/grandfather-passage/) (phonetically complete)
- [CMU Arctic prompt list](http://festvox.org/cmu_arctic/cmuarctic.data) (phonetically balanced, but only one sentence per line)
- [MOCHA-TIMIT](https://data.cstr.ed.ac.uk/mocha/mocha-timit.txt) ("designed to include the main connected speech processes in English (eg. assimilations, weak forms ..)")
- (multilingual!) [Common Voice sentences](https://github.com/common-voice/common-voice/blob/main/server/data/en/sentence-collector.txt) (not at all phonetically balanced, also quite short)
- [LJSpeech transcript](https://github.com/NVIDIA/tacotron2/blob/master/filelists/ljs_audio_text_train_filelist.txt) (sentence fragments abound, which I personally think of as useful)
- [Harvard sentences](https://www.cs.columbia.edu/~hgs/audio/harvard.html) (phonetically balanced, but only one sentence per line and they're all equal length)
