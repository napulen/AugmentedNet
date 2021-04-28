from music21.key import Key
from music21.pitch import Pitch
from music21.interval import Interval, intervalFromGenericAndChromatic

_transposeKey = {}
_transposePitch = {}
_transposePcSet = {}
_pitch = {}
_key = {}
_intervalStr = {}
_intervalGenChr = {}


def TransposeKey(key, interval):
    if key == "None":
        # This is because of frames with empty tonicized keys
        return "None"
    duple = (key, interval)
    if duple in _transposeKey:
        return _transposeKey[duple]
    keyObj = m21Key(key)
    transposed = keyObj.transpose(interval).tonicPitchNameWithCase
    _transposeKey[duple] = transposed
    return transposed


def TransposePitch(pitch, interval):
    duple = (pitch, interval)
    if duple in _transposePitch:
        return _transposePitch[duple]
    pitchObj = m21Pitch(pitch)
    transposed = pitchObj.transpose(interval).nameWithOctave
    _transposePitch[duple] = transposed
    return transposed


def TransposePcSet(pcset, interval):
    duple = (pcset, interval)
    if duple in _transposePcSet:
        return _transposePcSet[duple]
    semitones = Interval(interval).semitones
    transposed = [(x + semitones) % 12 for x in pcset]
    transposed = tuple(sorted(transposed))
    return transposed


def m21IntervalStr(interval):
    if interval in _intervalStr:
        return _intervalStr[interval]
    intervalObj = Interval(interval)
    _intervalStr[interval] = intervalObj
    return intervalObj


def m21IntervalGenChr(generic, chromatic):
    duple = (generic, chromatic)
    if duple in _intervalGenChr:
        return _intervalGenChr[duple]
    intervalObj = intervalFromGenericAndChromatic(generic, chromatic)
    _intervalGenChr[duple] = intervalObj
    return intervalObj


def m21Key(key):
    if key in _key:
        return _key[key]
    keyObj = Key(key)
    _key[key] = keyObj
    return keyObj


def m21Pitch(pitch):
    if pitch in _pitch:
        return _pitch[pitch]
    pitchObj = Pitch(pitch)
    _pitch[pitch] = pitchObj
    return pitchObj
