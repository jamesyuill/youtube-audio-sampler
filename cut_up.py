import librosa
import os
import soundfile as sf

def cut_up_audio(path):
    print('analysing audio...')

    audio_path = "downloads/video-audio.mp3"
    y, sr = librosa.load(audio_path)

    tempo, beat_frames = librosa.beat.beat_track(y=y,sr=sr)
    print(f'tempo: {tempo}')

    beat_samples = librosa.frames_to_samples(beat_frames)

    output_dir = 'temp'
    os.makedirs(output_dir, exist_ok=True)

    targets = [
        (4, 1),
        (2, 2),
        (8, 3), 
        (6, 4), 
        (10,5),
        (20,3),
        (3,19),
        (8,12)
    ]

    beat_duration = int(sr * 60 / tempo )
    half_beat_duration = beat_duration//2

    print('cutting up audio...')

    for i, (bar, beat) in enumerate(targets):
        beat_index = (bar - 1) * 4 + (beat - 1)
        
        if beat_index >= len(beat_samples):
            print(f"Skipping: bar {bar}, beat {beat} — index out of range")
            continue

        start_sample = beat_samples[beat_index]
        end_sample = start_sample + half_beat_duration

        clip = y[start_sample:end_sample]
        output_path = os.path.join(output_dir, f"sample_{i}.wav")
        sf.write(output_path, clip, sr)
        print(f"Saved: {output_path}")