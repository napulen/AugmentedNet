from music21.key import Key
from music21.pitch import Pitch
from music21.interval import Interval

_transposeKey = {}
_transposePitch = {}
_pitch = {}
_key = {}


def TransposeKey(key, interval):
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


def m21Key(key):
    if key in _key:
        return _key[key]
    m21Key = Key(key)
    _key[key] = m21Key
    return m21Key


def m21Pitch(pitch):
    if pitch in _pitch:
        return _pitch[pitch]
    m21Pitch = Pitch(pitch)
    _pitch[pitch] = m21Pitch
    return m21Pitch