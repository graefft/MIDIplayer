import mido
from mido import MidiFile, MidiTrack, tempo2bpm
import signal
import sys



def adjust_tempo(midi_file, new_tempo, shift):
    ticks_per_beat = midi_file.ticks_per_beat
    old_tempo = tempo2bpm(ticks_per_beat)

    adjusted_file = MidiFile()
    track = MidiTrack()
    adjusted_file.tracks.append(track)

    for msg in midi_file:
        if msg.time != 0:
            msg.time = int(msg.time * old_tempo / new_tempo)
        if msg.type == 'note_on' :
            if msg.channel != 9:
                if msg.note + shift <= 127:
                    msg.note += shift
        if msg.type == 'note_off' :
            if msg.channel != 9:
                msg.note += shift
        track.append(msg)

    return adjusted_file

def play_midi(midi_file):
    for msg in midi_file.play():
        if msg.type == 'note_on':
#            print(msg)
            with mido.open_output() as port:
                port.send(msg)
        if msg.type == 'note_off':
            with mido.open_output() as port:
                port.send(msg)

selected_track = input("Which Song? ")

selected_track = ("MIDI/" + selected_track)

mid = mido.MidiFile(selected_track)
#mid = mido.MidiFile("MIDI/usher-yeah.mid", clip=True)
#mid = mido.MidiFile("MIDI/Queen - Bohemian Rhapsody.mid")
#mid = mido.MidiFile("MIDI/Town.mid")

try:
    print("MIDI Type:", mid.type)
    print("Ticks per Beat:", mid.ticks_per_beat)


    for msg in mid.tracks[0]:
        print(msg)

#    for track in mid.tracks:
#        print(track)
#    for i, track in enumerate(mid.tracks):
#        print(f"\nTrack {i+1}:")
#        for message in track:
#            print(message)
except Exception as e:
    print("Error:", e)



#print(selected_track)
#mid = mido.MidiFile("MIDI/usher-yeah.mid")

print("Track info: ")
for i, track in enumerate(mid.tracks):
    print(f"Track {i + 1}:")
    for message in track:
        if message.type == 'key_signature':
            print(f"Key Signature: {message.key}")
        if message.type == 'set_tempo':
            print(f"Tempo: {message.tempo}")
    
desired_tempo = input("Enter bpm: ")
desired_tempo = int(desired_tempo)

pitch_shift = input("Pitch shift: ")
pitch_shift = int(pitch_shift)
#Call the function to play the MIDI file

adjusted_mid = adjust_tempo(mid, desired_tempo, pitch_shift )
#adjusted_mid = mid

play_midi(adjusted_mid)

