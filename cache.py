from music21.key import Key
from music21.pitch import Pitch
from music21.interval import Interval, intervalFromGenericAndChromatic

_transposeKey = {}
_transposePitch = {}
_transposePcSet = {}
_pitchObj = {}
_keyObj = {}
_intervalObj = {}


def TransposeKey(key, interval):
    """Transposes a key based on an interval string (e.g., 'm3').

    Several music21 objects are cached for performance reasons.
    """
    duple = (key, interval)
    if duple in _transposeKey:
        return _transposeKey[duple]
    keyObj = m21Key(key)
    transposed = keyObj.transpose(interval).tonicPitchNameWithCase
    _transposeKey[duple] = transposed
    return transposed


def TransposePitch(pitch, interval):
    """Transposes a pitch based on an interval string (e.g., 'm3').

    Several music21 objects are cached for performance reasons.
    """
    duple = (pitch, interval)
    if duple in _transposePitch:
        return _transposePitch[duple]
    pitchObj = m21Pitch(pitch)
    transposed = pitchObj.transpose(interval).nameWithOctave
    _transposePitch[duple] = transposed
    return transposed


def TransposePcSet(pcset, interval):
    """Transposes a pcset based on an interval string (e.g., 'm3').

    Several music21 objects are cached for performance reasons.
    """
    duple = (pcset, interval)
    if duple in _transposePcSet:
        return _transposePcSet[duple]
    semitones = m21IntervalStr(interval).semitones
    transposed = [(x + semitones) % 12 for x in pcset]
    transposed = tuple(sorted(transposed))
    return transposed


def m21IntervalStr(interval):
    """A cached interval object, based on the string (e.g., 'm3').

    Several music21 objects are cached for performance reasons.
    """
    if interval in _intervalObj:
        return _intervalObj[interval]
    intervalObj = Interval(interval)
    _intervalObj[interval] = intervalObj
    return intervalObj


def m21IntervalGenChr(generic, chromatic):
    """A cached interval object, based on a pair of (generic, chromatic)
    intervals.

    Several music21 objects are cached for performance reasons.
    """
    duple = (generic, chromatic)
    if duple in _intervalObj:
        return _intervalObj[duple]
    intervalObj = intervalFromGenericAndChromatic(generic, chromatic)
    _intervalObj[duple] = intervalObj
    return intervalObj


def m21Key(key):
    """A cached key object, based on a string (e.g., 'c#').

    Several music21 objects are cached for performance reasons.
    """
    if key in _keyObj:
        return _keyObj[key]
    keyObj = Key(key)
    _keyObj[key] = keyObj
    return keyObj


def m21Pitch(pitch):
    """A cached pitch object, based on a string (e.g., 'C#').

    Several music21 objects are cached for performance reasons.
    """
    if pitch in _pitchObj:
        return _pitchObj[pitch]
    pitchObj = Pitch(pitch)
    _pitchObj[pitch] = pitchObj
    return pitchObj
