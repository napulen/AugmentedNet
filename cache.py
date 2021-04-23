from music21.key import Key
from music21.pitch import Pitch

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
    keyObj = Key(key)
    _key[key] = keyObj
    return keyObj


def m21Pitch(pitch):
    if pitch in _pitch:
        return _pitch[pitch]
    pitchObj = Pitch(pitch)
    _pitch[pitch] = pitchObj
    return pitchObj
