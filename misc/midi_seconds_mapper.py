import mido
from AugmentedNet.common import ANNOTATIONSCOREDUPLES

score = "bps_01_01.mid"


def get_events_seconds(mid):
    events = {}
    t = 0.0
    for m in mid:
        t += m.time
        if m.type == "note_on" and m.velocity > 0:
            if t not in events:
                events[t] = []
            events[t].append(m.note)
    return events


def get_events_quarterLength(mid):
    events = {}
    for track in mid.tracks:
        t = 0.0
        for m in track:
            t += m.time
            # if m.type != "note_on":
            #     print(m.is_meta, "\t", m.dict())
            # else:
            #     print(m.is_meta, m.dict())
            quarterLength = t / mid.ticks_per_beat
            q = round(quarterLength, 3)
            if m.type == "note_on" and m.velocity > 0:
                if q not in events:
                    events[q] = []
                events[q].append(m.note)
    return events


if __name__ == "__main__":
    for nick, (a, s) in ANNOTATIONSCOREDUPLES.items():
        print(nick)
        m = s.replace(".mxl", ".mid")
        mid = mido.MidiFile(m)

        secs = get_events_seconds(mid)
        qs = get_events_quarterLength(mid)

        for s, notes in sorted(qs.items()):
            print(f"{s}, {notes}")
        break